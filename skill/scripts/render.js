#!/usr/bin/env node
/**
 * Gerador de Imagens HTML — Renderizador standalone
 *
 * Renderiza um arquivo HTML (ou stdin) para PNG usando Puppeteer.
 *
 * Uso:
 *   node render.js <input.html> [output.png] [--width 1080] [--height 1080] [--scale 2]
 *   cat template.html | node render.js --stdin -o output.png
 *
 * Opcoes:
 *   --width   Largura do viewport em pixels (padrao: 1080)
 *   --height  Altura do viewport em pixels (padrao: 1080)
 *   --scale   Fator de escala para output retina (padrao: 2)
 *   --stdin   Ler HTML do stdin ao inves de arquivo
 *   -o        Caminho do arquivo de saida (alternativa ao arg posicional)
 *   --format  feed (1080x1080), story (1080x1920), ou custom (padrao: custom)
 */

const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");

const FORMATS = {
  feed: { width: 1080, height: 1080 },
  story: { width: 1080, height: 1920 },
  carousel: { width: 1080, height: 1080 },
  banner: { width: 1200, height: 628 },
  "twitter-post": { width: 1200, height: 675 },
  "og-image": { width: 1200, height: 630 },
  "youtube-thumb": { width: 1280, height: 720 },
  square: { width: 1080, height: 1080 },
  landscape: { width: 1920, height: 1080 },
  portrait: { width: 1080, height: 1350 },
};

function parseArgs(argv) {
  const args = {
    input: null,
    output: null,
    width: null,
    height: null,
    scale: 2,
    stdin: false,
    format: null,
  };

  let i = 2; // pular node e caminho do script
  while (i < argv.length) {
    const arg = argv[i];
    if (arg === "--width" && argv[i + 1]) {
      args.width = parseInt(argv[++i], 10);
    } else if (arg === "--height" && argv[i + 1]) {
      args.height = parseInt(argv[++i], 10);
    } else if (arg === "--scale" && argv[i + 1]) {
      args.scale = parseInt(argv[++i], 10);
    } else if (arg === "--format" && argv[i + 1]) {
      args.format = argv[++i];
    } else if (arg === "--stdin") {
      args.stdin = true;
    } else if (arg === "-o" && argv[i + 1]) {
      args.output = argv[++i];
    } else if (!arg.startsWith("-") && !args.input) {
      args.input = arg;
    } else if (!arg.startsWith("-") && !args.output) {
      args.output = arg;
    }
    i++;
  }

  // Aplicar presets de formato
  if (args.format && FORMATS[args.format]) {
    if (!args.width) args.width = FORMATS[args.format].width;
    if (!args.height) args.height = FORMATS[args.format].height;
  }

  // Valores padrao
  if (!args.width) args.width = 1080;
  if (!args.height) args.height = 1080;
  if (!args.output) {
    if (args.input) {
      const base = path.basename(args.input, path.extname(args.input));
      args.output = `${base}.png`;
    } else {
      args.output = "output.png";
    }
  }

  return args;
}

async function readStdin() {
  return new Promise((resolve, reject) => {
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => (data += chunk));
    process.stdin.on("end", () => resolve(data));
    process.stdin.on("error", reject);
  });
}

async function render(html, outputPath, width, height, scale) {
  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  try {
    const page = await browser.newPage();

    await page.setViewport({
      width,
      height,
      deviceScaleFactor: scale,
    });

    // Se o HTML referencia arquivos locais, definir URL base do diretorio do arquivo
    await page.setContent(html, { waitUntil: "networkidle0" });

    // Aguardar carregamento das web fonts
    await page.evaluateHandle("document.fonts.ready");

    const screenshot = await page.screenshot({
      type: "png",
      clip: { x: 0, y: 0, width, height },
    });

    // Garantir que o diretorio de saida existe
    const outputDir = path.dirname(path.resolve(outputPath));
    fs.mkdirSync(outputDir, { recursive: true });

    fs.writeFileSync(outputPath, screenshot);

    const actualWidth = width * scale;
    const actualHeight = height * scale;
    console.log(
      JSON.stringify({
        status: "ok",
        output: path.resolve(outputPath),
        viewport: `${width}x${height}`,
        actual: `${actualWidth}x${actualHeight}`,
        scale,
      })
    );
  } finally {
    await browser.close();
  }
}

async function main() {
  const args = parseArgs(process.argv);

  let html;
  if (args.stdin) {
    html = await readStdin();
  } else if (args.input) {
    if (!fs.existsSync(args.input)) {
      console.error(JSON.stringify({ status: "erro", message: `Arquivo nao encontrado: ${args.input}` }));
      process.exit(1);
    }
    html = fs.readFileSync(args.input, "utf-8");
  } else {
    console.error(
      JSON.stringify({
        status: "erro",
        message: "Uso: node render.js <input.html> [output.png] [--width 1080] [--height 1080] [--scale 2] [--format feed|story|banner]",
        formats: Object.keys(FORMATS),
      })
    );
    process.exit(1);
  }

  await render(html, args.output, args.width, args.height, args.scale);
}

main().catch((err) => {
  console.error(JSON.stringify({ status: "erro", message: err.message }));
  process.exit(1);
});
