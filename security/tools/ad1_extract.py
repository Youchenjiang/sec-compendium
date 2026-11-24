#!/usr/bin/env python3
"""ad1_extract.py - AccessData AD1 (FTK Imager 邏輯映像) 離線解析與提取工具

純標準函式庫實作，無需 FTK Imager、無需聯網，適用於封閉靶場環境。

用法:
    python ad1_extract.py --list   <image.ad1>                 # 列出檔案樹 (TSV)
    python ad1_extract.py --meta   <image.ad1> <path-keyword>   # 印出指定項目的完整 metadata
    python ad1_extract.py --extract <image.ad1> <outdir>        # 提取全部內容
    python ad1_extract.py --stats  <image.ad1>                  # 統計與結構摘要

AD1 結構 (v4):
    0x000  16B  segment 簽章 "ADSEGMENTEDFILE\\0"
    0x200  16B  image 簽章 "ADLOGICALIMAGE\\0\\0"
    +0x10  4B   version (3 或 4)
    +0x14  4B   unknown
    +0x18  4B   zlib 區塊大小 (0x10000)
    +0x1C  8B   image_header_length
    +0x24  8B   image_header_length_2
    +0x2C  4B   logical_image_path 長度
    +0x30  44B  unknown
    +0x5C  長度 logical_image_path ("Custom Content Image([Multi])")
    之後為連續的 block 串流 (檔案樹 + 檔案內容 + metadata)
"""
import argparse
import json
import os
import struct
import sys
import zlib

from safe_paths import join_within, resolve_cli_path

SEGMENT_SIGNATURE = b"ADSEGMENTEDFILE\x00"
IMAGE_SIGNATURE = b"ADLOGICALIMAGE\x00\x00"
IMAGE_HEADER_OFFSET = 0x200
PATH_LENGTH_OFFSET = 0x22C
PATH_OFFSET = 0x25C
ITEM_TYPE_FILE = 0
ITEM_TYPE_FOLDER = 5
MAX_NAME_LENGTH = 4096
MAX_BLOCK_COUNT = 5_000_000


class AD1Error(Exception):
    pass


class SegmentReader:
    """跨多段 (.ad1/.ad2/...) 的連續讀取器。

    每個 segment 對像的內容都從自己的 image header (0x200) 開始，
    因此邏輯位移採 base_k = base_{k-1} + size_{k-1} - 0x200，
    使 folder_index 這種「相對 image header」的位移能直接加上 0x200 查表。
    """

    def __init__(self, paths):
        self.paths = list(paths)
        self.current_index = -1
        self.fh = None
        self.pos = 0
        self.absolute_offset = 0
        self._open_next()

    def _open_next(self):
        if self.fh:
            self.fh.close()
        if self.current_index >= 0:
            self.absolute_offset += os.path.getsize(self.paths[self.current_index]) - IMAGE_HEADER_OFFSET
        self.current_index += 1
        if self.current_index >= len(self.paths):
            raise EOFError("沒有更多 segment")
        self.fh = open(self.paths[self.current_index], "rb")
        self.pos = IMAGE_HEADER_OFFSET if self.current_index > 0 else 0

    @property
    def size(self):
        return os.path.getsize(self.paths[self.current_index])

    @property
    def logical_pos(self):
        return self.absolute_offset + self.pos

    def read(self, length):
        chunks = []
        remaining = length
        while remaining > 0:
            available = self.size - self.pos
            if available <= 0:
                self._open_next()
                continue
            take = min(remaining, available)
            self.fh.seek(self.pos)
            data = self.fh.read(take)
            if not data:
                raise EOFError("讀取失敗")
            chunks.append(data)
            self.pos += len(data)
            remaining -= len(data)
        return b"".join(chunks)



def find_segments(image_path):
    base, ext = os.path.splitext(image_path)
    if ext.lower() != ".ad1":
        raise AD1Error(f"非 .ad1 檔案: {image_path}")
    paths = [image_path]
    index = 2
    while True:
        candidate = f"{base}.ad{index}"
        if os.path.exists(candidate):
            paths.append(candidate)
            index += 1
        else:
            break
    return paths


