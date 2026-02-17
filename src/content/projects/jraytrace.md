---
title: "JRaytrace"
description: "A software raytracing engine written entirely in Java with no external libraries. Supports primitives, OBJ models, coloured lighting, texturing, normal mapping, and reflection."
date: 2024-09-15
tags: ["Java", "Raytracing", "Rendering", "Computer Graphics"]
thumb: "/images/projects/raytracer/thumb.mp4"
hero: "/images/projects/raytracer/hero.mp4"
featured: true
featuredOrder: 3
---

## Overview

JRaytrace is a from-scratch software raytracing engine written in pure Java. Every part of the pipeline (ray generation, intersection testing, shading, and final image output) is implemented without any external rendering libraries or frameworks.

## Features

- **Geometric primitives**: spheres, planes, triangles, and other standard shapes with analytical intersection routines
- **OBJ model loading**: imports arbitrary triangle-mesh geometry from Wavefront OBJ files
- **Lighting**: point lights and directional lights, each with configurable colour and intensity
- **Texturing & texture mapping**: UV-mapped image textures applied to surfaces
- **Normal mapping**: per-pixel perturbation of surface normals for added surface detail without extra geometry
- **Reflection**: recursive mirror reflections with configurable depth

## Rendering Pipeline

The renderer casts primary rays from the camera through each pixel, tests intersections against every object in the scene, evaluates lighting contributions using the Phong reflection model, and recursively traces reflected rays where applicable. The entire driver, scene graph, material system, and image writer are self-contained Java code.

<p class="text-sm text-muted italic mt-6">Repository coming soon.</p>
