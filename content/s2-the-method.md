num: S2
part: second-look
slug: s2-the-method
title: The method
summary: How I applied Signal Box to an area-level analysis project.
standfirst: I applied Signal Box, the AI ethics check I built for my own Ethical Considerations in AI guide.
---
::: keypoints
I applied Signal Box to the published Unit 2 analysis and to what readers might do with it. A yes is a concern to investigate. A grey lamp means no concern was raised at that question; it doesn’t mean the project is safe to go ahead. Every concern needs a path to resolution: the orange lamp turns yellow only once the concern has been investigated, recorded, and either dealt with or given a safe way forward.
:::

## Where Signal Box comes from {#where-the-screen-comes-from}

I built [Ethical Considerations in AI](https://tidyweb.github.io/ethical-considerations-in-ai/) for fellow students as an independent companion to the Code Institute LMS lesson “Ethical considerations in AI”, drawing on that lesson and my wider research. It is not official Code Institute material. I created [Signal Box: the AI ethics check](https://tidyweb.github.io/ethical-considerations-in-ai/#screening-tool) within the guide; it is Section 11, separate from the guide’s 20-question student pre-project checklist. The guide’s “Sources and boundaries” section separates the LMS capture, independent research and invented examples. Its main sources include UNESCO’s Recommendation on the Ethics of Artificial Intelligence, the OECD AI Principles, NIST’s AI Risk Management Framework, UK GDPR changes under the Data (Use and Access) Act 2025, ICO guidance, and the EU AI Act. The guide records its legal checks as of 14 October 2026.

I wanted a practical checklist that turns ethical principles into specific questions. Signal Box was not part of Unit 2; Unit 3 is my application of it to that project and a practical test of the tool. The report records the evidence and action for each answer, then links concerns to the Unit 3 stages where they need attention.

::: signalbox full
:::

## The six checkpoints

- **A — Purpose and benefit:** what the project is for, and who benefits or may bear a cost.
- **B — Data:** sensitivity, provenance, thin groups and possible proxies.
- **C — Decisions and oversight:** whether the work makes decisions and how those decisions are reviewed.
- **D — People affected:** who is described, who can understand or question the work, and who was involved.
- **E — Safety and robustness:** possible harm, testing, fallback and misuse.
- **F — Responsibility and law:** ownership, supplier limits, legal triggers and where findings apply.

## How to read the lamps

Signal Box asks one thing of each question: **a yes is a concern**. An orange lamp marks a yes, a concern to investigate. A yellow lamp means investigated and recorded; it does not mean the concern has disappeared. A grey lamp means no concern was raised. It does not mean “safe”. A “legal trigger” label (⚖ on the smaller boards) marks a question to check against the relevant law; all four legal-trigger questions in this application had no flag.

Before I turn a lamp yellow, I use the say-it-out-loud test: I must be able to say what could go wrong, who it would happen to, what deals with it, and who is responsible. If I cannot say that in a sentence or two, the lamp stays orange.

Applying Signal Box exposed weaknesses in my own tool: the pop-up did not explain how to clear an orange lamp, the guidance repeated itself, and there was no test for what earned yellow. I fixed those on 19 October 2026; [What changed](what-changed.html#re-testing-the-yellows-out-loud) records what happened when I applied the sharper test to my own answers.

The six checkpoints organise the questions. The stage links identify where each concern meets the project lifecycle: choosing sources, preparing and aggregating, the joined table, hypothesis testing, machine learning, hotspots, or the dashboards and site.

## Applying Signal Box to this project {#applying-an-ai-screen-to-this-project}

The questions were written for AI systems that make decisions about people. Birmingham Healthy Life is an area-level analysis with two simple machine-learning models, published for the public. I treated “the system” as the published project and what readers might do with it. That makes interpretation part of Signal Box, even though the project does not decide anything about an individual.

Some questions do not fit the project. There is no consequential automated decision, no decision workflow for a reviewer to overrule, and no change to jobs or monitoring. The EU AI Act high-risk-use question was checked as a legal trigger; the report records that this UK project was not deployed in the EU and was not in a listed high-risk area. These answers are recorded as not applying or no-flag, not as proof that every part of the work is safe.

## Limits

This is my own Signal Box applied to my own work. It is useful for consistency, but it is not independent; another reviewer should check the concerns. It is also a first pass: some answers rely on the README and site text rather than a fresh review of every notebook cell. The legal triggers were checked against the guide’s 14 October 2026 snapshot, not fresh legal advice.
