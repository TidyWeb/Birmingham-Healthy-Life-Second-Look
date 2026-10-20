num: 7
slug: my-dashboard
title: My own dashboard
summary: The map I built myself, what it adds, and a few things to try.
standfirst: So I built the dashboard I wanted myself, in plain HTML and JavaScript, around a Leaflet map.
---
<div class="btn-row"><a class="btn btn-ink" href="{root}dashboard/">Open the dashboard</a></div>

I built it for a laptop or desktop screen. If you open it on a phone, it tells you so.

::: image dashboard-card.webp wide
alt: The dashboard map of the West Midlands coloured by healthy life expectancy, with the "Area in focus" card open for Kingswood.
caption: The map with an area picked. The card gives its HLE with the margin of error, its rank, the figures for men and women, and its biggest gap with a neighbour.
:::

## What it adds

- **Area cards.** You can pick any of the 660 areas by clicking it, typing a familiar place name, or choosing it from a list. A card then opens with its HLE, margin of error, rank, the male and female figures, and its biggest gap with a neighbour.
- **Raised tiles.** When you pick an area, it lifts off the map instead of changing colour. The colours are the key to the whole map, so I didn't want a picked area to look healthier or less healthy than it is.
- **Every measure on the same map.** You can switch the map from HLE to any of the other measures. I show those on an orange scale, so you can't mistake them for HLE.
- **The big-gap pairs.** You can outline the 95 pairs from Notebook 04 on the map.
- **Charts and Data.** The card opens six views: the area's neighbours, its full profile, HLE against another measure, the distribution, local authorities ranked, and all the area data in a table.

I kept two rules on every chart. Values always rise from left to right and from bottom to top. And colour carries the meaning, so darker is poorer, in both scales.

::: image dashboard-scatter.webp wide
alt: The dashboard showing overcrowded households on an orange scale, with a scatter of HLE against no qualifications open.
caption: The same map switched to overcrowding, with HLE plotted against no qualifications. Each dot is an area.
:::

## Things to try

- Pick **Druids Heath**, and then look across its southern edge at **Wythall**. That's one of the boundaries in the hotspots chapter.
- Turn on the big-gap pairs under *Explore & layers*, and see how many of the red outlines sit on council boundaries.
- Open *HLE against another measure* and switch between income and NO₂. Income makes a tight band, and NO₂ makes a loose cloud.
