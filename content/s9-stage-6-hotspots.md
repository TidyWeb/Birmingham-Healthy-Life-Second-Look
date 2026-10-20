num: S9
part: second-look
slug: stage-6-hotspots
title: Stage 6: Hotspots
summary: Repeated neighbour gaps, the hotspot map, and the limits of model residuals.
standfirst: The map can show where measured differences cluster. It cannot say what caused them.
---
I used Signal Box from my own [Ethical Considerations in AI](https://tidyweb.github.io/ethical-considerations-in-ai/) guide; [The method](s2-the-method.html) explains its origin and how I applied it.

::: keypoints
I grouped repeated large gaps between neighbouring areas into hotspot patches. Signal Box’s concern is that residual and hotspot maps can look like proof, so I describe estimates and spatial association plainly.
:::

## What I did in Unit 2

^ nb06#af25607b | Large neighbour gaps grouped into connected patches.
I joined large-gap pairs where they shared an area, then mapped the largest patches. I also compared each area's measured HLE with the model estimate to see where the model's residuals clustered.

::: figure hotspots/01_hotspot_overview wide nb06#9c4f9cfc
alt: A map showing the five largest patches of repeated neighbour gaps.
caption: The patches locate repeated area-level HLE differences. They show spatial association, not cause.
:::

## What Signal Box asked {#what-the-screen-asked}

**Q14 — Could an output be treated as proof rather than a prompt? Concern.** Signal Box found that a residual map could read as an “underperforming” place, even though a residual is only the difference between observed HLE and the model's estimate.

::: signalbox stage S6
:::

## What I found

The hotspot pattern shows where large area-level differences cluster. The residual map shows what the selected model estimates fail to account for. Neither map identifies a cause or describes each resident.

## What changes

I changed only the residual-map and hotspot-map captions. They now name the model estimate and the spatial association, and state that the maps do not show cause. The size of a measured difference remains visible.
