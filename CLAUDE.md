# CLAUDE.md — MicTest12-1.0 Codebase Guide

## Project Overview

**MicTest12-1.0** is a dual-interface calculator application consisting of:

1. **Python Backend** (`calc.py`) — A simple command-line calculator module providing arithmetic operations (add, subtract, multiply, divide) with error handling and a `sum_evens` helper function.
2. **HTML/JavaScript Frontend** (`calculator.html`) — A fully-functional, interactive calculator UI with light/dark mode support, responsive design, keyboard input, and accessibility features.

The repository also contains an **SRS document** (`SRS.md`) outlining a future vision for the project as a web-based microphone testing utility. At this stage, MicTest12-1.0 is a proof-of-concept calculator; the SRS serves as a requirements reference for future expansion.

---

## Repository Structure

```
MicTest12-1.0/
├── .git/                    # Git history and metadata
├── .gitignore              # Excludes Python bytecode (__pycache__, *.pyc)
├── README.md               # Brief project title
├── CLAUDE.md              # This file — codebase documentation
├── SRS.md                 # Software Requirements Specification (future vision)
├── calc.py                # Python calculator module with CLI entry point
└── calculator.html        # Standalone HTML calculator with embedded CSS/JS
```

### Key Files

#### `calc.py` (51 lines)
- **Purpose**: Core arithmetic logic and CLI interface
- **Exports**: Functions `add()`, `subtract()`, `multiply()`, `divide()`, `calculate()`, `sum_evens()`
- **Entry point**: `main()` — prompts user for two numbers and an operator, prints result
- **Error handling**: Division by zero raises `ValueError`; invalid operators raise `ValueError`

#### `calculator.html` (299 lines)
- **Purpose**: Self-contained browser calculator application
- **Technology**: Vanilla JavaScript (no dependencies), CSS custom properties for theming
- **Features**:
  - Light/dark mode support (respects `prefers-color-scheme`)
  - 4×5 button grid layout (digits 0–9, operators, functions)
  - Live expression and result display
  - Keyboard support (digits, operators, Enter for =, Escape for clear)
  - Accessible markup (ARIA labels, `aria-live` for announcements)
  - Stateful calculator logic (chain operations, percentage, sign toggle)
- **Styling**: CSS variables for theming; responsive design (min-width 320px, max-width 360px)

#### `SRS.md` (279 lines)
- **Purpose**: Software Requirements Specification for a future microphone-testing web app
- **Status**: Draft (v0.1, dated 2026-04-26)
- **Contents**: Functional requirements (device enumeration, live metering, recording, diagnostics), non-functional requirements (performance, security, accessibility), acceptance criteria, and open questions
- **Note**: Does not reflect current code; included for context on product vision

---

## Development Workflows

### Setting Up the Repository

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd MicTest12-1.0
   ```

2. **Branch naming convention:**
   - Feature branches: `feature/<description>`
   - Bug fixes: `bugfix/<description>`
   - Documentation: `docs/<description>`
   - Claude-assisted work: `claude/<task-id>`
   - Example: `claude/add-claude-documentation-EXGvx`

3. **Python environment (optional):**
   ```bash
   # Run the CLI calculator
   python3 calc.py
   ```

4. **Open the HTML calculator:**
   - Open `calculator.html` directly in any modern browser (no server required)
   - Or serve locally: `python3 -m http.server 8000` then visit `http://localhost:8000/calculator.html`

### Making Changes

1. **Create a feature branch** from the designated development branch (currently `claude/add-claude-documentation-EXGvx`).
2. **Edit files** using a text editor or IDE.
3. **Test locally:**
   - For Python: Run `python3 calc.py` and manually test operations.
   - For HTML: Open in a browser, test all buttons, keyboard input, theme switching.
4. **Commit with clear messages:**
   ```bash
   git add <files>
   git commit -m "Brief description of change"
   ```
5. **Push to your branch:**
   ```bash
   git push -u origin <branch-name>
   ```

### Git Conventions

- **Commit messages**: Use imperative mood and be specific.
  - ✅ Good: `"Add sum_evens helper function"`
  - ❌ Bad: `"fixed stuff"`, `"Update calc.py"`
- **Merge strategy**: Pull requests are merged via GitHub (visible in git log as merge commits).
- **Branch cleanup**: Delete merged branches after PR merges.

---

## Code Conventions

### Python (`calc.py`)