def parse_blocks(reader, verbose=False):
    """產生 (item_type, path, meta, content_offset_reader) 序列。"""
    if reader.logical_pos == 0:
        reader.read(IMAGE_HEADER_OFFSET)
    signature = reader.read(16)
    if signature != IMAGE_SIGNATURE:
        raise AD1Error(f"image 簽章不符: {signature!r}")

    header = reader.read(4 + 4 + 4 + 8 + 8 + 4)  # version..path_length
    version, _unknown, chunk_size, _h1, _h2, path_length = struct.unpack("<IIIqqI", header)
    if version not in (3, 4):
        raise AD1Error(f"不支援的 AD1 版本: {version}")
    if version == 4:
        reader.read(44)
    logical_path = reader.read(path_length).decode("utf-8", "replace")
    if verbose:
        print(f"# version={version} chunk_size={chunk_size} logical_path={logical_path}",
              file=sys.stderr)

    folder_cache = {}
    count = 0
    while True:
        try:
            block_start = reader.logical_pos
            header = reader.read(40)
            next_group, next_in_group, next_block, start_of_data, decompressed_size = struct.unpack("<5q", header)
            item_type, name_length = struct.unpack("<2I", reader.read(8))
            if item_type not in (ITEM_TYPE_FILE, ITEM_TYPE_FOLDER):
                if verbose:
                    print(f"# 停止: 未知 item_type={item_type} @0x{block_start:x}", file=sys.stderr)
                break
            if not 0 < name_length < MAX_NAME_LENGTH:
                if verbose:
                    print(f"# 停止: 名稱長度異常 {name_length} @0x{block_start:x}", file=sys.stderr)
                break
            raw_name = reader.read(name_length)
            name = raw_name.decode("utf-8")
            folder_index, = struct.unpack("<q", reader.read(8))
            if decompressed_size < 0 or decompressed_size > 8 * 1024 ** 3:
                if verbose:
                    print(f"# 停止: 大小異常 {decompressed_size} @0x{block_start:x}", file=sys.stderr)
                break
        except (EOFError, struct.error, UnicodeDecodeError):
            if verbose:
                print(f"# 停止: 解析中斷 @0x{reader.logical_pos:x}", file=sys.stderr)
            break

        parent = folder_cache.get(folder_index + IMAGE_HEADER_OFFSET, "")
        path = f"{parent}/{name}" if parent else name
        folder_cache[block_start] = path

        content = b""
        if decompressed_size > 0:
            chunk_count, = struct.unpack("<q", reader.read(8))
            chunk_count += 1
            offsets = struct.unpack(f"<{chunk_count}q", reader.read(8 * chunk_count))
            parts = []
            for i in range(1, chunk_count):
                compressed = reader.read(offsets[i] - offsets[i - 1])
                parts.append(zlib.decompress(compressed))
            content = b"".join(parts)

        metadata = {}
        while next_block > 0:
            next_block, = struct.unpack("<q", reader.read(8))
            category, key, value_length = struct.unpack("<3I", reader.read(12))
            value = reader.read(value_length)
            metadata.setdefault(category, {})[key] = value

        count += 1
        if count > MAX_BLOCK_COUNT:
            raise AD1Error("block 數量超過上限，可能解析錯誤")
        yield {
            "type": item_type,
            "path": path,
            "name": name,
            "size": decompressed_size,
            "content": content,
            "metadata": metadata,
            "offset": block_start,
            "start_of_data": start_of_data,
            "next_group": next_group,
            "next_in_group": next_in_group,
        }


def decode_metadata(metadata):
    """把 metadata 的 bytes 值轉成可讀字串或 hex。"""
    out = {}
    for category, entries in metadata.items():
        converted = {}
        for key, value in entries.items():
            try:
                text = value.decode("utf-16-le") if b"\x00" in value else value.decode("utf-8")
                if all(ch.isprintable() or ch in "\r\n\t" for ch in text):
                    converted[str(key)] = text.strip()
                    continue
            except UnicodeDecodeError:
                pass
            converted[str(key)] = value.hex()
        out[str(category)] = converted
    return out


def cmd_stats(image_path):
    reader = SegmentReader(find_segments(image_path))
    files = folders = 0
    total_bytes = 0
    top_level = {}
    for block in parse_blocks(reader, verbose=True):
        if block["type"] == ITEM_TYPE_FOLDER:
            folders += 1
        else:
            files += 1
            total_bytes += len(block["content"])
        root = block["path"].split("/")[0]
        top_level[root] = top_level.get(root, 0) + 1
    print(f"檔案: {files}  目錄: {folders}  內容總位元組: {total_bytes}")
    print("頂層節點分布:")
    for name, n in sorted(top_level.items(), key=lambda kv: -kv[1]):
        print(f"  {n:6d}  {name}")


def cmd_list(image_path, show_meta=False):
    reader = SegmentReader(find_segments(image_path))
    print("type\tpath\tsize\tmetadata")
    for block in parse_blocks(reader):
        kind = "DIR" if block["type"] == ITEM_TYPE_FOLDER else "FILE"
        meta = json.dumps(decode_metadata(block["metadata"]), ensure_ascii=False) if show_meta else ""
        print(f"{kind}\t{block['path']}\t{block['size']}\t{meta}")


