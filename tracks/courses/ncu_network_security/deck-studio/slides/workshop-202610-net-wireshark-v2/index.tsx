import type { CSSProperties, ReactNode } from 'react';
import type { DesignSystem, Page, SlideMeta, SlideTransition } from '@open-slide/core';
import { useSlidePageNumber } from '@open-slide/core';

import imgInterfacesOverview from './assets/step0-interfaces-overview.png';
import imgFindNetroute from './assets/step0-find-netroute.png';
import imgInterfaceSelection from './assets/step0-interface-selection.png';
import imgPingNormal from './assets/step1-ping-normal.png';
import imgUnreachableType3 from './assets/step1-unreachable-type3.png';
import imgTimeoutDrop from './assets/step1-timeout-drop.png';
import imgOfflineTimeout from './assets/step1-offline-timeout.png';
import imgTracertTtl from './assets/step1-tracert-ttl.png';
import imgTcpRstTnc from './assets/step2-tcp-rst-tnc.png';
import imgFtpPacketList from './assets/step2-ftp-packet-list.png';
import imgFtpFollowStream from './assets/step2-ftp-follow-stream.png';
import imgTelnetStream from './assets/step3-telnet-stream.png';
import imgFilterIcmp from './assets/filter-icmp.png';
import imgFilterIpAddr from './assets/filter-ip-addr.png';
import imgFilterTcpPort from './assets/filter-tcp-port.png';
import imgInterfaceRegions from './assets/interface-regions.png';
import iconBrowser from './assets/icon-browser.svg';
import iconOs from './assets/icon-os.svg';
import iconWireshark from './assets/icon-wireshark.svg';
import iconNic from './assets/icon-nic.svg';
import iconRouter from './assets/icon-router.svg';

export const design: DesignSystem = {
  palette: { bg: '#fbfbfb', text: '#111827', accent: '#0284c7' },
  fonts: {
    display: '"PingFang TC", "Noto Sans TC", "Microsoft JhengHei", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
    body: '"PingFang TC", "Noto Sans TC", "Microsoft JhengHei", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
  },
  typeScale: { hero: 118, body: 32 },
  radius: 16,
};

export const meta: SlideMeta = {
  title: 'Wireshark 網路封包分析：實務操作與通訊協定檢視',
  createdAt: '2026-10-06T00:00:00.000Z',
};

export const transition: SlideTransition = {
  duration: 180,
  enter: {
    duration: 180,
    easing: 'cubic-bezier(0.22, 1, 0.36, 1)',
    keyframes: [
      { opacity: 0, transform: 'translateY(6px)' },
      { opacity: 1, transform: 'translateY(0)' },
    ],
  },
  exit: { duration: 120, easing: 'ease-out', keyframes: [{ opacity: 1 }, { opacity: 0 }] },
};

const c = {
  bg: '#fbfbfb',
  text: '#111827',
  gray: '#4b5563',
  grayLight: '#9ca3af',
  line: '#e5e7eb',
  blue: '#0284c7',
  blueSoft: '#f0f9ff',
  slate: '#334155',
  slateSoft: '#f8fafc',
  termBg: '#0f172a',
  termText: '#f8fafc',
  redText: '#dc2626',
  greenText: '#16a34a',
};

const font = {
  body: '"PingFang TC", "Noto Sans TC", "Microsoft JhengHei", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
  display: '"PingFang TC", "Noto Sans TC", "Microsoft JhengHei", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
  mono: 'Consolas, ui-monospace, SFMono-Regular, Menlo, monospace',
};

const fill: CSSProperties = {
  position: 'relative',
  width: '100%',
  height: '100%',
  overflow: 'hidden',
  background: c.bg,
  color: c.text,
  fontFamily: font.body,
};

const Styles = () => (
  <style>{`
    .rise {
      animation: riseIn 0.35s cubic-bezier(0.16, 1, 0.3, 1) both;
    }
    @keyframes riseIn {
      from { opacity: 0; transform: translateY(8px); }
      to { opacity: 1; transform: translateY(0); }
    }
  `}</style>
);

const Footer = () => {
  const { current = 1 } = useSlidePageNumber() ?? {};
  return (
    <div
      style={{
        position: 'absolute',
        right: 110,
        bottom: 30,
        fontSize: 22,
        fontFamily: font.mono,
        fontWeight: 700,
        color: c.gray,
      }}
    >
      {current}
    </div>
  );
};

const Frame = ({
  eyebrow,
  title,
  children,
}: {
  eyebrow: string;
  title: string;
  children: ReactNode;
}) => (
  <div style={fill}>
    <Styles />
    <div
      className="rise"
      style={{
        position: 'absolute',
        left: 110,
        top: 40,
      }}
    >
      <span
        style={{
          display: 'inline-block',
          background: c.slateSoft,
          color: c.slate,
          fontSize: 20,
          fontWeight: 800,
          padding: '6px 16px',
          borderRadius: 8,
          border: `1px solid ${c.line}`,
          letterSpacing: '0.04em',
        }}
      >
        {eyebrow}
      </span>
    </div>

    <h1
      className="rise"
      style={{
        position: 'absolute',
        left: 110,
        top: 104,
        width: 1700,
        margin: 0,
        fontFamily: font.display,
        fontSize: 48,
        fontWeight: 900,
        lineHeight: 1.2,
        letterSpacing: '-0.02em',
      }}
    >
      {title}
    </h1>

    <div
      className="rise"
      style={{
        position: 'absolute',
        left: 110,
        right: 110,
        top: 195,
        bottom: 105,
      }}
    >
      {children}
    </div>
    <Footer />
  </div>
);

const ScreenshotCard = ({
  src,
  caption,
}: {
  src: string;
  caption?: string;
}) => (
  <div
    style={{
      height: '100%',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      gap: 10,
    }}
  >
    <div
      style={{
        flex: 1,
        minHeight: 0,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: '#fff',
        borderRadius: 16,
        border: `2px solid ${c.line}`,
        boxShadow: '0 8px 24px rgba(0,0,0,0.04)',
        overflow: 'hidden',
        padding: 8,
      }}
    >
      <img
        src={src}
        alt={caption || 'Wireshark Screenshot'}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'contain',
          borderRadius: 10,
        }}
      />
    </div>
    {caption && (
      <div
        style={{
          fontSize: 22,
          fontWeight: 700,
          color: c.gray,
          fontFamily: font.mono,
          textAlign: 'center',
        }}
      >
        {caption}
      </div>
    )}
  </div>
);

