import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import Handlebars from "handlebars";
import { FORMATOS } from "../utils/formats.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
export const RAIZ_PROJETO = path.resolve(__dirname, "..", "..");
export const PASTA_TEMPLATES = path.join(RAIZ_PROJETO, "templates");
const CAMINHO_BRAND = path.join(RAIZ_PROJETO, "brand.json");

// Helper: converte numero de estrelas em emojis
Handlebars.registerHelper("stars", function (num: unknown) {
  const n = Math.min(5, Math.max(0, parseInt(String(num), 10) || 5));
  return "★".repeat(n) + "☆".repeat(5 - n);
});

export interface MetaTemplate {
  nome: string;
  nomeExibicao: string;
  descricao: string;
  formatos: string[];
  variaveis: Record<
    string,
    {
      tipo: string;
      obrigatorio?: boolean;
      padrao?: string;
      descricao: string;
    }
  >;
}

export function carregarBrand(): Record<string, unknown> {
  const conteudo = fs.readFileSync(CAMINHO_BRAND, "utf-8");
  return JSON.parse(conteudo);
}

export function listarTemplates(): MetaTemplate[] {
  const pastas = fs.readdirSync(PASTA_TEMPLATES, { withFileTypes: true });
  const templates: MetaTemplate[] = [];

  for (const pasta of pastas) {
    if (!pasta.isDirectory()) continue;

    const metaPath = path.join(PASTA_TEMPLATES, pasta.name, "meta.json");
    if (!fs.existsSync(metaPath)) continue;

    const meta = JSON.parse(fs.readFileSync(metaPath, "utf-8")) as MetaTemplate;
    templates.push(meta);
  }

  return templates;
}

export function compilarTemplate(
  nomeTemplate: string,
  formato: string,
  dados: Record<string, unknown>
): string {
  const pastaTemplate = path.join(PASTA_TEMPLATES, nomeTemplate);
  const htmlPath = path.join(pastaTemplate, "template.html");
  const metaPath = path.join(pastaTemplate, "meta.json");

  if (!fs.existsSync(htmlPath)) {
    throw new Error(`Template "${nomeTemplate}" nao encontrado.`);
  }

  const dimensoes = FORMATOS[formato];
  if (!dimensoes) {
    throw new Error(`Formato "${formato}" nao suportado. Use: feed, story ou carrossel.`);
  }

  // Carrega meta pra pegar valores padrao
  const meta = JSON.parse(fs.readFileSync(metaPath, "utf-8")) as MetaTemplate;
  const padrao: Record<string, unknown> = {};
  for (const [chave, config] of Object.entries(meta.variaveis)) {
    if (config.padrao !== undefined) {
      padrao[chave] = config.padrao;
    }
  }

  // Carrega brand
  const brand = carregarBrand();

  // Resolve caminhos de assets pra file:// absoluto
  const assetsGlobal = path.join(RAIZ_PROJETO, "assets");
  const assetsTemplate = path.join(pastaTemplate, "assets");

  const brandComPaths = resolverPathsBrand(brand, assetsGlobal);

  // Monta dados finais: padrao < brand < dados do usuario
  const dadosFinais = {
    ...padrao,
    ...dados,
    marca: brandComPaths,
    __largura: dimensoes.largura,
    __altura: dimensoes.altura,
    __formato: formato,
  };

  // Compila HTML com Handlebars
  const htmlRaw = fs.readFileSync(htmlPath, "utf-8");
  const template = Handlebars.compile(htmlRaw);
  return template(dadosFinais);
}

function resolverPathsBrand(
  obj: Record<string, unknown>,
  assetsDir: string
): Record<string, unknown> {
  const resultado: Record<string, unknown> = {};

  for (const [chave, valor] of Object.entries(obj)) {
    if (typeof valor === "string" && valor.startsWith("assets/")) {
      // Converte caminho relativo pra file:// absoluto
      const absoluto = path.join(assetsDir, "..", valor);
      resultado[chave] = `file://${absoluto}`;
    } else if (typeof valor === "object" && valor !== null && !Array.isArray(valor)) {
      resultado[chave] = resolverPathsBrand(
        valor as Record<string, unknown>,
        assetsDir
      );
    } else {
      resultado[chave] = valor;
    }
  }

  return resultado;
}
