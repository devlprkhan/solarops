# SolarOps UI Design Brief

> **Purpose:** Visual and UX direction for the SolarOps Streamlit application. This document describes the design language and intended experience only. It is not an implementation plan or a request to change the ML pipeline.

## 1. Product context

SolarOps is a **solar performance intelligence** application. It helps people understand what a solar installation should produce under its environmental conditions, compare expected output with actual output, and investigate meaningful deviations.

The interface should feel like a credible energy-analytics product used by solar operators, system owners, analysts, and maintenance teams.

The central product story is:

**Solar conditions → Expected generation → Actual generation → Performance deviation → Investigation**

The UI must make that story understandable at a glance. It should communicate operational evidence, not make unsupported claims about equipment faults.

## 2. Design direction

Use the attached solar-energy website screenshots as visual inspiration, not as page templates.

### What to take from the references

- **Reference 1:** clean white space, strong editorial typography, large solar photography, rounded image panels, restrained card layouts, and a dark footer treatment.
- **Reference 2:** deep natural greens, landscape-scale renewable-energy imagery, confident typography, simple navigation, and a balance between large visual sections and concise information.
- Both references use a clear visual hierarchy and avoid making every section look like the same generic card.

### How to adapt this for SolarOps

Translate the references into a **premium energy-monitoring dashboard**, not a solar installation company's marketing website.

The result should feel:
- Professional, calm, technical, and trustworthy.
- Modern and visually distinctive without looking experimental.
- Data-first, with photography used selectively to establish the solar/energy identity.
- Easy to scan during a quick operational check.
- Consistent across all application pages.

Avoid turning the application into a long promotional landing page. The user came to understand system performance, not browse solar products.

## 3. Visual identity

### Colour direction

Use a restrained palette inspired by solar panels, daylight, and the green landscapes in the references.

| Role | Direction |
|---|---|
| Primary | Deep forest green; use for key actions and selected navigation |
| Secondary | Solar / electric green; use sparingly for highlights and positive states |
| Dark surface | Deep charcoal with a subtle green undertone |
| Main background | Warm off-white or very light neutral |
| Card surface | White or near-white |
| Primary text | Dark charcoal, high contrast |
| Secondary text | Muted slate / grey-green |
| Grid and borders | Very light neutral grey |
| Warning | Muted amber |
| Anomaly / critical | Restrained red |
| Unreliable / unavailable | Neutral grey |

Do not make the whole interface bright green. Green is an accent and identity colour; the data must remain easy to read.

Use semantic colours consistently:
- **Normal / healthy:** green.
- **Needs attention / anomaly:** amber or red according to severity.
- **Unreliable input / unavailable:** neutral grey.
- Never use colour alone to communicate a state; pair it with a label or icon.

### Typography

- Use a clean modern sans-serif.
- Use strong, compact page titles and clear section headings.
- Use readable body text with comfortable line height.
- Use tabular numerals for metrics, timestamps, and measurements where possible.
- Keep labels short and explanatory text quieter than the data.
- Avoid oversized marketing-style headlines inside analytical pages.

### Shape, spacing, and surfaces

- Prefer generous spacing and a clear alignment grid.
- Use medium rounded corners on cards, panels, and image containers.
- Use subtle borders and restrained shadows; avoid heavy elevation everywhere.
- Keep card padding consistent.
- Use a small, consistent icon set. Avoid emoji as interface icons.
- Avoid excessive gradients, glassmorphism, decorative blobs, and animated effects.

## 4. Application shell and navigation

The experience should behave like one coherent product, not five unrelated Streamlit demos.

Use the existing application structure and navigation if present. The repository's documented application pages are:

1. **Overview**
2. **Anomalies**
3. **Investigate**
4. **Predict**
5. **Model**

Design the shared shell around these destinations:
- A compact SolarOps brand mark / wordmark.
- Clear primary navigation with an obvious active-page state.
- A consistent content width and page gutter.
- A compact context area for the active solar system / dataset when that concept is supported by the current application.
- A consistent footer or low-emphasis product/version area where useful.

The navigation should remain easy to use on narrow screens. Do not let a large sidebar consume most of the available dashboard width.

## 5. Page-level visual direction

