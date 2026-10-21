num: S8
part: second-look
slug: stage-5-machine-learning
title: Stage 5: Machine learning
summary: Why I used a simple model, what its features overlap with, and where its errors point.
standfirst: The model estimates how much the selected measures account for the area pattern. It does not make decisions about people.
---
::: keypoints
I used clustering and a plain regression to describe how the selected measures line up with healthy life expectancy. Notebook 07 then tested proxy overlap and error direction; the findings stay visible and the features stay in the model.
:::

## What I did in Unit 2

^ nb05#5f9797c5 | Clustering and linear regression use area-level measures.
Most of my findings come from plain statistics: the joined table, correlations and the neighbour-gap test. I use the models to ask how much seven measures explain together in councils the model has not seen.

I grouped areas using the selected measures without HLE, then compared those groups with HLE. I also fitted a plain linear regression and tested it by holding out whole local authorities, so each prediction came from a model that had not trained on that council.

::: figure ml/05_linear_coefficients nb05#6cc77907
alt: A coefficient chart showing the model weights for the seven area-level measures.
caption: The model weights describe association while the other measures are held constant. They do not show cause.
:::

## What Signal Box asked {#what-the-screen-asked}

**Q2 — Could a simpler non-AI process do this? Concern.** Most of the core findings come from descriptive statistics, the neighbour-gap test and spatial autocorrelation. The model adds an estimate of how much the selected measures account for the pattern; it is not necessary for the central story and it informs no individual decision.

**Q7 — Could features act as proxies for sensitive measures? Concern.** Notebook 05 excluded ethnicity and deprivation directly, but Signal Box found that proxy overlap had not been tested.

**Q11 — Does crime encode decisions about reporting or policing? Concern.** Recorded crime is a model feature, so I tested whether the conclusions changed when it was removed.

**Q15 — Do errors fall more on some groups? Concern.** Unit 2 reported overall residual autocorrelation but did not compare errors across ethnic-composition or deprivation groups.

::: signalbox stage S5
:::

## What I found

^ nb07#4c2239b1 | Bias and absolute error by deprivation third.
By absolute error, accuracy is similar across deprivation thirds: MAE is 1.31–1.34 years, with overlapping intervals. Direction is different: the model under-predicts HLE in the least deprived third by 0.31 years and over-predicts it in the most deprived third by 0.46 years, so it understates the real gap. That underclaim is an accuracy failure under my stated position.

## What changes

I keep the seven features and report their proxy overlap as a finding. Crime stays because it tracks local conditions and income; recorded crime also depends on policing, reporting and footfall, so visitor hubs remain excluded from the model. The crime test shows the conclusions barely change without it. The full tables and the ethnic-composition comparison are in [Proxies, fairness and crime](proxies-fairness-and-crime.html).