def cmd_meta(image_path, keyword):
    reader = SegmentReader(find_segments(image_path))
    for block in parse_blocks(reader):
        if keyword.lower() in block["path"].lower():
            print(f"=== {block['path']} (type={block['type']}, size={block['size']}) ===")
            print(json.dumps(decode_metadata(block["metadata"]), ensure_ascii=False, indent=2))
            print()


def cmd_csv(image_path, outfile):
    """匯出檔案級時間軸 CSV (含 AD1 metadata 的四組時間戳與雜湊)。

    AD1 metadata 採用 (category, key) 兩層編號，本工具依實測對映輸出，
    未識別的 key 一概保留在 extra 欄位，避免臆測語意。
    """
    import csv
    image_path = resolve_cli_path(image_path)
    outfile = resolve_cli_path(outfile)
    reader = SegmentReader(find_segments(str(image_path)))
    rows = []
    for block in parse_blocks(reader):
        meta = decode_metadata(block["metadata"])
        cat5 = meta.get("5", {})
        cat3 = meta.get("3", {})
        cat1 = meta.get("1", {})
        known = {("5", "7"), ("5", "8"), ("5", "9"), ("5", "49155"),
                 ("3", "3"), ("1", "8193"), ("1", "20481"), ("1", "20482"), ("3", "49153")}
        extra = {f"{c}.{k}": v for c, entries in meta.items() for k, v in entries.items()
                 if (c, k) not in known}
        rows.append({
            "type": "DIR" if block["type"] == ITEM_TYPE_FOLDER else "FILE",
            "path": block["path"],
            "size": block["size"],
            "t7": cat5.get("7", ""),
            "t8": cat5.get("8", ""),
            "t9": cat5.get("9", ""),
            "t49155": cat5.get("49155", ""),
            "alloc_size": cat3.get("3", ""),
            "inode": cat3.get("49153", ""),
            "mode": cat1.get("8193", ""),
            "md5": cat1.get("20481", ""),
            "sha1": cat1.get("20482", ""),
            "extra": json.dumps({k: v for k, v in sorted(extra.items())}, ensure_ascii=False),
        })
    with open(outfile, "w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"已輸出 {len(rows)} 筆 metadata 至 {outfile}")


def cmd_extract(image_path, outdir, strip_prefix=None):
    image_path = resolve_cli_path(image_path)
    outdir = resolve_cli_path(outdir)
    reader = SegmentReader(find_segments(str(image_path)))
    written = 0
    skipped = 0
    for block in parse_blocks(reader, verbose=True):
        rel = block["path"]
        if strip_prefix and rel.startswith(strip_prefix):
            rel = rel[len(strip_prefix):].lstrip("/")
        safe = rel.replace(":", "_").replace("\\", "_").lstrip("/")
        # Item paths come from the image itself: refuse any that climb out of outdir.
        target = join_within(outdir, safe)
        if block["type"] == ITEM_TYPE_FOLDER:
            os.makedirs(target, exist_ok=True)
            continue
        os.makedirs(target.parent, exist_ok=True)
        if os.path.exists(target):
            skipped += 1
        with open(target, "wb") as out:
            out.write(block["content"])
        written += 1
    print(f"提取完成: 寫入 {written} 個檔案 (已存在略過 {skipped})，輸出目錄: {outdir}")


def main():
    parser = argparse.ArgumentParser(
        description="AccessData AD1 離線解析工具",
        epilog="範例: python ad1_extract.py image.ad1 --extract outdir",
    )
    parser.add_argument("image", help=".ad1 映像路徑")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", dest="list_", action="store_true", help="列出檔案樹 (TSV)")
    group.add_argument("--stats", action="store_true", help="統計摘要")
    group.add_argument("--meta", metavar="KEYWORD", help="列出路徑含 KEYWORD 的項目 metadata")
    group.add_argument("--csv", metavar="OUT.csv", help="匯出檔案級 metadata 時間軸 CSV")
    group.add_argument("--extract", metavar="OUTDIR", help="提取全部內容至 OUTDIR")
    parser.add_argument("--strip-prefix", default=None, help="提取時剰除的路徑前綴")
    parser.add_argument("--with-meta", action="store_true", help="--list 時一併輸出 metadata")
    args = parser.parse_args()

    if args.stats:
        cmd_stats(args.image)
    elif args.csv:
        cmd_csv(args.image, args.csv)
    elif args.list_:
        cmd_list(args.image, args.with_meta)
    elif args.meta:
        cmd_meta(args.image, args.meta)
    elif args.extract:
        cmd_extract(args.image, args.extract, args.strip_prefix)


if __name__ == "__main__":
    main()
