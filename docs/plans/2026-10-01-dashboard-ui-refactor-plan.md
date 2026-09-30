# Dashboard UI Refactor Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Refactor the K26 Violation Dashboard comparison table to use a minimalist inline UI for CC, BT, and EL metrics without cluttering the rows.

**Architecture:** We will inject custom CSS classes into the existing HTML `<style>` block and update the JavaScript rendering logic (`compHTML`) to output inline spans instead of stacked divs.

**Tech Stack:** HTML, CSS, JavaScript (Vanilla)

---

### Task 1: Add CSS Classes for Minimalist Alerting

**Files:**
- Modify: `output/dashboards/management/k26_violation_dashboard.html`

**Step 1: Write the minimal implementation**
We will add the following CSS to the `<style>` block:

```css
        .text-safe { color: #94a3b8; }
        .text-warn { color: #d97706; font-weight: 600; }
        .text-danger { color: #e11d48; font-weight: 700; }
        .text-divider { color: #cbd5e1; margin: 0 4px; }
```

**Step 2: Commit**

```bash
git add output/dashboards/management/k26_violation_dashboard.html
git commit -m "style: add minimalist alerting css classes"
```

---

### Task 2: Update Table Headers

**Files:**
- Modify: `output/dashboards/management/k26_violation_dashboard.html`

**Step 1: Write the minimal implementation**
Update the table header HTML from:
```html
<th>Lớp</th><th style="min-width: 140px;">SSK101 (CC / BT / EL)</th><th style="min-width: 140px;" id="col-course-1">Môn 1</th><th style="min-width: 140px;" id="col-course-2">Môn 2</th><th style="min-width: 140px;" id="col-course-3">Môn 3</th><th>Xu hướng (CC)</th>
```
To:
```html
<th>Lớp</th><th style="min-width: 160px;">SSK101 <br><span style="font-size:0.75rem; font-weight:normal; color:#64748b">(CC | BT | EL)</span></th><th style="min-width: 160px;" id="col-course-1">Môn 1</th><th style="min-width: 160px;" id="col-course-2">Môn 2</th><th style="min-width: 160px;" id="col-course-3">Môn 3</th><th>Xu hướng (CC)</th>
```

**Step 2: Commit**

```bash
git add output/dashboards/management/k26_violation_dashboard.html
git commit -m "feat: update comparison table headers layout"
```

---

### Task 3: Refactor JavaScript Render Logic

**Files:**
- Modify: `output/dashboards/management/k26_violation_dashboard.html`

**Step 1: Write the minimal implementation**
Update the `renderStats` function and `courseCells` logic in the JavaScript block to generate inline spans.

```javascript
    const getLevelClass = (v) => v >= 20 ? 'text-danger' : v >= 10 ? 'text-warn' : 'text-safe';
    const renderStats = (stat) => {
        const cc = stat.ccViolationPct || 0;
        const bt = stat.btViolationPct || 0;
        const el = stat.elViolationPct || 0;
        return \`<span class="\${getLevelClass(cc)}">CC: \${cc.toFixed(1)}%</span> \` +
               \`<span class="text-divider">|</span> \` +
               \`<span class="\${getLevelClass(bt)}">BT: \${bt.toFixed(1)}%</span> \` +
               \`<span class="text-divider">|</span> \` +
               \`<span class="\${getLevelClass(el)}">EL: \${el.toFixed(1)}%</span>\`;
    };
    const courses = Object.entries(comp.currentCourses).filter(([k]) => k !== 'Orientation');
    const courseCells = courses.slice(0, 3).map(([name, v]) => \`<td>\${name} <br><div style="font-size:0.8rem; margin-top:4px;">\${renderStats(v)}</div></td>\`).join('');
```

And similarly, update the SSK101 cell:
```javascript
        <td>SSK101 <br><div style="font-size:0.8rem; margin-top:4px;">${renderStats(ssk)}</div></td>
```

**Step 2: Commit**

```bash
git add output/dashboards/management/k26_violation_dashboard.html
git commit -m "feat: apply inline minimalist ui to comparison table"
```
