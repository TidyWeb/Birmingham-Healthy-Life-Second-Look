<!-- DRAFT: Phil to rewrite in his own words -->
num: S18
part: second-look
slug: reflection
title: Reflection
summary: What I missed, what the audits found, and what I learned while rebuilding the project.
standfirst: What I have learned from this ethics first look at my Birmingham Healthy Life project, and how this ethical audit has changed my understanding, and improved the work.
---
::: keypoints
I started Unit 2 - Birmingham Healthy Life by thinking about ethics mainly from the standpoint of privacy. Clearly, dealing with health data involves protecting personal information, but it also involves ensuring that the data is used responsibly and ethically. The re-screen and the audits I ran here made me look at uncertainty, proxy overlap, model error, stigmatisation, aggregation and accountability as well.
:::

## What I missed in Unit 2

In Unit 2 I treated ethics mainly as a privacy question. The 27-question screen I built did not find a legal-trigger concern, but it found other issues I had not written down: false certainty, possible proxy effects in the model, how area patterns might be read as claims about people, and how someone could question the work. Privacy was just one part of the review, not the whole of it.

The audits gave me results I needed to state plainly. The seven model features predicted area-level household deprivation with an R² of 0.898, and their overlap with the six broad ethnicity shares varied. The error audit found a direction difference across deprivation thirds: in the least-deprived third the model ran low by about 0.31 years, while in the most-deprived third it ran high by about 0.46 years; both bootstrap intervals excluded zero. That is a result about area-level predictions, not a description of any resident.

Notebook 08 also changed how I describe the lowest estimates. Of the 66 areas with the lowest published HLE values, 35 had at least a 95% simulated chance of staying in the bottom tenth. The other 31 did not meet that threshold. A rank on its own looked firmer than the uncertainty allowed.

Notebook 09 showed why an MSOA average can hide variation inside it. Across the 3,205 LSOA fuel-poverty percentages, 30.3% of the variance was within MSOAs and 69.7% was between LSOA-count-weighted MSOA means. That does not tell me why the LSOAs differ, but it shows what the larger-area mean leaves out.

## A method I had to correct

I first compared an MSOA's internal LSOA range with a difference between neighbouring MSOA means. Those are not like-for-like quantities, and that rule marked 581 of 660 areas. I replaced it with a range-versus-range comparison: the internal LSOA range against the range of means across that MSOA and its Notebook 04 neighbours. The revised descriptive rule flags 255 of 660. The change matters because a large count from a mismatched comparison can sound like a strong finding even when the rule itself is poorly matched.

An earlier draft also got the screen count wrong: it said 16 concerns and 11 no-flags, instead of the source screen's 17 and 10. I corrected it against the screen data. I need to check counts against the underlying output, not trust a sentence because it reads smoothly.

## The position I reached

My stance came from argument, not from applying a sentence I had been handed. I went back and forth over respect, the risk of causing offence, and the risk of hiding an uncomfortable result. I came back to accuracy: the claim should be as strong as the evidence, no stronger and no weaker. I cannot control every reader's interpretation. I am responsible for what I claim and how firmly I claim it.

## Working with AI

AI sped up planning, notebook code, checking and first drafts. It also made mistakes that I had to catch. Work split across staging and working clones, so it became harder to see which changes were already pushed and which copy was current. The early 16/11 count was wrong. The first aggregation flag compared unlike quantities and produced 581/660. Those are reasons I had to keep a firm hand on the work: check the source, check the method, and verify the numbers against the saved outputs. The tools helped produce drafts; they did not decide what the evidence could support.

## What I would do next

User testing is complete: on 20 October 2026, three testers rated every task green on the Detailed view and story pages. I need to rewrite this draft in my own words, then hand-edit and audit the final language. After that I can review the complete site, make the final site commit and push it, and check the published pages again. Until those steps are done, I should not present the project as fully finished.
