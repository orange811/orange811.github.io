---
title: "Coloured Fluid Simulator"
description: "Real-time 2D Navier-Stokes fluid simulation in pure Java with interactive dye injection and velocity visualization."
date: 2021-06-01
tags: ["Java", "Fluid Simulation", "Numerical Methods", "Swing"]
repo: "https://github.com/orange811/fluid-sim-col"
link: "https://youtu.be/aPf_i_lAKT4"
thumb: "/images/projects/fluid-sim/thumb.jpg"
---

## Overview

This is a real-time, grid-based 2D fluid simulation built in pure Java. Dragging the mouse injects **dye** and **velocity** into the field; the simulation then transports (advects) and diffuses them over time to produce the swirling "ink in water" effect.

The simulation runs on a 2D grid storing velocity and color fields, performing diffusion, incompressibility projection, and advection each frame to create realistic fluid motion.

## Demo

Watch the full demo on YouTube:

<iframe width="100%" height="400" src="https://www.youtube.com/embed/aPf_i_lAKT4" frameborder="0" allowfullscreen></iframe>

<video controls width="100%" style="margin-top: 1rem; border-radius: 0.5rem;">
  <source src="/images/projects/fluid-sim/demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## Controls

- **Mouse drag**: Add dye and push fluid (adds velocity)
- **Space**: Toggle velocity vector visualization
- **C**: Randomize dye color cycling
- **Esc**: Quit application

## Running the Simulation

Main entry point: `src/graphics/Fluid.java` (`public static void main`)

From the repo root:

```bash
javac -d bin src/utility/*.java src/graphics/*.java
java -cp bin graphics.Fluid
```

## Implementation Notes

The simulation uses a grid-based approach with the following key components:

### Data Structures
- **Velocity field** (`Vec2[][]`) — Stores fluid motion at each grid cell
- **Dye/color field** (`Color[][]`) — Tracks visual appearance of the fluid

### Simulation Steps (each frame)
1. **Diffusion** — Spreads velocity and dye to neighboring cells
2. **Incompressibility projection** — Ensures fluid doesn't compress (divergence-free velocity field)
3. **Advection** — Moves quantities along the velocity field (semi-Lagrangian method)
4. **Fading** — Optional gradual decay of dye intensity

### Rendering
- Uses Java Swing (`JFrame` + `JPanel`)
- Writes the dye field directly into a `BufferedImage` each frame
- Real-time visualization at interactive framerates

## Technical Approach

The implementation follows the stable fluids approach, using:
- **Semi-Lagrangian advection** for numerical stability
- **Gauss-Seidel iteration** for diffusion and pressure projection
- **Bilinear interpolation** for sampling velocity/dye fields
- **Grid-based discretization** for spatial representation

This approach prioritizes visual plausibility and real-time performance over physical accuracy, making it ideal for interactive applications and games.

## References & Inspiration

- **Jos Stam** — *Real-Time Fluid Dynamics for Games*  
  [ResearchGate Paper](https://www.researchgate.net/publication/2560062_Real-Time_Fluid_Dynamics_for_Games)

- **Mike Ash** — "Fluid Simulation for Dummies"  
  [Blog Post](https://www.mikeash.com/pyblog/fluid-simulation-for-dummies.html)

- **Inspecto** — "But How DO Fluid Simulations Work?"  
  [YouTube Video](https://www.youtube.com/watch?v=qsYE1wMEMPA)

- **The Coding Train** — "Coding Challenge 132: Fluid Simulation"  
  [YouTube Video](https://www.youtube.com/watch?v=alhpH6ECFvQ)
