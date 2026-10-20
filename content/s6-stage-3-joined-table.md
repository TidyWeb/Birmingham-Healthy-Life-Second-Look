num: S6
part: second-look
slug: stage-3-joined-table
title: Stage 3: The joined table
summary: The combined area-level data, the six-group public view, and the proxy and crime checks.
standfirst: I joined health, Census, crime and other area measures so I could compare their patterns. The comparisons describe association, not cause.
---
I used Signal Box from my own [Ethical Considerations in AI](https://tidyweb.github.io/ethical-considerations-in-ai/) guide; [The method](s2-the-method.html) explains its origin and how I applied it.

::: keypoints
I joined detailed Census measures with healthy life expectancy and other area data. The proxy test found overlap with ethnic composition and deprivation; I report that finding and keep the measures.
:::

## What I did in Unit 2

^ nb03#6fb444a5 | Each source was joined to the same set of study areas.
^ nb07#5a0ce1ca | Notebook 07's six broad ethnic-composition groups.
I joined the outcome and candidate measures by area code, checked that the sources matched, and explored how the measures varied together. The joined table retains all 19 detailed Census ethnicity-share columns because later notebooks use them; the public-facing views use six broad ethnic groups: White British, Other White, Asian, Black, Mixed and Other.

::: figure wide/04_scatter_grid_by_theme wide nb03#4a130c2f
alt: Scatter plots comparing area-level healthy life expectancy with selected measures.
caption: Each point represents an area. These patterns show association across areas, not a cause or a statement about individual residents.
:::

## What Signal Box asked {#what-the-screen-asked}

**Q7 — Could a measure stand in for sensitive information? Concern.** The joined data include health and ethnic-composition measures. Income, qualifications and employment could carry information about those measures even though Notebook 05 leaves ethnicity and deprivation out of its model features.

^ nb03#45c1fdcf | The detailed ethnic-share measures are plotted separately in Notebook 03.
**Q8 — Could combined fields single out a small group? Concern.** Signal Box found very small detailed ethnic shares, including Gypsy or Irish Traveller shares below 0.5% in 646 of 660 areas. The agreed public comparison uses six broad groups because tiny categories do not serve the purpose of broad cultural comparison.

**Q11 — Does a feature reflect past human decisions? Concern.** Recorded crime is shaped by what is reported and recorded, including policing and footfall. Signal Box asked for a sensitivity check and a caveat that travels with crime views.

**Q23 — Could the work be used outside its purpose? Concern.** Placing health, crime, ethnicity and food-environment measures side by side can make association look like explanation. The accuracy response is to state the limits and keep causal claims out.

::: signalbox stage S3
:::

## What I found

^ nb07#8d87af50 | Cross-validated proxy R-squared values.
The seven model features predict the six area-level ethnic-composition measures with R² values from 0.277 to 0.743, and predict the deprivation measure with R² 0.898. That is measurable overlap. It is a finding about area-level information, not a cause or a reason to remove a feature.

## What changes {#six-groups-and-crime-caveat}

The joined table remains unchanged so the existing notebooks retain the Census detail they use; the Census publishes those figures openly. Public-facing comparisons use the six broad groups already defined in Notebook 07. Crime stays, with the reporting, policing and footfall caveat; takeaways stay as outlet density, not diet. No measure is removed because of the proxy result.
