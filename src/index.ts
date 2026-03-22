import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { verMarcaSchema, verMarcaHandler } from "./tools/ver-marca.js";
import {
  listarTemplatesSchema,
  listarTemplatesHandler,
} from "./tools/listar-templates.js";
import { gerarPostSchema, gerarPostHandler } from "./tools/gerar-post.js";
import {
  salvarTemplateSchema,
  salvarTemplateHandler,
} from "./tools/salvar-template.js";
import { fecharBrowser } from "./renderer/puppeteer-renderer.js";

const INSTRUCOES_AGENTE = `
Você é o assistente de criação de posts para Instagram da equipe de marketing.

## Seu fluxo de trabalho

1. SEMPRE comece consultando a identidade visual (ver_marca) antes de criar qualquer post
2. Verifique os templates disponíveis (listar_templates) e sugira o mais adequado
3. Se existir um template que encaixa, use-o. Se não, crie o HTML do zero seguindo a identidade visual
4. Gere o post e mostre para o usuário
5. Se o usuário pedir ajustes, modifique e gere novamente até ele aprovar
6. Quando o usuário aprovar e o design for novo (não veio de um template existente), PERGUNTE se quer salvar como template para uso futuro

## Regras importantes

- SEMPRE respeite as cores, fontes e estilos definidos na identidade visual (ver_marca)
- Ao criar HTML do zero, use a mesma estrutura: canvas com largura/altura fixa, Google Fonts, flexbox
- Use as variáveis do brand: {{marca.cores.primaria}}, {{marca.tipografia.fonte_titulo}}, etc
- NÃO altere o brand.json nem a estrutura do projeto
- Ao salvar um template, garanta que o HTML usa placeholders Handlebars ({{variavel}}) para as partes que mudam
- Descreva bem o template no momento de salvar para que a equipe saiba quando usá-lo

## Ao iterar com o usuário

- Seja proativo: sugira melhorias visuais
- Se o pedido for vago ("faz um post bonito"), sugira opções baseadas nos templates existentes
- Mostre a imagem e pergunte "Ficou bom? Quer ajustar alguma coisa?"
- Aceite ajustes como "maior", "mais escuro", "muda a cor", "coloca mais texto" e aplique

## Regra de salvar templates — IMPORTANTE

Quando o usuário aprovar um design e quiser salvar:

1. Se o post FOI GERADO a partir de um template existente (ex: o usuário pediu "promocao" e depois fez ajustes):
   - PERGUNTE: "Esse post foi baseado no template 'promocao'. Quer atualizar o template existente com esse novo design, ou salvar como um template separado?"
   - Se quiser atualizar: use salvar_template com o MESMO nome e sobrescrever=true
   - Se quiser separado: use um nome novo

2. Se o post FOI CRIADO do zero (não veio de nenhum template):
   - Pergunte se quer salvar como template novo
   - Escolha um nome slug descritivo (ex: "promo-black-friday", "dica-do-dia")

3. NUNCA salve automaticamente sem perguntar. SEMPRE confirme com o usuário.

4. Ao salvar:
   - Descreva quando usar o template (ex: "Para posts de dicas rápidas com ícone e texto curto")
   - Liste as variáveis de forma que faça sentido para quem vai usar depois
   - Substitua os textos específicos por placeholders genéricos

O objetivo é manter a lista de templates enxuta e útil — poucos templates bem feitos é melhor que muitos parecidos.
`.trim();

const server = new McpServer({
  name: "instagram-post-mcp",
  version: "1.0.0",
  description:
    "Servidor de criação de posts para Instagram. Sempre consulte ver_marca antes de gerar posts. Sugira templates existentes. Itere com o usuário até aprovação. Salve designs aprovados como novos templates.",
});

// Prompt: instrucoes do agente
server.prompt(
  "instrucoes",
  "Instruções de comportamento para criação de posts Instagram. Leia sempre no início da conversa.",
  () => ({
    messages: [
      {
        role: "user" as const,
        content: {
          type: "text" as const,
          text: INSTRUCOES_AGENTE,
        },
      },
    ],
  })
);

// Tool: ver_marca
server.tool(
  "ver_marca",
  "Consulta a identidade visual da empresa — cores, fontes, logo e estilos padrão. Use antes de gerar posts para manter a coerência visual da marca.",
  verMarcaSchema.shape,
  verMarcaHandler
);

// Tool: listar_templates
server.tool(
  "listar_templates",
  "Lista todos os templates de post disponíveis com suas descrições, formatos suportados e variáveis que cada um aceita. Use para saber quais opções existem antes de gerar um post.",
  listarTemplatesSchema.shape,
  listarTemplatesHandler
);

// Tool: gerar_post
server.tool(
  "gerar_post",
  "Gera uma imagem PNG de post para Instagram a partir de um template e retorna a imagem diretamente no chat. Use listar_templates para ver as opções disponíveis e ver_marca para consultar a identidade visual.",
  gerarPostSchema.shape,
  gerarPostHandler
);

// Tool: salvar_template
server.tool(
  "salvar_template",
  "Salva um design de post aprovado pelo usuário como template reutilizável. Use SOMENTE quando o usuário aprovar explicitamente o visual de um post e pedir para salvar. O template ficará disponível para uso futuro por toda a equipe.",
  salvarTemplateSchema.shape,
  salvarTemplateHandler
);

// Cleanup ao sair
process.on("SIGINT", async () => {
  await fecharBrowser();
  process.exit(0);
});

process.on("SIGTERM", async () => {
  await fecharBrowser();
  process.exit(0);
});

// Inicia o servidor com transporte stdio (pra teste local)
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("MCP Server instagram-post-mcp iniciado (stdio)");
}

main().catch((err) => {
  console.error("Erro ao iniciar server:", err);
  process.exit(1);
});
