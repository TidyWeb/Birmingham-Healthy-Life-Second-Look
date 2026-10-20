num: 5
slug: first-findings
title: What the data showed first
summary: How HLE is spread, what moves with it, and a test of whether the gaps between neighbours are real.
standfirst: I found a 22-year spread, a strong link with money, and neighbour gaps far too big to be noise.
---
::: keypoints
- Healthy life expectancy runs from 53.7 to 75.7 years across my areas.
- Income and deprivation rank my areas almost exactly the way HLE does.
- The gaps between neighbours are real. 69.8% of pairs are past the noise line, where chance alone would give 5%.
:::

## How HLE is spread

^ nb01#cb04e3b0 | My areas against the rest of England and Wales.
My areas sit a little below the rest of England and Wales, by about a year and a half on average. But the spread inside them is just as wide as the national spread. So I'm not looking at a uniformly poorer region. I'm looking at a region with a lot going on inside it.

::: figure wide/01_hle_histograms wide nb03#31cbe73a
alt: Two histograms of healthy life expectancy, for men and for women, both spreading from the low 50s to the mid 70s.
caption: Male and female HLE across the 660 areas, on the same scale. Both spread across more than 20 years.
:::

::: stats nb03#81b6902d
53.7 to 75.7 | years of HLE, lowest area to highest (average of men and women)
64.1 | years, the median area
5.1 | years, the standard deviation between areas
:::

^ nb01#0971f58d | How precise the estimates are.
Each estimate has a margin of error of about a year and a half either way. That matters, because it means I can't really tell apart two areas that are a year apart. So I don't rank areas that close together.

## What moves with HLE

^ nb03#a01dd366 | The full set of correlations.
To see which measures move with HLE, I used Spearman correlation. It asks whether the areas that rank high on one measure also rank high, or low, on another. Household deprivation (−0.95) and income after housing costs (+0.94) rank my areas almost exactly the way HLE does. Overcrowding, unemployment and no qualifications come close behind. Crime, pollution and fuel poverty are weaker.

::: figure wide/04_scatter_grid_by_theme wide nb03#4a130c2f
alt: A grid of scatter plots of HLE against each measure, grouped by theme.
caption: Each measure against HLE, one dot per area. The money measures make the tightest bands.
:::

I have to be careful here. That's a link across areas, and I found it after looking at a lot of measures. It doesn't show that money is the cause, and it says nothing about any one person.

## Are the neighbour gaps real?

This was the question I couldn't leave alone. Every HLE figure is an estimate, and two estimates can look far apart just by chance. So before I built anything on the gaps, I tested them.

^ nb04#97394d74 | The hypothesis, written down before the test.
I wrote my hypothesis down first. If neighbouring areas don't really differ, and the gaps come only from estimate noise, then about 5% of neighbour pairs should pass the usual line of 1.96 standard errors.

^ nb04#5a64afb1 | 10,000 simulated runs of pure noise.
Then I simulated that world 10,000 times. Under pure noise, the share of pairs past the line stays between 3.5% and 6.6%. The real figure is 69.8%. So I reject the idea that the gaps are just noise. Neighbouring areas really do differ.

::: figure neighbours/01_gap_distribution nb04#f2184c4d
alt: Two overlaid distributions of neighbour gaps. The simulated noise gaps pile up under one year; the real gaps spread out past 15 years.
caption: Real neighbour gaps against gaps from pure noise. The noise gaps pile up under a year. The real ones spread out past 15.
:::

::: stats nb04#34e57c35
1,885 | pairs of neighbouring areas
69.8% | of pairs past the noise line
2.85 | years, the typical gap between neighbours
:::

## Neighbours look alike, mostly

^ nb04#2b4d8cac | Moran's I and the 999 shuffled maps.
Then I asked a different question. Do areas tend to look like their neighbours, with high next to high and low next to low? Moran's I measures that, starting from 0 for no pattern at all. HLE scores 0.576, and none of the 999 shuffled maps I compared it with came close. So the lower-HLE areas sit together, and so do the higher ones. And that tells me the big gaps are the edges, where a healthier patch meets a less healthy one.

## The biggest gaps

^ nb04#3f21d022 | The fixed rule and the 95 pairs.
I picked out the biggest gaps with a rule I fixed before I looked. A big-gap pair has to be in the top 5% of all neighbour gaps, and past the noise line as well. That gives me 95 pairs, starting at 9.59 years. The biggest of all is New Oscott and Perry Common College Road, at 15.85 years apart. And in every one of the top ten pairs, the two margins of error are nowhere near overlapping.

::: figure neighbours/04_big_gap_neighbours_map wide nb04#783deefd
alt: Two maps of HLE across the study area and Birmingham, with red outlines around every area in a big-gap pair.
caption: Every area in one of the 95 big-gap pairs, outlined in red. The right-hand map is Birmingham up close.
:::

^ nb04#4d315833 | Men's and women's gaps point the same way.
Finally, I checked that my average of men and women wasn't hiding anything. In 1,302 of the 1,316 pairs past the noise line, the men's gap and the women's gap point the same way. So where one side of a boundary is healthier for men, it's healthier for women too.
