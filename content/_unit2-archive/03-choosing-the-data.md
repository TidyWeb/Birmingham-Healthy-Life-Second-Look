num: 3
slug: choosing-the-data
title: Choosing the data
summary: Eleven public datasets on the same 660 areas, what I left out, and the areas that need care.
standfirst: I chose eleven public datasets, cut them all to the same 660 areas, and left a few out on purpose.
---
::: keypoints
- HLE is my outcome, and I compare everything else against it.
- I use ten other datasets to cover money, housing, work, education, air, crime and who lives in each area.
- I left some things out because they would hand HLE its own answers back.
- I flag ten areas, but I don't delete any of them.
:::

## What I brought in

^ nb02#e934d6fb | The full table of datasets, periods and catches.
I worked with data that's already published for every MSOA, or that I could build up to that level. All of it is open data from ONS, Defra, the government or the police, under the Open Government Licence.

| Measure | Source | Period | The catch |
|---|---|---|---|
| Healthy life expectancy | ONS health state life expectancy | 2019–2023 | Estimates with a margin of error |
| Household deprivation | Census 2021, TS011 | 2021 | One of its four parts is health |
| Overcrowding | Census 2021, TS052 | 2021 | Bedroom shortfall only |
| Fuel poverty | Fuel poverty statistics | 2024 | After the HLE period |
| NO₂ and PM2.5 | Defra modelled background | 2024 | A 1 km grid, after the HLE period |
| Employment and unemployment | Census 2021, TS066 | 2021 | Students distort it |
| Qualifications | Census 2021, TS067 | 2021 | Students again |
| Household income | ONS small area income estimates | Year to March 2023 | Modelled averages |
| Ethnic composition | Census 2021, TS021 | 2021 | 19 shares of one population |
| Recorded crime and anti-social behaviour | Police open data | 2024 | Town centres inflate the rate |

The years don't all line up. HLE covers 2019 to 2023, the Census was in March 2021, and my pollution, fuel poverty and crime figures come from 2024. I'm assuming the order of the areas hasn't changed much in between. I haven't tested that, so I say so wherever it matters.

## What I left out, and why

- **The railways.** They started the project, but in the end they were just window dressing, because my question is about neighbours and not about stations.
- **Health and disability measures.** ONS builds HLE partly from people saying how healthy they are. If I tested health measures against it, I'd just be handing HLE its own answer back.
- **Smoking.** I'd have liked it, but it's only published for whole councils and not for my small areas.
- **The Index of Multiple Deprivation.** It has health built into it, so I left it out for the same reason as the health and disability measures.

I did bring in household deprivation, but I only use it to describe areas. One of its four dimensions is health and disability, so I never put it into a model.

## Areas that need care

^ nb02#786d538f | The two flagging rules and how I checked them.
Some areas are so unlike the rest that their numbers mean something different. So I flag them, and I don't delete them.

**Visitor hubs.** I count crime per resident, but city and town centres have far more people passing through than living there. Birmingham city centre's rate comes out at about 14 times the typical area's. Six centres sit above the usual outlier fence, so I leave them out of the crime analysis, and only the crime analysis. I keep everything else about them.

**Student areas.** In six areas, more than half of the adults are full-time students. That means their employment and qualification figures describe students, and not the local economy. I keep these areas in everything, and treat the flag as a caveat when I read their results.

^ nb02#0eadbcb7 | The ten flagged areas by name.
That makes ten areas out of 660, because Central Coventry and Birmingham Dartmouth Circus are both. Every row stays in my data, and I keep a flags file that says which areas I flagged and why.