These are design intentions for the documented pages. They are not permission to invent backend capabilities or fabricate data. The coding agent must inspect the current app and use only data and actions that actually exist.

### 5.1 Overview

**Job:** Give the user a fast, trustworthy summary of solar-system performance.

Visual hierarchy:
1. Page title and short context sentence.
2. A compact row of key performance metrics.
3. A prominent expected-versus-actual power visualization.
4. A clear performance / trust status area.
5. Supporting trends and environmental context.
6. A short list of recent items that may need attention, only if the application has this data.

The most important visual should be the relationship between expected and actual AC power. Avoid filling the first screen with decorative content.

Metric cards should have:
- A concise label.
- A large, legible value.
- A unit where relevant.
- A small context label or comparison when available.

### 5.2 Anomalies

**Job:** Help users identify and review periods where actual output differs meaningfully from expected output.

Visual direction:
- A clear page heading and short explanation of what an anomaly means.
- A compact summary of anomaly counts or severity only when supported by real results.
- A readable table/list with timestamp, measured output, expected output, deviation, and trust/severity information when those fields exist.
- Clear status chips with text labels.
- Filters grouped neatly and visually separated from the results.
- A useful empty state when no anomalies are found.

Do not imply that an anomaly proves a panel, inverter, or other component is faulty.

### 5.3 Investigate

**Job:** Let a user understand one selected deviation in context.

Visual direction:
- Make the selected event and its time range obvious.
- Give the expected-versus-actual comparison the strongest visual emphasis.
- Show relevant environmental measurements alongside the power comparison when available.
- Use aligned time-series charts where possible so the user can compare conditions and output over the same period.
- Keep explanations factual and distinguish measured evidence from possible interpretations.
- Provide a clear route back to the anomaly list.

Avoid presenting speculative root causes as confirmed diagnoses.

### 5.4 Predict

**Job:** Provide a focused way to obtain or inspect an expected AC power prediction.

Visual direction:
- Separate input controls from the prediction result.
- Group related environmental/system inputs logically.
- Make units and valid ranges clear.
- Give the predicted output a strong, prominent result treatment.
- Display input trust/validation feedback clearly when available.
- Include actual-versus-expected comparison only when an actual measurement exists for the selected record.
- Make invalid or incomplete inputs understandable without exposing raw tracebacks.

Do not add input fields for measurements the current prediction interface does not support.

### 5.5 Model

**Job:** Make the model understandable and provide confidence in what is powering the application.

Visual direction:
- Present model identity/version and status clearly when available.
- Use compact metric cards for evaluation metrics.
- Show model evaluation and validation information in readable charts/tables.
- Distinguish training/evaluation metrics from live operational performance.
- Keep technical details accessible without making the page feel like a notebook.
- Make missing metadata or unavailable information explicit.

Do not invent model scores, monitoring status, retraining dates, or deployment health.

## 6. Data visualisation language

Charts are a core part of SolarOps and should receive more attention than decorative imagery.

### Expected vs actual

- Use two clearly distinguishable series.
- Keep the colours consistent across every page.
- Use a shared time axis and meaningful units.
- Include a legend, readable axis labels, and useful hover details where supported.
- Make gaps and missing/unreliable periods visible rather than silently implying continuous data.

### Deviations

- Make the direction and magnitude of the difference easy to understand.
- Use a zero/reference line where it improves interpretation.
- Do not exaggerate small deviations through misleading axis ranges.
- Clearly distinguish absolute difference from percentage difference.

### Environmental context

- Use aligned time-series plots for irradiance, temperature, wind, and power when those measurements are available.
- Avoid placing many unrelated charts in one dense grid.
- Prefer a small number of useful visualisations over a large gallery of charts.

### General chart rules

- Consistent units and formatting.
- Clear titles that explain what is being plotted.
- Light gridlines and restrained chart decoration.
- Legible ticks and tooltips.
- Consistent semantic colours.
- No 3D charts or ornamental chart effects.

## 7. Photography and imagery

The screenshots use large renewable-energy photographs effectively. Bring that visual identity into SolarOps carefully.

Good uses:
- A restrained welcome / overview banner, if the current Overview page benefits from it.
- A small contextual image on an empty or introductory state.
- A subtle image treatment in an About / product-information area, if one exists.

