num: S2
part: second-look
slug: s2-the-method
title: The method
summary: How I applied my 27-question screen to an area-level analysis project.
standfirst: I used the questions from my own AI-ethics guide as a first-pass screen of the published project.
---
::: keypoints
I applied a 27-question screen from my own AI-ethics guide to the published analysis and what readers might do with it. A yes is a concern to investigate; a grey lamp means no concern was raised, not that the project is safe.
:::

## Where the screen comes from {#where-the-screen-comes-from}

I built this 27-question screen as part of my independent [AI Ethics: a practical overview](https://tidyweb.github.io/ethical-considerations-in-ai/) study guide. I drew on the Code Institute LMS lesson “Ethical considerations in AI” and my wider research. The guide’s “Sources and boundaries” section separates the LMS capture, independent research and invented examples. Its main sources include UNESCO’s Recommendation on the Ethics of Artificial Intelligence, the OECD AI Principles, NIST’s AI Risk Management Framework, UK GDPR changes under the Data (Use and Access) Act 2025, ICO guidance, and the EU AI Act. The guide records its legal checks as of 14 October 2026.

I wanted a practical checklist that turns ethical principles into specific questions. The screen was not part of Unit 2; Unit 3 is the first time I have applied it to a real data project. The report records the evidence and action for each answer, then links concerns to the Unit 3 stages where they need attention.

::: image second-look/checkpoint-flow.svg
alt: Six checkpoints run from A through F. The concern counts beneath them are 4, 4, 1, 3, 4 and 1. The flow ends with an owner decision: proceed, narrow, redesign or stop.
caption: The six checkpoints lead to an owner decision. The number below each letter is the concern count recorded in the screen.
:::

## The six checkpoints

- **A — Purpose and benefit:** what the project is for, and who benefits or may bear a cost.
- **B — Data:** sensitivity, provenance, thin groups and possible proxies.
- **C — Decisions and oversight:** whether the work makes decisions and how those decisions are reviewed.
- **D — People affected:** who is described, who can understand or question the work, and who was involved.
- **E — Safety and robustness:** possible harm, testing, fallback and misuse.
- **F — Responsibility and law:** ownership, supplier limits, legal triggers and where findings apply.

## How to read the lamps

The screen asks one thing of each question: **a yes is a concern**. An orange lamp marks a yes. A grey, hollow lamp means no concern was raised. It does not mean “safe”. A ⚖ mark identifies a legal-trigger question to check against the relevant law; all four legal-trigger questions in this screen had no flag.

The six checkpoints organise the questions. The stage links identify where each concern meets the project lifecycle: choosing sources, preparing and aggregating, the joined table, hypothesis testing, machine learning, hotspots, or the dashboards and site.

## Applying an AI screen to this project

The questions were written for AI systems that make decisions about people. Birmingham Healthy Life is an area-level analysis with two simple machine-learning models, published for the public. I treated “the system” as the published project and what readers might do with it. That makes interpretation part of the screen, even though the project does not decide anything about an individual.

Some questions do not fit the project. There is no consequential automated decision, no decision workflow for a reviewer to overrule, and no change to jobs or monitoring. The EU AI Act high-risk-use question was checked as a legal trigger; the report records that this UK project was not deployed in the EU and was not in a listed high-risk area. These answers are recorded as not applying or no-flag, not as proof that every part of the work is safe.

## Limits

This is my own screen applied to my own work. It is useful for consistency, but it is not independent; another reviewer should check the concerns. It is also a first pass: some answers rely on the README and site text rather than a fresh review of every notebook cell. The legal triggers were checked against the guide’s 14 October 2026 snapshot, not fresh legal advice.
