num: S14
part: second-look
slug: lifecycle
title: Lifecycle
summary: How I build, check, update, review and eventually retire this analysis.
standfirst: The results depend on source data and choices that can change. This is how I keep track of that work.
---
::: keypoints
I keep the notebooks, source register, site build and checks together. When a source changes, I re-run the parts that depend on it and review the published result.
:::

## How I look after the work

| Stage | What happens | Who and evidence |
|---|---|---|
| Implementation | I prepare the data and analysis in notebooks 01–08, then build the explanatory pages and dashboard. | I own the work. Git commits, the notebooks, `build_site.py` and the project board record the changes. |
| Maintenance | I check that the site builds from the saved files and that its links still work. | I run `build_site.py` and `check_links.py`; the command output and commits are the record. |
| Updates | I check each source page, note the period and release, then re-run the notebooks that use changed data. | I maintain the source register and this calendar; the notebooks and project board show the work completed. |
| Evaluation | I review the conclusions against the updated outputs, uncertainty and stated limits. | I review notebooks 04–08, the ethics screen, dashboard and link-check results. I record questions and corrections on the project board and in the correction log. |
| Retirement | When a newer HLE release supersedes the 2019–23 estimates, I archive this version and put a banner on the site pointing readers to the newer data. | I make the retirement decision and record it in Git and on the project board. |

## Update calendar

The periods below are the periods in my source register. A source's publication schedule does not automatically change this saved project snapshot. I check the source page before refreshing it.

| Source in the register | Period used here | Publication or update frequency verified on the source page | Notebooks to re-run if the source changes |
|---|---|---|---|
| [Nomis Census 2021 tables](https://www.nomisweb.co.uk/census/2021/bulk) (45 table files) | Census 2021 | Fixed census vintage; the bulk page does not state a routine update cycle. Check the source page for corrections or additional geography files. | 02 → 03 → 05 → 06 → 07; rebuild 08 if its inputs or published interpretation change. |
| [ONS MSOA healthy life expectancy](https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandlifeexpectancies/bulletins/healthstatelifeexpectancyestimatesformiddlelayersuperoutputareasenglandandwales/2019to2023) | 2019–2023 | This release page says the next release date is to be announced. Check the source page. | 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08; then rerun 09 because it uses Notebook 04 neighbour pairs. |
| [DESNZ sub-regional fuel poverty](https://www.gov.uk/government/statistics/sub-regional-fuel-poverty-data-2026-2024-data) | 2024 | Published annually. Check the source page for the next release date. | 02 → 03 → 05 → 06 → 07; rerun 09 for its LSOA distribution and mixed-area comparison. |
| [Defra Pollution Climate Mapping](https://uk-air.defra.gov.uk/data/pcm-data) NO₂ and PM2.5 | 2024 | Defra describes the maps as annual; the page says they are made over summer, checked by autumn and available around mid-October. Check the source page for the next date. | 02 → 03 → 05 → 06 → 07. |
| [ONS MSOA 2021 boundaries, version 3](https://geoportal.statistics.gov.uk/datasets/ons::middle-layer-super-output-areas-december-2021-boundaries-ew-bgc-v3/about) | 2021 geography | A fixed 2021 geography release; no routine update frequency is stated. Check the source page for a newer boundary version. | 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08; then rebuild maps and the dashboard. |
| [ONS 2021 OA–LSOA–MSOA–LAD lookup](https://geoportal.statistics.gov.uk/datasets/ons::output-area-2021-to-lsoa-to-msoa-to-lad-december-2021-exact-fit-lookup-in-ew-v3/about) (7 saved query files) | 2021 geography; LAD fields labelled 2022 | No routine update frequency is stated. Check the source page. | 02 → 03; rerun 09 when the LSOA-to-MSOA mapping changes. Rebuild dependent maps if geography codes change. |
| [ONS Small Area Income Estimates](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/smallareaincomeestimatesformiddlelayersuperoutputareasenglandandwales) | Financial year ending March 2023 | ONS says estimates are published about every two years. Check the source page for the next release date. | 02 → 03 → 05 → 06 → 07. |
| [Police recorded crime](https://data.police.uk/docs/method/crime-last-updated/) | January–December 2024 | The Police API is updated monthly. This project keeps a fixed 2024 period; check the source page when choosing a new period. | 02 → 03 → 05 → 06 → 07. |
| [Food environment assessment tool (Feat)](https://www.feat-tool.org.uk/faq) | June 2023 snapshot; Census 2021 denominator | The Feat FAQ says the tool data are updated monthly. Check the source page for a new snapshot. | 02 → 03 → 05 → 06 → 07. |
| [House of Commons Library MSOA Names](https://houseofcommonslibrary.github.io/msoanames/) | 2021 names, version 2.3, published 13 February 2026 | The page gives a version and publication date but no recurring schedule. Check its source page and change notes. | No analytical notebook. Review labels, then rebuild the dashboard and site if names change. |

## Refresh order

I start by checking the source and updating the source register. Notebook 01 is for source exploration when the HLE source or geography changes. I run Notebook 02 to prepare data, then 03 to rebuild the joined table. Notebook 04 refreshes the HLE neighbour pairs; notebooks 05–08 refresh model, hotspot, fairness and uncertainty results that depend on the changed inputs. Notebook 09 uses fuel poverty, the LSOA-to-MSOA lookup and Notebook 04's neighbour pairs, so I run it after those inputs change. I rebuild the dashboard and site after the analysis is complete.

If only local area names change, I review the labels and rebuild the dashboard and site; I do not rerun an analytical notebook. I keep the project periods explicit rather than silently replacing a fixed snapshot with the latest available data.

## Questions and corrections

Readers can question a page using [Question this work](https://github.com/TidyWeb/Birmingham-Healthy-Life-Second-Look/issues/new?template=question-this-work.yml). I review the question and evidence. If it shows an error, I correct the data, analysis or explanation that caused it and enter the date, page, change and reason in the correction log. If it does not show an error, I explain the evidence and leave the result as it is. Readers can question the work; I make and record corrections.

## Retirement

When ONS publishes a newer HLE release that supersedes 2019–23, I will keep this version identifiable as an archive and add a banner linking to the newer data. I will not silently replace its results with a different period.

## Sources

Publication frequencies were checked against the source pages linked in the calendar on 17 October 2026. Where the page did not give a release date or regular schedule, I have said to check the source page rather than guessing.
