num: 9
slug: hotspots
title: Looking closer: the hotspots
summary: The five places where big gaps cluster, a check inside each council, and a wide Census screen.
standfirst: The broad picture is income. So I zoomed in on the five places where the sharpest drops keep turning up.
---
::: keypoints
- The 95 big gaps fall into 45 patches, and I call the five largest the hotspots.
- Two-thirds of their sharp boundaries also divide councils. But one hotspot sits entirely inside Birmingham.
- Inside each council, income still carries the most weight.
- A wide Census screen points to settled, owner-occupied households doing better than predicted.
:::

## Finding the hotspots

^ nb06#af25607b | How I build patches from the big-gap pairs.
One big-gap pair on its own could be a quirk of two estimates. But a patch where big gaps keep turning up is a place where the difference is real and repeated. So I joined the 95 pairs into patches wherever they share an area. That gave me 45 patches, and I took the five largest as my hotspots.

1. Chelmsley Wood and Castle Bromwich
2. Frankley and Bartley Green
3. Druids Heath and Wythall
4. Kingstanding and New Oscott
5. Yardley Wood and Fox Hollies

::: figure hotspots/01_hotspot_overview wide nb06#9c4f9cfc
alt: Map of the study area in light grey with five coloured patches marking the hotspots, numbered one to five.
caption: The highlighted patches group repeated gaps between area-level HLE estimates. They show spatial association, not cause.
:::

^ nb06#b39282ac | Council boundaries among hotspot, big-gap and ordinary pairs.
Council boundaries turn up far more often than I expected. 65.5% of the hotspot pairs cross from one council to another, against 24.7% of ordinary neighbour pairs. But Kingstanding and New Oscott sits entirely inside Birmingham, so the divide isn't only between councils.

## Inside each council

If one council is simply richer and healthier than the one next door, that alone could make income look important. So I took each council's average off every area, and refitted the model on what was left.

::: stats nb06#0098d9ea
2.41 | years of HLE per standard step of income, inside councils
86.6% | of the remaining variation the seven measures still account for
:::

Income still carries the most weight. So the income link isn't just richer councils sitting next to poorer ones. NO₂ is the exception. Its weight almost disappears, and that tells me it was mostly telling councils apart.

## The five up close

^ nb06#4b61f31f | The close-ups, with each area's prediction.
When I looked at each hotspot up close, I found something more local. Castle Bromwich East is 4.81 years above its prediction, and it sits right next to the Smith's Wood areas, which do worse than theirs. And Frankley, Druids Heath, Perry Common College Road and Yardley Wood West all sit well below their predictions.

::: figure hotspots/hotspot_1_flat_map nb06#50a9bf7b
alt: Map of the Chelmsley Wood and Castle Bromwich hotspot, areas coloured by HLE band, with red lines along the big-gap boundaries.
caption: Hotspot 1, Chelmsley Wood and Castle Bromwich. The map compares HLE estimates across area boundaries and shows spatial association, not cause.
:::

I'm building a 3D view of these five places. Height will show the drop from one area to the next, and you'll be able to switch between the actual drop and the one the model expected.

## Looking wider: a Census screen

Up to this point, I'd only looked where I expected to find answers. So for the last part I looked wider. I took nearly every Census topic published for my areas, and tested each one against what the model couldn't explain.

^ nb06#adfa80ac | Finding in one half of the councils, checking in the other.
If you test hundreds of things at once, some of them will look important by pure chance. So I split the councils into two halves. If something showed up in the first half, it only counted when it showed up again, the same way round, in the second.

::: stats nb06#fc01a42d
248 | characteristics tested
95 | candidates in the first half
81 | confirmed in the second
:::

^ nb06#e9a03f56 | One combined score and what it carries.
That was far more than I expected, and it made me suspicious. Area characteristics tend to travel together, so I combined the 81 into one score, and that one score carries 51% of their spread. So most of the result is one picture. Areas of settled, owner-occupied, mostly married households do better than my seven measures predict, and areas of single people renting do worse. Owning outright is closer to wealth than to income, and that may be part of it. But the Census can't tell me why.

::: figure hotspots/04_census_screen_correlations wide nb06#2bbbf95f-1
alt: Bar chart of the ten strongest positive and ten strongest negative Census characteristics against the model's misses.
caption: The ten strongest characteristics each way. Areas with more of the ones above the line do better than predicted, and areas with more of the ones below do worse.
:::

^ nb06#4da0a0c0 | What each addition does to the model.
When I add owning outright to the model, the typical miss drops from 1.64 years to 1.28. But there's a catch. I picked it because it lines up with the model's misses, so of course it helps fix them. I'd want another dataset, or the next Census, before I trusted the size of that gain.

^ nb06#a4f17b93 | The ethnic composition check.
I also checked ethnic composition. Areas with higher Black and Mixed shares sit below their predictions. But once I allow for the settled-household picture, those links all but disappear. And takeaways per resident didn't pass at all.

^ nb06#f2b6d0c8 | The hotspot areas side by side.
On the ground, the split is stark. In Frankley, 18% of households own their home outright. In Dodford, right next door and 15 years healthier, it's 51%.
