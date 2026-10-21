num: S18
part: second-look
slug: how-i-used-ai
title: How I used AI
summary: Where AI helped, where I kept control, and the rules that came from things going wrong.
standfirst: Where AI helped, where I kept control, and the rules that came from things going wrong.
---
::: keypoints
AI made me faster at almost every stage, from finding the data to pushing the work to GitHub. I did the thinking and made the decisions, and every result was checked before I relied on it. The tools needed continual oversight, not blind faith.
:::

I used AI throughout this project, in different ways at different stages, and I want to be open about how. What follows is a general picture rather than a log of every conversation, but it's an honest one.

I chose the questions and sources, made the methodological decisions, reran the analysis, checked numbers against the saved outputs and corrected errors. I am responsible for the final claims and wording.

The project started in Unit 2, and it started with a search. I used Google Gemini, and in particular a specialist data Gem I built for the job, to help me find and weigh up datasets. I wanted something that mattered in the Midlands, that was recent, and that I was free to use. It was a long process before we landed on the ONS healthy life expectancy figures for small areas, which were recent and published under an open licence. From there I used Claude for conceptual conversations: what could this data tell me, what other datasets could add context and richness to what I saw in the HLE data, and how might I use them?

The structure of the analysis was mine. I went out and found the other datasets, and I designed the schema: healthy life expectancy at MSOA level as the master data frame, with supplementary datasets brought in because they might tell us more about the differences the healthy life expectancy figures were showing. I didn't want the full width and breadth of those datasets, so I picked out the key elements, reduced each one down, and joined them all to the master table. That was Unit 2, and it's the foundation this project stands on.

Unit 3 worked differently. It was Claude first, and far more conceptual. Claude was my main conversation partner for the ethical lens: what we should really be thinking about, what could go wrong, and how to approach it. Gemini played a smaller part. Between us we worked out a plan for the whole project. I did the thinking and made the decisions; Claude turned them into precise prompts for Codex, which did most of the coding and building. Claude also checked Codex's work against the actual files, figures and pages, then I applied my manual review before I relied on any of it. Nothing went live until I'd seen it and approved it. Anything visible came to me as a preview first.

The part I most want to explain is GitHub. I built a skill for Codex that commits and pushes to GitHub for me and checks the result. This connects to something I made earlier: a [Git and GitHub guide](https://tidyweb.github.io/git_and_github/) for my fellow students, which a couple of them have used and thanked me for. I know how Git works. But connecting Codex to GitHub through a skill I wrote, with its own guardrails, is far more efficient than going into a terminal for every commit. It pushes only the commits I've approved, one piece of work at a time, and checks that the live site matches afterwards. I think that's exactly the kind of job an AI tool should do: specific, repetitive, guarded, and easy to check.

Using AI this way takes a keen eye and firm hand, and some of my rules came from things going wrong. AI can automate a lot of tedious processes but it requires continual oversight, not blind faith that it has done what it reports it has done.  An agent once sent an email to Code Institute I hadn't approved, so now the rule is no AI agent or tool sends anything on my behalf wihtout my express permission. Work got scattered across copies of the same repository as I explored and built different iterations, now there's one working copy. And every number gets checked against the output, however good the sentence around it sounds. The tools made me faster. The thinking, the decisions and the responsibility stayed mine.
