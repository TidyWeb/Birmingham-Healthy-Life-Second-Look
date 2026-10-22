num: S1
part: second-look
slug: s1-why-a-second-look
title: Why a second look
summary: The position behind revisiting my Unit 2 Birmingham Healthy Life analysis through an ethical lens.
standfirst: The Code Institute Unit 3 assessment asks for a data project with ethical considerations applied first. I had already done a data project in Unit 2, so I am revisiting that work through an ethics-first lens, describing what the evidence supports without in any way hiding uncomfortable findings, or claiming more than the data can show.

---
::: keypoints
The Ethics of a Birmingham Healthy Life is my Unit 3 project for the Code Institute Diploma in Data Analytics with AI. I am revisiting my Unit 2 Birmingham Healthy Life analysis, but coming to it through an ethics-first lens, describing what the evidence supports without in any way hiding uncomfortable findings, or claiming more than the data can show.
:::

## What this is

I want any claims I make in this project to be as strong as the evidence: no stronger, and no weaker. I keep in mind the principle often traced to Hippocrates, in the Hippocratic *Epidemics*: to help, or at least to do no harm.

Birmingham Healthy Life began as my Unit 2 project. In Unit 3 I am revisiting that work, examining the choices behind it and rebuilding how I explain the findings. The original chapters are on [the live Unit 2 site](https://tidyweb.github.io/Birmingham-Healthy-Life/).

I built [Ethical Considerations in AI](https://tidyweb.github.io/ethical-considerations-in-ai/) as an independent companion to the Code Institute LMS lesson for fellow students, then created [Signal Box: the AI ethics check](https://tidyweb.github.io/ethical-considerations-in-ai/#screening-tool) within it. I applied Signal Box to my Unit 2 Birmingham Healthy Life project; Unit 3 is that ethical rework and a practical test of whether Signal Box works. The guide is my own study material, not official Code Institute material; [The method](s2-the-method.html) explains how I applied Signal Box.

::: callout
“The aim is to see the truth about healthy life expectancy, told plainly. Ethical care means not causing avoidable harm and not claiming more than the evidence shows. It does not mean avoiding uncomfortable findings.”
:::

## Respect without avoiding the question

Respecting people and trying to avoid harm matter. That is different from becoming so worried about the possibility of offence that I stop saying what the evidence shows. Trying to please everyone all the time would leave the account too vague to be useful. I am not seeking approval. I am seeking the truth.

The message and the way each reader receives it are not the same thing. I cannot control every interpretation. I am however responsible for every claim I make, and how strongly I make it.

## An accuracy test

A claim should be exactly as strong as its evidence. Overclaiming is an accuracy failure: a precise ranking may not be supported when estimates overlap, and an association does not show a cause. Underclaiming is also an accuracy failure. If a real inequality is visible, softening it until it disappears would conceal something residents have a reason to see.

The figures are estimates, with margins of error. That is a reason to show uncertainty honestly, not a reason to stay silent. A single value can make a map readable; ranges are more appropriate where a ranking or comparison could otherwise imply more certainty than the estimate supports.

## Why rank and name places

The investigation is about healthy life expectancy, so I rank areas by healthy life expectancy. I name areas using familiar local names so people who know Birmingham and its surroundings can recognise them and relate the results to places they know.

The datasets were chosen through judgement. I began with measures that seemed plausibly connected to healthy life expectancy, based on intuition and life experience. I left out measures with no plausible route to the question, then plotted the selected data against healthy life expectancy to see what related and what stood out. Those choices and the reasons for keeping or dropping a dataset should be visible rather than left implicit.

My approach could have a weakness, and I should name it. Simply keeping a measure because it lined up with healthy life expectancy would be choosing on the outcome, so the strength of such links would be built in by the very choosing. The same might go for the hotspots.

So I didn’t take those links or gaps at face value. Before reading anything into the largest neighbour gaps, I tested them against what estimate noise alone would produce; 69.8% of neighbouring pairs passed that line, far more than noise explains. I re-ran the rankings 10,000 times within their margins of error, and I say plainly that only 35 of the 66 lowest areas stay in the bottom tenth with confidence. The large differences are real. What they can’t show is cause.

## Association, not cause; areas, not people

The measures are candidates for association with healthy life expectancy. They are not explanations of why a person is healthy, and the area results are not statements about the individuals who live there. These limits remain central to how I describe the work.

## What changes from Unit 2

My Unit 2 ethics account concentrated on privacy. Signal Box found that privacy was the part the project largely handled well: none of its four legal-trigger questions raised a flag. It also surfaced questions about interpretation, certainty, what area averages hide, possible proxy effects in the model, and accountability to people described by the results. Unit 3 widens the ethical frame to include those issues.

Outside readers checked the work too. Before Unit 3, a senior NHS performance analyst looked at my Unit 2 site out of interest and raised two points: that an area’s average can hide a lot of variation inside it, and that small numbers in some areas might explain where my model went wrong. I checked both against the data rather than argue with them. The second didn’t hold. Healthy life expectancy isn’t a survey, and its margins of error are too narrow to produce the big gaps or the model’s misses. The first did, and I now state it as a limit. S11 and S16 look at both questions more closely.

For Unit 3, I sent four independent testers, including him, a link to a guided preview of the site, and they ran it on 20 October 2026. A panel took them through six short tasks, one at a time, and asked whether each was clear. All four rated every task green: 24 out of 24.
