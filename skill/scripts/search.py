#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI/UX Pro Max Search - Motor de busca BM25 para guias de estilo UI/UX
Uso: python search.py "<query>" [--domain <dominio>] [--stack <stack>] [--max-results 3]
     python search.py "<query>" --design-system [-p "Nome do Projeto"]
     python search.py "<query>" --design-system --persist [-p "Nome do Projeto"] [--page "dashboard"]

Dominios: style, prompt, color, chart, landing, product, ux, typography
Stacks: html-tailwind, react, nextjs

Persistencia (padrao Master + Overrides):
  --persist    Salvar design system em design-system/MASTER.md
  --page       Tambem criar arquivo de override por pagina em design-system/pages/
"""

import argparse
import sys
import io
from core import CSV_CONFIG, AVAILABLE_STACKS, MAX_RESULTS, search, search_stack
from design_system import generate_design_system, persist_design_system

# Forcar UTF-8 para stdout/stderr para lidar com emojis no Windows (cp1252 padrao)
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def format_output(result):
    """Formatar resultados para consumo do Claude (otimizado em tokens)"""
    if "error" in result:
        return f"Erro: {result['error']}"

    output = []
    if result.get("stack"):
        output.append(f"## UI Pro Max Diretrizes de Stack")
        output.append(f"**Stack:** {result['stack']} | **Query:** {result['query']}")
    else:
        output.append(f"## UI Pro Max Resultados da Busca")
        output.append(f"**Dominio:** {result['domain']} | **Query:** {result['query']}")
    output.append(f"**Fonte:** {result['file']} | **Encontrados:** {result['count']} resultados\n")

    for i, row in enumerate(result['results'], 1):
        output.append(f"### Resultado {i}")
        for key, value in row.items():
            value_str = str(value)
            if len(value_str) > 300:
                value_str = value_str[:300] + "..."
            output.append(f"- **{key}:** {value_str}")
        output.append("")

    return "\n".join(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UI Pro Max Busca")
    parser.add_argument("query", help="Query de busca")
    parser.add_argument("--domain", "-d", choices=list(CSV_CONFIG.keys()), help="Dominio de busca")
    parser.add_argument("--stack", "-s", choices=AVAILABLE_STACKS, help="Busca por stack (html-tailwind, react, nextjs)")
    parser.add_argument("--max-results", "-n", type=int, default=MAX_RESULTS, help="Max resultados (padrao: 3)")
    parser.add_argument("--json", action="store_true", help="Saida em JSON")
    # Geracao de design system
    parser.add_argument("--design-system", "-ds", action="store_true", help="Gerar recomendacao completa de design system")
    parser.add_argument("--project-name", "-p", type=str, default=None, help="Nome do projeto para saida do design system")
    parser.add_argument("--format", "-f", choices=["ascii", "markdown"], default="ascii", help="Formato de saida do design system")
    # Persistencia (padrao Master + Overrides)
    parser.add_argument("--persist", action="store_true", help="Salvar design system em design-system/MASTER.md (cria estrutura hierarquica)")
    parser.add_argument("--page", type=str, default=None, help="Criar arquivo de override por pagina em design-system/pages/")
    parser.add_argument("--output-dir", "-o", type=str, default=None, help="Diretorio de saida para arquivos persistidos (padrao: diretorio atual)")

    args = parser.parse_args()

    # Design system tem prioridade
    if args.design_system:
        result = generate_design_system(
            args.query, 
            args.project_name, 
            args.format,
            persist=args.persist,
            page=args.page,
            output_dir=args.output_dir
        )
        print(result)
        
        # Imprimir confirmacao de persistencia
        if args.persist:
            project_slug = args.project_name.lower().replace(' ', '-') if args.project_name else "default"
            print("\n" + "=" * 60)
            print(f"✅ Design system persisted to design-system/{project_slug}/")
            print(f"   📄 design-system/{project_slug}/MASTER.md (Fonte Global de Verdade)")
            if args.page:
                page_filename = args.page.lower().replace(' ', '-')
                print(f"   📄 design-system/{project_slug}/pages/{page_filename}.md (Overrides da Pagina)")
            print("")
            print(f"📖 Uso: Ao construir uma pagina, verifique design-system/{project_slug}/pages/[pagina].md primeiro.")
            print(f"   Se existir, suas regras sobrescrevem MASTER.md. Caso contrario, use MASTER.md.")
            print("=" * 60)
    # Busca por stack
    elif args.stack:
        result = search_stack(args.query, args.stack, args.max_results)
        if args.json:
            import json
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_output(result))
    # Busca por dominio
    else:
        result = search(args.query, args.domain, args.max_results)
        if args.json:
            import json
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_output(result))