- **Style**: Follows PEP 8 guidelines (implied by the existing code).
- **Functions**: 
  - Pure functions (no side effects) for arithmetic operations.
  - Clear docstrings are optional for obvious functions; add them for non-trivial logic.
- **Error handling**: Raise `ValueError` with descriptive messages for invalid input.
- **Testing approach**: Consider unit tests for `calculate()` and `sum_evens()` if extended.

**Example:**
```python
def add(a, b):
    return a + b

def calculate(a, op, b):
    if op not in OPERATIONS:
        raise ValueError(f"Unknown operator: {op}")
    return OPERATIONS[op](a, b)
```

### HTML/JavaScript/CSS (`calculator.html`)

- **Markup**: Semantic HTML5; use `data-*` attributes for behavior coupling.
- **CSS**: Utility classes and CSS custom properties for theming; no external frameworks.
- **JavaScript**:
  - Use IIFE to scope state and functions (avoid global namespace pollution).
  - State object holds all calculator state; `render()` is the single source of truth.
  - Event listeners are attached via `addEventListener`; keyboard support via `keydown`.
  - Clear separation between input handling, computation, and rendering.
- **Accessibility**:
  - All buttons have descriptive labels (visually or via `aria-label`).
  - `aria-live="polite"` on the display for screen reader announcements.
  - Keyboard support: digits, operators, Enter (=), Escape (clear), % sign toggle.
  - Color not the only indicator (e.g., result display is always visible).

**Example:**
```javascript
const state = {
  current: '0',
  previous: null,
  operator: null,
  justEvaluated: false,
};

function render() {
  currEl.textContent = state.current;
  // ... update display
}
```

---

## Testing Approach

Currently, there are no automated tests in the repository. However, here's the recommended approach for expansion:

### Python (`calc.py`)

**Unit tests** (using `unittest` or `pytest`):
```python
def test_add():
    assert add(2, 3) == 5

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(1, 0)

def test_sum_evens():
    assert sum_evens([1, 2, 3, 4, 5]) == 6  # 2 + 4
```

### HTML/JavaScript

**Manual testing checklist**:
- [ ] All digit buttons (0–9) input correctly.
- [ ] Operators (+, −, ×, ÷) work in sequence (chain operations).
- [ ] Decimal point (.) cannot be entered twice in a number.
- [ ] Keyboard input works: digits, operators, Enter, Escape, %.
- [ ] Light and dark modes switch correctly (use DevTools to toggle `prefers-color-scheme`).
- [ ] Screen reader announces calculation results (test with NVDA, JAWS, or VoiceOver).

**Future**: Consider Playwright or Cypress for end-to-end testing if the app grows.

---

## Deployment and Tech Stack

### Current Stack

| Component | Technology | Notes |
| --- | --- | --- |
| **Python Backend** | Python 3 | CLI-only; no framework |
| **Frontend** | Vanilla JS, CSS3, HTML5 | No dependencies; single-file deployment |
| **Hosting** | Static files | Can be served from any HTTP server or CDN |

### Deployment Steps

1. **For the CLI calculator**:
   ```bash
   python3 calc.py
   ```
   No installation or build step needed.

2. **For the HTML calculator**:
   - Copy `calculator.html` to your web server.
   - Serve over HTTP or HTTPS.
   - No build process, no dependencies to install.

### Performance

- **Bundle size**: Single HTML file (~8.5 KB uncompressed).
- **Load time**: Instant (no network requests after page load).
- **Runtime**: Negligible CPU/memory usage; suitable for all devices.

---

## Common Development Tasks

### Adding a New Operation to `calc.py`

1. Define the operation function:
   ```python
   def modulo(a, b):
       if b == 0:
           raise ValueError("Cannot modulo by zero")
       return a % b
   ```

2. Register it in the `OPERATIONS` dict:
   ```python
   OPERATIONS = {
       "+": add,
       "-": subtract,
       "*": multiply,
       "/": divide,
       "%": modulo,  # Add this line
   }
   ```

3. Test manually:
   ```bash
   python3 calc.py
   # Input: 10, %, 3
   # Expected: 1
   ```

### Adding a Button to the HTML Calculator

1. Add a `<button>` element:
   ```html
   <button data-action="square">x²</button>
   ```

2. Add the corresponding handler in JavaScript:
   ```javascript
   else if (btn.dataset.action === 'square') {
       const n = parseFloat(state.current);
       state.current = formatNumber(n * n);
   }
   ```

3. Style as needed (add a CSS class if different styling is required).

### Updating the SRS

The SRS documents the long-term vision. To update it:

