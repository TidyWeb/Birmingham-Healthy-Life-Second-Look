num: 10A
slug: what-the-data-doesnt-say
title: What the data doesn't say
summary: The limit of all measurement: we see the ripples, never the stone. Culture, Marmot, and what I'd do differently.
standfirst: Everything I've measured points at something. The thing it points at, I can't measure.
---
## The ripples, not the stone

After I'd finished the notebooks, I went back through what they found, and something started to bother me. I've got eleven datasets measuring income, housing, work, qualifications, air, crime and who lives where. They all line up with healthy life expectancy, some of them very strongly. And yet none of them ever says anything definitive about *why*. The thing I actually want to understand isn't in any of them. It's only implied by them.

It's like throwing a stone into a pool. I never see the stone. I only see the ripples afterwards, and I have to work backwards from the ripples to what made them.

I think this is a limit of all data analysis, not just mine. Very often we can only measure what sits around the edge of the thing that matters. We measure the points where something landed, not the thing that did the landing.

## Reading the debris layer

The best example I know is the asteroid that ended the age of the dinosaurs, about 66 million years ago. Nobody saw it, and the asteroid itself no longer exists. What exists is the evidence it left. In 1980, Luis and Walter Alvarez reported a thin layer of clay in the rocks at Gubbio in Italy that was rich in iridium, a metal that's rare on Earth but common in asteroids. The same layer turns up in rocks all over the world. From that fine layer of debris, they argued there had been an impact. The crater itself, at Chicxulub in Mexico, was only linked to it about a decade later.

That's what I'm doing with my data. Income, tenure and qualifications are the iridium layer. They're real, they're measurable, and they tell me something happened. But they aren't the thing itself.

## Things that are real but can't be seen

Astronomy has the same problem, and it's dealt with it twice in a way I find deeply moving.

In the 1840s, astronomers noticed that Uranus wasn't moving quite the way it should. Something was pulling on it. Urbain Le Verrier in France worked out where an unseen planet would have to be to cause that pull, and in September 1846 Johann Galle pointed a telescope at the spot and found Neptune, very close to where Le Verrier had said it would be. Nobody had seen it, but its effect on everything around it had already given it away.

Dark matter is the same idea, except that we still can't see it. Galaxies spin faster at their edges than the stars and gas we can see could hold together. So something we can't see is there, adding its pull. Most physicists accept that it's real, and nobody has yet detected it directly. Dark energy goes further still. It's the name for whatever is making the universe expand faster, and it's known only through what it does.

That resonates with me. Things can be real and still be invisible to us, and the only way we know they exist is through what they do to everything we *can* see. I think the thing behind the gaps in healthy life expectancy is like that. My measures are the wobble in Uranus's orbit. Whatever is causing the wobble isn't in my data.

## What my measures stand in for

^ nb05#73844d12 | The model accounts for 89% of the variation in HLE.
My seven measures account for about 89% of the variation in HLE between areas. That sounds like an answer, but it isn't one. Income doesn't make anyone healthier on its own. It stands in for a whole way of living: what you eat, where you live, what work does to your body, how much stress you carry and what you can afford to do about it.

^ nb06#e9a03f56 | The settled-household picture from the Census screen.
And when I looked at what the model missed, the strongest signal wasn't about money at all. Areas of settled, owner-occupied, mostly married households do better than their income predicts, and areas of single people renting do worse. Tenure is another ripple. Owning your home outright isn't healthy in itself. It says something about planning, stability and time, and I can't measure any of those directly.

## A quick look at tenure

I wanted to see that ripple for myself, so I put social renting next to healthy life expectancy on the map. This is a quick exploratory check, not part of my notebook analysis. I made it with a separate script, straight from the Census 2021 tenure table (TS054), and I haven't tested it the way I tested everything in Notebooks 04 to 06.

::: image tenure-hle.webp wide
alt: Three maps of the 660 areas. Healthy life expectancy, the share of households in social rent, and a combined map showing where the two agree.
caption: Healthy life expectancy, social renting, and where the two agree. In the combined map, the darkest areas have high social renting and low HLE, and the lightest have low social renting and high HLE. An exploratory check, made outside the notebooks.
:::

The overlap is striking. Across the 660 areas, the rank correlation between social renting and HLE is −0.84. When I split both measures into thirds, 71.5% of areas land where the two maps agree. And at the extremes they hardly ever disagree: not one area has both high social renting and high HLE, and only two have low social renting and low HLE.

