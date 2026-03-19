# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Application

```bash
pip install matplotlib numpy
python Main.py
```

Python 3.12+ recommended. Requires `tkinter` (bundled on macOS/Windows; on Linux: `sudo apt-get install python3-tk`).

## Architecture

Two-stage physics simulator: **swing mechanics** → **ball trajectory**, connected through a Tkinter GUI.

### Data Flow

```
Main.py (UI entries dict)
  ├─→ Plot.py  → AppFunc.py  → BasicFunc.py   (swing simulation)
  └─→ Plot2.py → AppFunc2.py → BasicFunc2.py  (ball trajectory)
```

### Layer Responsibilities

- **BasicFunc.py / BasicFunc2.py** — Pure physics: RK4 integrators, force/torque equations, aerodynamics. No UI dependencies.
- **AppFunc.py / AppFunc2.py** — Run simulation loops calling BasicFunc, return result arrays.
- **Plot.py / Plot2.py** — Bridge between UI and simulation: read `entries` dict, call AppFunc, update UI fields, generate matplotlib plots.
- **Main.py** — Tkinter GUI layout. Two-panel scrollable design with ttk widgets. All UI state lives in a shared `entries` dict mapping string keys to `ttk.Entry` or `StringVar` objects.

### Key Function Signatures

**`AppFunc.Tracking(...)`** — Returns a 34-element tuple of arrays. Key indices:
- `[10]` time, `[11]` alpha, `[12]` beta, `[13]` theta, `[14]` VC_angle, `[20]` VC (clubhead velocity)
- Position arrays at `[0]-[9]`, torques at `[21]-[22]`, moments at `[23]-[25]`, rod segments at `[26]-[33]`

**`AppFunc2.TRACK(...)`** — Returns `(show_x, show_y, show_z)` position arrays.

### Angle Convention

- **UI/display**: degrees everywhere
- **Internal arrays**: radians (BasicFunc/AppFunc work in radians)
- Conversion happens at boundaries: Plot.py converts degrees→radians on input, radians→degrees on output/display

### Readonly Entry Pattern

Result fields use `ttk.Entry` with `state(['readonly'])`. The `_set_entry(entry, value)` helper in Plot.py and Plot2.py toggles readonly state to update values. Always use this helper — never call `.delete()/.insert()` directly on result entries.

### Input Validation

All public UI callbacks in Plot.py use the `@_validate_inputs` decorator which catches `ValueError`/`Exception` and shows a `messagebox` dialog. Plot2.py wraps its `Plot()` function with equivalent try/except.

## Case Files

`Case1.py`–`Case10.py` are standalone scripts that run specific simulation scenarios without the GUI. They import AppFunc/BasicFunc directly and generate plots.
