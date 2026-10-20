num: S13
part: second-look
slug: law-and-governance
title: Law and governance
summary: What the published figures describe, how I use them, and who is responsible for this work.
standfirst: I use area-level statistics to describe patterns. This page sets out the limits, licences and route for accountability.
---
::: keypoints
I publish area summaries, not records about people. I use the data to describe patterns, not to make decisions about anyone. The work is mine to answer for.
:::

## What the figures describe {#area-data}

The published figures are summaries for Middle Layer Super Output Areas (MSOAs). The Office for National Statistics describes an MSOA as having a usually resident population of about 5,000 to 15,000. I publish no person-level records. UK GDPR defines personal data by whether information relates to an identified or identifiable person, so I consider these area summaries not to be personal data on their own. This is my reading of the published data and [the legal definition](https://www.legislation.gov.uk/eur/2016/679/article/4/2026-09-30). [ONS describes MSOA population sizes](https://www.ons.gov.uk/methodology/geography/ukgeographies/censusgeographies/census2021geographies).

That assessment could change if I published very small groups, combined layers that made a person identifiable, or moved to a finer geography. I use six broad ethnic groups rather than the 19 narrower categories in the source table. That choice reduces the chance of describing a small group, but it does not make every possible disclosure risk disappear.

## Health and ethnicity

UK GDPR lists personal data revealing racial or ethnic origin and data concerning health as special categories. Here I publish area shares and area estimates, not a person's ethnic origin or health record. The care still matters at group level: an area pattern can be misread as a claim about every person in that area. I describe associations, not causes, and areas, not people. [UK GDPR Article 9](https://www.legislation.gov.uk/eur/2016/679/article/9).

## Automated decisions {#automated-decisions}

My k-means clustering and linear regression describe area-level patterns. I do not deploy them to make or support a decision about a person. Section 80 of the [Data (Use and Access) Act 2025](https://www.legislation.gov.uk/ukpga/2025/18/section/80) replaced UK GDPR Article 22 with Articles 22A–22D, which address automated decisions about data subjects and safeguards for significant decisions based solely on automated processing. As this project makes no decision about any person, I do not consider those automated-decision safeguards engaged here.

## EU Artificial Intelligence Act {#eu-ai-act}

Article 2 of the [EU Artificial Intelligence Act](https://eur-lex.europa.eu/eli/reg/2024/1689/2026-07-27/eng) includes providers placing or putting AI systems into service on the EU market, EU-based deployers, and providers or deployers outside the EU where the system's output is used in the EU. The scope can therefore reach beyond the EU. This is a UK analysis published as an explanatory website, not an AI product or service offered to people in the EU. I have not identified an EU deployment or meaningful use of this project's output in the EU.

Annex III, read with Article 6(2), lists high-risk use areas. This analysis falls in none of them, and it makes no decision about an individual. The models describe area-level patterns; they are not deployed to make or support decisions about people.

On that basis I don't consider the Act's obligations engaged; this is my reading, not legal advice.

## Equality and use

I use the ethnicity analysis descriptively and do not use it to target or exclude anyone. The [Equality Act 2010, section 9](https://www.legislation.gov.uk/ukpga/2010/15/section/9) identifies race as a protected characteristic and includes ethnic or national origins. My analysis does not make a legal finding about any person or organisation.

### Excluded uses {#excluded-uses}

This work is not for:

- judging or targeting individuals;
- insurance, credit or pricing decisions;
- property marketing;
- claims about the health of ethnic groups;
- generalising the results to other places.

Before I reuse this work for any new purpose, I run Signal Box from my own [Ethical Considerations in AI](https://tidyweb.github.io/ethical-considerations-in-ai/) guide again; [The method](s2-the-method.html) explains how I apply it. The data and site are public, so I cannot prevent others’ reuse or misuse; I can only refuse those uses in my own work and make the limits plain.

Legal permission to reuse data is not the same as appropriate use. A licence tells me how source material may be reused; I remain responsible for describing it accurately, explaining its limits and correcting errors.

## Licences and attribution

| Material | Reuse and credit |
|---|---|
| ONS, Nomis, DESNZ and Defra data | Open Government Licence v3.0. I credit the source as recorded in the [source register](https://github.com/TidyWeb/Code-Institute-DA-with-AI-Unit-3-Assessment/blob/main/data/source-register.csv). Defra's pollution maps also require: “© Crown copyright 2021 Defra via uk-air.defra.gov.uk”. [OGL v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). |
| MSOA names from the House of Commons Library | Open Parliament Licence. I acknowledge the House of Commons Library and link to the [Open Parliament Licence](https://www.parliament.uk/site-information/copyright-parliament/open-parliament-licence/). |
| Food environment assessment tool (Feat) | Cite: *Food environment assessment tool (Feat) 2023, MRC Epidemiology Unit, University of Cambridge*. The [Feat FAQ](https://www.feat-tool.org.uk/faq) requests this citation and gives its reuse terms. |
| MSOA boundaries and map tiles | For the boundaries: “Contains OS data © Crown copyright and database right 2021.” For map tiles: “© OpenStreetMap contributors”, linked to [OpenStreetMap copyright](https://www.openstreetmap.org/copyright). |

## Who answers for it {#accountability}

I am Phil (Tidy Web), the owner of this work. Readers can question it through [Question this work](https://github.com/TidyWeb/Birmingham-Healthy-Life-Second-Look/issues/new?template=question-this-work.yml). I decide whether a correction is needed, make it, and log what changed and why.
