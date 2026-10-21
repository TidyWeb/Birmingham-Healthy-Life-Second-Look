num: S7
part: second-look
slug: stage-4-hypothesis-test
title: Stage 4: The hypothesis test
summary: Neighbour gaps tested against estimate noise, then rankings checked against uncertainty.
standfirst: A difference can be real without giving every area a firm rank. I need to show both parts accurately.
---
::: keypoints
I tested whether the neighbour gaps were larger than estimate noise. I then tested whether the published-lowest areas stayed in the bottom tenth when uncertainty was simulated.
:::

## What I did in Unit 2

^ nb04#5a64afb1 | The noise simulation and real neighbour gaps.
I set a noise-only comparison before interpreting the biggest neighbour gaps. In the real data, 69.8% of neighbour pairs passed the noise line, far above the range from the noise simulations. That supports the claim that the measured gaps are not all random fluctuation; it does not explain why they occur.

::: figure neighbours/01_gap_distribution nb04#f2184c4d
alt: The distribution of observed neighbour gaps compared with gaps simulated under noise.
caption: Observed differences extend well beyond the noise-only gaps. The test asks whether differences are larger than estimate noise, not what caused them.
:::

## What Signal Box asked {#what-the-screen-asked}

**Q14 — Could an output be treated as proof rather than a prompt? Concern.** A single value or exact rank looks more certain than an estimate with a margin of error. Signal Box found that mid-table ranks could be unstable and that maps of model residuals could imply more than the model establishes.

::: signalbox stage S4
:::

## What I found

^ nb08#61b0ac31 | Simulated rank bands and the published-lowest comparison.
I simulated each area's estimate 10,000 times. Of the 66 areas with the lowest published estimates, 35 were confidently in the lowest tenth at the 95% threshold. The rest did not meet that confidence threshold. Each area's simulated draw is independent of the others, matching Notebook 04's simulation assumption.

## What changes

I keep single estimates where they answer the question clearly, and show ranges or confidence bands where an exact ordering would overstate what the estimates distinguish. The rank view is an accuracy check in practice, not a reason to hide a real difference.
