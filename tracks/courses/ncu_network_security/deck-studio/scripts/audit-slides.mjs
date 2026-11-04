import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const SLIDES_DIR = './slides';

function findSlideFiles(dir) {
  let results = [];
  const entries = readdirSync(dir);
  for (const entry of entries) {
    if (entry === 'getting-started') continue;
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) {
      results = results.concat(findSlideFiles(full));
    } else if (entry === 'index.tsx') {
      results.push(full);
    }
  }
  return results;
}

const slideFiles = findSlideFiles(SLIDES_DIR);
let hasError = false;

const AI_FLUFF = [
  '科學驗證',
  '親眼見證',
  '破案地圖',
  '驚人反轉',
  '驚心動魄',
  '心智模型',
];

console.log(`\n🔍 正在審查 ${slideFiles.length} 份投影片原始碼...\n`);

for (const file of slideFiles) {
  const content = readFileSync(file, 'utf-8');
  if (content.includes('// slide-audit-ignore: all')) {
    console.log(`⏩ [跳過審查] ${file} (已標記 slide-audit-ignore: all)`);
    continue;
  }
  const lines = content.split('\n');

  lines.forEach((line, index) => {
    const lineNum = index + 1;

    // 1. 垂直電梯井死空間檢查
    if (line.includes("flexDirection: 'column'") && line.includes("justifyContent: 'space-between'")) {
      console.warn(`⚠️ [死空間陷阱] ${file}:${lineNum}`);
      console.warn(`   發現垂直 column 搭配 space-between，容易造成卡片中間出現大面積無人區！`);
      hasError = true;
    }

    // 2. AI 浮誇詞彙檢查
    for (const fluff of AI_FLUFF) {
      if (line.includes(fluff)) {
        console.error(`❌ [AI 浮誇腔調] ${file}:${lineNum}`);
        console.error(`   發現禁用辭彙: "${fluff}"，請改用技術因果陳述。`);
        hasError = true;
      }
    }

      // 3. 截圖純黑 letterboxing 檢查
      if (line.includes("background: '#000'") || line.includes('background: "#000"') || line.includes("background: 'black'")) {
        console.warn(`⚠️ [黑邊陷阱] ${file}:${lineNum}`);
        console.warn(`   發現圖片外框設置了純黑背景，極易造成 letterboxing 黑邊！請改用 aspectRatio 貼合與原生邊框。`);
        hasError = true;
      }

      // 4. 字體大小底線檢查 (Typography Floor: 1080p 簡報禁止低於 20px)
      const fontSizeMatch = line.match(/fontSize:\s*(\d+)/);
      if (fontSizeMatch) {
        const size = parseInt(fontSizeMatch[1], 10);
        if (size < 20) {
          console.error(`❌ [字體過小陷阱] ${file}:${lineNum}`);
          console.error(`   發現 fontSize: ${size}px，1080p 投影片禁止低於 20px（會導致投影後無法辨識）！`);
          hasError = true;
        }
      }
    });

  // 5. 防禦頁面誤用紅色檢查
  const defenseMatches = content.match(/title="[^"]*(防禦|修復|修補)[^"]*"[\s\S]{1,200}?accentColor=\{c\.accent\}/g);
  if (defenseMatches) {
    console.error(`❌ [色彩語意衝突] ${file}`);
    console.error(`   防禦/修補相關投影片誤用了警戒紅色 accentColor={c.accent}，請改用 c.green！`);
    hasError = true;
  }

  // 6. 資訊過密與多重嵌套檢查 (防止單頁超過 12 個小框框造成視覺混亂)
  const nestedCardMatches = content.match(/borderRadius:\s*(\d+)/g) || [];
  if (nestedCardMatches.length > 250) {
    console.warn(`⚠️ [資訊密度警示] ${file}`);
    console.warn(`   整份投影片包含過多 (${nestedCardMatches.length}) 容器外框，建議精簡版面避免視覺疲勞。`);
  }
}

if (!hasError) {
  console.log('✅ 所有投影片排版與語意審查通過！零死空間、零 AI 浮誇腔、語意色彩合規。\n');
  process.exit(0);
} else {
  console.log('\n⚠️ 發現排版或語意潛在缺陷，請參閱上述建議進行修正。\n');
  process.exit(1);
}
