#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Context Loader - Consolida contexto da empresa para o Claude

Uso: python3 context.py [--project-root /path]

Carrega e apresenta:
1. brand.json (identidade visual)
2. company.md (voz, tom, publico, calendario)
3. Templates disponiveis (.image-gen/templates/)
4. Campanhas ativas (.image-gen/campaigns/)
5. Assets disponiveis (.image-gen/assets/)
6. Historico recente (.image-gen/history/log.jsonl)
7. Proximas datas do calendario (30 dias)

Se nada encontrado → instrucao de onboarding.
"""

import argparse
import json
import sys
import io
from pathlib import Path
from datetime import datetime, timedelta
import re

# Forcar UTF-8
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def find_project_root(start_path=None):
    """Encontrar raiz do projeto (onde tem brand.json, company.md ou .image-gen/)"""
    path = Path(start_path) if start_path else Path.cwd()

    # Subir ate encontrar indicadores de projeto
    for candidate in [path] + list(path.parents):
        if (candidate / "brand.json").exists():
            return candidate
        if (candidate / "company.md").exists():
            return candidate
        if (candidate / ".image-gen").exists():
            return candidate
        # Parar no home ou raiz
        if candidate == candidate.parent:
            break

    # Se nao encontrou, usar diretorio atual
    return Path(start_path) if start_path else Path.cwd()


def load_brand(project_root):
    """Carregar brand.json"""
    brand_path = project_root / "brand.json"
    if not brand_path.exists():
        return None

    with open(brand_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_company(project_root):
    """Carregar company.md"""
    company_path = project_root / "company.md"
    if not company_path.exists():
        return None

    with open(company_path, 'r', encoding='utf-8') as f:
        return f.read()


def list_templates(project_root):
    """Listar templates disponiveis em .image-gen/templates/"""
    templates_dir = project_root / ".image-gen" / "templates"
    if not templates_dir.exists():
        return []

    templates = []
    for meta_path in templates_dir.glob("*/meta.json"):
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
        meta["_dir"] = meta_path.parent.name
        templates.append(meta)

    return templates


def list_campaigns(project_root):
    """Listar campanhas em .image-gen/campaigns/"""
    campaigns_dir = project_root / ".image-gen" / "campaigns"
    if not campaigns_dir.exists():
        return []

    campaigns = []
    for campaign_path in campaigns_dir.glob("*/campaign.json"):
        with open(campaign_path, 'r', encoding='utf-8') as f:
            campaign = json.load(f)
        campaign["_dir"] = campaign_path.parent.name
        campaigns.append(campaign)

    return campaigns


def list_assets(project_root):
    """Listar assets disponiveis em .image-gen/assets/"""
    assets_dir = project_root / ".image-gen" / "assets"
    if not assets_dir.exists():
        return {}

    assets = {}
    for category_dir in sorted(assets_dir.iterdir()):
        if category_dir.is_dir():
            files = [f.name for f in sorted(category_dir.iterdir()) if f.is_file()]
            if files:
                assets[category_dir.name] = files

    return assets


def load_history(project_root, limit=20):
    """Carregar ultimas entradas do historico"""
    log_path = project_root / ".image-gen" / "history" / "log.jsonl"
    if not log_path.exists():
        return []

    entries = []
    with open(log_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))

    return entries[-limit:]


def get_upcoming_dates(company_text, days=30):
    """Extrair datas do calendario nos proximos N dias"""
    if not company_text:
        return []

    today = datetime.now()
    upcoming = []

    # Procurar linhas de tabela com formato | Mes | Data/Evento | Tipo |
    for line in company_text.split('\n'):
        if '|' not in line or '---' in line:
            continue

        cells = [c.strip() for c in line.split('|') if c.strip()]
        if len(cells) < 2:
            continue

        # Tentar extrair mes e dia
        month_names = {
            'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6,
            'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12
        }

        month_cell = cells[0].lower()[:3]
        if month_cell in month_names:
            month = month_names[month_cell]
            # Tentar extrair dia do evento
            day_match = re.search(r'\((\d{1,2})\)', cells[1])
            if day_match:
                day = int(day_match.group(1))
                try:
                    event_date = datetime(today.year, month, day)
                    # Se ja passou esse ano, considerar proximo ano
                    if event_date < today - timedelta(days=7):
                        event_date = datetime(today.year + 1, month, day)

                    delta = (event_date - today).days
                    if 0 <= delta <= days:
                        upcoming.append({
                            "data": event_date.strftime("%d/%m"),
                            "dias": delta,
                            "evento": cells[1],
                            "tipo": cells[2] if len(cells) > 2 else ""
                        })
                except ValueError:
                    pass

    return sorted(upcoming, key=lambda x: x["dias"])


def analyze_history(entries):
    """Analisar historico para sugestoes de variacao"""
    if not entries:
        return None

    analysis = {
        "total": len(entries),
        "aprovados": sum(1 for e in entries if e.get("approved")),
        "rejeitados": sum(1 for e in entries if not e.get("approved")),
        "layouts": {},
        "estilos": {},
        "alertas": [],
        "anti_patterns": [],
        "sugestao_proximo": None,
    }

    for entry in entries:
        layout = entry.get("layout", "desconhecido")
        style = entry.get("style", "desconhecido")
        analysis["layouts"][layout] = analysis["layouts"].get(layout, 0) + 1
        analysis["estilos"][style] = analysis["estilos"].get(style, 0) + 1

    # Detectar repeticao de layout (ultimos 3)
    recent = entries[-3:]
    recent_layouts = [e.get("layout", "") for e in recent]
    if len(set(recent_layouts)) == 1 and recent_layouts[0]:
        usado = recent_layouts[0]
        analysis["alertas"].append(f"Ultimos 3 posts usaram layout '{usado}' — considere variar")
        # Sugerir layouts nao usados recentemente
        todos_layouts = set(analysis["layouts"].keys()) - {"desconhecido"}
        nao_recentes = todos_layouts - {usado}
        if nao_recentes:
            analysis["sugestao_proximo"] = f"Sugestao: tente '{sorted(nao_recentes)[0]}' no proximo post"

    # Detectar repeticao de estilo (ultimos 3)
    recent_styles = [e.get("style", "") for e in recent]
    if len(set(recent_styles)) == 1 and recent_styles[0]:
        analysis["alertas"].append(f"Ultimos 3 posts usaram estilo '{recent_styles[0]}' — considere variar")

    # Coletar anti-patterns (rejeicoes com feedback)
    for entry in entries:
        if not entry.get("approved") and entry.get("feedback"):
            anti = f"{entry.get('style', '?')}/{entry.get('layout', '?')}: {entry['feedback']}"
            if anti not in analysis["anti_patterns"]:
                analysis["anti_patterns"].append(anti)

    # Taxa de aprovacao
    if analysis["total"] > 0:
        analysis["taxa_aprovacao"] = round(analysis["aprovados"] / analysis["total"] * 100)
        # Alerta se taxa caiu muito
        if analysis["taxa_aprovacao"] < 50 and analysis["total"] >= 5:
            analysis["alertas"].append(f"Taxa de aprovacao baixa ({analysis['taxa_aprovacao']}%) — revisar abordagem ou identidade visual")

    return analysis


def format_output(project_root, brand, company, templates, campaigns, assets, history, upcoming):
    """Formatar saida consolidada"""
    output = []
    has_context = False

    output.append("# Contexto da Empresa")
    output.append(f"**Projeto:** {project_root}\n")

    # 1. Brand
    if brand:
        has_context = True
        output.append("## Identidade Visual (brand.json)")
        company_info = brand.get("company", {})
        if company_info.get("name"):
            output.append(f"**Empresa:** {company_info['name']}")

        colors = brand.get("colors", {})
        if colors:
            color_str = " | ".join(f"{k}: {v}" for k, v in colors.items() if not isinstance(v, list))
            output.append(f"**Cores:** {color_str}")

        typo = brand.get("typography", {})
        if typo:
            output.append(f"**Fontes:** {typo.get('heading_font', '?')} (titulo) + {typo.get('body_font', '?')} (corpo)")

        style = brand.get("style", {})
        if style.get("preferred_visual_style"):
            output.append(f"**Estilo:** {style['preferred_visual_style']}")

        output.append("")

    # 2. Company
    if company:
        has_context = True
        output.append("## Voz e Contexto (company.md)")
        # Resumir — pegar primeiras linhas de cada secao
        lines = company.split('\n')
        for line in lines[:30]:
            if line.startswith('## ') or line.startswith('- '):
                output.append(line)
        output.append(f"\n(company.md completo: {len(lines)} linhas — leia o arquivo para detalhes)\n")

    # 3. Templates
    if templates:
        has_context = True
        output.append("## Templates Disponiveis")
        for t in templates:
            tags = ", ".join(t.get("tags", []))
            output.append(f"- **{t.get('name', t['_dir'])}** ({t.get('format', '?')}) — {tags}")
        output.append("")

    # 4. Campanhas
    if campaigns:
        has_context = True
        active = [c for c in campaigns if c.get("status") == "active"]
        if active:
            output.append("## Campanhas Ativas")
            for c in active:
                total = c.get("total_planned", "?")
                done = sum(1 for p in c.get("posts", []) if p.get("status") == "approved")
                output.append(f"- **{c.get('name', c['_dir'])}** — {done}/{total} posts aprovados")
                rules = c.get("visual_rules", {})
                if rules.get("layout"):
                    output.append(f"  Layout: {rules['layout']}")
                if rules.get("variation_strategy"):
                    output.append(f"  Variacao: {rules['variation_strategy']}")
            output.append("")

    # 5. Assets
    if assets:
        has_context = True
        output.append("## Assets Disponiveis")
        for category, files in assets.items():
            output.append(f"- **{category}/**: {len(files)} arquivo(s) — {', '.join(files[:5])}" +
                         (" ..." if len(files) > 5 else ""))
        output.append("")

    # 6. Historico
    if history:
        has_context = True
        analysis = analyze_history(history)
        output.append("## Historico Recente")
        output.append(f"**Total:** {analysis['total']} geracoes | **Aprovacao:** {analysis.get('taxa_aprovacao', 0)}%")

        for alerta in analysis.get("alertas", []):
            output.append(f"**ALERTA:** {alerta}")

        if analysis.get("sugestao_proximo"):
            output.append(f"**{analysis['sugestao_proximo']}**")

        if analysis["layouts"]:
            top_layouts = sorted(analysis["layouts"].items(), key=lambda x: x[1], reverse=True)[:3]
            output.append(f"**Layouts:** {', '.join(f'{k} ({v}x)' for k, v in top_layouts)}")

        if analysis["estilos"]:
            top_styles = sorted(analysis["estilos"].items(), key=lambda x: x[1], reverse=True)[:3]
            output.append(f"**Estilos:** {', '.join(f'{k} ({v}x)' for k, v in top_styles)}")

        if analysis.get("anti_patterns"):
            output.append(f"**Anti-patterns (rejeitados):**")
            for ap in analysis["anti_patterns"][-5:]:
                output.append(f"  - {ap}")
        output.append("")

    # 7. Proximas datas
    if upcoming:
        has_context = True
        output.append("## Proximas Datas (30 dias)")
        for d in upcoming:
            output.append(f"- **{d['data']}** ({d['dias']} dias) — {d['evento']} | {d['tipo']}")
        output.append("")

    # 8. Revisao de identidade
    review_triggers = []

    if company:
        revision_match = re.search(r'ultima_revisao:\s*(\d{4}-\d{2}-\d{2})', company)
        if revision_match:
            last_review = datetime.strptime(revision_match.group(1), "%Y-%m-%d")
            days_since = (datetime.now() - last_review).days
            if days_since > 90:
                review_triggers.append(f"Tempo: {days_since} dias desde ultima revisao ({revision_match.group(1)})")
        else:
            review_triggers.append("Campo 'ultima_revisao' ausente no company.md — adicione para rastrear")

    if history:
        history_analysis = analyze_history(history)
        if history_analysis and history_analysis.get("taxa_aprovacao", 100) < 50 and history_analysis["total"] >= 5:
            review_triggers.append(f"Rejeicoes: taxa de aprovacao em {history_analysis['taxa_aprovacao']}% nas ultimas {history_analysis['total']} geracoes")
        # Verificar se anti-patterns se repetem (mesmo feedback aparece 2+ vezes)
        if history_analysis and history_analysis.get("anti_patterns"):
            feedbacks = [ap.split(": ", 1)[-1] for ap in history_analysis["anti_patterns"]]
            repeated = [f for f in set(feedbacks) if feedbacks.count(f) >= 2]
            if repeated:
                review_triggers.append(f"Feedback recorrente: '{repeated[0]}' apareceu multiplas vezes")

    if review_triggers:
        output.append("## Revisao de Identidade Recomendada")
        output.append("Motivos:")
        for trigger in review_triggers:
            output.append(f"- {trigger}")
        output.append("")
        output.append("Opcoes:")
        output.append("- **Revisao parcial**: ajustar apenas cores, fontes ou estilo especifico")
        output.append("- **Revisao completa**: refazer onboarding mostrando valores atuais como padrao")
        output.append("")

    # Sem contexto → onboarding
    if not has_context:
        output.clear()
        output.append("# Sem Contexto de Empresa")
        output.append("")
        output.append("Nenhum arquivo de contexto encontrado neste projeto.")
        output.append("Para configurar, siga o onboarding em `docs/onboarding-guide.md`.")
        output.append("")
        output.append("**Arquivos esperados:**")
        output.append("- `brand.json` — identidade visual (cores, fontes, logo)")
        output.append("- `company.md` — voz, tom, publico, pilares, calendario")
        output.append("- `.image-gen/` — assets, templates, campanhas, historico")
        output.append("")
        output.append("Inicie com: \"Vamos configurar a identidade visual da empresa\"")

    return "\n".join(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Context Loader - Consolida contexto da empresa")
    parser.add_argument("--project-root", "-r", type=str, default=None, help="Raiz do projeto")
    parser.add_argument("--json", action="store_true", help="Saida em JSON")
    args = parser.parse_args()

    project_root = find_project_root(args.project_root)

    brand = load_brand(project_root)
    company = load_company(project_root)
    templates = list_templates(project_root)
    campaigns = list_campaigns(project_root)
    assets = list_assets(project_root)
    history = load_history(project_root)
    upcoming = get_upcoming_dates(company) if company else []

    if args.json:
        result = {
            "project_root": str(project_root),
            "has_context": any([brand, company, templates, campaigns, assets, history]),
            "brand": brand,
            "company_exists": company is not None,
            "templates": templates,
            "campaigns": campaigns,
            "assets": assets,
            "history_count": len(history),
            "history_analysis": analyze_history(history),
            "upcoming_dates": upcoming,
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_output(project_root, brand, company, templates, campaigns, assets, history, upcoming))