// ==========================================
// Slide 1: 封面
// ==========================================
const Slide01_Cover: Page = () => (
  <div style={fill}>
    <Styles />

    {/* 上方：主標題與定位 */}
    <div
      className="rise"
      style={{
        position: 'absolute',
        left: 110,
        right: 110,
        top: 130,
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <h1
        style={{
          margin: 0,
          fontFamily: font.display,
          fontSize: 104,
          fontWeight: 900,
          lineHeight: 1.1,
          letterSpacing: '-0.03em',
          color: c.text,
        }}
      >
        Wireshark 練習
      </h1>

      <div
        style={{
          fontSize: 40,
          fontWeight: 800,
          color: c.blue,
          marginTop: 20,
          letterSpacing: '0.01em',
        }}
      >
        ICMP 檢測 ｜ FTP · Telnet 鑑識
      </div>
    </div>

    {/* 下方：三大實作模組卡片（極簡化版） */}
    <div
      className="rise"
      style={{
        position: 'absolute',
        left: 110,
        right: 110,
        top: 480,
        bottom: 110,
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: 32,
      }}
    >
      {/* 模組一 */}
      <div
        style={{
          background: '#fff',
          border: `2px solid ${c.line}`,
          borderRadius: 20,
          padding: '36px 32px',
          boxShadow: '0 8px 24px rgba(0,0,0,0.02)',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          gap: 16,
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontSize: 44, fontWeight: 900, color: c.blue, fontFamily: font.mono }}>
            01
          </span>
          <span style={{ fontSize: 22, fontWeight: 800, background: c.blueSoft, color: c.blue, padding: '4px 14px', borderRadius: 8 }}>
            L3 · ICMP
          </span>
        </div>
        <div style={{ fontSize: 36, fontWeight: 900, color: c.text }}>
          本機連線診斷
        </div>
        <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.5 }}>
          正常 8/0 往返與 Type 3 / TTL 異常退信解析
        </div>
      </div>

      {/* 模組二 */}
      <div
        style={{
          background: '#fff',
          border: `2px solid ${c.line}`,
          borderRadius: 20,
          padding: '36px 32px',
          boxShadow: '0 8px 24px rgba(0,0,0,0.02)',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          gap: 16,
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontSize: 44, fontWeight: 900, color: c.blue, fontFamily: font.mono }}>
            02
          </span>
          <span style={{ fontSize: 22, fontWeight: 800, background: c.slateSoft, color: c.slate, padding: '4px 14px', borderRadius: 8 }}>
            L7 · FTP
          </span>
        </div>
        <div style={{ fontSize: 36, fontWeight: 900, color: c.text }}>
          明文傳輸鑑識
        </div>
        <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.5 }}>
          Port 21 裸露帳密與 Follow TCP Stream 串流重組
        </div>
      </div>

      {/* 模組三 */}
      <div
        style={{
          background: '#fff',
          border: `2px solid ${c.line}`,
          borderRadius: 20,
          padding: '36px 32px',
          boxShadow: '0 8px 24px rgba(0,0,0,0.02)',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          gap: 16,
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontSize: 44, fontWeight: 900, color: c.blue, fontFamily: font.mono }}>
            03
          </span>
          <span style={{ fontSize: 22, fontWeight: 800, background: c.slateSoft, color: c.slate, padding: '4px 14px', borderRadius: 8 }}>
            L7 · Telnet
          </span>
        </div>
        <div style={{ fontSize: 36, fontWeight: 900, color: c.text }}>
          串流異狀探究
        </div>
        <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.5 }}>
          仿照實作二重組串流，藉由 AI 探究回顯成因
        </div>
      </div>
    </div>

    <Footer />
  </div>
);

// ==========================================
// Slide 2: 封包分析基礎
// ==========================================
const Slide02_Basics: Page = () => (
  <Frame eyebrow="基本觀念" title="封包分析基礎：應用層 Log 與網路層封包">
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.15fr', gap: 36, height: '100%' }}>
      {/* 左欄：核心觀念 */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 32, justifyContent: 'center' }}>
        <div>
          <div style={{ fontSize: 36, fontWeight: 900, color: c.text, marginBottom: 10 }}>
            • 應用層 Log 的侷限性
          </div>
          <div style={{ fontSize: 30, color: c.gray, lineHeight: 1.45, paddingLeft: 24 }}>
            伺服器與程式日誌僅記錄程式碼執行結果；若連線於網路層中斷則無紀錄。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 36, fontWeight: 900, color: c.text, marginBottom: 10 }}>
            • 封包側錄攔截層級
          </div>
          <div style={{ fontSize: 30, color: c.gray, lineHeight: 1.45, paddingLeft: 24 }}>
            透過 Npcap 驅動程式，在網卡底層側錄進出電腦的原始二進位訊號。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 36, fontWeight: 900, color: c.text, marginBottom: 10 }}>
            • 協定分層結構解析
          </div>
          <div style={{ fontSize: 30, color: c.gray, lineHeight: 1.45, paddingLeft: 24 }}>
            自動將訊號解析為乙太訊框、IP 標頭、TCP/UDP 與應用層通訊內容。
          </div>
        </div>
      </div>

      {/* 右欄：封包側錄位置架構流程圖（精簡低密度版） */}
      <div
        style={{
          background: '#fff',
          border: `2px solid ${c.line}`,
          borderRadius: 18,
          padding: '24px 28px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          gap: 14,
          boxShadow: '0 8px 24px rgba(0,0,0,0.03)',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 2 }}>
          <span style={{ fontSize: 30, fontWeight: 900, color: c.slate }}>
            封包側錄位置與通訊路徑
          </span>
          <span style={{ fontSize: 22, fontWeight: 800, background: c.blueSoft, color: c.blue, padding: '4px 14px', borderRadius: 8 }}>
            Npcap 驅動層攔截
          </span>
        </div>

        {/* 節點 1: 應用程式 */}
        <div
          style={{
            background: '#f8fafc',
            border: `1.5px solid ${c.line}`,
            borderRadius: 12,
            padding: '12px 18px',
            display: 'flex',
            alignItems: 'center',
            gap: 16,
          }}
        >
          <img
            src={iconBrowser}
            alt="Browser / App"
            style={{ width: 46, height: 46, objectFit: 'contain', flexShrink: 0 }}
          />
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 28, fontWeight: 900, color: c.text }}>
              應用程式 / 瀏覽器 (Application Layer)
            </div>
            <div style={{ fontSize: 26, color: c.gray, marginTop: 2 }}>
              發起 HTTP、FTP、Telnet 請求；Log 僅止於此
            </div>
          </div>
        </div>

        <div style={{ textAlign: 'center', fontSize: 22, fontWeight: 800, color: c.grayLight, lineHeight: 1 }}>
          ↓
        </div>

        {/* 節點 2: 作業系統 TCP/IP 核心 */}
        <div
          style={{
            background: '#f8fafc',
            border: `1.5px solid ${c.line}`,
            borderRadius: 12,
            padding: '12px 18px',
            display: 'flex',
            alignItems: 'center',
            gap: 16,
          }}
        >
          <img
            src={iconOs}
            alt="Operating System Kernel"
            style={{ width: 46, height: 46, objectFit: 'contain', flexShrink: 0 }}
          />
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 28, fontWeight: 900, color: c.text }}>
              作業系統核心 (OS TCP/IP Stack)
            </div>
            <div style={{ fontSize: 26, color: c.gray, marginTop: 2 }}>
              封包拆裝打包、三次交握與 IP 路由轉發
            </div>
          </div>
        </div>

        {/* 核心側錄點亮點：Npcap / Wireshark */}
        <div
          style={{
            background: '#f0f9ff',
            border: '2px solid #38bdf8',
            borderRadius: 12,
            padding: '14px 18px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            boxShadow: '0 4px 12px rgba(2,132,199,0.08)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
            <img
              src={iconWireshark}
              alt="Wireshark"
              style={{ width: 44, height: 44, objectFit: 'contain', flexShrink: 0 }}
            />
            <div>
              <div style={{ fontSize: 28, fontWeight: 900, color: c.blue }}>
                ★ 驅動層側錄攔截點 (Npcap)
              </div>
              <div style={{ fontSize: 26, color: '#0369a1', fontWeight: 700, marginTop: 2 }}>
                直接拷貝進出網卡原始訊號 ➔ 遞送 Wireshark
              </div>
            </div>
          </div>
          <span style={{ fontSize: 22, fontWeight: 800, background: '#bae6fd', color: '#0369a1', padding: '6px 14px', borderRadius: 6, fontFamily: font.mono }}>
            RAW PACKETS
          </span>
        </div>

        <div style={{ textAlign: 'center', fontSize: 22, fontWeight: 800, color: c.grayLight, lineHeight: 1 }}>
          ↓
        </div>

        {/* 節點 3: 實體網卡與閘道 */}
        <div
          style={{
            background: '#f8fafc',
            border: `1.5px solid ${c.line}`,
            borderRadius: 12,
            padding: '12px 18px',
            display: 'flex',
            alignItems: 'center',
            gap: 16,
          }}
        >
          <div style={{ display: 'flex', gap: 8, flexShrink: 0 }}>
            <img
              src={iconNic}
              alt="NIC"
              style={{ width: 44, height: 44, objectFit: 'contain' }}
            />
            <img
              src={iconRouter}
              alt="Router"
              style={{ width: 44, height: 44, objectFit: 'contain' }}
            />
          </div>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 28, fontWeight: 900, color: c.text }}>
              實體網路卡 (NIC) ➔ 預設閘道 (Gateway)
            </div>
            <div style={{ fontSize: 26, color: c.gray, marginTop: 2 }}>
              轉為電氣/無線射頻訊號，實體發射至目標伺服器
            </div>
          </div>
        </div>
      </div>
    </div>
  </Frame>
);

