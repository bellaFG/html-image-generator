import { z } from "zod";
import fs from "node:fs";
import path from "node:path";
import { PASTA_TEMPLATES } from "../templates/template-manager.js";

export const salvarTemplateSchema = z.object({
  nome: z
    .string()
    .regex(/^[a-z0-9-]+$/, "Use apenas letras minúsculas, números e hífens")
    .describe(
      "Nome do template (slug). Se já existir, será atualizado. Ex: 'promocao', 'black-friday'."
    ),
  nome_exibicao: z
    .string()
    .describe("Nome amigável para exibição. Ex: 'Post de Black Friday'"),
  descricao: z
    .string()
    .describe(
      "Descrição do template — quando usar, pra que serve. Ajuda a escolher o template certo no futuro."
    ),
  formatos: z
    .array(z.enum(["feed", "story", "carrossel"]))
    .describe("Formatos em que este template funciona"),
  variaveis: z
    .record(
      z.object({
        tipo: z.string().default("string"),
        obrigatorio: z.boolean().default(false),
        descricao: z.string(),
        padrao: z.string().optional(),
      })
    )
    .describe(
      "Variáveis que o template aceita. Chave = nome da variável, valor = configuração."
    ),
  html: z
    .string()
    .describe(
      "Código HTML completo do template com placeholders Handlebars ({{variavel}}, {{marca.cores.primaria}}, etc). Deve incluir <!DOCTYPE html>, <style> e toda a estrutura."
    ),
  sobrescrever: z
    .boolean()
    .default(false)
    .describe(
      "Se true, sobrescreve o template existente. O Claude DEVE perguntar ao usuário antes de passar true."
    ),
});

export async function salvarTemplateHandler(
  params: z.infer<typeof salvarTemplateSchema>
) {
  const { nome, nome_exibicao, descricao, formatos, variaveis, html, sobrescrever } =
    params;

  const pastaTemplate = path.join(PASTA_TEMPLATES, nome);
  const jaExiste = fs.existsSync(pastaTemplate);

  // Se ja existe e nao autorizou sobrescrever, avisa o Claude pra perguntar
  if (jaExiste && !sobrescrever) {
    return {
      content: [
        {
          type: "text" as const,
          text: [
            `O template "${nome}" já existe.`,
            "",
            "Pergunte ao usuário:",
            `- "Quer atualizar o template '${nome}' com esse novo design?"`,
            `- "Ou prefere salvar como um template novo com outro nome?"`,
            "",
            "Se o usuário quiser atualizar, chame salvar_template novamente com sobrescrever=true.",
          ].join("\n"),
        },
      ],
      isError: true,
    };
  }

  // Cria pasta (ou garante que existe)
  fs.mkdirSync(path.join(pastaTemplate, "assets"), { recursive: true });

  // Salva meta.json
  const meta = {
    nome,
    nomeExibicao: nome_exibicao,
    descricao,
    formatos,
    variaveis,
  };

  fs.writeFileSync(
    path.join(pastaTemplate, "meta.json"),
    JSON.stringify(meta, null, 2),
    "utf-8"
  );

  // Salva template.html
  fs.writeFileSync(path.join(pastaTemplate, "template.html"), html, "utf-8");

  const acao = jaExiste ? "atualizado" : "criado";

  return {
    content: [
      {
        type: "text" as const,
        text: [
          `Template "${nome_exibicao}" ${acao} com sucesso!`,
          "",
          `Nome: ${nome}`,
          `Ação: ${jaExiste ? "Atualização do template existente" : "Novo template"}`,
          `Formatos: ${formatos.join(", ")}`,
          `Variáveis: ${Object.keys(variaveis).join(", ")}`,
          "",
          jaExiste
            ? "O template foi atualizado. A próxima geração já usará o novo design."
            : "O template já está disponível para uso. Na próxima vez que alguém pedir algo parecido, vou sugerir este template.",
        ].join("\n"),
      },
    ],
  };
}
