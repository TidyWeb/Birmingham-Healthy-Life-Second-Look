num: S11
part: second-look
slug: how-certain-are-the-rankings
title: How certain are the rankings?
summary: Rank intervals and confidence bands show which areas can be called among the lowest.
standfirst: I tested whether the areas with the lowest published estimates stay at the bottom when their uncertainty is carried through the ranking.
---
::: keypoints
Every area's ranking figure is an estimate with a margin of error. I re-ran the ranking 10,000 times within those margins to see which areas stayed near the bottom of the ranking list. 35 of the 66 lowest-ranked areas stayed in the lowest tenth in at least 95% of those runs. The other 31 moved in and out, so the evidence does not support describing them as consistently among the lowest ranks.
:::

## The question

Which areas can honestly be described as among the lowest, and which estimates overlap enough that a firm ordering would claim too much?

## The method

^ nb08#61b0ac31 | The simulation design and independence assumption.
I used the published area means and standard errors derived from their 95% intervals, then drew an HLE value for every area and ranked all areas in each of 10,000 simulations. For every area I kept its median simulated rank and central 90% rank interval, and I counted how often it fell in the bottom or top tenth. Each area's draw is independent of every other area's draw, matching Notebook 04's simulation; that independence is an assumption, not a measured relationship.

## What I found

^ nb08#61b0ac31 | Confidence bands for the bottom and top tenths.
^ nb08#26b1fe2a | The intervals for the published-lowest areas and all areas.
The bands are based on the simulated chance that each area falls in an extreme tenth. “Confidently” means at least 95%; the other bands separate likely, possible and unlikely membership.

| Confidence band | Bottom tenth | Top tenth |
|---|---:|---:|
| Confidently | 35 | 37 |
| Likely | 33 | 27 |
| Possibly | 27 | 38 |
| Not | 565 | 558 |

::: figure uncertainty/rank_intervals_lowest_100 wide nb08#26b1fe2a
alt: Rank intervals for the areas near the lowest published HLE estimates.
caption: The intervals show how far each area's simulated rank can move; close or overlapping ranges do not support a firm ordering.
:::

::: figure uncertainty/rank_intervals_all_areas wide nb08#26b1fe2a
alt: Simulated rank intervals across all study areas.
caption: The full ranking shows uncertainty across the whole distribution, not only among the lowest estimates.
:::

^ nb08#fc6a2ef5 | Probability of falling in the bottom tenth.
::: figure uncertainty/probability_bottom_tenth_map wide nb08#fc6a2ef5
alt: Map showing each area's simulated probability of being in the bottom tenth.
caption: The map shows an estimated probability for each area, not a certain label for its residents.
:::

## What it means {#uncertainty-response}

I present rankings as ranges and confidence bands wherever a single order would look more certain than the estimates allow. This is the accuracy test in practice: the intervals separate areas that can be described as confidently low from those that cannot. A real HLE difference should remain visible, but a rank should not be firmer than the evidence.
