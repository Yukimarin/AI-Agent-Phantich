# -*- coding: utf-8 -*-
"""
Ultra-Polished Curriculum Architecture & Visual Redesign v7
"""
import json
import os
import sys

sys.path.append(os.path.dirname(__file__))
from build_complete_suite import load_data
from modern_theme import get_shared_css

def get_enhanced_curriculum_css():
    return """
    /* ── ENHANCED CURRICULUM SECTION STYLES ── */
    .curric-overview-strip {
        display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem;
    }
    .curric-pill-stat {
        background: var(--bg-surface); border: 1px solid var(--border-subtle);
        border-radius: var(--radius-md); padding: 0.85rem 1.15rem;
        display: flex; align-items: center; justify-content: space-between;
    }
    .curric-pill-stat strong { font-size: 0.85rem; color: #fff; }
    .curric-pill-stat span { font-size: 0.75rem; color: var(--text-muted); }

    .curric-tri-grid {
        display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.25rem; margin-bottom: 1.75rem;
    }
    .curric-column {
        background: var(--bg-surface); border: 1px solid var(--border-subtle);
        border-radius: var(--radius-lg); padding: 1.25rem;
        display: flex; flex-direction: column; gap: 1rem;
    }
    .curric-column-header {
        display: flex; justify-content: space-between; align-items: flex-start;
        padding-bottom: 0.85rem; border-bottom: 1px solid var(--border-subtle);
    }
    .curric-column-title { font-family: var(--font-heading); font-size: 0.98rem; font-weight: 700; color: #fff; }
    .curric-column-sub { font-size: 0.74rem; color: var(--text-muted); margin-top: 2px; }

    /* Modern Subject Decision Card */
    .decision-card {
        background: var(--bg-card); border: 1px solid var(--border-subtle);
        border-radius: var(--radius-md); padding: 1rem;
        display: flex; flex-direction: column; gap: 0.65rem;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .decision-card:hover { transform: translateY(-2px); border-color: var(--border-focus); }
    
    .decision-card-top {
        display: flex; justify-content: space-between; align-items: center; gap: 0.5rem;
    }
    .subject-name-tag {
        font-family: var(--font-heading); font-size: 0.84rem; font-weight: 700; color: #fff;
        display: flex; align-items: center; gap: 0.4rem;
    }
    .code-chip {
        background: rgba(255,255,255,0.06); color: var(--text-muted);
        font-size: 0.68rem; font-weight: 600; padding: 0.15rem 0.45rem; border-radius: 4px;
    }
    .status-badge {
        font-size: 0.67rem; font-weight: 700; padding: 0.2rem 0.5rem; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.4px;
    }
    .status-badge.upgrade { background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }
    .status-badge.reduce  { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }
    .status-badge.newmod  { background: rgba(59,130,246,0.15); color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }
    .status-badge.danger  { background: rgba(244,63,94,0.15); color: #fb7185; border: 1px solid rgba(244,63,94,0.3); }

    /* 2-Tone Problem & Action Block */
    .gap-block {
        background: rgba(244,63,94,0.06); border-left: 3px solid #f43f5e;
        padding: 0.45rem 0.65rem; border-radius: 0 4px 4px 0;
        font-size: 0.75rem; color: #fecdd3; line-height: 1.4;
    }
    .gap-block strong { color: #fb7185; font-weight: 700; }

    .action-block {
        background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05);
        padding: 0.55rem 0.65rem; border-radius: 6px;
    }
    .action-list { list-style: none; display: flex; flex-direction: column; gap: 0.4rem; }
    .action-list li {
        font-size: 0.76rem; color: var(--text-muted); line-height: 1.45;
        display: flex; gap: 0.45rem; align-items: flex-start;
    }
    .action-list li strong { color: #f1f5f9; font-weight: 600; }
    .action-list li::before {
        content: '⚡'; font-size: 0.7rem; flex-shrink: 0; margin-top: 1px; color: var(--color-pri);
    }
    .action-list.green li::before { color: #10b981; }
    .action-list.blue li::before { color: #3b82f6; }
    .action-list.gold li::before { color: #f59e0b; }

    /* Wide Electives VIP Banner */
    .electives-master-banner {
        background: linear-gradient(135deg, rgba(139,92,246,0.08) 0%, rgba(59,130,246,0.04) 50%, rgba(16,185,129,0.04) 100%);
        border: 1px solid rgba(139,92,246,0.35); border-radius: var(--radius-lg);
        padding: 1.5rem;
    }
    .electives-banner-header {
        display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;
    }
    .electives-banner-title {
        font-family: var(--font-heading); font-size: 1.05rem; font-weight: 700; color: #c084fc;
        display: flex; align-items: center; gap: 0.5rem;
    }
    .electives-grid-3 {
        display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.25rem;
    }
    .elective-card-box {
        background: rgba(12, 13, 16, 0.7); border: 1px solid rgba(139,92,246,0.25);
        border-radius: var(--radius-md); padding: 1.15rem;
        display: flex; flex-direction: column; justify-content: space-between;
    }
    .elective-target-role {
        display: inline-flex; align-items: center; gap: 0.35rem;
        background: rgba(139,92,246,0.15); color: #c084fc; border: 1px solid rgba(139,92,246,0.3);
        font-size: 0.68rem; font-weight: 700; padding: 0.15rem 0.5rem; border-radius: 4px;
        margin-bottom: 0.5rem; text-transform: uppercase;
    }
    .elective-card-name { font-family: var(--font-heading); font-size: 0.9rem; font-weight: 700; color: #fff; margin-bottom: 0.35rem; }
    .elective-card-desc { font-size: 0.76rem; color: var(--text-muted); line-height: 1.45; }
    .elective-skills-tag {
        margin-top: 0.75rem; padding-top: 0.65rem; border-top: 1px solid rgba(255,255,255,0.06);
        font-size: 0.72rem; color: #a78bfa; font-weight: 600; display: flex; gap: 0.35rem; flex-wrap: wrap;
    }
    """

print("Enhanced curriculum styling ready.")
