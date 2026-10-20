num: 10
slug: what-the-data-says
title: What I learned from the data
summary: The findings in plain sentences, each tied to its evidence, and the limits.
standfirst: What my six notebooks add up to, and where it stops.
---
## What I found

**The gaps between neighbours are real.** 69.8% of neighbour pairs differ by more than estimate noise can explain, where pure chance would give about 5%. The biggest gap, between New Oscott and Perry Common College Road, is 15.85 years. [Chapter 5](first-findings.html)

**Income, and what travels with it, accounts for most of the difference between areas.** My seven measures predict HLE to within about a year and a half in councils the model never saw, and income carries by far the most weight. [Chapter 8](machine-learning.html)

**It isn't just richer councils sitting next to poorer ones.** When I take each council's average off, income still carries the most weight, and my measures still account for 86.6% of what's left. [Chapter 9](hotspots.html)

**The sharpest drops sit on boundaries.** Two-thirds of the hotspot boundaries also divide councils, against a quarter of ordinary neighbours. But one hotspot is entirely inside Birmingham. [Chapter 9](hotspots.html)

**What my measures miss looks more like settledness, or wealth, than income.** Areas of settled, owner-occupied households do better than I'd predict, and areas of single people renting do worse. [Chapter 9](hotspots.html)

**Some places don't fit at all.** Castle Bromwich East does nearly 5 years better than its measures suggest, and Central Solihull does 7 years better. Frankley, Druids Heath and parts of south Birmingham do worse. Those are the places I'd look at next. [Chapter 8](machine-learning.html)

## The limits

- **Areas, not people.** Every number I give describes an area. None of it says anything about the health of a person who lives there.
- **Links, not causes.** Income lines up with HLE, but that doesn't show income causes it. And my Census screen can't say why owning matters.
- **Different years.** HLE covers 2019 to 2023. The Census was in 2021, and my pollution, fuel poverty and crime figures are from 2024. I'm assuming the order of the areas held, and I haven't tested that.
- **Estimates.** HLE is an estimate with its own margin of error, and my average of men and women is my own measure. Its margin of error is probably a little too narrow.
- **Chosen from HLE itself.** I picked the big-gap pairs and the hotspots because their gaps are extreme, so some of what I found about them is built in. And I chose the Census additions from the same misses they fix.
- **Neighbours aren't independent.** Areas next to each other share a lot, and that makes some of my statistics more confident than they should be. Splitting the data by council is my main guard against that.
