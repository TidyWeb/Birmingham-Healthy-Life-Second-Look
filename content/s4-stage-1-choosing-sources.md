num: S4
part: second-look
slug: s4-stage-1-choosing-sources
title: Stage 1: Choosing sources
summary: The data choices behind the healthy-life analysis, and the limits that travel with them.
standfirst: I chose published measures that seemed plausibly connected to healthy life expectancy. Those links are questions about association, not causes.
---
::: keypoints
I chose area-level sources that could help me examine differences in healthy life expectancy. Signal Box found that some inputs are modelled estimates I cannot reproduce, so I now record their limits and revision risks plainly.
:::

## What I did in Unit 2

^ nb02#e934d6fb | The source table records each dataset's period and catch.
I started with healthy life expectancy, then chose Census, income, environmental, crime and food-environment measures that seemed plausibly related to it. I recorded their periods, geographies, roles and licence notes. These were choices to investigate, not claims that any measure caused health differences.

::: figure wide/01_hle_histograms wide nb03#31cbe73a
alt: Two histograms showing male and female healthy life expectancy estimates across the study areas.
caption: Healthy life expectancy was the outcome I set out to describe. The distributions show why the analysis compares areas rather than treating the region as one uniform place.
:::

## What Signal Box asked {#what-the-screen-asked}

**Q25 — Does the work depend on a supplier's model or data I cannot inspect? Concern.** Signal Box identified ONS healthy-life estimates, ONS small-area income, DESNZ fuel-poverty estimates and Defra pollution maps as modelled inputs. They cannot be reproduced from the published output alone and may be revised.

**Grey — Q9, origin, accuracy or permission unknown? No concern raised.** The register already records source pages, periods, geographies, file hashes and licence notes. The issue was to make known limits visible, not to imply that the sources had unknown origins.

::: signalbox stage S1
:::

## What I found

The source register now distinguishes modelled inputs from other sources and gives every source a plain-language limit and a revision-risk note. The modelled values remain estimates; the new notes make that status visible instead of suggesting they can be recreated exactly.

## What changes {#modelled-inputs}

I added `modelled`, `known_limits` and `revision_risk` to the source register. I kept the source files and their existing uses unchanged.
