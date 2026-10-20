num: 4
slug: shaping-the-data
title: Shaping the data
summary: Rolling small areas up, turning counts into rates, one HLE per area, and one measure per theme.
standfirst: Each dataset had far more in it than I needed. The work was cutting it down without losing what matters.
---
## The same steps for every dataset

^ nb02#817b9646 | The four steps, in Notebook 02.
I put every dataset through the same four steps. First I pick out my 660 areas. Then I look at every field, so I know what I'm dealing with. Then I keep the few measures I want. And finally I save the file and read it back, to check it holds what I meant to save. I never change the original source files.

## Getting everything onto the same areas

Most of the Census tables already come by MSOA, but the others needed some work.

- **Fuel poverty** is published for smaller areas, called LSOAs. So for each of my areas I add up the fuel-poor households and the total households in its LSOAs, and then divide. I don't average the small-area percentages, because then a tiny area would count as much as a big one.
- **Pollution** comes as 1 km grid squares. So for each area I take the squares that overlap it, and I weight each square by how much of it falls inside the boundary.
- **Crime** comes as individual records with a small-area code. So I count the records into my areas and divide by the number of residents.

## Counts into rates and shares

A big area has more of everything, so raw counts mostly tell you how big an area is. That's why I turn every count into a share or a rate, such as the share of households short of a bedroom, the share of adults with degree-level qualifications, or crimes per 1,000 residents. Then I can compare areas of different sizes fairly.

## One HLE for each area

^ nb01#710ce0cf | Men and women correlate at 0.97 across my areas.
ONS publishes HLE separately for men and women. But across my areas the two track each other almost exactly, with a correlation of 0.97, so places that are low for men are low for women too. If I ran every analysis twice, I'd mostly get the same answer twice. So I use the average of the two as my single outcome, and I keep the separate figures for one final check.

^ nb03#b230c918 | How the margin of error for the average is worked out.
The average needs a margin of error too, so I built one from the two published intervals. To do that I have to assume the male and female errors are independent. They probably aren't quite, so my margin of error is likely a little too narrow, and I treat it as a guide. The average is my own measure, and not an ONS one.

## One measure per theme

When I compared the measures with each other, I found many of them were telling the same story in different ways. NO₂ and PM2.5 are almost the same map. And income, deprivation, overcrowding and no qualifications all rank the areas in much the same order.

::: figure wide/05_core_overlap wide nb03#62df90ff
alt: A grid of correlations between every pair of measures, with strong overlaps among income, deprivation, overcrowding and qualifications.
caption: How closely each measure moves with every other. The darker the square, the more two measures rank the areas in the same order.
:::

^ nb03#0b9455ba | The 0.80 working rule and how I picked the list.
If I put near-copies into one model, the same idea gets counted several times over. So I picked a short list. I started with income after housing costs as my anchor, because it has no health in it. Then I went down the other measures, from the strongest link with HLE to the weakest. If a measure overlapped 0.80 or more with one I'd already picked, I held it in reserve instead.

::: stats nb03#a4160786
7 | measures on my shortlist
4 | held in reserve as near-copies
0.80 | my working line for "too similar"
:::

My seven are income, degree-level qualifications, recorded crime, fuel poverty, NO₂, employment and anti-social behaviour. You can follow every step in Notebooks 02 and 03.