1. Edit `SRS.md` directly.
2. Update the revision history table (Section 6, Appendix A).
3. Commit with a message like: `"Update SRS: add feature XYZ requirements"`.

---

## Key Decisions and Rationale

### Why Two Interfaces?

The Python CLI and HTML frontend serve different use cases:
- **CLI**: For system integration, scripting, and server-side use.
- **HTML**: For end-user interactions in a browser; no server required.

### Why No Build Tool?

Both components are intentionally simple and framework-free:
- Python: Pure standard library; no dependencies.
- JavaScript: Vanilla, single-file IIFE; no bundler needed.

This keeps the project lightweight and maintainable.

### Why No Tests (Currently)?

The codebase is small and the logic straightforward. Tests should be added if:
- The app grows beyond ~500 lines of code.
- Complex state management is introduced.
- Multiple contributors need regression coverage.

### Why CSS Custom Properties?

CSS variables enable:
- Dynamic theme switching without JavaScript complexity.
- Clear separation of colors and spacing values.
- Easier maintenance and future theming.

---

## Accessibility and Internationalization

### Accessibility (WCAG 2.1 Level AA)

- **Semantic HTML**: Use `<button>`, `<main>`, `<div role="...">`.
- **ARIA labels**: All icon-only buttons have `aria-label` or visible text.
- **Keyboard support**: All functionality accessible via keyboard.
- **Color contrast**: Ensure 4.5:1 ratio for text; don't rely on color alone.
- **Screen reader testing**: Test with NVDA, JAWS, or VoiceOver.

### Internationalization (i18n)

Currently, the calculator uses English labels only. To add translations:

1. Extract all user-facing strings into a translations object:
   ```javascript
   const i18n = {
     en: { clear: 'AC', divide: '÷' },
     es: { clear: 'Borrar', divide: '÷' },
   };
   ```

2. Use a language selector to switch locales.
3. Update the SRS if translations become a v1.0 requirement.

---

## Future Considerations

### SRS Vision (Microphone Testing)

The SRS outlines a future feature set including:
- Device enumeration and selection.
- Real-time audio level metering and waveform visualization.
- Test recording and diagnostics.
- Browser compatibility testing.

If this becomes the next major feature:
1. Create a new `index.html` or refactor the current structure.
2. Use the Web Audio API for real-time signal processing.
3. Add unit tests for audio analysis (RMS, peak, noise floor).
4. Plan for HTTPS deployment (required by `getUserMedia`).

### Testing Infrastructure

As the project grows:
- Add `pytest` for Python unit tests.
- Use Playwright or Cypress for end-to-end testing.
- Set up GitHub Actions CI/CD to run tests on push.

### Linting and Type Checking

- **Python**: Use `black` for formatting and `pylint`/`flake8` for linting.
- **JavaScript**: Use ESLint and consider migrating to TypeScript if complexity increases.

---

## Troubleshooting

### Python Calculator Won't Run

- Ensure Python 3 is installed: `python3 --version`
- Run from the repository root: `python3 calc.py`
- Check for syntax errors: `python3 -m py_compile calc.py`

### HTML Calculator Displays Incorrectly

- Open the browser DevTools console (F12) and look for errors.
- Ensure the file is served over `file://` or `http(s)://` (not from a zip).
- Check `prefers-color-scheme` in DevTools (Settings → Rendering → Emulate CSS media feature).

### Git Push Fails

- Verify your branch exists: `git branch -a`
- Ensure you're on the correct branch: `git branch`
- Check remote URL: `git remote -v`
- If network errors occur, retry with exponential backoff (wait 2s, 4s, 8s, 16s between attempts).

---

## Contributing Guidelines

1. **Read this file** before making significant changes.
2. **Create a branch** for your work (see Branch Naming Convention above).
3. **Write clear commit messages** with context.
4. **Test your changes** locally before pushing.
5. **Keep commits focused**: One logical change per commit.
6. **Update documentation** if you change behavior.
7. **Submit a pull request** for review (follow the PR template if one exists).

---

## Resources

- **IEEE Std 830-1998**: SRS best practices (referenced in `SRS.md`)
- **Web Audio API**: https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API
- **Web Accessibility**: https://www.w3.org/WAI/WCAG21/quickref/
- **Git**: https://git-scm.com/doc
- **Python**: https://docs.python.org/3/

---

## Document History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-05-09 | Claude | Initial CLAUDE.md documenting current calc.py and calculator.html; notes SRS vision. |

---

*Last updated: 2026-05-09*
