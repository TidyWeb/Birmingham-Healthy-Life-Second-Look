num: 12
slug: sources-and-ethics
title: Sources and ethics
summary: Every dataset, the credits, ethics, the AI acknowledgement and how to run the notebooks.
standfirst: Where every number comes from, who I owe, why the data raises no privacy issues, and how you can run it yourself.
---
## Data

All of these are published under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/), unless I say otherwise.

- **Healthy life expectancy:** ONS, [health state life expectancy for MSOAs, 2019 to 2023](https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandlifeexpectancies/bulletins/healthstatelifeexpectancyestimatesformiddlelayersuperoutputareasenglandandwales/2019to2023).
- **Census 2021:** ONS tables TS011 (household deprivation), TS052 (occupancy rating), TS066 (economic activity), TS067 (qualifications), TS021 (ethnic group) and TS007A (population), plus the [Nomis bulk files](https://www.nomisweb.co.uk/sources/census_2021_bulk) I used in the Census screen.
- **Household income:** ONS, [small area income estimates, financial year ending 2023](https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/incomeandwealth/bulletins/smallareamodelbasedincomeestimates/financialyearending2023).
- **Fuel poverty:** Department for Energy Security and Net Zero, sub-regional fuel poverty statistics, 2024.
- **Air pollution:** Defra, [modelled background NO₂ and PM2.5, 2024](https://uk-air.defra.gov.uk/data/pcm-data).
- **Crime:** [Police open data](https://data.police.uk/about/), January to December 2024.
- **Takeaways:** [Food environment assessment tool (FEAT)](https://www.feat-tool.org.uk/), MRC Epidemiology Unit, University of Cambridge, June 2023.
- **Boundaries:** ONS MSOA 2021 boundaries. Contains OS data © Crown copyright and database right.
- **Area names:** House of Commons Library MSOA names, which I adapted, used under the [Open Parliament Licence](https://www.parliament.uk/site-information/copyright-parliament/open-parliament-licence/).
- **Basemap:** © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors.

## Credits

My idea came from [*Lives on the Line*](https://jcheshire.com/featured-maps/lives-on-the-line/) by James Cheshire and Oliver O'Brien.

## Reading

- Michael Marmot and colleagues, [*Fair Society, Healthy Lives: The Marmot Review*](https://www.instituteofhealthequity.org/resources-reports/fair-society-healthy-lives-the-marmot-review) (2010).
- Michael Marmot, Jessica Allen, Tammy Boyce, Peter Goldblatt and Joana Morrison, [*Health Equity in England: The Marmot Review 10 Years On*](https://www.instituteofhealthequity.org/resources-reports/marmot-review-10-years-on), Institute of Health Equity (2020).
- Luis W. Alvarez, Walter Alvarez, Frank Asaro and Helen V. Michel, "Extraterrestrial cause for the Cretaceous-Tertiary extinction", *Science* (1980).

## Ethics

I don't think this project raises any privacy issues, for two reasons.

First, every dataset I use is open, public data, published by the government and public bodies under open licences. I didn't collect any data myself, and I didn't use anything that needed permission or consent to access.

Second, everything is at MSOA level. Each area holds roughly 5,000 to 15,000 residents, and every figure is a total, a rate or an estimate for the whole area. There are no records about individual people anywhere in the project, so there's no way to identify anyone from it. ONS also protects its Census tables against disclosure before publishing them, and the police data is anonymised to approximate locations before it's released.

The one thing I've been careful about is how I describe places. Calling a neighbourhood "unhealthy" could stigmatise the people who live there. So I describe areas and not people, I say links and not causes, and I don't treat any area's figures as a judgement on its residents. I've treated ethnic composition the same way: as a description of who lives in an area, and never as an explanation of anyone's health.

## AI

I used Gemini, Codex and Claude at every stage of this project, from finding data and talking through ideas to writing code and drafting text. The decisions are mine, and so is every check on the numbers. There's more in [How I worked](how-i-worked.html).

## Run it yourself

My notebooks and their data are in the [assessment repository on GitHub](https://github.com/TidyWeb/Code-Institute-DA-with-AI-Unit-2-Assessment). If you want to run them, clone it, create a Python virtual environment, install `requirements.txt`, and run the notebooks in order from 01 to 06. Each one reads what the last one saved and overwrites its own outputs, so a full run reproduces every number on this site.
