import { z } from "zod";
import { compilarTemplate } from "../templates/template-manager.js";
import { renderizarHtml } from "../renderer/puppeteer-renderer.js";
import { FORMATOS_DISPONIVEIS } from "../utils/formats.js";

export const gerarPostDefinicao = {
  name: "gerar_post",
  description:
    "Gera uma imagem PNG de post para Instagram a partir de um template e retorna a imagem diretamente no chat. Use listar_templates para ver as opções disponíveis e ver_marca para consultar a identidade visual.",
};

export const gerarPostSchema = z.object({
  template: z
    .string()
    .describe(
      "Nome do template (use listar_templates para ver as opções disponíveis)"
    ),
  formato: z
    .enum(["feed", "story", "carrossel"])
    .describe("Formato do post: feed (1080x1080), story (1080x1920) ou carrossel (1080x1080)"),
  dados: z
    .record(z.unknown())
    .describe(
      "Variáveis do template: textos, cores, etc. Cada template tem variáveis diferentes — veja listar_templates."
    ),
  slide_atual: z
    .number()
    .optional()
    .describe("Número do slide atual (para carrossel). Começa em 1."),
  total_slides: z
    .number()
    .optional()
    .describe("Total de slides (para carrossel)."),
});

export async function gerarPostHandler(
  params: z.infer<typeof gerarPostSchema>
) {
  const { template, formato, dados } = params;

  if (!FORMATOS_DISPONIVEIS.includes(formato)) {
    return {
      content: [
        {
          type: "text" as const,
          text: `Formato "${formato}" não suportado. Use: ${FORMATOS_DISPONIVEIS.join(", ")}`,
        },
      ],
      isError: true,
    };
  }

  try {
    // Adiciona info de slide nos dados se for carrossel
    const dadosFinais = { ...dados };
    if (formato === "carrossel") {
      dadosFinais.__slide_atual = params.slide_atual ?? 1;
      dadosFinais.__total_slides = params.total_slides ?? 1;
    }

    // Compila template HTML com dados
    const html = compilarTemplate(template, formato, dadosFinais);

    // Renderiza HTML em PNG via Puppeteer
    const { FORMATOS } = await import("../utils/formats.js");
    const dim = FORMATOS[formato];
    const pngBuffer = await renderizarHtml(html, dim.largura, dim.altura);

    const base64 = pngBuffer.toString("base64");

    const descricao =
      formato === "carrossel"
        ? `Post carrossel (slide ${params.slide_atual ?? 1}/${params.total_slides ?? 1}) gerado com template "${template}" em ${dim.largura}x${dim.altura} (@2x: ${dim.largura * 2}x${dim.altura * 2}px)`
        : `Post ${formato} gerado com template "${template}" em ${dim.largura}x${dim.altura} (@2x: ${dim.largura * 2}x${dim.altura * 2}px)`;

    return {
      content: [
        { type: "text" as const, text: descricao },
        {
          type: "image" as const,
          data: base64,
          mimeType: "image/png",
        },
      ],
    };
  } catch (error) {
    const msg = error instanceof Error ? error.message : String(error);
    return {
      content: [
        {
          type: "text" as const,
          text: `Erro ao gerar post: ${msg}`,
        },
      ],
      isError: true,
    };
  }
}