// ==========================================
// Slide 3: Wireshark 介面配置
// ==========================================
const Slide03_Interface: Page = () => (
  <Frame eyebrow="介面導覽" title="Wireshark 介面配置：四大核心顯示區域導覽">
    <div style={{ display: 'grid', gridTemplateColumns: '520px 1fr', gap: 36, height: '100%' }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 20, justifyContent: 'center' }}>
        <div>
          <div style={{ fontSize: 32, fontWeight: 900, color: '#16a34a', marginBottom: 8, display: 'flex', alignItems: 'center', gap: 12 }}>
            <span style={{ width: 16, height: 16, borderRadius: '50%', background: '#16a34a' }} />
            ① 綠框：顯示過濾列 (Filter)
          </div>
          <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.45, paddingLeft: 28 }}>
            輸入協定或條件式過濾，綠底代表語法正確有效，排除背景雜訊。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 32, fontWeight: 900, color: '#2563eb', marginBottom: 8, display: 'flex', alignItems: 'center', gap: 12 }}>
            <span style={{ width: 16, height: 16, borderRadius: '50%', background: '#2563eb' }} />
            ② 藍框：封包清單 (Packet List)
          </div>
          <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.45, paddingLeft: 28 }}>
            條列捕獲封包之序號、相對時間、來源/目的 IP、協定與摘要。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 32, fontWeight: 900, color: '#ea580c', marginBottom: 8, display: 'flex', alignItems: 'center', gap: 12 }}>
            <span style={{ width: 16, height: 16, borderRadius: '50%', background: '#ea580c' }} />
            ③ 橘框：協定細節 (Packet Detail)
          </div>
          <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.45, paddingLeft: 28 }}>
            核心分析區。樹狀展開 Ethernet、IP、TCP 各層標頭與旗標數值。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 32, fontWeight: 900, color: '#dc2626', marginBottom: 8, display: 'flex', alignItems: 'center', gap: 12 }}>
            <span style={{ width: 16, height: 16, borderRadius: '50%', background: '#dc2626' }} />
            ④ 紅框：原始資料 (Packet Bytes)
          </div>
          <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.45, paddingLeft: 28 }}>
            顯示封包底層原始 Hex Dump 與右側 ASCII 字元之即時對照。
          </div>
        </div>
      </div>

      <ScreenshotCard src={imgInterfaceRegions} caption="Wireshark 四大顯示區域" />
    </div>
  </Frame>
);

// ==========================================
// Slide 4: 起手式 (一)：多網卡環境辨識與虛擬介面干擾
// ==========================================
const Slide04_InterfacesOverview: Page = () => (
  <Frame eyebrow="起手關鍵" title="起手式 (一)：多網卡環境辨識與虛擬介面干擾">
    <div style={{ display: 'grid', gridTemplateColumns: '500px 1fr', gap: 36, height: '100%' }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 24, justifyContent: 'center' }}>
        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 虛擬網卡林立的陷阱
          </div>
          <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            電腦常安裝 VMware、WSL、Tailscale 或 VPN 虛擬網卡；若選到未承接預設路由的介面，畫面將完全空白。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 觀察即時折線圖 (Sparkline)
          </div>
          <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            首頁網卡右側會顯示即時流量折線；只有出現起伏波動的網卡，才代表有封包正在進出。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 肉眼判斷的局限性
          </div>
          <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            當多張虛擬網卡同時有背景流量（如廣播或連線保持），單憑折線圖難以斷定誰是通往特定目標 IP 的出口。
          </div>
        </div>
      </div>

      <ScreenshotCard src={imgInterfacesOverview} caption="首頁網卡清單與即時波形" />
    </div>
  </Frame>
);

