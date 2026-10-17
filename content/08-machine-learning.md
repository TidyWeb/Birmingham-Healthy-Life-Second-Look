num: 8
slug: machine-learning
title: Machine learning
summary: Clustering without HLE, then one plain regression tested on councils it never saw.
standfirst: If I know seven things about a place, how much of its healthy life expectancy can I guess?
---
::: keypoints
- When I group the areas by the seven measures alone, without HLE, the groups still differ by over 11 years of HLE.
- One straight-line model predicts HLE to within about a year and a half, in councils it has never seen.
- Income does most of the work. And what the model misses still clusters on the map.
:::

## Why these two methods {#why-ml}

^ nb05#5f9797c5 | Why k-means and a plain linear regression.
I came at it two ways. First I used **clustering**, to sort the areas into groups using only the seven measures. I kept HLE out of it, so the groups can't just be HLE in disguise. Then I brought HLE back to see whether the groups differ. Second, I used **regression**, to fit one straight-line model that predicts HLE from the same seven measures.

I picked k-means because each group has a centre, a sort of average area for that group, and I can describe that in plain words. And I picked a plain linear regression because it gives me one number for each measure, in years of HLE, and I can explain every one of them. A fancier model might squeeze out a bit more accuracy, but I'd struggle to say what it was doing. For this project I'd rather understand the answer.

I leave six city and town centres out of both of these. I do that because their crime figures are more about footfall and the number of visitors than about the people who live there. So with that exclusion made, I have 654 areas.

## The groups

^ nb05#ec4c2f1e | How I chose the number of groups.
I tried between two and eight groups, and I chose four, using the silhouette score. That score asks how clearly each area belongs to its own group. My scores were low, and that told me something. My areas don't fall into neat types. They sit along one long slope from worse-off to better-off, and my groups are slices of that slope. I also resampled the areas 50 times to see if the groups held, and I got much the same groups back each time (an average agreement of 0.80).

::: figure ml/04_cluster_map wide nb05#97216829
alt: Map of the 654 areas coloured by four groups, with six city and town centres hatched grey.
caption: The four groups on the map. I made them from the seven measures alone, without HLE.
:::

^ nb05#9585f4ee | HLE by group, once I brought it back.
Then I brought HLE back. The better-off group averages 68.9 years in good health, and the poorest group averages 57.3. That's over 11 years between groups that never saw HLE. And the groups account for about 71% of the variation in it.

::: figure ml/03_hle_by_cluster nb05#6770b89a
alt: Box plots of HLE for each of the four groups, rising from about 57 to about 69 years.
caption: HLE in each group. Every group still has areas well above and below its average.
:::

^ nb05#233175fa | Big-gap pairs against all neighbour pairs.
Then I went back to the neighbours. Of the 92 big-gap pairs I could classify, 90% cross from one group to another. Across all neighbour pairs, only 42% do. So the big gaps really do sit where neighbouring areas are different kinds of place.

## The regression

^ nb05#a0ce0033 | How I tested the model.
How I tested the model mattered more than the model itself. Neighbouring areas resemble each other, so if I split the areas at random, the model would learn from an area's next-door neighbour and then get tested on the area itself. So I split the data by local authority instead. The model learns from most of the councils and predicts the rest, and I rotate until a model that never saw its council has predicted every area.

I also need something to beat. So I compare the model with a baseline that ignores the measures and just guesses the average HLE every time.

::: stats nb05#73844d12
1.64 | years, the model's typical miss (RMSE)
5.19 | years, the typical miss when I just guess the average
0.89 | R², the share of the variation in HLE the model accounts for
:::

That's a lot higher than I expected. If I know an area's income, its qualifications and the rest, I can predict its healthy life expectancy to within a year or two most of the time.

## Which measures carry the weight

^ nb05#f72403b6 | The weights, and why employment comes out negative.
Income dominates. One standard step up in income, which is about £5,000 a year after housing costs, goes with 3.1 more years in good health, with the other six measures held still. Qualifications come next, at 1.1 years. More polluted areas do a little worse even at the same income (−0.6). Crime, fuel poverty and anti-social behaviour all point the way you'd expect, but their weights are small.

::: figure ml/05_linear_coefficients nb05#6cc77907
alt: Horizontal bar chart of the seven regression weights, with income far the largest at about 3.1 years.
caption: The weight on each measure, in years of HLE per standard step, with the other six held still.
:::

Employment comes out slightly negative, and I want to be clear about why. It isn't saying work is bad for health. Employment is tangled up with income and qualifications, and once those two are in the model, there's very little left for employment to explain.

## Where it gets it wrong

^ nb05#983c5353 | The areas the model gets most wrong.
A residual is an area's actual HLE minus what the model predicted for it, and these are the places I'm most interested in. Central Solihull does 7 years better than its measures suggest. And a run of south Birmingham areas, Frankley, Druids Heath, Kings Heath and Bournville East, do worse.

::: figure ml/06_residual_map wide nb05#d63444a3
alt: Map of residuals, with areas doing better than predicted in one colour and worse in another.
caption: Each area is shown by how its measured HLE differs from the model estimate. The map shows spatial association, not cause.
:::

^ nb05#e9d393a4 | Moran's I for HLE and for the residuals.
And the misses still cluster. HLE itself scores 0.57 on Moran's I, and the residuals score 0.15. So my seven measures take out about three-quarters of the resemblance between neighbours, but not all of it. That tells me something local is going on that my measures don't see.

::: callout
The 89% mostly confirms what you'd expect. I'm more drawn to the 11%.
:::
