import puppeteer, { Browser } from "puppeteer";

let browser: Browser | null = null;

async function getBrowser(): Promise<Browser> {
  if (!browser || !browser.connected) {
    browser = await puppeteer.launch({
      headless: true,
      args: ["--no-sandbox", "--disable-setuid-sandbox"],
    });
  }
  return browser;
}

export async function renderizarHtml(
  html: string,
  largura: number,
  altura: number
): Promise<Buffer> {
  const b = await getBrowser();
  const page = await b.newPage();

  try {
    await page.setViewport({
      width: largura,
      height: altura,
      deviceScaleFactor: 2,
    });

    await page.setContent(html, { waitUntil: "networkidle0" });

    // Espera fontes do Google carregarem
    await page.evaluateHandle("document.fonts.ready");

    const screenshot = await page.screenshot({
      type: "png",
      clip: { x: 0, y: 0, width: largura, height: altura },
    });

    return Buffer.from(screenshot);
  } finally {
    await page.close();
  }
}

export async function fecharBrowser(): Promise<void> {
  if (browser) {
    await browser.close();
    browser = null;
  }
}
