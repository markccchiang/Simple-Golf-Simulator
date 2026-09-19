<p align="center">
  <img src="assets/logo.png" alt="Simple Golf Simulator logo" width="160">
</p>

# Simple Golf Simulator

A physics-based golf swing and ball trajectory simulator with an interactive GUI built using Tkinter and Matplotlib.

## Requirements

- **Python 3.12+** is recommended for best compatibility
- Third-party packages: `matplotlib`, `numpy`
- Standard library: `tkinter`, `math`, `cmath`, `sys`

## Installation

With [uv](https://docs.astral.sh/uv/) (recommended), which installs Python 3.12 (including `tkinter`) and all dependencies into `.venv`:

```bash
uv sync
```

Or with pip:

```bash
pip install matplotlib numpy
```

With pip, on some Linux systems, `tkinter` may need to be installed separately:

```bash
# Debian/Ubuntu
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

## Getting Started

```bash
uv run src/Main.py        # or: python src/Main.py
```

Each step uses the previous step's results, so click the buttons in order: **Optimize wrist-cock torque** → **Simulate / Plot Golf Swing** → **Calculate launch speed and elevation angle from impact** → **Simulate / Plot Ball Trajectory**. If a step is skipped, the error message names the button to click first.

## Features

### Swing Simulation

The simulator models a two-degree-of-freedom golf swing using torque-driven angular mechanics. Users can configure:

- **Golfer parameters** -- gender, weight, shoulder radius, arm length
- **Club parameters** -- head/shaft mass and length
- **Swing conditions** -- swing plane angle, initial/impact arm angle, wrist-cock angle, swing type (Type I / Type II)
- **Torques** -- arm torque, wrist-cock torque (with automatic optimization)

Four numerical solution methods are available. Solution 4 (the default) is the classical 4th-order Runge-Kutta method; Solutions 1–3 are the original Runge-Kutta-based schemes, which are first-order accurate overall and are kept for comparison.

### Ball Trajectory

The ball flight model includes drag, lift, spin (Magnus effect), and wind. Configurable parameters:

- Ball mass, diameter, drag/lift coefficients
- Coefficient of restitution (COR)
- Air density, wind speed/direction
- Clubhead loft angle, launch angles, spin angles

### Plots

**Swing plots:**
Tracks, angles, angular velocities, angular accelerations, clubhead velocity, torques, arm length, and moment of inertia.

**Ball trajectory plots:**
X-Z (elevation), X-Y (horizontal), Y-Z (lateral), and 3D flight path.

## Running Tests

```bash
uv run pytest
uv run ruff check .    # lint
```

The tests in `tests/` run the swing and ball-trajectory simulations headless and check the GUI's error messages without opening a window.

## Documentation

The full technical report (two-rod swing model, aerodynamic equations, simulation cases, and user's guide) is available as Sphinx documentation under `docs/`.

To build:

```bash
uv sync --group docs
cd docs
uv run --group docs sphinx-build -b html . _build/html
```

(Or with pip: `pip install sphinx sphinx-rtd-theme`, then run `sphinx-build` the same way.)

Then open `docs/_build/html/index.html` in your browser.

## Project Structure

| File | Description |
|------|-------------|
| `src/Main.py` | GUI application entry point |
| `src/BasicFunc.py` | Core swing physics |
| `src/BasicFunc2.py` | Ball trajectory physics |
| `src/AppFunc.py` | Swing simulation functions |
| `src/AppFunc2.py` | Ball trajectory simulation functions |
| `src/Plot.py` | Swing visualization |
| `src/Plot2.py` | Ball trajectory visualization |
| `src/UIFunc.py` | Shared input reading and error dialogs |
| `examples/Case1.py` - `examples/Case10.py` | Standalone example cases, e.g. `uv run examples/Case1.py`; figures are saved as `.eps` in the current directory |
| `tests/` | pytest suite |
| `pyproject.toml`, `uv.lock` | Dependencies (uv) |

## License

ISC License -- Copyright (c) 2026, Cheng-Chin Chiang
