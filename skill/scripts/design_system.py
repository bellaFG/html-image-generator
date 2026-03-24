#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de Design System - Agrega resultados de busca e aplica raciocinio
para gerar recomendacoes abrangentes de design system.

Uso:
    from design_system import generate_design_system
    result = generate_design_system("SaaS dashboard", "Meu Projeto")

    # Com persistencia (padrao Master + Overrides)
    result = generate_design_system("SaaS dashboard", "Meu Projeto", persist=True)
    result = generate_design_system("SaaS dashboard", "Meu Projeto", persist=True, page="dashboard")
"""

import csv
import json
import os
from datetime import datetime
from pathlib import Path
from core import search, DATA_DIR


# ============ CONFIGURACAO ============
REASONING_FILE = "ui-reasoning.csv"

SEARCH_CONFIG = {
    "product": {"max_results": 1},
    "style": {"max_results": 3},
    "color": {"max_results": 2},
    "landing": {"max_results": 2},
    "typography": {"max_results": 2}
}


# ============ GERADOR DE DESIGN SYSTEM ============
class DesignSystemGenerator:
    """Gera recomendacoes de design system a partir de buscas agregadas."""

    def __init__(self):
        self.reasoning_data = self._load_reasoning()

    def _load_reasoning(self) -> list:
        """Carregar regras de raciocinio do CSV."""
        filepath = DATA_DIR / REASONING_FILE
        if not filepath.exists():
            return []
        with open(filepath, 'r', encoding='utf-8') as f:
            return list(csv.DictReader(f))

    def _multi_domain_search(self, query: str, style_priority: list = None) -> dict:
        """Executar buscas em multiplos dominios."""
        results = {}
        for domain, config in SEARCH_CONFIG.items():
            if domain == "style" and style_priority:
                # Para estilo, tambem buscar com palavras-chave prioritarias
                priority_query = " ".join(style_priority[:2]) if style_priority else query
                combined_query = f"{query} {priority_query}"
                results[domain] = search(combined_query, domain, config["max_results"])
            else:
                results[domain] = search(query, domain, config["max_results"])
        return results

    def _find_reasoning_rule(self, category: str) -> dict:
        """Encontrar regra de raciocinio correspondente para uma categoria."""
        category_lower = category.lower()

        # Tentar match exato primeiro
        for rule in self.reasoning_data:
            if rule.get("UI_Category", "").lower() == category_lower:
                return rule

        # Tentar match parcial
        for rule in self.reasoning_data:
            ui_cat = rule.get("UI_Category", "").lower()
            if ui_cat in category_lower or category_lower in ui_cat:
                return rule

        # Tentar match por palavra-chave
        for rule in self.reasoning_data:
            ui_cat = rule.get("UI_Category", "").lower()
            keywords = ui_cat.replace("/", " ").replace("-", " ").split()
            if any(kw in category_lower for kw in keywords):
                return rule

        return {}

    def _apply_reasoning(self, category: str, search_results: dict) -> dict:
        """Aplicar regras de raciocinio aos resultados de busca."""
        rule = self._find_reasoning_rule(category)

        if not rule:
            return {
                "pattern": "Hero + Features + CTA",
                "style_priority": ["Minimalism", "Flat Design"],
                "color_mood": "Professional",
                "typography_mood": "Clean",
                "key_effects": "Subtle hover transitions",
                "anti_patterns": "",
                "decision_rules": {},
                "severity": "MEDIUM"
            }

        # Parsear JSON das regras de decisao
        decision_rules = {}
        try:
            decision_rules = json.loads(rule.get("Decision_Rules", "{}"))
        except json.JSONDecodeError:
            pass

        return {
            "pattern": rule.get("Recommended_Pattern", ""),
            "style_priority": [s.strip() for s in rule.get("Style_Priority", "").split("+")],
            "color_mood": rule.get("Color_Mood", ""),
            "typography_mood": rule.get("Typography_Mood", ""),
            "key_effects": rule.get("Key_Effects", ""),
            "anti_patterns": rule.get("Anti_Patterns", ""),
            "decision_rules": decision_rules,
            "severity": rule.get("Severity", "MEDIUM")
        }

    def _select_best_match(self, results: list, priority_keywords: list) -> dict:
        """Selecionar melhor resultado baseado em palavras-chave prioritarias."""
        if not results:
            return {}

        if not priority_keywords:
            return results[0]

        # Primeiro: tentar match exato pelo nome do estilo
        for priority in priority_keywords:
            priority_lower = priority.lower().strip()
            for result in results:
                style_name = result.get("Style Category", "").lower()
                if priority_lower in style_name or style_name in priority_lower:
                    return result

        # Segundo: pontuar por match de palavra-chave em todos os campos
        scored = []
        for result in results:
            result_str = str(result).lower()
            score = 0
            for kw in priority_keywords:
                kw_lower = kw.lower().strip()
                # Pontuacao maior para match no nome do estilo
                if kw_lower in result.get("Style Category", "").lower():
                    score += 10
                # Pontuacao menor para match no campo de palavras-chave
                elif kw_lower in result.get("Keywords", "").lower():
                    score += 3
                # Ainda menor para matches em outros campos
                elif kw_lower in result_str:
                    score += 1
            scored.append((score, result))

        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1] if scored and scored[0][0] > 0 else results[0]

    def _extract_results(self, search_result: dict) -> list:
        """Extrair lista de resultados do dict de busca."""
        return search_result.get("results", [])

    def generate(self, query: str, project_name: str = None) -> dict:
        """Gerar recomendacao completa de design system."""
        # Passo 1: Primeiro buscar produto para obter categoria
        product_result = search(query, "product", 1)
        product_results = product_result.get("results", [])
        category = "General"
        if product_results:
            category = product_results[0].get("Product Type", "General")

        # Passo 2: Obter regras de raciocinio para esta categoria
        reasoning = self._apply_reasoning(category, {})
        style_priority = reasoning.get("style_priority", [])

        # Passo 3: Busca multi-dominio com dicas de prioridade de estilo
        search_results = self._multi_domain_search(query, style_priority)
        search_results["product"] = product_result  # Reusar busca de produto

        # Passo 4: Selecionar melhores matches de cada dominio usando prioridade
        style_results = self._extract_results(search_results.get("style", {}))
        color_results = self._extract_results(search_results.get("color", {}))
        typography_results = self._extract_results(search_results.get("typography", {}))
        landing_results = self._extract_results(search_results.get("landing", {}))

        best_style = self._select_best_match(style_results, reasoning.get("style_priority", []))
        best_color = color_results[0] if color_results else {}
        best_typography = typography_results[0] if typography_results else {}
        best_landing = landing_results[0] if landing_results else {}

        # Passo 5: Construir recomendacao final
        # Combinar efeitos do raciocinio e da busca de estilo
        style_effects = best_style.get("Effects & Animation", "")
        reasoning_effects = reasoning.get("key_effects", "")
        combined_effects = style_effects if style_effects else reasoning_effects

        return {
            "project_name": project_name or query.upper(),
            "category": category,
            "pattern": {
                "name": best_landing.get("Pattern Name", reasoning.get("pattern", "Hero + Features + CTA")),
                "sections": best_landing.get("Section Order", "Hero > Features > CTA"),
                "cta_placement": best_landing.get("Primary CTA Placement", "Above fold"),
                "color_strategy": best_landing.get("Color Strategy", ""),
                "conversion": best_landing.get("Conversion Optimization", "")
            },
            "style": {
                "name": best_style.get("Style Category", "Minimalism"),
                "type": best_style.get("Type", "General"),
                "effects": style_effects,
                "keywords": best_style.get("Keywords", ""),
                "best_for": best_style.get("Best For", ""),
                "performance": best_style.get("Performance", ""),
                "accessibility": best_style.get("Accessibility", "")
            },
            "colors": {
                "primary": best_color.get("Primary (Hex)", "#2563EB"),
                "secondary": best_color.get("Secondary (Hex)", "#3B82F6"),
                "cta": best_color.get("CTA (Hex)", "#F97316"),
                "background": best_color.get("Background (Hex)", "#F8FAFC"),
                "text": best_color.get("Text (Hex)", "#1E293B"),
                "notes": best_color.get("Notes", "")
            },
            "typography": {
                "heading": best_typography.get("Heading Font", "Inter"),
                "body": best_typography.get("Body Font", "Inter"),
                "mood": best_typography.get("Mood/Style Keywords", reasoning.get("typography_mood", "")),
                "best_for": best_typography.get("Best For", ""),
                "google_fonts_url": best_typography.get("Google Fonts URL", ""),
                "css_import": best_typography.get("CSS Import", "")
            },
            "key_effects": combined_effects,
            "anti_patterns": reasoning.get("anti_patterns", ""),
            "decision_rules": reasoning.get("decision_rules", {}),
            "severity": reasoning.get("severity", "MEDIUM")
        }


# ============ FORMATADORES DE SAIDA ============
BOX_WIDTH = 90  # Caixa mais larga para mais conteudo

def format_ascii_box(design_system: dict) -> str:
    """Formatar design system como caixa ASCII (estilo MCP)."""
    project = design_system.get("project_name", "PROJECT")
    pattern = design_system.get("pattern", {})
    style = design_system.get("style", {})
    colors = design_system.get("colors", {})
    typography = design_system.get("typography", {})
    effects = design_system.get("key_effects", "")
    anti_patterns = design_system.get("anti_patterns", "")

    def wrap_text(text: str, prefix: str, width: int) -> list:
        """Quebrar texto longo em multiplas linhas."""
        if not text:
            return []
        words = text.split()
        lines = []
        current_line = prefix
        for word in words:
            if len(current_line) + len(word) + 1 <= width - 2:
                current_line += (" " if current_line != prefix else "") + word
            else:
                if current_line != prefix:
                    lines.append(current_line)
                current_line = prefix + word
        if current_line != prefix:
            lines.append(current_line)
        return lines

    # Construir secoes a partir do padrao
    sections = pattern.get("sections", "").split(">")
    sections = [s.strip() for s in sections if s.strip()]

    # Construir linhas de saida
    lines = []
    w = BOX_WIDTH - 1

    lines.append("+" + "-" * w + "+")
    lines.append(f"|  ALVO: {project} - DESIGN SYSTEM RECOMENDADO".ljust(BOX_WIDTH) + "|")
    lines.append("+" + "-" * w + "+")
    lines.append("|" + " " * BOX_WIDTH + "|")

    # Secao de padrao
    lines.append(f"|  PADRAO: {pattern.get('name', '')}".ljust(BOX_WIDTH) + "|")
    if pattern.get('conversion'):
        lines.append(f"|     Conversao: {pattern.get('conversion', '')}".ljust(BOX_WIDTH) + "|")
    if pattern.get('cta_placement'):
        lines.append(f"|     CTA: {pattern.get('cta_placement', '')}".ljust(BOX_WIDTH) + "|")
    lines.append("|     Secoes:".ljust(BOX_WIDTH) + "|")
    for i, section in enumerate(sections, 1):
        lines.append(f"|       {i}. {section}".ljust(BOX_WIDTH) + "|")
    lines.append("|" + " " * BOX_WIDTH + "|")

    # Secao de estilo
    lines.append(f"|  ESTILO: {style.get('name', '')}".ljust(BOX_WIDTH) + "|")
    if style.get("keywords"):
        for line in wrap_text(f"Keywords: {style.get('keywords', '')}", "|     ", BOX_WIDTH):
            lines.append(line.ljust(BOX_WIDTH) + "|")
    if style.get("best_for"):
        for line in wrap_text(f"Best For: {style.get('best_for', '')}", "|     ", BOX_WIDTH):
            lines.append(line.ljust(BOX_WIDTH) + "|")
    if style.get("performance") or style.get("accessibility"):
        perf_a11y = f"Performance: {style.get('performance', '')} | Accessibility: {style.get('accessibility', '')}"
        lines.append(f"|     {perf_a11y}".ljust(BOX_WIDTH) + "|")
    lines.append("|" + " " * BOX_WIDTH + "|")

    # Secao de cores
    lines.append("|  CORES:".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     Primaria:   {colors.get('primary', '')}".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     Secundaria: {colors.get('secondary', '')}".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     CTA:        {colors.get('cta', '')}".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     Fundo:      {colors.get('background', '')}".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     Texto:      {colors.get('text', '')}".ljust(BOX_WIDTH) + "|")
    if colors.get("notes"):
        for line in wrap_text(f"Notas: {colors.get('notes', '')}", "|     ", BOX_WIDTH):
            lines.append(line.ljust(BOX_WIDTH) + "|")
    lines.append("|" + " " * BOX_WIDTH + "|")

    # Secao de tipografia
    lines.append(f"|  TIPOGRAFIA: {typography.get('heading', '')} / {typography.get('body', '')}".ljust(BOX_WIDTH) + "|")
    if typography.get("mood"):
        for line in wrap_text(f"Mood: {typography.get('mood', '')}", "|     ", BOX_WIDTH):
            lines.append(line.ljust(BOX_WIDTH) + "|")
    if typography.get("best_for"):
        for line in wrap_text(f"Best For: {typography.get('best_for', '')}", "|     ", BOX_WIDTH):
            lines.append(line.ljust(BOX_WIDTH) + "|")
    if typography.get("google_fonts_url"):
        lines.append(f"|     Google Fonts: {typography.get('google_fonts_url', '')}".ljust(BOX_WIDTH) + "|")
    if typography.get("css_import"):
        lines.append(f"|     CSS Import: {typography.get('css_import', '')[:70]}...".ljust(BOX_WIDTH) + "|")
    lines.append("|" + " " * BOX_WIDTH + "|")

    # Secao de efeitos principais
    if effects:
        lines.append("|  EFEITOS PRINCIPAIS:".ljust(BOX_WIDTH) + "|")
        for line in wrap_text(effects, "|     ", BOX_WIDTH):
            lines.append(line.ljust(BOX_WIDTH) + "|")
        lines.append("|" + " " * BOX_WIDTH + "|")

    # Secao de anti-patterns
    if anti_patterns:
        lines.append("|  EVITAR (Anti-patterns):".ljust(BOX_WIDTH) + "|")
        for line in wrap_text(anti_patterns, "|     ", BOX_WIDTH):
            lines.append(line.ljust(BOX_WIDTH) + "|")
        lines.append("|" + " " * BOX_WIDTH + "|")

    # Secao de checklist pre-entrega
    lines.append("|  CHECKLIST PRE-ENTREGA:".ljust(BOX_WIDTH) + "|")
    checklist_items = [
        "[ ] Sem emojis como icones (use SVG: Heroicons/Lucide)",
        "[ ] cursor-pointer em todos os elementos clicaveis",
        "[ ] Estados hover com transicoes suaves (150-300ms)",
        "[ ] Modo claro: contraste de texto 4.5:1 minimo",
        "[ ] Estados de foco visiveis para navegacao por teclado",
        "[ ] prefers-reduced-motion respeitado",
        "[ ] Responsivo: 375px, 768px, 1024px, 1440px"
    ]
    for item in checklist_items:
        lines.append(f"|     {item}".ljust(BOX_WIDTH) + "|")
    lines.append("|" + " " * BOX_WIDTH + "|")

    lines.append("+" + "-" * w + "+")

    return "\n".join(lines)


def format_markdown(design_system: dict) -> str:
    """Formatar design system como markdown."""
    project = design_system.get("project_name", "PROJECT")
    pattern = design_system.get("pattern", {})
    style = design_system.get("style", {})
    colors = design_system.get("colors", {})
    typography = design_system.get("typography", {})
    effects = design_system.get("key_effects", "")
    anti_patterns = design_system.get("anti_patterns", "")

    lines = []
    lines.append(f"## Design System: {project}")
    lines.append("")

    # Secao de padrao
    lines.append("### Padrao")
    lines.append(f"- **Nome:** {pattern.get('name', '')}")
    if pattern.get('conversion'):
        lines.append(f"- **Foco de Conversao:** {pattern.get('conversion', '')}")
    if pattern.get('cta_placement'):
        lines.append(f"- **Posicao do CTA:** {pattern.get('cta_placement', '')}")
    if pattern.get('color_strategy'):
        lines.append(f"- **Estrategia de Cores:** {pattern.get('color_strategy', '')}")
    lines.append(f"- **Secoes:** {pattern.get('sections', '')}")
    lines.append("")

    # Secao de estilo
    lines.append("### Estilo")
    lines.append(f"- **Nome:** {style.get('name', '')}")
    if style.get('keywords'):
        lines.append(f"- **Palavras-chave:** {style.get('keywords', '')}")
    if style.get('best_for'):
        lines.append(f"- **Melhor Para:** {style.get('best_for', '')}")
    if style.get('performance') or style.get('accessibility'):
        lines.append(f"- **Performance:** {style.get('performance', '')} | **Acessibilidade:** {style.get('accessibility', '')}")
    lines.append("")

    # Secao de cores
    lines.append("### Cores")
    lines.append(f"| Funcao | Hex |")
    lines.append(f"|--------|-----|")
    lines.append(f"| Primaria | {colors.get('primary', '')} |")
    lines.append(f"| Secundaria | {colors.get('secondary', '')} |")
    lines.append(f"| CTA | {colors.get('cta', '')} |")
    lines.append(f"| Fundo | {colors.get('background', '')} |")
    lines.append(f"| Texto | {colors.get('text', '')} |")
    if colors.get("notes"):
        lines.append(f"\n*Notas: {colors.get('notes', '')}*")
    lines.append("")

    # Secao de tipografia
    lines.append("### Tipografia")
    lines.append(f"- **Titulo:** {typography.get('heading', '')}")
    lines.append(f"- **Corpo:** {typography.get('body', '')}")
    if typography.get("mood"):
        lines.append(f"- **Humor:** {typography.get('mood', '')}")
    if typography.get("best_for"):
        lines.append(f"- **Melhor Para:** {typography.get('best_for', '')}")
    if typography.get("google_fonts_url"):
        lines.append(f"- **Google Fonts:** {typography.get('google_fonts_url', '')}")
    if typography.get("css_import"):
        lines.append(f"- **CSS Import:**")
        lines.append(f"```css")
        lines.append(f"{typography.get('css_import', '')}")
        lines.append(f"```")
    lines.append("")

    # Secao de efeitos principais
    if effects:
        lines.append("### Efeitos Principais")
        lines.append(f"{effects}")
        lines.append("")

    # Secao de anti-patterns
    if anti_patterns:
        lines.append("### Evitar (Anti-patterns)")
        newline_bullet = '\n- '
        lines.append(f"- {anti_patterns.replace(' + ', newline_bullet)}")
        lines.append("")

    # Secao de checklist pre-entrega
    lines.append("### Checklist Pre-Entrega")
    lines.append("- [ ] Sem emojis como icones (use SVG: Heroicons/Lucide)")
    lines.append("- [ ] cursor-pointer em todos os elementos clicaveis")
    lines.append("- [ ] Estados hover com transicoes suaves (150-300ms)")
    lines.append("- [ ] Modo claro: contraste de texto 4.5:1 minimo")
    lines.append("- [ ] Estados de foco visiveis para navegacao por teclado")
    lines.append("- [ ] prefers-reduced-motion respeitado")
    lines.append("- [ ] Responsivo: 375px, 768px, 1024px, 1440px")
    lines.append("")

    return "\n".join(lines)


# ============ PONTO DE ENTRADA PRINCIPAL ============
def generate_design_system(query: str, project_name: str = None, output_format: str = "ascii",
                           persist: bool = False, page: str = None, output_dir: str = None) -> str:
    """
    Ponto de entrada principal para geracao de design system.

    Args:
        query: Query de busca (ex: "SaaS dashboard", "e-commerce luxo")
        project_name: Nome opcional do projeto para cabecalho
        output_format: "ascii" (padrao) ou "markdown"
        persist: Se True, salvar design system na pasta design-system/
        page: Nome opcional da pagina para arquivo de override
        output_dir: Diretorio de saida opcional (padrao: diretorio atual)

    Returns:
        String formatada do design system
    """
    generator = DesignSystemGenerator()
    design_system = generator.generate(query, project_name)
    
    # Persistir em arquivos se solicitado
    if persist:
        persist_design_system(design_system, page, output_dir, query)

    if output_format == "markdown":
        return format_markdown(design_system)
    return format_ascii_box(design_system)


# ============ FUNCOES DE PERSISTENCIA ============
def persist_design_system(design_system: dict, page: str = None, output_dir: str = None, page_query: str = None) -> dict:
    """
    Persistir design system na pasta design-system/<projeto>/ usando padrao Master + Overrides.

    Args:
        design_system: Dicionario do design system gerado
        page: Nome opcional da pagina para arquivo de override
        output_dir: Diretorio de saida opcional (padrao: diretorio atual)
        page_query: Query opcional para geracao inteligente de override de pagina

    Returns:
        dict com caminhos dos arquivos criados e status
    """
    base_dir = Path(output_dir) if output_dir else Path.cwd()
    
    # Usar nome do projeto para pasta especifica
    project_name = design_system.get("project_name", "default")
    project_slug = project_name.lower().replace(' ', '-')
    
    design_system_dir = base_dir / "design-system" / project_slug
    pages_dir = design_system_dir / "pages"
    
    created_files = []
    
    # Criar diretorios
    design_system_dir.mkdir(parents=True, exist_ok=True)
    pages_dir.mkdir(parents=True, exist_ok=True)
    
    master_file = design_system_dir / "MASTER.md"
    
    # Gerar e escrever MASTER.md
    master_content = format_master_md(design_system)
    with open(master_file, 'w', encoding='utf-8') as f:
        f.write(master_content)
    created_files.append(str(master_file))
    
    # Se pagina especificada, criar arquivo de override com conteudo inteligente
    if page:
        page_file = pages_dir / f"{page.lower().replace(' ', '-')}.md"
        page_content = format_page_override_md(design_system, page, page_query)
        with open(page_file, 'w', encoding='utf-8') as f:
            f.write(page_content)
        created_files.append(str(page_file))
    
    return {
        "status": "success",
        "design_system_dir": str(design_system_dir),
        "created_files": created_files
    }


def format_master_md(design_system: dict) -> str:
    """Formatar design system como MASTER.md com logica de override hierarquica."""
    project = design_system.get("project_name", "PROJECT")
    pattern = design_system.get("pattern", {})
    style = design_system.get("style", {})
    colors = design_system.get("colors", {})
    typography = design_system.get("typography", {})
    effects = design_system.get("key_effects", "")
    anti_patterns = design_system.get("anti_patterns", "")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    lines = []
    
    # Cabecalho de logica
    lines.append("# Arquivo Master do Design System")
    lines.append("")
    lines.append("> **LOGICA:** Ao construir uma pagina especifica, primeiro verifique `design-system/pages/[nome-pagina].md`.")
    lines.append("> Se esse arquivo existir, suas regras **sobrescrevem** este arquivo Master.")
    lines.append("> Caso contrario, siga estritamente as regras abaixo.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"**Projeto:** {project}")
    lines.append(f"**Gerado em:** {timestamp}")
    lines.append(f"**Categoria:** {design_system.get('category', 'General')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Secao de regras globais
    lines.append("## Regras Globais")
    lines.append("")
    
    # Paleta de Cores
    lines.append("### Paleta de Cores")
    lines.append("")
    lines.append("| Funcao | Hex | Variavel CSS |")
    lines.append("|--------|-----|--------------|")
    lines.append(f"| Primaria | `{colors.get('primary', '#2563EB')}` | `--color-primary` |")
    lines.append(f"| Secundaria | `{colors.get('secondary', '#3B82F6')}` | `--color-secondary` |")
    lines.append(f"| CTA/Destaque | `{colors.get('cta', '#F97316')}` | `--color-cta` |")
    lines.append(f"| Fundo | `{colors.get('background', '#F8FAFC')}` | `--color-background` |")
    lines.append(f"| Texto | `{colors.get('text', '#1E293B')}` | `--color-text` |")
    lines.append("")
    if colors.get("notes"):
        lines.append(f"**Notas de Cores:** {colors.get('notes', '')}")
        lines.append("")
    
    # Tipografia
    lines.append("### Tipografia")
    lines.append("")
    lines.append(f"- **Fonte de Titulo:** {typography.get('heading', 'Inter')}")
    lines.append(f"- **Fonte de Corpo:** {typography.get('body', 'Inter')}")
    if typography.get("mood"):
        lines.append(f"- **Humor:** {typography.get('mood', '')}")
    if typography.get("google_fonts_url"):
        lines.append(f"- **Google Fonts:** [{typography.get('heading', '')} + {typography.get('body', '')}]({typography.get('google_fonts_url', '')})")
    lines.append("")
    if typography.get("css_import"):
        lines.append("**CSS Import:**")
        lines.append("```css")
        lines.append(typography.get("css_import", ""))
        lines.append("```")
        lines.append("")
    
    # Variaveis de Espacamento
    lines.append("### Variaveis de Espacamento")
    lines.append("")
    lines.append("| Token | Valor | Uso |")
    lines.append("|-------|-------|-----|")
    lines.append("| `--space-xs` | `4px` / `0.25rem` | Espacos apertados |")
    lines.append("| `--space-sm` | `8px` / `0.5rem` | Espacos de icone, inline |")
    lines.append("| `--space-md` | `16px` / `1rem` | Padding padrao |")
    lines.append("| `--space-lg` | `24px` / `1.5rem` | Padding de secao |")
    lines.append("| `--space-xl` | `32px` / `2rem` | Espacos grandes |")
    lines.append("| `--space-2xl` | `48px` / `3rem` | Margens de secao |")
    lines.append("| `--space-3xl` | `64px` / `4rem` | Padding de hero |")
    lines.append("")
    
    # Profundidades de Sombra
    lines.append("### Profundidades de Sombra")
    lines.append("")
    lines.append("| Nivel | Valor | Uso |")
    lines.append("|-------|-------|-----|")
    lines.append("| `--shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | Elevacao sutil |")
    lines.append("| `--shadow-md` | `0 4px 6px rgba(0,0,0,0.1)` | Cards, botoes |")
    lines.append("| `--shadow-lg` | `0 10px 15px rgba(0,0,0,0.1)` | Modais, dropdowns |")
    lines.append("| `--shadow-xl` | `0 20px 25px rgba(0,0,0,0.15)` | Imagens hero, cards destaque |")
    lines.append("")
    
    # Secao de specs de componentes
    lines.append("---")
    lines.append("")
    lines.append("## Specs de Componentes")
    lines.append("")
    
    # Botoes
    lines.append("### Botoes")
    lines.append("")
    lines.append("```css")
    lines.append("/* Botao Primario */")
    lines.append(".btn-primary {")
    lines.append(f"  background: {colors.get('cta', '#F97316')};")
    lines.append("  color: white;")
    lines.append("  padding: 12px 24px;")
    lines.append("  border-radius: 8px;")
    lines.append("  font-weight: 600;")
    lines.append("  transition: all 200ms ease;")
    lines.append("  cursor: pointer;")
    lines.append("}")
    lines.append("")
    lines.append(".btn-primary:hover {")
    lines.append("  opacity: 0.9;")
    lines.append("  transform: translateY(-1px);")
    lines.append("}")
    lines.append("")
    lines.append("/* Botao Secundario */")
    lines.append(".btn-secondary {")
    lines.append(f"  background: transparent;")
    lines.append(f"  color: {colors.get('primary', '#2563EB')};")
    lines.append(f"  border: 2px solid {colors.get('primary', '#2563EB')};")
    lines.append("  padding: 12px 24px;")
    lines.append("  border-radius: 8px;")
    lines.append("  font-weight: 600;")
    lines.append("  transition: all 200ms ease;")
    lines.append("  cursor: pointer;")
    lines.append("}")
    lines.append("```")
    lines.append("")
    
    # Cards
    lines.append("### Cards")
    lines.append("")
    lines.append("```css")
    lines.append(".card {")
    lines.append(f"  background: {colors.get('background', '#FFFFFF')};")
    lines.append("  border-radius: 12px;")
    lines.append("  padding: 24px;")
    lines.append("  box-shadow: var(--shadow-md);")
    lines.append("  transition: all 200ms ease;")
    lines.append("  cursor: pointer;")
    lines.append("}")
    lines.append("")
    lines.append(".card:hover {")
    lines.append("  box-shadow: var(--shadow-lg);")
    lines.append("  transform: translateY(-2px);")
    lines.append("}")
    lines.append("```")
    lines.append("")
    
    # Campos de entrada
    lines.append("### Campos de Entrada")
    lines.append("")
    lines.append("```css")
    lines.append(".input {")
    lines.append("  padding: 12px 16px;")
    lines.append("  border: 1px solid #E2E8F0;")
    lines.append("  border-radius: 8px;")
    lines.append("  font-size: 16px;")
    lines.append("  transition: border-color 200ms ease;")
    lines.append("}")
    lines.append("")
    lines.append(".input:focus {")
    lines.append(f"  border-color: {colors.get('primary', '#2563EB')};")
    lines.append("  outline: none;")
    lines.append(f"  box-shadow: 0 0 0 3px {colors.get('primary', '#2563EB')}20;")
    lines.append("}")
    lines.append("```")
    lines.append("")
    
    # Modais
    lines.append("### Modais")
    lines.append("")
    lines.append("```css")
    lines.append(".modal-overlay {")
    lines.append("  background: rgba(0, 0, 0, 0.5);")
    lines.append("  backdrop-filter: blur(4px);")
    lines.append("}")
    lines.append("")
    lines.append(".modal {")
    lines.append("  background: white;")
    lines.append("  border-radius: 16px;")
    lines.append("  padding: 32px;")
    lines.append("  box-shadow: var(--shadow-xl);")
    lines.append("  max-width: 500px;")
    lines.append("  width: 90%;")
    lines.append("}")
    lines.append("```")
    lines.append("")
    
    # Secao de estilo
    lines.append("---")
    lines.append("")
    lines.append("## Diretrizes de Estilo")
    lines.append("")
    lines.append(f"**Estilo:** {style.get('name', 'Minimalism')}")
    lines.append("")
    if style.get("keywords"):
        lines.append(f"**Palavras-chave:** {style.get('keywords', '')}")
        lines.append("")
    if style.get("best_for"):
        lines.append(f"**Melhor Para:** {style.get('best_for', '')}")
        lines.append("")
    if effects:
        lines.append(f"**Efeitos Principais:** {effects}")
        lines.append("")
    
    # Padrao de Layout
    lines.append("### Padrao de Pagina")
    lines.append("")
    lines.append(f"**Nome do Padrao:** {pattern.get('name', '')}")
    lines.append("")
    if pattern.get('conversion'):
        lines.append(f"- **Estrategia de Conversao:** {pattern.get('conversion', '')}")
    if pattern.get('cta_placement'):
        lines.append(f"- **Posicao do CTA:** {pattern.get('cta_placement', '')}")
    lines.append(f"- **Ordem das Secoes:** {pattern.get('sections', '')}")
    lines.append("")
    
    # Secao de Anti-Patterns
    lines.append("---")
    lines.append("")
    lines.append("## Anti-Patterns (NAO Use)")
    lines.append("")
    if anti_patterns:
        anti_list = [a.strip() for a in anti_patterns.split("+")]
        for anti in anti_list:
            if anti:
                lines.append(f"- ❌ {anti}")
    lines.append("")
    lines.append("### Padroes Proibidos Adicionais")
    lines.append("")
    lines.append("- ❌ **Emojis como icones** — Use icones SVG (Heroicons, Lucide, Simple Icons)")
    lines.append("- ❌ **Falta de cursor:pointer** — Todos os elementos clicaveis devem ter cursor:pointer")
    lines.append("- ❌ **Hovers que deslocam layout** — Evite transforms de escala que deslocam o layout")
    lines.append("- ❌ **Texto com baixo contraste** — Manter taxa de contraste minima de 4.5:1")
    lines.append("- ❌ **Mudancas de estado instantaneas** — Sempre use transicoes (150-300ms)")
    lines.append("- ❌ **Estados de foco invisiveis** — Estados de foco devem ser visiveis para acessibilidade")
    lines.append("")
    
    # Checklist Pre-Entrega
    lines.append("---")
    lines.append("")
    lines.append("## Checklist Pre-Entrega")
    lines.append("")
    lines.append("Antes de entregar qualquer codigo de UI, verifique:")
    lines.append("")
    lines.append("- [ ] Sem emojis usados como icones (use SVG)")
    lines.append("- [ ] Todos os icones de um set consistente (Heroicons/Lucide)")
    lines.append("- [ ] `cursor-pointer` em todos os elementos clicaveis")
    lines.append("- [ ] Estados hover com transicoes suaves (150-300ms)")
    lines.append("- [ ] Modo claro: contraste de texto 4.5:1 minimo")
    lines.append("- [ ] Estados de foco visiveis para navegacao por teclado")
    lines.append("- [ ] `prefers-reduced-motion` respeitado")
    lines.append("- [ ] Responsivo: 375px, 768px, 1024px, 1440px")
    lines.append("- [ ] Sem conteudo escondido atras de navbars fixas")
    lines.append("- [ ] Sem scroll horizontal no mobile")
    lines.append("")
    
    return "\n".join(lines)


def format_page_override_md(design_system: dict, page_name: str, page_query: str = None) -> str:
    """Formatar arquivo de override por pagina com conteudo inteligente."""
    project = design_system.get("project_name", "PROJECT")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    page_title = page_name.replace("-", " ").replace("_", " ").title()
    
    # Detectar tipo de pagina e gerar overrides inteligentes
    page_overrides = _generate_intelligent_overrides(page_name, page_query, design_system)
    
    lines = []
    
    lines.append(f"# Overrides da Pagina {page_title}")
    lines.append("")
    lines.append(f"> **PROJETO:** {project}")
    lines.append(f"> **Gerado em:** {timestamp}")
    lines.append(f"> **Tipo de Pagina:** {page_overrides.get('page_type', 'General')}")
    lines.append("")
    lines.append("> ⚠️ **IMPORTANTE:** Regras neste arquivo **sobrescrevem** o arquivo Master (`design-system/MASTER.md`).")
    lines.append("> Apenas desvios do Master sao documentados aqui. Para todas as outras regras, consulte o Master.")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Regras especificas da pagina com conteudo real
    lines.append("## Regras Especificas da Pagina")
    lines.append("")
    
    # Overrides de Layout
    lines.append("### Overrides de Layout")
    lines.append("")
    layout = page_overrides.get("layout", {})
    if layout:
        for key, value in layout.items():
            lines.append(f"- **{key}:** {value}")
    else:
        lines.append("- Sem overrides — usar layout do Master")
    lines.append("")
    
    # Overrides de Espacamento
    lines.append("### Overrides de Espacamento")
    lines.append("")
    spacing = page_overrides.get("spacing", {})
    if spacing:
        for key, value in spacing.items():
            lines.append(f"- **{key}:** {value}")
    else:
        lines.append("- Sem overrides — usar espacamento do Master")
    lines.append("")
    
    # Overrides de Tipografia
    lines.append("### Overrides de Tipografia")
    lines.append("")
    typography = page_overrides.get("typography", {})
    if typography:
        for key, value in typography.items():
            lines.append(f"- **{key}:** {value}")
    else:
        lines.append("- Sem overrides — usar tipografia do Master")
    lines.append("")
    
    # Overrides de Cores
    lines.append("### Overrides de Cores")
    lines.append("")
    colors = page_overrides.get("colors", {})
    if colors:
        for key, value in colors.items():
            lines.append(f"- **{key}:** {value}")
    else:
        lines.append("- Sem overrides — usar cores do Master")
    lines.append("")
    
    # Overrides de Componentes
    lines.append("### Overrides de Componentes")
    lines.append("")
    components = page_overrides.get("components", [])
    if components:
        for comp in components:
            lines.append(f"- {comp}")
    else:
        lines.append("- Sem overrides — usar specs de componentes do Master")
    lines.append("")
    
    # Componentes Especificos da Pagina
    lines.append("---")
    lines.append("")
    lines.append("## Componentes Especificos da Pagina")
    lines.append("")
    unique_components = page_overrides.get("unique_components", [])
    if unique_components:
        for comp in unique_components:
            lines.append(f"- {comp}")
    else:
        lines.append("- Sem componentes unicos para esta pagina")
    lines.append("")
    
    # Recomendacoes
    lines.append("---")
    lines.append("")
    lines.append("## Recomendacoes")
    lines.append("")
    recommendations = page_overrides.get("recommendations", [])
    if recommendations:
        for rec in recommendations:
            lines.append(f"- {rec}")
    lines.append("")
    
    return "\n".join(lines)


def _generate_intelligent_overrides(page_name: str, page_query: str, design_system: dict) -> dict:
    """
    Gerar overrides inteligentes baseados no tipo de pagina usando busca em camadas.

    Usa a infraestrutura de busca existente para encontrar dados relevantes de estilo,
    UX e layout ao inves de tipos de pagina hardcoded.
    """
    from core import search
    
    page_lower = page_name.lower()
    query_lower = (page_query or "").lower()
    combined_context = f"{page_lower} {query_lower}"
    
    # Buscar em multiplos dominios por orientacao especifica de pagina
    style_search = search(combined_context, "style", max_results=1)
    ux_search = search(combined_context, "ux", max_results=3)
    landing_search = search(combined_context, "landing", max_results=1)
    
    # Extrair resultados da resposta de busca
    style_results = style_search.get("results", [])
    ux_results = ux_search.get("results", [])
    landing_results = landing_search.get("results", [])
    
    # Detectar tipo de pagina a partir dos resultados ou contexto
    page_type = _detect_page_type(combined_context, style_results)
    
    # Construir overrides a partir dos resultados de busca
    layout = {}
    spacing = {}
    typography = {}
    colors = {}
    components = []
    unique_components = []
    recommendations = []
    
    # Extrair overrides baseados em estilo
    if style_results:
        style = style_results[0]
        style_name = style.get("Style Category", "")
        keywords = style.get("Keywords", "")
        best_for = style.get("Best For", "")
        effects = style.get("Effects & Animation", "")
        
        # Inferir layout a partir de palavras-chave de estilo
        if any(kw in keywords.lower() for kw in ["data", "dense", "dashboard", "grid"]):
            layout["Max Width"] = "1400px or full-width"
            layout["Grid"] = "12-column grid for data flexibility"
            spacing["Content Density"] = "High — optimize for information display"
        elif any(kw in keywords.lower() for kw in ["minimal", "simple", "clean", "single"]):
            layout["Max Width"] = "800px (narrow, focused)"
            layout["Layout"] = "Single column, centered"
            spacing["Content Density"] = "Low — focus on clarity"
        else:
            layout["Max Width"] = "1200px (standard)"
            layout["Layout"] = "Full-width sections, centered content"
        
        if effects:
            recommendations.append(f"Effects: {effects}")
    
    # Extrair diretrizes de UX como recomendacoes
    for ux in ux_results:
        category = ux.get("Category", "")
        do_text = ux.get("Do", "")
        dont_text = ux.get("Don't", "")
        if do_text:
            recommendations.append(f"{category}: {do_text}")
        if dont_text:
            components.append(f"Avoid: {dont_text}")
    
    # Extrair info de padrao de landing para estrutura de secoes
    if landing_results:
        landing = landing_results[0]
        sections = landing.get("Section Order", "")
        cta_placement = landing.get("Primary CTA Placement", "")
        color_strategy = landing.get("Color Strategy", "")
        
        if sections:
            layout["Sections"] = sections
        if cta_placement:
            recommendations.append(f"CTA Placement: {cta_placement}")
        if color_strategy:
            colors["Strategy"] = color_strategy
    
    # Adicionar defaults especificos do tipo de pagina se sem resultados
    if not layout:
        layout["Max Width"] = "1200px"
        layout["Layout"] = "Responsive grid"
    
    if not recommendations:
        recommendations = [
            "Consultar MASTER.md para todas as regras de design",
            "Adicionar overrides especificos conforme necessario para esta pagina"
        ]
    
    return {
        "page_type": page_type,
        "layout": layout,
        "spacing": spacing,
        "typography": typography,
        "colors": colors,
        "components": components,
        "unique_components": unique_components,
        "recommendations": recommendations
    }


def _detect_page_type(context: str, style_results: list) -> str:
    """Detectar tipo de pagina a partir do contexto e resultados de busca."""
    context_lower = context.lower()
    
    # Verificar padroes comuns de tipo de pagina
    page_patterns = [
        (["dashboard", "admin", "analytics", "data", "metrics", "stats", "monitor", "overview"], "Dashboard / Data View"),
        (["checkout", "payment", "cart", "purchase", "order", "billing"], "Checkout / Payment"),
        (["settings", "profile", "account", "preferences", "config"], "Settings / Profile"),
        (["landing", "marketing", "homepage", "hero", "home", "promo"], "Landing / Marketing"),
        (["login", "signin", "signup", "register", "auth", "password"], "Authentication"),
        (["pricing", "plans", "subscription", "tiers", "packages"], "Pricing / Plans"),
        (["blog", "article", "post", "news", "content", "story"], "Blog / Article"),
        (["product", "item", "detail", "pdp", "shop", "store"], "Product Detail"),
        (["search", "results", "browse", "filter", "catalog", "list"], "Search Results"),
        (["empty", "404", "error", "not found", "zero"], "Empty State"),
    ]
    
    for keywords, page_type in page_patterns:
        if any(kw in context_lower for kw in keywords):
            return page_type
    
    # Fallback: tentar inferir dos resultados de estilo
    if style_results:
        style_name = style_results[0].get("Style Category", "").lower()
        best_for = style_results[0].get("Best For", "").lower()
        
        if "dashboard" in best_for or "data" in best_for:
            return "Dashboard / Data View"
        elif "landing" in best_for or "marketing" in best_for:
            return "Landing / Marketing"
    
    return "General"


# ============ SUPORTE CLI ============
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Gerar Design System")
    parser.add_argument("query", help="Query de busca (ex: 'SaaS dashboard')")
    parser.add_argument("--project-name", "-p", type=str, default=None, help="Nome do projeto")
    parser.add_argument("--format", "-f", choices=["ascii", "markdown"], default="ascii", help="Formato de saida")

    args = parser.parse_args()

    result = generate_design_system(args.query, args.project_name, args.format)
    print(result)