// ==========================================
// Slide 5: 起手式 (二)：透過 Find-NetRoute 查詢出口網卡
// ==========================================
const Slide05_FindNetroute: Page = () => (
  <Frame eyebrow="起手關鍵" title="起手式 (二)：透過 Find-NetRoute 查詢出口網卡">
    <div style={{ display: 'grid', gridTemplateColumns: '500px 1fr', gap: 36, height: '100%' }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 24, justifyContent: 'center' }}>
        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 查詢系統路由決策
          </div>
          <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            在 Windows PowerShell 執行 <code style={{ fontFamily: font.mono, color: c.blue }}>Find-NetRoute -RemoteIPAddress 8.8.8.8</code>，直接查詢核心路由表決策。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 鎖定 InterfaceAlias
          </div>
          <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            輸出結果明確標示當前承接該目標 IP 的出口網卡名稱（例如本例之 <code style={{ fontFamily: font.mono, color: c.blue }}>Radmin VPN</code>）。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 定位實體出口介面
          </div>
          <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            藉由系統路由表資訊，排查斷網後出口是否遭 VPN 接管，確保後續側錄目標精準無誤。
          </div>
        </div>
      </div>

      <ScreenshotCard src={imgFindNetroute} caption="Find-NetRoute 查詢出口網卡" />
    </div>
  </Frame>
);

// ==========================================
// Slide 6: 起手式 (三)：依即時流量波形雙擊進入網卡
// ==========================================
const Slide06_SelectInterface: Page = () => (
  <Frame eyebrow="起手關鍵" title="起手式 (三)：依即時流量波形雙擊進入網卡">
    <div style={{ display: 'grid', gridTemplateColumns: '500px 1fr', gap: 36, height: '100%' }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 24, justifyContent: 'center' }}>
        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 鎖定已確認之出口介面
          </div>
          <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            經由路由表確認出口介面後，在 Wireshark 首頁清單中找到對應項目。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 檢視波動波形
          </div>
          <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            確認右側即時折線圖 (Sparkline) 持續有微幅跳動，確保網卡處於啟用狀態。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 雙擊進入主捕獲視窗
          </div>
          <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            滑鼠雙擊該網卡名稱即可開啟封包側錄引擎，開始即時攔截進出訊號。
          </div>
        </div>
      </div>

      <ScreenshotCard src={imgInterfaceSelection} caption="選擇目標網卡" />
    </div>
  </Frame>
);

