import { z } from "zod";
import { listarTemplates } from "../templates/template-manager.js";

export const listarTemplatesDefinicao = {
  name: "listar_templates",
  description:
    "Lista todos os templates de post disponíveis com suas descrições, formatos suportados e variáveis que cada um aceita. Use para saber quais opções existem antes de gerar um post.",
  schema: {},
};

export const listarTemplatesSchema = z.object({});

export async function listarTemplatesHandler() {
  const templates = listarTemplates();

  if (templates.length === 0) {
    return {
      content: [
        { type: "text" as const, text: "Nenhum template encontrado." },
      ],
    };
  }

  let texto = "Templates disponíveis:\n\n";

  for (const t of templates) {
    texto += `**${t.nomeExibicao}** (nome: \`${t.nome}\`)\n`;
    texto += `Descrição: ${t.descricao}\n`;
    texto += `Formatos: ${t.formatos.join(", ")}\n`;
    texto += `Variáveis:\n`;

    for (const [chave, config] of Object.entries(t.variaveis)) {
      const obrig = config.obrigatorio ? " (obrigatório)" : " (opcional)";
      const pad = config.padrao ? ` — padrão: ${config.padrao}` : "";
      texto += `  - \`${chave}\`: ${config.descricao}${obrig}${pad}\n`;
    }

    texto += "\n";
  }

  return {
    content: [{ type: "text" as const, text: texto }],
  };
}
