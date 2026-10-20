num: 6
slug: tableau
title: The Tableau dashboard
summary: My first dashboard, built in Tableau Public, and the things it couldn't do.
standfirst: The course asks for a business intelligence tool, so I built my first dashboard in Tableau Public.
---
## What it shows

I built it in Tableau Public's web editor, from my joined table. It has three linked views:

- a map of HLE by area;
- a box plot of HLE by local authority;
- a scatter plot of HLE against household income.

If you click an area on the map, the same area lights up in the scatter. And if you hover over anything, you get the area's name and figures.

::: tableau
:::

## What it couldn't do

Tableau got me a working dashboard quickly, and it's good at what it's built for. But when I tried to make it look and behave the way I wanted, I kept hitting walls.

- **No 3D.** I couldn't raise areas by their value, and that's how I want to show the drop at a boundary.
- **A legend I couldn't pin to the map.** I had to place a floating legend by hand, and it doesn't stay with the map.
- **A layout that doesn't adapt.** It's built for one fixed size, and it doesn't reflow for a smaller screen.
- **Limited colour control.** The web editor gives me a grid of swatches, with no way to type in an exact colour. I can only change the box plot fills in the desktop version, and a trend line takes the colour of its dots.
- **No limit on zooming out.** You can zoom out until Birmingham is a speck, and I found no setting to stop it.
- **Slow going.** Clicks and drags in the web editor were slow and unreliable.

None of these is a disaster on its own. But together they meant I couldn't build the dashboard I had in my head in Tableau. And that's the honest reason the next chapter exists.

## The data flow

I feed both dashboards from the same place. My notebooks save the joined table and the boundaries. Tableau reads a copy of that table, and my own dashboard reads a compact version that a small Python script builds from the same files. I never retype anything by hand, so the two dashboards always agree on the numbers.