Prefer real-looking solar farms, photovoltaic panels, inverters, and energy infrastructure. Use natural daylight, deep greens, muted blues, and realistic environments.

Do not:
- Put a large stock-photo hero on every page.
- Place text over busy imagery where contrast suffers.
- Use wind turbines as a substitute for solar context in charts or system status.
- Use images as decoration that pushes useful performance information below the fold.
- add generic marketing sections such as product catalogues, customer testimonials, blog cards, newsletter forms, country maps, or sales CTAs unless the existing product explicitly requires them.

## 8. Interaction and component behaviour

- Buttons should have clear primary, secondary, and disabled appearances.
- Filters should be compact and visually grouped.
- Tables should support scanning, with aligned numeric values and clear status labels.
- Use progressive disclosure for technical detail rather than showing every field at once.
- Provide loading, empty, error, and unavailable states.
- Keep feedback close to the control or data it relates to.
- Use confirmation for consequential actions.
- Preserve user selections across normal Streamlit reruns where appropriate.
- Avoid unnecessary animations and interactions that do not help the user interpret data.

## 9. Responsive behaviour

The desktop experience is the primary reference, but the interface must remain usable at smaller widths.

- Desktop: use the available width for charts and comparison layouts without stretching text excessively.
- Tablet: allow metric cards and chart panels to wrap naturally.
- Mobile: stack cards and charts vertically; keep navigation accessible; avoid wide tables overflowing the viewport.
- Prioritise the expected-versus-actual comparison and essential status information at every width.
- Do not shrink chart labels until they become unreadable.

## 10. Streamlit-specific design considerations

SolarOps currently uses Streamlit. The visual direction should work with Streamlit's layout and interaction model.

- Prefer native Streamlit components where they can deliver the required quality.
- Use custom CSS selectively for visual consistency, not to fight the framework.
- Keep styling maintainable and scoped; avoid brittle selectors tied to generated DOM structure.
- Preserve Streamlit accessibility, keyboard interaction, and widget behaviour.
- Avoid building a complex front-end framework inside Streamlit just to reproduce the reference screenshots.
- Do not change the underlying ML pipeline, prediction logic, data contracts, or model behaviour as part of visual styling.

## 11. What this design is not

The references are solar-energy company websites. SolarOps is a performance intelligence application.

Do **not** copy their:
- Sales-oriented hero copy and “Get Started” marketing structure.
- Product / installation catalogues.
- Testimonials and editorial blog sections.
- Generic claims about savings, incentives, certifications, or worldwide installations.
- Decorative statistics that are not backed by SolarOps data.

Do not invent multiple solar installations, live sensor feeds, user accounts, maps, alerts, maintenance workflows, or integrations unless the repository already implements them or they are separately approved as product features.

## 12. Quality bar

The finished interface should pass these visual checks:

- It is immediately recognisable as SolarOps.
- The active page and navigation are obvious.
- The most important information is visible without excessive scrolling.
- Expected and actual power are visually easy to compare.
- Status colours and labels mean the same thing throughout the app.
- Charts are readable and do not misrepresent the data.
- Empty, loading, error, anomaly, and unreliable-input states feel intentionally designed.
- The five pages feel like parts of one product.
- The interface looks polished without sacrificing analytical clarity.

## 13. Instructions to the coding agent

1. Read this brief together with `README.md` and `PROJECT_OVERVIEW.md`.
2. Inspect the **actual current working tree** before deciding what to change. The documented five-page app is Overview, Anomalies, Investigate, Predict, and Model; verify the current files and implementation rather than assuming paths or structure.
3. Review the two supplied reference screenshots for visual direction.
4. Keep this task focused on the UI's visual design and user experience.
5. Preserve existing working functionality, data contracts, prediction behaviour, and page responsibilities.
6. Do not invent data or implement unsupported product features to make a mockup look complete.
7. Do not refactor the ML pipeline or change model logic as part of this design task.
8. If a design idea requires data or functionality that does not exist, present it as a future design consideration instead of faking it.
9. Make the smallest coherent set of UI changes needed to achieve the design direction.
10. After implementation, check all five pages and their key states for visual consistency and responsive behaviour.

**Design principle:** SolarOps should look like a modern renewable-energy intelligence product: natural and confident like the references, but focused, evidence-led, and useful like a professional analytics dashboard.
