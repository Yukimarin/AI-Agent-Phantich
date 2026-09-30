# Dashboard UI Refactor Design

## Context
The previous update to the K26 Violation Dashboard (`k26_violation_dashboard.html`) added Comprehensive (CC/BT/EL) metrics to the comparison table. However, it stacked these metrics vertically in individual blocks/cards, resulting in extremely tall table rows, cluttered visuals, and poor scannability ("nhìn không tổng thể, UI/UX không tốt"). The user requested a minimalist approach that maintains the comprehensive view without the clutter.

## Requirements
- Display CC (Chuyên cần), BT (BTVN), and EL (Elearning) side-by-side in a single line.
- Avoid large badges/cards.
- Retain alerting for high-risk metrics to allow for quick scanning by the Training Director.
- Update the table headers to clearly denote the metrics layout.

## Approved Design: Inline Minimalist Alerting
1. **HTML Layout:**
   - Instead of a flex-column, metrics will be rendered as inline text: `CC: 0.0% | BT: 27.9% | EL: 0.0%`.
   - The vertical dividers `|` will be colored light gray to visually separate the metrics without drawing attention.

2. **Styling Rules (Minimalist Alerting):**
   - **Safe (0%):** `#94a3b8` (Muted gray) - Blends into the background.
   - **Warning (>= 10%):** `#d97706` (Amber/Warning) - Draws moderate attention.
   - **Danger (>= 20%):** `#e11d48` (Rose/Danger) with `font-weight: bold` - Draws immediate attention.
   - These styles replace the previous chunky `<span class="badge">` backgrounds, relying purely on text color to guide the eye.

3. **Header Optimization:**
   - Headers will be updated to: `CourseName <br><span style="font-size:0.7rem">(CC | BT | EL)</span>` to match the inline format of the data cells.
   - The SSK101 header will follow the exact same format.

## Implementation Steps
1. Add new CSS classes (`.text-safe`, `.text-warn`, `.text-danger`, `.text-divider`) to the `<style>` block in `k26_violation_dashboard.html`.
2. Rewrite the JavaScript template literal inside the comparison table generator (`compHTML`) to output the new inline HTML structure.
3. Update the table `<th>` elements to match the new format.
