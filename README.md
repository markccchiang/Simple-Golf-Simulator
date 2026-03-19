# Simple Golf Simulator

A physics-based golf swing and ball trajectory simulator with an interactive GUI built using Tkinter and Matplotlib.

## Requirements

- **Python 3.12+** is recommended for best compatibility
- Third-party packages: `matplotlib`, `numpy`
- Standard library: `tkinter`, `math`, `cmath`, `sys`

## Installation

```bash
pip install matplotlib numpy
```

On some Linux systems, `tkinter` may need to be installed separately:

```bash
# Debian/Ubuntu
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

## Getting Started

```bash
python Main.py
```

## Features

### Swing Simulation

The simulator models a two-degree-of-freedom golf swing using torque-driven angular mechanics. Users can configure:

- **Golfer parameters** -- gender, weight, shoulder radius, arm length
- **Club parameters** -- head/shaft mass and length
- **Swing conditions** -- swing plane angle, initial/impact arm angle, wrist-cock angle, swing type (Type I / Type II)
- **Torques** -- arm torque, wrist-cock torque (with automatic optimization)

Three numerical solution methods are available, all based on 4th-order Runge-Kutta integration.

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

## Project Structure

| File | Description |
|------|-------------|
| `Main.py` | GUI application entry point |
| `BasicFunc.py` | Core swing physics |
| `BasicFunc2.py` | Ball trajectory physics |
| `AppFunc.py` | Swing simulation functions |
| `AppFunc2.py` | Ball trajectory simulation functions |
| `Plot.py` | Swing visualization |
| `Plot2.py` | Ball trajectory visualization |
| `Case1.py` - `Case10.py` | Standalone example cases |

## License

ISC License -- Copyright (c) 2026, Cheng-Chin Chiang
