# Changelog

## v1.0

The second tagged release. The 2016 simulator is brought up to date: a redesigned panel, a fourth-order solver, one-command setup, and tests. The swing and ball-flight models are unchanged.

### Highlights

- **Redesigned panel.** Inputs in three tabs, a **Run all steps** button with four steps that know what they depend on, results cards (with mph, yards and feet), and plots in tabs inside the window. Change an input and only the affected results are marked stale and re-run.
- **A true 4th-order solver.** Solution 4 is the classical Runge-Kutta method and the new default: about 100× more accurate than the original schemes and twice as fast. Solutions 1–3 are kept for comparison; a step-halving study showed they are first-order accurate.
- **One-command setup with uv:** `uv sync && uv run src/Main.py` installs Python 3.12 (including Tk) and every dependency.
- **Documentation and tests:** the full report as Sphinx docs, plus 47 tests and a lint pass.

### Fixes

- Swings longer than one second crashed; a swing that never reached impact reported its 2-second state as the result.
- The ball-flight loop crashed for a very low landing height, and reported a mid-air "landing" when the target height was above the ball's apex.
- The wrist-torque optimizer silently reported 0 N·m when no torque in the range could reach the target; it now says which limit to change.
- Error messages name the field or the step to run, instead of "fields must be numeric".
- Angular accelerations were plotted one step late; the impact values are now interpolated to the exact impact angle.
- Plot windows no longer block the panel, and the 3D plot works again on current matplotlib.

### Breaking changes

- **Python 2 is no longer supported**; Python 3.12+ with `pyproject.toml`.
- **New paths:** the app is `src/Main.py` and the cases are `examples/Case1.py` … `Case10.py`.
- The GUI default solver changed to Solution 4, so results differ slightly from the report (52.76 m/s instead of 52.80 m/s for the default swing).

### Getting started

```bash
uv sync
uv run src/Main.py
```

### Note on the report

`Simple-Golf-Simulator-Report.pdf` is the original report (version 1.0, 2016), kept as published. It predates Solution 4, the redesigned panel and the current Case 1 numbers; the Sphinx documentation under `docs/` is the up-to-date reference.