// ==========================================
// Slide 7: 顯示過濾器
// ==========================================
const Slide07_DisplayFilter: Page = () => (
  <Frame eyebrow="過濾技巧" title="顯示過濾器 (Display Filter)：排除背景雜訊">
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 36, height: '100%' }}>
      {/* 左欄：核心過濾觀念 */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 32, justifyContent: 'center' }}>
        <div>
          <div style={{ fontSize: 36, fontWeight: 900, color: c.text, marginBottom: 10 }}>
            • 排除背景雜訊
          </div>
          <div style={{ fontSize: 32, color: c.gray, lineHeight: 1.45, paddingLeft: 24 }}>
            網卡待機時每秒上百筆廣播，需設定條件縮小分析範圍。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 36, fontWeight: 900, color: c.text, marginBottom: 10 }}>
            • 常用協定關鍵字
          </div>
          <div style={{ fontSize: 32, color: c.gray, lineHeight: 1.45, paddingLeft: 24 }}>
            輸入 <code style={{ fontFamily: font.mono, color: c.blue }}>icmp</code>（連線）、<code style={{ fontFamily: font.mono, color: c.blue }}>ftp</code>（傳輸）或 <code style={{ fontFamily: font.mono, color: c.blue }}>telnet</code>（終端）。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 36, fontWeight: 900, color: c.text, marginBottom: 10 }}>
            • 常用邏輯運算子
          </div>
          <div style={{ fontSize: 32, color: c.gray, lineHeight: 1.45, paddingLeft: 24 }}>
            支援 <code style={{ fontFamily: font.mono, color: c.blue }}>==</code>（等）、<code style={{ fontFamily: font.mono, color: c.blue }}>&amp;&amp;</code>（且）、<code style={{ fontFamily: font.mono, color: c.blue }}>||</code>（或）、<code style={{ fontFamily: font.mono, color: c.blue }}>!</code>（非）。
          </div>
        </div>
      </div>

      {/* 右欄：三組常用實拍語法 */}
      <div
        style={{
          background: '#fff',
          border: `2px solid ${c.line}`,
          borderRadius: 18,
          padding: '24px 28px',
          display: 'flex',
          flexDirection: 'column',
          gap: 16,
          justifyContent: 'center',
          boxShadow: '0 8px 24px rgba(0,0,0,0.03)',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontSize: 30, fontWeight: 900, color: c.slate }}>
            常用過濾語法
          </span>
          <span style={{ fontSize: 22, fontWeight: 800, background: '#dcfce7', color: '#15803d', padding: '6px 14px', borderRadius: 8 }}>
            語法有效
          </span>
        </div>

        {/* 語法一：icmp */}
        <div
          style={{
            background: '#f8fafc',
            border: `1.5px solid ${c.line}`,
            borderRadius: 14,
            padding: '16px 20px',
            display: 'flex',
            flexDirection: 'column',
            gap: 10,
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span style={{ fontSize: 28, fontWeight: 900, color: c.blue }}>
              ① 協定層級過濾
            </span>
            <span style={{ fontSize: 26, fontWeight: 700, color: c.gray }}>
              僅顯示 ICMP
            </span>
          </div>
          <div
            style={{
              background: '#15191d',
              padding: '6px 10px',
              borderRadius: 8,
              border: '1px solid #30363d',
              display: 'inline-flex',
              alignSelf: 'flex-start',
            }}
          >
            <img
              src={imgFilterIcmp}
              alt="icmp"
              style={{
                height: 48,
                display: 'block',
                borderRadius: 4,
              }}
            />
          </div>
        </div>

        {/* 語法二：ip.addr */}
        <div
          style={{
            background: '#f8fafc',
            border: `1.5px solid ${c.line}`,
            borderRadius: 14,
            padding: '16px 20px',
            display: 'flex',
            flexDirection: 'column',
            gap: 10,
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span style={{ fontSize: 28, fontWeight: 900, color: c.blue }}>
              ② 主機 IP 位址過濾
            </span>
            <span style={{ fontSize: 26, fontWeight: 700, color: c.gray }}>
              過濾 8.8.8.8
            </span>
          </div>
          <div
            style={{
              background: '#15191d',
              padding: '6px 10px',
              borderRadius: 8,
              border: '1px solid #30363d',
              display: 'inline-flex',
              alignSelf: 'flex-start',
            }}
          >
            <img
              src={imgFilterIpAddr}
              alt="ip.addr"
              style={{
                height: 48,
                display: 'block',
                borderRadius: 4,
              }}
            />
          </div>
        </div>

        {/* 語法三：tcp.port */}
        <div
          style={{
            background: '#f8fafc',
            border: `1.5px solid ${c.line}`,
            borderRadius: 14,
            padding: '16px 20px',
            display: 'flex',
            flexDirection: 'column',
            gap: 10,
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span style={{ fontSize: 28, fontWeight: 900, color: c.blue }}>
              ③ 傳輸層 Port 過濾
            </span>
            <span style={{ fontSize: 26, fontWeight: 700, color: c.gray }}>
              過濾 Port 21
            </span>
          </div>
          <div
            style={{
              background: '#15191d',
              padding: '6px 10px',
              borderRadius: 8,
              border: '1px solid #30363d',
              display: 'inline-flex',
              alignSelf: 'flex-start',
            }}
          >
            <img
              src={imgFilterTcpPort}
              alt="Wireshark filter tcp.port"
              style={{
                height: 48,
                display: 'block',
                borderRadius: 4,
              }}
            />
          </div>
        </div>
      </div>
    </div>
  </Frame>
);

// ==========================================
// Slide 8: 實作一：正常連線檢測
// ==========================================
const Slide08_IcmpPing: Page = () => (
  <Frame eyebrow="實作" title="實作一：正常連線 — 使用 ping 檢測外部連通性">
    <div style={{ display: 'grid', gridTemplateColumns: '500px 1fr', gap: 36, height: '100%' }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 24, justifyContent: 'center' }}>
        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 基準測試端點
          </div>
          <div style={{ fontSize: 30, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            執行 <code style={{ fontFamily: font.mono, color: c.blue }}>ping -n 2 8.8.8.8</code>（Google Public DNS）。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 往返對稱封包
          </div>
          <div style={{ fontSize: 30, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            本機發送 <code style={{ fontFamily: font.mono, color: c.blue }}>Echo Request (Type: 8)</code>，伺服器回傳 <code style={{ fontFamily: font.mono, color: c.greenText }}>Echo Reply (Type: 0)</code>。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 實體與網路層暢通
          </div>
          <div style={{ fontSize: 30, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            往返延遲維持數毫秒，排除本機網卡與外部網路實體中斷疑慮。
          </div>
        </div>
      </div>

      <ScreenshotCard src={imgPingNormal} caption="ICMP Echo 正常往返（Type 8 / 0）" />
    </div>
  </Frame>
);

// ==========================================
// Slide 9: 實作一：異常分析 (一) Type 3 報錯
// ==========================================
const Slide09_IcmpUnreachable: Page = () => (
  <Frame eyebrow="實作" title="實作一：異常分析 (一) — 中途節點主動報錯 (Type 3)">
    <div style={{ display: 'grid', gridTemplateColumns: '500px 1fr', gap: 36, height: '100%' }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 24, justifyContent: 'center' }}>
        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 測試保留網段
          </div>
          <div style={{ fontSize: 30, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            執行 <code style={{ fontFamily: font.mono, color: c.blue }}>ping -n 2 192.0.2.1</code>（RFC 5737 官方保留，全球無路由）。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 路由器主動退信
          </div>
          <div style={{ fontSize: 30, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            上游骨幹路由器查無路由條目，回傳 <code style={{ fontFamily: font.mono, color: c.redText }}>Destination unreachable (Type: 3)</code>。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 終端機統計誤導分析
          </div>
          <div style={{ fontSize: 30, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            終端機統計顯示「Received=1, 0% loss」，但 Wireshark 證實這不是 Reply，而是中途節點發出的退信報錯。
          </div>
        </div>
      </div>

      <ScreenshotCard src={imgUnreachableType3} caption="路由器不可達報錯（Type 3）" />
    </div>
  </Frame>
);

// ==========================================
// Slide 10: 實作一：異常分析 (二) 頻率限制與請求逾時
// ==========================================
const Slide10_IcmpTimeout: Page = () => (
  <Frame eyebrow="實作" title="實作一：異常分析 (二) — 頻率限制與請求逾時 (Timeout)">
    <div style={{ display: 'grid', gridTemplateColumns: '500px 1fr', gap: 36, height: '100%' }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 24, justifyContent: 'center' }}>
        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 次發封包現象
          </div>
          <div style={{ fontSize: 30, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            連續發送時，終端機轉為顯示「Request timed out」，封包回報遺失率 100%。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 觸發 ICMP Rate Limit
          </div>
          <div style={{ fontSize: 30, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            依 RFC 1812 規範，路由器具備防禦機制，短時間內連續無效請求將觸發頻率限制，轉為靜默丟棄（已讀不回）。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • Wireshark 封包層級鐵證
          </div>
          <div style={{ fontSize: 30, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            僅有 Type 8 請求出網卡，右側標記 <code style={{ fontFamily: font.mono, color: c.grayLight }}>[no response found!]</code>，證實中途無人回應。
          </div>
        </div>
      </div>

      <ScreenshotCard src={imgTimeoutDrop} caption="逾時丟包（no response found!）" />
    </div>
  </Frame>
);

// ==========================================
// Slide 11: 實作一：異常分析 (三) 實體斷網與 [No response seen]
// ==========================================
const Slide11_OfflineTimeout: Page = () => (
  <Frame eyebrow="實作" title="實作一：異常分析 (三) — 實體斷網與 [No response seen]">
    <div style={{ display: 'grid', gridTemplateColumns: '500px 1fr', gap: 36, height: '100%' }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 24, justifyContent: 'center' }}>
        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 終端機與封包的印證
          </div>
          <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            終端機連續顯示「Request timed out」且 100% 掉包時，Wireshark 側錄到送出的 Echo Request 均無回音。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • [No response seen] 狀態標記
          </div>
          <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            Wireshark 內部狀態機會自動標記 <code style={{ fontFamily: font.mono, color: c.redText }}>[No response seen]</code>，證實根本沒有收到回傳 Reply。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 實體中斷與路由失效
          </div>
          <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            此特徵通常代表實體網路線脫落、網卡斷線、出口閘道失效，或目標主機已完全離線。
          </div>
        </div>
      </div>

      <ScreenshotCard src={imgOfflineTimeout} caption="斷網無回應（No response seen）" />
    </div>
  </Frame>
);

// ==========================================
// Slide 12: 實作一：Tracert 原理與 TTL 遞減
// ==========================================
const Slide12_TracertTtl: Page = () => (
  <Frame eyebrow="實作" title="實作一：節點報錯 — TTL 遞減與 Tracert 核心原理">
    <div style={{ display: 'grid', gridTemplateColumns: '500px 1fr', gap: 36, height: '100%' }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 24, justifyContent: 'center' }}>
        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 強制設定 TTL=1
          </div>
          <div style={{ fontSize: 30, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            執行 <code style={{ fontFamily: font.mono, color: c.blue }}>ping -i 1 -n 1 8.8.8.8</code>，封包初始生命值僅允許跳躍 1 次。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 第一跳路由器報錯
          </div>
          <div style={{ fontSize: 30, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            本機閘道（分享器）將 TTL 減為 0 後丟棄，主動回傳 <code style={{ fontFamily: font.mono, color: c.redText }}>Time-to-live exceeded (Type: 11)</code>。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • Tracert 機制揭密
          </div>
          <div style={{ fontSize: 30, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            tracert 本質即為自動遞增 TTL 數值之迴圈，藉由逼迫沿途路由器回傳報錯，逐步描繪網路跳點路徑。
          </div>
        </div>
      </div>

      <ScreenshotCard src={imgTracertTtl} caption="TTL 歸零報錯（Type 11）" />
    </div>
  </Frame>
);

// ==========================================
// Slide 13: 實作二：傳輸層探測 — Test-NetConnection 與 TCP RST 重設
// ==========================================
const Slide13_TcpRstTnc: Page = () => (
  <Frame eyebrow="實作" title="實作二：傳輸層探測 — Test-NetConnection 與 TCP RST 重設">
    <div style={{ display: 'grid', gridTemplateColumns: '500px 1fr', gap: 36, height: '100%' }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 24, justifyContent: 'center' }}>
        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • Test-NetConnection (tnc) 探測
          </div>
          <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            執行 <code style={{ fontFamily: font.mono, color: c.blue }}>tnc 127.0.0.1 -p 65535</code>，測試目標連接埠是否開放服務。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 連接埠未開啟的反射
          </div>
          <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            目標主機存活但目標 Port 未被監聽 (LISTEN) 時，作業系統核心會主動送回 <code style={{ fontFamily: font.mono, color: c.redText }}>[RST, ACK]</code> 連線重設封包。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • Wireshark 紅底警示
          </div>
          <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            清單中以醒目紅底標記 RST，證實連線遭核心主動拒絕 (Connection Refused)，非中途阻斷。
          </div>
        </div>
      </div>

      <ScreenshotCard src={imgTcpRstTnc} caption="未開放 Port 連線重設（[RST, ACK]）" />
    </div>
  </Frame>
);

// ==========================================
// Slide 14: 實作二：FTP 協定明文傳輸
// ==========================================
const Slide14_FtpPlaintext: Page = () => (
  <Frame eyebrow="實作" title="實作二：內網稽核 — FTP 控制連線明文指令 (Root-Me 97)">
    <div style={{ display: 'grid', gridTemplateColumns: '500px 1fr', gap: 36, height: '100%' }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 24, justifyContent: 'center' }}>
        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 側錄檔分析背景
          </div>
          <div style={{ fontSize: 30, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            開啟 <code style={{ fontFamily: font.mono }}>ch1.pcap</code>，於過濾列輸入 <code style={{ fontFamily: font.mono, color: c.blue }}>ftp</code> 檢驗內部檔案傳輸協定。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 未加密風險 (CWE-319)
          </div>
          <div style={{ fontSize: 30, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            FTP 控制連線 (Port 21) 採 ASCII 純文字傳輸，傳輸過程無任何金鑰交換或雜湊保護。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 驗證憑證直接現形
          </div>
          <div style={{ fontSize: 30, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            封包清單直接裸露 <code style={{ fontFamily: font.mono, color: c.redText }}>USER</code> 與 <code style={{ fontFamily: font.mono, color: c.redText }}>PASS</code> 欄位，同網段側錄即可直視密碼。
          </div>
        </div>
      </div>

      <ScreenshotCard src={imgFtpPacketList} caption="FTP 明文指令（USER / PASS）" />
    </div>
  </Frame>
);

// ==========================================
// Slide 15: 實作二：Follow TCP Stream
// ==========================================
const Slide15_FollowStream: Page = () => (
  <Frame eyebrow="實作" title="實作二：串流重組 — Follow TCP Stream 還原帳號密碼">
    <div style={{ display: 'grid', gridTemplateColumns: '500px 1fr', gap: 36, height: '100%' }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 24, justifyContent: 'center' }}>
        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 串流重組功能
          </div>
          <div style={{ fontSize: 30, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            任一 TCP 封包按右鍵 ➔ 選擇「Follow」➔「TCP Stream」，將多個封包重組為完整雙向文字對話。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 雙向色彩標記
          </div>
          <div style={{ fontSize: 30, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            視窗中<span style={{ color: c.redText, fontWeight: 700 }}>紅色字體</span>代表客戶端發送（含帳密），<span style={{ color: c.blue, fontWeight: 700 }}>藍色字體</span>代表伺服器回應。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 34, fontWeight: 900, color: c.text, marginBottom: 8 }}>
            • 資安處置建議
          </div>
          <div style={{ fontSize: 30, color: c.gray, lineHeight: 1.5, paddingLeft: 24 }}>
            全面停用 Port 21 (FTP)，改用具備 SSH 加密的 SFTP (Port 22) 或 FTPS。
          </div>
        </div>
      </div>

      <ScreenshotCard src={imgFtpFollowStream} caption="Follow TCP Stream 串流還原" />
    </div>
  </Frame>
);

// ==========================================
// Slide 16: 實作三：Telnet 終端回顯分析
// ==========================================
const Slide16_TelnetEcho: Page = () => (
  <Frame eyebrow="實作" title="實作三：仿照實作二重組串流 — 觀察異狀並詢問 AI">
    <div style={{ display: 'grid', gridTemplateColumns: '520px 1fr', gap: 36, height: '100%' }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 20, justifyContent: 'center' }}>
        <div>
          <div style={{ fontSize: 32, fontWeight: 900, color: c.blue, marginBottom: 6 }}>
            ① 仿照實作二操作
          </div>
          <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.45, paddingLeft: 20 }}>
            載入 <code style={{ fontFamily: font.mono }}>ch2.pcap</code>，對任一 Telnet 封包按右鍵 ➔ 選擇「Follow TCP Stream」。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 32, fontWeight: 900, color: c.text, marginBottom: 6 }}>
            ② 發現異狀：字元重複出現？
          </div>
          <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.45, paddingLeft: 20 }}>
            視窗中帳號為何印出雙重字元（紅藍相間）？但密碼卻又只印出一次？與實作二的 FTP 截然不同。
          </div>
        </div>

        <div>
          <div style={{ fontSize: 32, fontWeight: 900, color: c.text, marginBottom: 6 }}>
            ③ 詢問 AI：探究底層協定差異
          </div>
          <div
            style={{
              fontSize: 24,
              color: c.slate,
              background: c.slateSoft,
              border: `1.5px solid ${c.line}`,
              borderRadius: 10,
              padding: '12px 16px',
              lineHeight: 1.4,
              fontFamily: font.mono,
              marginTop: 4,
            }}
          >
            「我在 Wireshark 看 Telnet TCP Stream，為什麼帳號字元重複紅藍交錯，但密碼只出現一次？」
          </div>
        </div>
      </div>

      <ScreenshotCard src={imgTelnetStream} caption="Telnet 字元回顯還原" />
    </div>
  </Frame>
);

// ==========================================
// Slide 17: 封包分析操作流程
// ==========================================
const Slide17_Workflow: Page = () => (
  <Frame eyebrow="操作流程" title="封包分析操作流程：四步驟標準程序">
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24, height: '100%', justifyContent: 'center' }}>
      {/* 上方：四步驟核心橫向進程 */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 24 }}>
        {[
          {
            step: '01',
            title: '選定網卡',
            cmd: 'Find-NetRoute',
            desc: '依路由表鎖定出口介面，避開虛擬網卡與零流量介面。',
          },
          {
            step: '02',
            title: '套用過濾',
            cmd: 'icmp / ftp / telnet',
            desc: '排除背景廣播雜訊，聚焦目標主機與通訊協定。',
          },
          {
            step: '03',
            title: '展開細節',
            cmd: 'Packet Details',
            desc: '展開 L3/L4 標頭，分析退信代碼、TTL 與連線旗標。',
          },
          {
            step: '04',
            title: '重組串流',
            cmd: 'Follow TCP Stream',
            desc: '重組多個封包，檢視雙向明文或分析字元回顯行為。',
          },
        ].map((item) => (
          <div
            key={item.step}
            style={{
              background: '#fff',
              border: `2px solid ${c.line}`,
              borderRadius: 20,
              padding: '32px 26px',
              boxShadow: '0 4px 16px rgba(0,0,0,0.02)',
              display: 'flex',
              flexDirection: 'column',
              gap: 16,
            }}
          >
            <div style={{ fontSize: 52, fontWeight: 900, color: c.blue, fontFamily: font.mono, lineHeight: 1 }}>
              {item.step}
            </div>

            <div style={{ fontSize: 40, fontWeight: 900, color: c.text }}>
              {item.title}
            </div>

            <div
              style={{
                background: '#1e293b',
                color: '#38bdf8',
                borderRadius: 10,
                padding: '12px 16px',
                fontSize: 26,
                fontFamily: font.mono,
                fontWeight: 700,
                lineHeight: 1.3,
                wordBreak: 'break-all',
              }}
            >
              {item.cmd}
            </div>

            <div style={{ fontSize: 30, color: c.gray, lineHeight: 1.5, marginTop: 4 }}>
              {item.desc}
            </div>
          </div>
        ))}
      </div>

      {/* 下方：標準程序推進橫幅 */}
      <div
        style={{
          background: c.slateSoft,
          border: `2px solid ${c.line}`,
          borderRadius: 16,
          padding: '24px 36px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <span style={{ fontSize: 34, color: c.text, fontWeight: 900, letterSpacing: '0.02em' }}>
          確認出口介面 ➔ 過濾排除雜訊 ➔ 標頭檢視代碼 ➔ 串流還原交談
        </span>
      </div>
    </div>
  </Frame>
);

// ==========================================
// Slide 18: 作業說明
// ==========================================
const Slide18_Assignment: Page = () => (
  <Frame eyebrow="作業說明" title="課後實作作業：連線診斷與未加密通訊檢視">
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: '1.2fr 0.8fr',
        gap: 32,
        height: '100%',
      }}
    >
      {/* 左欄：三大實作任務 */}
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: 16,
          height: '100%',
        }}
      >
        {/* 實作一 */}
        <div
          style={{
            flex: 1,
            background: '#fff',
            border: `2px solid ${c.line}`,
            borderRadius: 16,
            padding: '22px 28px',
            boxShadow: '0 4px 16px rgba(0,0,0,0.02)',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            gap: 10,
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: 32, fontWeight: 900, color: c.blue }}>
              實作一：ICMP 連線測試
            </span>
            <span style={{ fontSize: 20, fontWeight: 800, background: c.blueSoft, color: c.blue, padding: '4px 12px', borderRadius: 6, fontFamily: font.mono }}>
              ICMP · Ping
            </span>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <div style={{ fontSize: 28, color: c.text, lineHeight: 1.4 }}>
              • 側錄 <code style={{ fontFamily: font.mono, color: c.blue }}>8.8.8.8</code> 與 <code style={{ fontFamily: font.mono, color: c.blue }}>192.0.2.1</code> ping 封包
            </div>
            <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.4 }}>
              • 截圖 Type 8/0 與 Type 3 封包，簡述兩者差異
            </div>
          </div>
        </div>

        {/* 實作二 */}
        <div
          style={{
            flex: 1,
            background: '#fff',
            border: `2px solid ${c.line}`,
            borderRadius: 16,
            padding: '22px 28px',
            boxShadow: '0 4px 16px rgba(0,0,0,0.02)',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            gap: 10,
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: 32, fontWeight: 900, color: c.blue }}>
              實作二：FTP 明文傳輸還原
            </span>
            <span style={{ fontSize: 20, fontWeight: 800, background: c.blueSoft, color: c.blue, padding: '4px 12px', borderRadius: 6, fontFamily: font.mono }}>
              FTP · Stream
            </span>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <div style={{ fontSize: 28, color: c.text, lineHeight: 1.4 }}>
              • 載入 <code style={{ fontFamily: font.mono, color: c.blue }}>ch1.pcap</code>，使用 Follow TCP Stream 找出帳密
            </div>
            <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.4 }}>
              • 附交談截圖，並寫出 2 種替代加密方案
            </div>
          </div>
        </div>

        {/* 實作三 */}
        <div
          style={{
            flex: 1,
            background: '#fff',
            border: `2px solid ${c.line}`,
            borderRadius: 16,
            padding: '22px 28px',
            boxShadow: '0 4px 16px rgba(0,0,0,0.02)',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            gap: 10,
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: 32, fontWeight: 900, color: c.blue }}>
              實作三：Telnet 串流異狀探究
            </span>
            <span style={{ fontSize: 20, fontWeight: 800, background: c.blueSoft, color: c.blue, padding: '4px 12px', borderRadius: 6, fontFamily: font.mono }}>
              Telnet · Echo
            </span>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <div style={{ fontSize: 28, color: c.text, lineHeight: 1.4 }}>
              • 仿實作二載入 <code style={{ fontFamily: font.mono, color: c.blue }}>ch2.pcap</code> 並 Follow TCP Stream
            </div>
            <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.4 }}>
              • 截圖串流畫面，並透過 AI 釐清為何字元呈現與 FTP 截然不同
            </div>
          </div>
        </div>
      </div>

      {/* 右欄：繳交資訊與審查項目 */}
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: 16,
          height: '100%',
        }}
      >
        {/* 卡片 1：繳交方式 */}
        <div
          style={{
            flex: 1,
            background: c.slateSoft,
            border: `2px solid ${c.line}`,
            borderRadius: 18,
            padding: '26px 28px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            gap: 12,
            boxShadow: '0 4px 16px rgba(0,0,0,0.02)',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: 30, fontWeight: 900, color: c.slate }}>
              繳交方式
            </span>
            <span style={{ fontSize: 22, fontWeight: 800, background: '#e0e7ff', color: '#4338ca', padding: '4px 14px', borderRadius: 8 }}>
              ee-class
            </span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            <div style={{ fontSize: 28, color: c.text, lineHeight: 1.45 }}>
              • <strong>格式</strong>：匯出單一 PDF 檔
            </div>
            <div style={{ fontSize: 28, color: c.text, lineHeight: 1.45 }}>
              • <strong>檔名</strong>：<code style={{ fontFamily: font.mono, color: c.blue, fontWeight: 700 }}>學號_姓名_作業.pdf</code>
            </div>
            <div style={{ fontSize: 28, color: c.gray, lineHeight: 1.45 }}>
              • <strong>截圖要求</strong>：過濾條件需清晰、框出關鍵封包
            </div>
          </div>
        </div>

        {/* 卡片 2：評量項目 */}
        <div
          style={{
            flex: 1,
            background: '#fff',
            border: `2px solid ${c.line}`,
            borderRadius: 18,
            padding: '26px 28px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            gap: 12,
            boxShadow: '0 4px 16px rgba(0,0,0,0.02)',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: 30, fontWeight: 900, color: c.slate }}>
              評量重點
            </span>
            <span style={{ fontSize: 22, fontWeight: 800, background: c.blueSoft, color: c.blue, padding: '4px 14px', borderRadius: 8 }}>
              核對標準
            </span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            <div style={{ fontSize: 28, color: c.text, lineHeight: 1.45 }}>
              • <strong>封包截圖</strong>：包含過濾條件與目標封包明細
            </div>
            <div style={{ fontSize: 28, color: c.text, lineHeight: 1.45 }}>
              • <strong>問題簡答</strong>：正確說明協定運作與代碼意涵
            </div>
            <div style={{ fontSize: 28, color: c.text, lineHeight: 1.45 }}>
              • <strong>改善對策</strong>：寫出具體可行的加密替代作法
            </div>
          </div>
        </div>

        {/* 底部提醒 */}
        <div
          style={{
            background: '#fff',
            border: `1.5px solid ${c.line}`,
            borderRadius: 14,
            padding: '16px 20px',
            fontSize: 24,
            fontWeight: 800,
            color: c.slate,
            textAlign: 'center',
          }}
        >
          截止時間依 ee-class 系統設定為準
        </div>
      </div>
    </div>
  </Frame>
);

export const notes: string[] = [
  'P1 封面：引導學員建立封包分析基本概念，說明本次 20 分鐘聚焦在連線測試與未加密協定檢視。',
  'P2 基礎：說明 Application Log 與網路層封包的差異，點出封包側錄的運作層級與協定解析原理。',
  'P3 介面：導覽 Packet List、Packet Details 與 Packet Bytes 三個核心顯示區，說明各自查看重點。',
  'P4 網卡一：介紹 Wireshark 首頁介面清單，分析虛擬網卡（VMware、VPN 等）對側錄造成的干擾。',
  'P5 網卡二：示範使用 PowerShell Find-NetRoute 指令，查詢目標 IP 之出口網卡決策。',
  'P6 網卡三：教學員如何看右側流量波形折線（Sparkline）雙擊進入目標實體網卡開始側錄。',
  'P7 過濾：介紹 Display Filter 的基本語法與運算子，說明如何排除背景廣播雜訊。',
  'P8 實作一：說明 ping 指令與 ICMP 運作機制，介紹 Echo Request (Type 8) 與 Echo Reply (Type 0)。',
  'P9 實作一：分析 Destination unreachable (Type 3) 路由器主動報錯與終端機統計誤導。',
  'P10 實作一：分析 Request timed out 現象，說明路由器 ICMP Rate Limit 頻率限制之靜默丟棄。',
  'P11 實作一：分析實體斷網與 VPN 阻斷情境，以 Wireshark [No response seen] 狀態標記印證連線中斷。',
  'P12 實作一：介紹 tracert 運作原理，以 ping -i 1 展示 TTL 遞減歸零與 ICMP Type 11 報錯。',
  'P13 實作二：介紹 Test-NetConnection (tnc) 指令探測關閉連接埠，側錄紅底 [RST, ACK] 連線重設。',
  'P14 實作二：介紹 FTP 控制連線，展示過濾 ftp 後於清單直接裸露之 USER/PASS 封包。',
  'P15 實作二：示範 Follow TCP Stream 功能，展示重組後的雙向紅藍對話框與還原之明文密碼。',
  'P16 實作三：引導學員仿照實作二 Follow TCP Stream，觀察字元紅藍交錯與密碼單向出現之異狀，並透過 AI 探究協定回顯成因。',
  'P17 流程：整理封包分析四步驟：選擇介面、設定過濾、展開欄位、重組串流。',
  'P18 作業：公告課後作業項目、截圖規範與評分比重。',
];

export default [
  Slide01_Cover,
  Slide02_Basics,
  Slide03_Interface,
  Slide04_InterfacesOverview,
  Slide05_FindNetroute,
  Slide06_SelectInterface,
  Slide07_DisplayFilter,
  Slide08_IcmpPing,
  Slide09_IcmpUnreachable,
  Slide10_IcmpTimeout,
  Slide11_OfflineTimeout,
  Slide12_TracertTtl,
  Slide13_TcpRstTnc,
  Slide14_FtpPlaintext,
  Slide15_FollowStream,
  Slide16_TelnetEcho,
  Slide17_Workflow,
  Slide18_Assignment,
];
