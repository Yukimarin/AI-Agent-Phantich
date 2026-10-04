# -*- coding: utf-8 -*-
"""
Ultra-Modern UI Re-Architect for All DGNL Reports
Theme: Modern Executive Bento Grid, High-Contrast Typography, Clean Action Cards, Refined Hierarchy
"""
import json
import os
import sys

sys.path.append(os.path.dirname(__file__))
from build_complete_suite import load_data

def get_shared_css(primary_color="#3b82f6", accent_color="#8b5cf6"):
    return f"""
    :root {{
        --bg-body:       #0c0d10;
        --bg-surface:    #14151a;
        --bg-surface-elevated: #1a1b22;
        --bg-card:       #171820;
        --border-subtle: #242632;
        --border-focus:  #36394a;
        --text-main:     #f8fafc;
        --text-muted:    #94a3b8;
        --text-dim:      #64748b;
        --color-pri:     {primary_color};
        --color-acc:     {accent_color};
        --color-ks24:    #10b981;
        --color-ks25:    #3b82f6;
        --color-qtkd:    #f59e0b;
        --color-danger:  #f43f5e;
        --color-success: #10b981;
        --color-warning: #f59e0b;
        --radius-sm:     6px;
        --radius-md:     10px;
        --radius-lg:     14px;
        --font-main:     'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        --font-heading:  'Outfit', sans-serif;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: var(--font-main); }}
    body {{ background: var(--bg-body); color: var(--text-main); line-height: 1.5; padding-bottom: 80px; -webkit-font-smoothing: antialiased; }}

    /* ── HEADER ── */
    .header {{
        background: rgba(18, 19, 26, 0.85);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid var(--border-subtle);
        position: sticky; top: 0; z-index: 300;
    }}
    .header-inner {{
        max-width: 1440px; margin: 0 auto; padding: 0.9rem 2rem;
        display: flex; justify-content: space-between; align-items: center;
    }}
    .logo-wrap {{ display: flex; align-items: center; gap: 0.85rem; }}
    .logo-badge {{
        background: linear-gradient(135deg, var(--color-pri), var(--color-acc));
        color: #fff; width: 42px; height: 42px; border-radius: var(--radius-md);
        display: flex; align-items: center; justify-content: center;
        font-family: var(--font-heading); font-weight: 800; font-size: 1.15rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }}
    .logo-title {{ font-family: var(--font-heading); font-weight: 700; font-size: 1.12rem; color: #fff; letter-spacing: -0.2px; }}
    .logo-sub {{ font-size: 0.74rem; color: var(--text-muted); margin-top: 1px; }}
    .header-meta {{ font-size: 0.76rem; color: var(--text-dim); text-align: right; line-height: 1.35; }}

    /* ── CONTAINER ── */
    .container {{ max-width: 1440px; margin: 1.75rem auto; padding: 0 2rem; }}

    /* ── TABS ── */
    .nav-tabs-wrapper {{
        background: var(--bg-surface);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-lg);
        padding: 0.35rem;
        margin-bottom: 2rem;
        display: inline-flex;
        gap: 0.25rem;
        overflow-x: auto;
        max-width: 100%;
    }}
    .nav-tab-btn {{
        background: transparent; border: none; color: var(--text-muted);
        font-family: var(--font-heading); font-size: 0.88rem; font-weight: 600;
        padding: 0.6rem 1.25rem; border-radius: var(--radius-md); cursor: pointer;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex; align-items: center; gap: 0.45rem; white-space: nowrap;
    }}
    .nav-tab-btn:hover {{ color: var(--text-main); background: rgba(255,255,255,0.04); }}
    .nav-tab-btn.active {{
        color: #fff; background: var(--bg-surface-elevated);
        border: 1px solid var(--border-focus);
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }}

    .tab-pane {{ display: none; }}
    .tab-pane.active {{ display: block; animation: fadeInUp 0.3s ease; }}
    @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}

    /* ── KPI BENTO STRIP ── */
    .kpi-grid {{
        display: grid; grid-template-columns: repeat(6, 1fr); gap: 1rem; margin-bottom: 2rem;
    }}
    .kpi-card {{
        background: var(--bg-card); border: 1px solid var(--border-subtle);
        border-radius: var(--radius-lg); padding: 1.15rem 1.25rem;
        position: relative; overflow: hidden; transition: transform 0.2s, border-color 0.2s;
    }}
    .kpi-card:hover {{ transform: translateY(-2px); border-color: var(--border-focus); }}
    .kpi-card::before {{
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
        background: var(--kpi-accent, var(--color-pri));
    }}
    .kpi-label {{ font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.6px; color: var(--text-dim); margin-bottom: 0.35rem; font-weight: 700; }}
    .kpi-value {{ font-family: var(--font-heading); font-size: 1.75rem; font-weight: 800; color: #fff; letter-spacing: -0.5px; line-height: 1.1; }}
    .kpi-sub   {{ font-size: 0.72rem; color: var(--text-muted); margin-top: 0.35rem; font-weight: 500; }}

    /* ── SECTION HEADINGS ── */
    .section-header {{
        display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;
    }}
    .section-title {{
        font-family: var(--font-heading); font-size: 1.15rem; font-weight: 700;
        color: #fff; display: flex; align-items: center; gap: 0.6rem; letter-spacing: -0.2px;
    }}
    .section-desc {{ font-size: 0.8rem; color: var(--text-muted); margin-top: 0.15rem; }}

    /* ── BENTO CARD BASE ── */
    .bento-card {{
        background: var(--bg-card); border: 1px solid var(--border-subtle);
        border-radius: var(--radius-lg); padding: 1.5rem; margin-bottom: 1.75rem;
    }}

    /* ── BOTTLENECK ALERT BANNER ── */
    .bottleneck-banner {{
        background: linear-gradient(180deg, rgba(244,63,94,0.08) 0%, rgba(244,63,94,0.02) 100%);
        border: 1px solid rgba(244,63,94,0.35); border-radius: var(--radius-lg);
        padding: 1.5rem; margin-bottom: 2rem;
    }}
    .bottleneck-title {{
        font-family: var(--font-heading); font-size: 1rem; font-weight: 700; color: #fb7185;
        display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;
    }}
    .bottleneck-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }}
    .bottleneck-cell {{
        background: rgba(12, 13, 16, 0.6); border: 1px solid rgba(244,63,94,0.2);
        border-radius: var(--radius-md); padding: 1rem; display: flex; flex-direction: column;
    }}
    .bottleneck-cell strong {{ font-size: 0.84rem; color: #fff; margin-bottom: 0.35rem; display: block; }}
    .bottleneck-cell p {{ font-size: 0.77rem; color: var(--text-muted); line-height: 1.45; margin-top: auto; }}

    /* ── CURRICULUM BENTO CARDS (REDESIGNED) ── */
    .curric-bento-grid {{
        display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; margin-bottom: 2rem;
    }}
    .curric-cohort-card {{
        background: var(--bg-surface); border: 1px solid var(--border-subtle);
        border-radius: var(--radius-lg); padding: 1.5rem; display: flex; flex-direction: column; gap: 1.25rem;
    }}
    .curric-cohort-header {{
        display: flex; justify-content: space-between; align-items: flex-start;
        padding-bottom: 0.85rem; border-bottom: 1px solid var(--border-subtle);
    }}
    .cohort-badge-tag {{
        display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.3rem 0.75rem;
        border-radius: 999px; font-size: 0.75rem; font-weight: 700; font-family: var(--font-heading);
    }}
    .cohort-badge-tag.ks24 {{ background: rgba(16,185,129,0.12); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }}
    .cohort-badge-tag.ks25 {{ background: rgba(59,130,246,0.12); color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }}
    .cohort-badge-tag.qtkd {{ background: rgba(245,158,11,0.12); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }}

    /* Subject Item Card */
    .subject-item-card {{
        background: var(--bg-card); border: 1px solid var(--border-subtle);
        border-radius: var(--radius-md); padding: 1.15rem; transition: border-color 0.2s;
    }}
    .subject-item-card:hover {{ border-color: var(--border-focus); }}
    .subject-item-top {{
        display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.65rem;
    }}
    .subject-code {{
        font-family: var(--font-heading); font-size: 0.82rem; font-weight: 700; color: #fff;
        display: flex; align-items: center; gap: 0.4rem;
    }}
    .credit-tag {{
        background: rgba(255,255,255,0.06); color: var(--text-muted);
        font-size: 0.7rem; padding: 0.15rem 0.5rem; border-radius: 4px; font-weight: 600;
    }}
    .action-tag {{
        font-size: 0.7rem; font-weight: 700; padding: 0.2rem 0.55rem; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.3px;
    }}
    .action-tag.core {{ background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }}
    .action-tag.sec  {{ background: rgba(59,130,246,0.15); color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }}
    .action-tag.ai   {{ background: rgba(139,92,246,0.15); color: #a78bfa; border: 1px solid rgba(139,92,246,0.3); }}
    .action-tag.reduce {{ background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }}

    .subject-feature-list {{ list-style: none; display: flex; flex-direction: column; gap: 0.45rem; }}
    .subject-feature-list li {{
        font-size: 0.78rem; color: var(--text-muted); line-height: 1.45;
        display: flex; gap: 0.5rem; align-items: flex-start;
    }}
    .subject-feature-list li strong {{ color: var(--text-main); font-weight: 600; }}
    .subject-feature-list li::before {{
        content: '✓'; color: var(--color-ks24); font-weight: 800; font-size: 0.75rem; flex-shrink: 0; margin-top: 1px;
    }}
    .subject-feature-list.blue li::before {{ color: var(--color-ks25); }}
    .subject-feature-list.gold li::before {{ color: var(--color-qtkd); }}

    /* Elective VIP Box */
    .elective-vip-card {{
        background: linear-gradient(135deg, rgba(139,92,246,0.08) 0%, rgba(59,130,246,0.04) 100%);
        border: 1px solid rgba(139,92,246,0.35); border-radius: var(--radius-lg);
        padding: 1.25rem 1.5rem; margin-top: 0.5rem;
    }}
    .elective-vip-title {{
        font-family: var(--font-heading); font-size: 0.95rem; font-weight: 700; color: #c084fc;
        display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.85rem;
    }}
    .elective-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }}
    .elective-item {{
        background: rgba(12, 13, 16, 0.7); border: 1px solid rgba(139,92,246,0.25);
        border-radius: var(--radius-md); padding: 1rem;
    }}
    .elective-item strong {{ font-size: 0.84rem; color: #fff; display: block; margin-bottom: 0.35rem; }}
    .elective-item p {{ font-size: 0.76rem; color: var(--text-muted); line-height: 1.45; }}

    /* ── TABLES ── */
    .table-wrapper {{ overflow-x: auto; border-radius: var(--radius-md); border: 1px solid var(--border-subtle); }}
    .data-table {{ width: 100%; border-collapse: collapse; font-size: 0.82rem; }}
    .data-table th, .data-table td {{ padding: 0.75rem 0.9rem; text-align: center; border-bottom: 1px solid var(--border-subtle); }}
    .data-table th {{
        background: var(--bg-surface-elevated); color: var(--text-muted);
        font-family: var(--font-heading); font-weight: 600; font-size: 0.72rem;
        text-transform: uppercase; letter-spacing: 0.5px;
    }}
    .data-table tr:hover td {{ background: rgba(255,255,255,0.02); }}
    .data-table tr:last-child td {{ border-bottom: none; }}

    /* Badges */
    .badge {{
        display: inline-flex; align-items: center; gap: 0.25rem;
        padding: 0.2rem 0.6rem; border-radius: 999px;
        font-size: 0.72rem; font-weight: 700; line-height: 1.3;
    }}
    .badge.pass {{ background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }}
    .badge.lvl-3 {{ background: rgba(139,92,246,0.15); color: #a78bfa; border: 1px solid rgba(139,92,246,0.3); }}
    .badge.lvl-2 {{ background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }}
    .badge.lvl-1 {{ background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }}
    .badge.lvl-0 {{ background: rgba(244,63,94,0.15); color: #fb7185; border: 1px solid rgba(244,63,94,0.3); }}

    /* Filter Bar */
    .filter-bar {{
        display: flex; gap: 0.75rem; flex-wrap: wrap; margin-bottom: 1.25rem;
        background: var(--bg-surface); border: 1px solid var(--border-subtle);
        padding: 0.85rem 1rem; border-radius: var(--radius-lg); align-items: center;
    }}
    .filter-input, .filter-select {{
        background: var(--bg-card); border: 1px solid var(--border-subtle);
        color: #fff; padding: 0.55rem 0.85rem; border-radius: var(--radius-md);
        font-size: 0.82rem; outline: none; transition: border-color 0.2s;
    }}
    .filter-input:focus, .filter-select:focus {{ border-color: var(--color-pri); }}

    /* Footer */
    .footer-bar {{
        margin-top: 3.5rem; border-top: 1px solid var(--border-subtle);
        padding-top: 1.5rem; display: flex; justify-content: space-between; align-items: center;
        font-size: 0.76rem; color: var(--text-dim);
    }}
    .footer-bar a {{ color: var(--color-pri); text-decoration: none; font-weight: 600; }}
    """

print("Shared modern CSS engine loaded.")
