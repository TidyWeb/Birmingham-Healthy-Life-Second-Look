num: 1
slug: the-idea
title: The idea
summary: A Tube map of life expectancy, a railway idea I dropped, and the question I ended up asking.
standfirst: It started with a map of the London Underground and ended with a question about next-door neighbours.
---
## Where it came from

I didn't want to do this project on a Kaggle dataset. My Unit 1 assessment was one, and it taught me the tools, but I discovered somebody else had already cleaned and shaped that data before I ever saw it, which totally undermined my whole rationale for selecting that dataset as it was historically known to be messy and full of missing data points.

For Unit 2 I wanted real public data about something I could care about.  About a place I know, with all the mess that comes with it.

The spark for this project was *Lives on the Line* by James Cheshire and Oliver O'Brien. It's a map of the Tube, and every station is coloured by the life expectancy of the people who live around it. If you ride a few stops east from the City, you lose years. I loved how the railway line made the inequality so easy to see.

::: image lives-on-the-line.webp
alt: The Lives on the Line map, showing London Underground lines with each station coloured by the life expectancy of the people living around it.
caption: *Lives on the Line* by James Cheshire and Oliver O'Brien, the map that inspired this project. See the original on [James Cheshire's site](https://jcheshire.com/featured-maps/lives-on-the-line/).
:::

So my first plan was to do the same thing for Birmingham.  I began by plotting the route of the number 11 bus (known as the outer circle route).  I got into maps and GIS, and discovered immediately that a circle drawn a fairly standard distance from a centre tends to reveal little, as all of the areas it traverses tend to be of similar socio-economic status.  So my mind moved to  rail corridors.  I live in Solihull, my one pal Terry lives in Dorridge, and our other pal Malcolm lives in Sheldon.  I could see three distinct variances in life expectancy for these three places.  So I investigated using rail lines as linear sections across the region.

Each station would become a datapoint, and all I had to do was set a radius around it to compare and contrast outcomes. I spent quite a while on it. But the more I looked at the data, the more I cared about something else: areas right next to each other that differ a lot, whether there's a railway between them or not. The line on the map was only ever a way of showing that. So I dropped the railway idea as window dressing.  Cute, but fundamentally not that informative, so I decided to go city-wide, using geo-located data, and using a map that would be a living visualisation.

## What healthy life expectancy is

^ nb01#c1b2aaa9 | Why I chose HLE over plain life expectancy.
Life expectancy tells you how long people are expected to live. Healthy life expectancy (HLE) tells you how many of those years they can expect to spend in good health. Two places can have a similar life expectancy and a very different HLE.  I am interested in difference, so HLE offers more of it and that's why I chose it.

ONS builds it for each area from death rates and from how healthy people said they were in the Census. So it's an estimate for a population. It isn't a forecast for anyone who lives there.

## The areas

^ nb01#c1b2aaa9 | The 660 areas and why MSOAs.
I work with the smallest areas ONS publishes HLE for, which are called MSOAs (middle layer super output areas). Each one holds roughly 5,000 to 15,000 residents. I have 660 of them, covering Birmingham and the areas around it, out to Shropshire, Coventry and Derby. I've given them their familiar local names, so my maps say Sparkbrook North and not "Birmingham 001".

## Who it's for

I made this for people who know Birmingham and the places around it, both the public and the professionals who work there. I want them to recognise the areas by name, read the maps, and relate what they see to what they already know.

## The question

::: callout
Why do areas that share a boundary differ in healthy life expectancy, in some cases by 14 to 16 years?
:::

The rest of this site follows how I went about answering that. The short answer is income, and the things that travel with it. But the longer answer is more interesting than that.
