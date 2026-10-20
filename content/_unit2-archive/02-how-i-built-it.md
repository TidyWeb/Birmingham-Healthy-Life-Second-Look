num: 2
slug: how-i-built-it
title: How I built it
summary: Six notebooks in a row, each feeding the next, plus two dashboards and this site.
standfirst: I built the analysis as six Jupyter notebooks that run in order, each one reading what the last one saved.
---
## The pipeline

I split the analysis into six notebooks. Each one does one job and saves its results to its own folder, and then the next notebook picks them up from there. I never type numbers in by hand between them. So if I change something early on, I just run the chain again and every later number updates.

<div class="pipeline" markdown="1">

1. **[Source exploration]({root}notebooks/01-source-exploration.html).** I open the HLE data and look hard at it. I check how my areas compare with the rest of the country, how men and women differ, how precise the estimates are, and how much neighbours differ.
2. **[Data preparation]({root}notebooks/02-data-preparation.html).** I prepare ten more datasets, one at a time. I cut each one down to my 660 areas, keep only the few measures I need, then save the file and check it.
3. **[Joined table and exploration]({root}notebooks/03-joined-table-and-exploration.html).** I join everything into one table, with one row per area, and take a first look at what moves with HLE.
4. **[Hypothesis and neighbour gaps]({root}notebooks/04-hypothesis-and-neighbour-gaps.html).** I test whether the gaps between neighbours are real, and I pick out the biggest ones with a rule I fix in advance.
5. **[Machine learning]({root}notebooks/05-machine-learning.html).** I use clustering and one plain regression, and I test the regression on local authorities it has never seen.
6. **[Hotspots]({root}notebooks/06-hotspots.html).** I zoom in on the five places where the big gaps cluster, check whether the pattern holds inside each council, and run a wide screen of Census characteristics.

</div>

Every notebook overwrites its own outputs each time it runs. I don't keep dated copies, because the data doesn't change, and so a rerun always gives the same answer.

## Extract, transform, load

Most of my ETL happens in Notebook 02. First I extract each source exactly as it's published, whether that's an Excel workbook, a Census zip file, a national pollution grid or 84 monthly police files. Then I transform it. I cut it down to my areas, turn counts into rates and shares, and roll smaller areas up into mine. Finally I load it, which for me means saving a small, checked file keyed on the area code, ready to join. Chapter 4 says more about the transforming.

## The tools

- I wrote the notebooks in **Python**, in Jupyter, running in VS Code on Fedora Linux.
- I used **pandas** for the tables, **GeoPandas** for the boundaries and shared edges, and **NumPy** and **SciPy** for the statistics.
- I used **scikit-learn** for the clustering and the regression.
- I drew the notebook charts with **Matplotlib** and **seaborn**.
- I built the first dashboard in **Tableau Public**, and my own dashboard with **Leaflet**.
- I keep everything in **GitHub**, and this site is served by **GitHub Pages**.

## Two repositories

I keep the notebooks and their data in one GitHub repository, and that's the one the course marks. This site lives in a second, smaller repository that only holds web pages. I build the notebook pages on this site straight from the executed notebooks in the assessment repository, so the two can't drift apart.