^ nb06#fc01a42d | Renting from the council or a housing association, against the model's misses.
But I have to read it carefully. Social renting runs alongside income almost as closely as HLE does, so a lot of this overlap is the money story again. The stronger evidence is in Notebook 06. Even after income and the other six measures were in the model, areas with more renting from the council or a housing association still did worse than predicted. So tenure does seem to carry something beyond money. What it carries, the map can't tell me. It's another ripple.

## My hunch: culture

I'll be honest about where I think this points, and it comes from my own life rather than my data.

I'm from a working-class background. I started work as a carpenter at 16, and between 16 and 24 I earned really good money for the area I grew up in. I hit my earnings ceiling young, the way tradespeople do. While I was doing that, I went to night school, which was unusual for a tradesman. Later I went to university as a mature student.

What I noticed, and still notice, is that the people who went straight into skilled work had something like a ten-year head start on income. A bricklayer can be fully qualified and earning the top rate within about three years, at an age when someone on the university route is still earning very little. But that financial head start doesn't clearly convert into a higher healthy life expectancy. So while income is a strong correlator with HLE, it cannot be the sole key determining factor. In my experience, early money often came with early habits: going to the pub most nights, smoking cigarettes, a tendency to get takeaways instead of cooking. The path of deferring gratification, of making the effort to stay informed and take responsibility for one's own health seems to me to fit better with the slower route.

So my hunch is that the invisible thing is cultural, the sociology of an area. But I have to be careful here, because that is a hunch from experience and not a finding. My data can tell me that something is missing from my measures. It can't tell me that the something is the culture or ideology of the subjects being studied.

## Marmot, and the causes of the causes

I only came across the work of Professor Sir Michael Marmot late in this project, and I wish I'd found it at the start, because it would have changed how I shaped the whole thing. His review for England, *Fair Society, Healthy Lives*, came out in 2010, and the Institute of Health Equity followed it up in 2020 with *Health Equity in England: The Marmot Review 10 Years On*.

The 2020 review found that life expectancy in England had stopped improving for the first time in more than 100 years, and had actually fallen for the poorest 10% of women. It found that people were spending more of their lives in poor health. And it found that the gap between more and less deprived areas had grown steeper over the decade. That's the same gradient my maps show, at a national scale.

Marmot's argument sits right on top of my hunch, and it challenges it too. He'd agree that smoking, drinking and diet matter. But he asks what causes *them*, and his answer is the conditions people live in: insecure work, stress, poor housing, what food is on the doorstep and how much control people have over their lives. He calls these the causes of the causes. On that reading, the habits I noticed growing up aren't a failing of character. They come out of circumstances.

I don't think I have to choose. Culture and conditions might be the same stone seen from two sides. But my own life experience doesn't tally with the conditions I've just described, because they belong to a different rung of the ladder from the one I grew up on. Marmot describes a gradient, where health gets worse at every step down, and the insecure work and poor housing sit near the bottom of it: unskilled, zero-hours, no contract, casual labour. That is the worst position to be in.

I grew up one rung above that, in a working-class culture where skilled trades were seen as THE route to go. Learning a trade was the key thing about being a kid, precisely because everyone knew they didn't want to end up at the bottom of the heap. There was pressure and stress, but not the job insecurity or poor housing. In fact house ownership was a key element among all my peers, even when the interest rate on a mortgage was 14%. So on my rung, the conditions were reasonably good, and the money was good too. That's exactly why I think something else, something cultural, is at work there.

So culture and conditions may vary, but what my data definitely can't do is tell them apart. Both would leave exactly the same ripples in area-level statistics.

## Two more things the data can't see

**What work does to a body.** A carpenter or a bricklayer spends years on scaffolding, lifting, kneeling and breathing dust. That costs healthy years directly, whatever anyone's habits or attitudes are. My own knees are worn out from it, and there are tasks I physically can't do any more. My employment measure counts whether people work. It doesn't say what the work does to them.

**A life, rather than a moment.** My own story is about a life course: earning early, peaking early, and habits set young. Every dataset I have is a snapshot of areas at one point in time. None of them follows a person from 16 to 60. To see that, I'd need data that follows the same people for years, like the UK's longitudinal household studies, and that would be a different project.

## What I'd do differently

If I started again, I'd start from Marmot. I'd take his framework of the conditions that shape health, and go looking for data that measures those conditions as directly as possible, to test them, rather than starting from whatever datasets happen to be published and asking what they line up with.

But I'd still expect to end up here. However good the data, it measures the debris layer. It doesn't measure the asteroid. And I think saying that clearly is part of doing this data analysis, indeed any data analysis, honestly.
