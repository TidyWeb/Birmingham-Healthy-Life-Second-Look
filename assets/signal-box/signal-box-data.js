window.SBX_DATA = {
 "groups": [
  {
   "id": "A",
   "name": "Purpose and benefit",
   "qs": [
    {
     "n": 1,
     "g": "A",
     "q": "Will it make or shape a decision that matters to someone's life: work, money, care, safety, liberty?",
     "legal": false,
     "lamp": "y",
     "before": "o",
     "stages": [
      "S7"
     ],
     "evidence": [
      "No decisions about individuals. But the stated audience is \"the public and professionals\", and maps of named places can shape where people buy, how councils see places, or what the press writes. Indirect.",
      "Unit 3 check: The site explains the intended descriptive use and the limits on decisions about people."
     ],
     "action": "State the intended use and what it is not for.",
     "where": {
      "href": "stage-7-dashboards-and-site.html#recorded-responses",
      "label": "Stage 7: Dashboards and site",
      "ext": false
     }
    },
    {
     "n": 2,
     "g": "A",
     "q": "Could a simpler non-AI process do the job?",
     "legal": false,
     "lamp": "y",
     "before": "o",
     "stages": [
      "S5"
     ],
     "evidence": [
      "Most findings come from descriptive stats, Notebook 04's noise test and Moran's I. The ML (k-means plus one linear regression) adds an \"explained share\" figure but isn't needed for the core story.",
      "Unit 3 check: The site explains why the two models sit alongside simpler descriptive analysis."
     ],
     "action": "Record why ML is there (it estimates how much of the pattern the measures explain) and that it informs nothing about individuals.",
     "where": {
      "href": "stage-5-machine-learning.html",
      "label": "Stage 5: Machine learning",
      "ext": false
     }
    },
    {
     "n": 3,
     "g": "A",
     "q": "Is the purpose vague, or likely to grow beyond what was agreed?",
     "legal": false,
     "lamp": "y",
     "before": "o",
     "stages": [
      "S7"
     ],
     "evidence": [
      "Purpose is clear (where HLE differs and what lines up with it), but there are no excluded uses written down.",
      "Unit 3 check: The site lists excluded uses, including decisions about individuals and property marketing."
     ],
     "action": "Add \"not for\": targeting individuals, insurance or credit, property marketing, or claims about ethnic groups.",
     "where": {
      "href": "law-and-governance.html#excluded-uses",
      "label": "Law and governance",
      "ext": false
     }
    },
    {
     "n": 4,
     "g": "A",
     "q": "Does most of the benefit go to the organisation while the cost falls on others?",
     "legal": false,
     "lamp": "o",
     "before": "o",
     "stages": [
      "S7"
     ],
     "evidence": [
      "The benefit goes mainly to me (assessment, portfolio). Any cost falls on residents of low-HLE areas through stigma, and they had no say.",
      "Settled by executive decision: I accept this cost as the price of describing the differences honestly. Banding, certainty labels and a naming policy keep it down."
     ],
     "action": "A cui bono / cui damno card on the site, and harm-reducing presentation (banding, certainty, naming policy).",
     "where": {
      "href": "stage-7-dashboards-and-site.html#recorded-responses",
      "label": "Stage 7: Dashboards and site",
      "ext": false
     }
    }
   ]
  },
  {
   "id": "B",
   "name": "Data",
   "qs": [
    {
     "n": 5,
     "g": "B",
     "q": "Does it collect or use information about identifiable people?",
     "legal": true,
     "lamp": "g",
     "before": "g",
     "stages": [
      "S2"
     ],
     "evidence": [
      "All outputs are MSOA aggregates (about 5,000–15,000 residents). The police data is incident records snapped to approximate locations and was rolled up to rates.",
      "Unit 3 check: Unit 3 still publishes MSOA area summaries and no person-level records."
     ],
     "action": "Record the reasoning. Note that the raw crime rows are incidents, not people, and are never published at point level.",
     "where": {
      "href": "law-and-governance.html#area-data",
      "label": "Law and governance",
      "ext": false
     }
    },
    {
     "n": 6,
     "g": "B",
     "q": "Is that information used automatically to evaluate or predict something about someone (profiling)?",
     "legal": true,
     "lamp": "g",
     "before": "g",
     "stages": [
      "S2"
     ],
     "evidence": [
      "The models predict area values, not personal ones.",
      "Unit 3 check: Unit 3 says the models describe area patterns and are not used to decide about people."
     ],
     "action": "Say so plainly. Warn against reading area results as statements about residents (ecological fallacy).",
     "where": {
      "href": "law-and-governance.html#automated-decisions",
      "label": "Law and governance",
      "ext": false
     }
    },
    {
     "n": 7,
     "g": "B",
     "q": "Does it use sensitive data (health, ethnicity, biometrics, religion, sexuality) or a stand-in for it, like a postcode?",
     "legal": false,
     "lamp": "y",
     "before": "o",
     "stages": [
      "S3",
      "S5"
     ],
     "evidence": [
      "Yes: health (HLE) and 17 ethnicity-share columns. Income, qualifications and employment are plausible proxies. Notebook 05 excludes ethnicity and deprivation from the features, but proxy leakage is untested.",
      "Unit 3 check: Notebook 07 tests overlap between model features, ethnic composition and deprivation."
     ],
     "action": "Run the proxy test.",
     "where": {
      "href": "proxies-fairness-and-crime.html#proxy-overlap",
      "label": "Proxies, fairness and crime",
      "ext": false
     }
    },
    {
     "n": 8,
     "g": "B",
     "q": "Could people be re-identified by combining fields, even with names removed?",
     "legal": false,
     "lamp": "y",
     "before": "o",
     "stages": [
      "S3"
     ],
     "evidence": [
      "Some ethnicity shares are tiny: Gypsy or Irish Traveller is below 0.5% in 646 of 660 areas, and the smallest non-zero is 0.007%, which is likely only one or a few people in an area. Census disclosure control applies, but showing these beside health and crime on a public map singles out very small communities.",
      "Unit 3 check: The public site uses six broad ethnic groups and explains the remaining disclosure limits."
     ],
     "action": "The analysis already uses six aggregated groups in Notebook 06, because tiny groups don't serve the purpose of testing broad cultural differences. Housekeeping: publish the six-group table, not the 17-column one, and state why. (Decision, 16 Oct.)",
     "where": {
      "href": "law-and-governance.html#area-data",
      "label": "Law and governance",
      "ext": false
     }
    },
    {
     "n": 9,
     "g": "B",
     "q": "Is any data's origin, accuracy or permission to use unknown?",
     "legal": false,
     "lamp": "g",
     "before": "g",
     "stages": [
      "S1"
     ],
     "evidence": [
      "The source register records the URL, period, geography, SHA-256 and licence note for every file. Accuracy limits are known (9 male HLE values imputed; estimate intervals carried).",
      "Unit 3 check: The source register and S4 record source pages, periods, geographies, file hashes, licence notes and known limits."
     ],
     "action": "Add a \"known limits\" column to the register.",
     "where": {
      "href": "s4-stage-1-choosing-sources.html#modelled-inputs",
      "label": "Stage 1: Choosing sources",
      "ext": false
     }
    },
    {
     "n": 10,
     "g": "B",
     "q": "Are some groups missing or thin in the data?",
     "legal": false,
     "lamp": "y",
     "before": "o",
     "stages": [
      "S2"
     ],
     "evidence": [
      "Thin ethnic groups (see Q8). MSOA averaging hides within-area inequality. 6 student-dominated and 6 visitor-hub areas are flagged as unusual.",
      "Unit 3 check: Notebook 09 describes variation among LSOA fuel-poverty percentages within MSOAs."
     ],
     "action": "Within-area spread check, and state who is under-represented.",
     "where": {
      "href": "what-aggregation-hides.html#aggregation",
      "label": "What aggregation hides",
      "ext": false
     }
    },
    {
     "n": 11,
     "g": "B",
     "q": "Is the system learning from past human decisions, such as who was hired before?",
     "legal": false,
     "lamp": "y",
     "before": "o",
     "stages": [
      "S3",
      "S5"
     ],
     "evidence": [
      "The target (HLE) is survey plus mortality data, not a human decision. But crime_for_analysis is a model feature, and recorded crime reflects policing and reporting decisions.",
      "Unit 3 check: Notebook 07 compares the model with and without recorded crime, and its discussion notes policing and reporting limits."
     ],
     "action": "Crime sensitivity test, plus a caveat on every crime view.",
     "where": {
      "href": "proxies-fairness-and-crime.html#crime-sensitivity",
      "label": "Proxies, fairness and crime",
      "ext": false
     }
    }
   ]
  },
  {
   "id": "C",
   "name": "Decisions and oversight",
   "qs": [
    {
     "n": 12,
     "g": "C",
     "q": "Is a consequential decision made without meaningful human involvement (solely automated)?",
     "legal": true,
     "lamp": "g",
     "before": "g",
     "stages": [
      "S7"
     ],
     "evidence": [
      "No decisions are made about anyone.",
      "Unit 3 check: The site confirms that no consequential decisions are automated."
     ],
     "action": "None. Note that the UK GDPR automated-decision safeguards don't apply.",
     "where": {
      "href": "law-and-governance.html#automated-decisions",
      "label": "Law and governance",
      "ext": false
     }
    },
    {
     "n": 13,
     "g": "C",
     "q": "Would a human reviewer lack the time, information or authority to overrule it?",
     "legal": false,
     "lamp": "g",
     "before": "g",
     "stages": [
      "S7"
     ],
     "evidence": [
      "There is no decision workflow to review.",
      "Unit 3 check: The site confirms that there is no decision workflow for a reviewer to overrule."
     ],
     "action": "None.",
     "where": {
      "href": "law-and-governance.html#automated-decisions",
      "label": "Law and governance",
      "ext": false
     }
    },
    {
     "n": 14,
     "g": "C",
     "q": "Is the output likely to be treated as proof rather than a prompt (automation bias)?",
     "legal": false,
     "lamp": "y",
     "before": "o",
     "stages": [
      "S4",
      "S6",
      "S7"
     ],
     "evidence": [
      "Single HLE values and rankings (\"ranks every area\") look precise. The average 95% interval is about 2.1 years wide, up to 5.2 years. Mid-table ranks are likely unstable. The residual map can read as places that \"underperform\".",
      "Unit 3 check: S11 reports rank intervals and confidence bands and explains their limits."
     ],
     "action": "Show rank intervals by default, label maps as estimates, and reword the residual map.",
     "where": {
      "href": "how-certain-are-the-rankings.html#uncertainty-response",
      "label": "How certain are the rankings?",
      "ext": false
     }
    }
   ]
  },
  {
   "id": "D",
   "name": "People affected",
   "qs": [
    {
     "n": 15,
     "g": "D",
     "q": "Could errors fall more heavily on some groups than others?",
     "legal": false,
     "lamp": "y",
     "before": "o",
     "stages": [
      "S5"
     ],
     "evidence": [
      "Notebook 05 reports residual Moran's I (0.154) overall but never breaks error down by community or deprivation level.",
      "Unit 3 check: Notebook 07 compares model errors across deprivation and ethnic-composition thirds."
     ],
     "action": "An error-parity audit by ethnic-composition and deprivation thirds.",
     "where": {
      "href": "proxies-fairness-and-crime.html#error-parity",
      "label": "Proxies, fairness and crime",
      "ext": false
     }
    },
    {
     "n": 16,
     "g": "D",
     "q": "Could people be affected without knowing AI was involved?",
     "legal": false,
     "lamp": "g",
     "before": "g",
     "stages": [
      "S7"
     ],
     "evidence": [
      "AI use is disclosed on the site and in the README. (Residents don't know the analysis exists, but that's Q17/Q18.)",
      "Unit 3 check: The site says AI use is disclosed and explains that Phil makes the project decisions and checks."
     ],
     "action": "Keep, and expand the AI statement with a log of checks I made by hand.",
     "where": {
      "href": "stage-7-dashboards-and-site.html#screen-findings",
      "label": "Stage 7: Dashboards and site",
      "ext": false
     }
    },
    {
     "n": 17,
     "g": "D",
     "q": "Would an affected person be unable to understand, correct or challenge the result?",
     "legal": false,
     "lamp": "y",
     "before": "o",
     "stages": [
      "S7"
     ],
     "evidence": [
      "There's no route for anyone to question how their area is described. No contact point or issue link on the site.",
      "Unit 3 check: A public question form and correction route are documented; GitHub sign-in is now stated in S15."
     ],
     "action": "Add a transparent, public route to question the work (a GitHub issue template). Readers don't edit it: the work is mine. Where a question exposes a real error, I correct it and log it publicly. (Decision, 16 Oct.)",
     "where": {
      "href": "stage-7-dashboards-and-site.html#recorded-responses",
      "label": "Stage 7: Dashboards and site",
      "ext": false
     }
    },
    {
     "n": 18,
     "g": "D",
     "q": "Were the people affected left out of design and testing?",
     "legal": false,
     "lamp": "o",
     "before": "o",
     "stages": [
      "S7"
     ],
     "evidence": [
      "Settled by executive decision. The study covers 660 areas and several million people. There is no practical way to involve them, and publishing area-level statistics does not need their consent.",
      "User testing with three Birmingham readers adds evidence, but it does not close this concern."
     ],
     "action": "User testing with at least one non-technical local reader; record what changed. Name the limit honestly.",
     "where": {
      "href": "what-changed.html#user-testing",
      "label": "What changed",
      "ext": false
     }
    },
    {
     "n": 19,
     "g": "D",
     "q": "Does it change anyone's job, pace of work or level of monitoring?",
     "legal": false,
     "lamp": "g",
     "before": "g",
     "stages": [
      "S7"
     ],
     "evidence": [
      "Not applicable.",
      "Unit 3 check: The site records that the project does not change jobs or monitor staff."
     ],
     "action": "None.",
     "where": {
      "href": "stage-7-dashboards-and-site.html#screen-findings",
      "label": "Stage 7: Dashboards and site",
      "ext": false
     }
    }
   ]
  },
  {
   "id": "E",
   "name": "Safety and robustness",
   "qs": [
    {
     "n": 20,
     "g": "E",
     "q": "Could a failure cause physical or psychological harm?",
     "legal": false,
     "lamp": "y",
     "before": "o",
     "stages": [
      "S7"
     ],
     "evidence": [
      "No physical risk. A misread map could cause distress or reputational harm to places and communities.",
      "Unit 3 check: The site records the risk of misreading area maps and carries uncertainty and use caveats."
     ],
     "action": "Covered by the Q4/Q14 fixes; state it as a risk in the register.",
     "where": {
      "href": "stage-7-dashboards-and-site.html#recorded-responses",
      "label": "Stage 7: Dashboards and site",
      "ext": false
     }
    },
    {
     "n": 21,
     "g": "E",
     "q": "Has it only been tested in a demo or lab, not the real setting?",
     "legal": false,
     "lamp": "o",
     "before": "o",
     "stages": [
      "S7"
     ],
     "evidence": [
      "Settled by executive decision. This is a course project built for assessment, not for real use, so it will not be tested in real use.",
      "User testing with three Birmingham readers checks that the site can be understood; that is not real use."
     ],
     "action": "User testing (also handbook evidence for LO2.2).",
     "where": {
      "href": "what-changed.html#user-testing",
      "label": "What changed",
      "ext": false
     }
    },
    {
     "n": 22,
     "g": "E",
     "q": "Is there no tested way to pause it, override it or switch to a manual fallback?",
     "legal": false,
     "lamp": "y",
     "before": "o",
     "stages": [
      "S7"
     ],
     "evidence": [
      "It's a static site, so it can be taken down. But there's no written correction, takedown or archive procedure.",
      "Unit 3 check: S14 records how I check questions, correct errors, keep a correction log and retire or archive an old version."
     ],
     "action": "Write a correction and retirement policy (lifecycle).",
     "where": {
      "href": "lifecycle.html#correction-route",
      "label": "Lifecycle",
      "ext": false
     }
    },
    {
     "n": 23,
     "g": "E",
     "q": "Could it be attacked, misused or used outside its intended purpose?",
     "legal": false,
     "lamp": "y",
     "before": "o",
     "stages": [
      "S3",
      "S7"
     ],
     "evidence": [
      "Public tables and maps combining ethnicity, crime, takeaways and health could be lifted for property marketing, insurance profiling or divisive narratives.",
      "Unit 3 check: S13 lists excluded uses and S12 keeps the crime and ethnicity findings descriptive."
     ],
     "action": "Excluded-uses statement, suppress small groups, caveats travel with the figures, no single \"worst places\" list.",
     "where": {
      "href": "law-and-governance.html#excluded-uses",
      "label": "Law and governance",
      "ext": false
     }
    }
   ]
  },
  {
   "id": "F",
   "name": "Responsibility and law",
   "qs": [
    {
     "n": 24,
     "g": "F",
     "q": "Is there no named person who owns it, monitors it and can stop it?",
     "legal": false,
     "lamp": "g",
     "before": "g",
     "stages": [
      "S7"
     ],
     "evidence": [
      "I'm named as owner (Tidy Web). The gap is monitoring: no review cadence.",
      "Unit 3 check: S13 names Phil as owner and describes responsibility for questions and corrections."
     ],
     "action": "Add an owner, monitor and review-date line to the README.",
     "where": {
      "href": "law-and-governance.html#accountability",
      "label": "Law and governance",
      "ext": false
     }
    },
    {
     "n": 25,
     "g": "F",
     "q": "Does it depend on a supplier's model, data or updates you can't inspect?",
     "legal": false,
     "lamp": "y",
     "before": "o",
     "stages": [
      "S1"
     ],
     "evidence": [
      "Several inputs are modelled estimates I can't reproduce: ONS HLE (with imputation), ONS small-area income, DESNZ fuel poverty, Defra PCM pollution. They're also subject to revision. Code was co-written with Codex.",
      "Unit 3 check: S4 marks the source estimates that are modelled, describes their limits and records revision risk."
     ],
     "action": "Mark modelled inputs in the register and on the site, state the revision risk, and keep the record of human checks on AI-written code.",
     "where": {
      "href": "s4-stage-1-choosing-sources.html#modelled-inputs",
      "label": "Stage 1: Choosing sources",
      "ext": false
     }
    },
    {
     "n": 26,
     "g": "F",
     "q": "Does the EU AI Act class its intended use as high-risk?",
     "legal": true,
     "lamp": "g",
     "before": "g",
     "stages": [
      "S7"
     ],
     "evidence": [
      "UK data, a UK audience, not deployed in the EU, and not in a listed high-risk area.",
      "Unit 3 check: S13 records the Article 2 scope check and the Article 6 and Annex III high-risk-use check."
     ],
     "action": "Record the check.",
     "where": {
      "href": "law-and-governance.html#eu-ai-act",
      "label": "Law and governance",
      "ext": false
     }
    },
    {
     "n": 27,
     "g": "F",
     "q": "Will it be used in a different country, population or language from the one it was built for?",
     "legal": false,
     "lamp": "g",
     "before": "g",
     "stages": [
      "S7"
     ],
     "evidence": [
      "Built for the Birmingham area. Findings shouldn't be generalised to other areas.",
      "Unit 3 check: S13 says the work is for Birmingham and should not be generalised to other places."
     ],
     "action": "One line warning against generalising.",
     "where": {
      "href": "law-and-governance.html#excluded-uses",
      "label": "Law and governance",
      "ext": false
     }
    }
   ]
  }
 ],
 "decision": {
  "intro": "I've published with three concerns settled by executive decision. I looked at each one and decided to go ahead anyway; this is why.",
  "items": [
   {
    "n": 4,
    "title": "Q4. The benefit is mine; any cost falls on others.",
    "text": "If anyone pays a cost it's the people living in the areas with the fewest years in good health, through stigma. I accept that as the cost of trying to get to the truth about these differences, and I've kept it down with broad labels, honest uncertainty and a policy on naming places.",
    "g": "A"
   },
   {
    "n": 18,
    "title": "Q18. The people affected weren't involved.",
    "text": "The study covers 660 areas and several million people. There's no practical way to involve them all, and publishing area-level statistics doesn't need their permission. Three Birmingham readers are testing the site, which helps, but three people can't speak for everyone.",
    "g": "D"
   },
   {
    "n": 21,
    "title": "Q21. It hasn't been tested in real use.",
    "text": "This is a course project, built to be assessed, not for anyone to rely on. It won't ever be used for real, so this lamp can't honestly turn yellow.",
    "g": "E"
   }
  ]
 },
 "stages": [
  {
   "id": "S1",
   "href": "s4-stage-1-choosing-sources.html",
   "title": "Stage 1: Choosing sources"
  },
  {
   "id": "S2",
   "href": "stage-2-preparing-and-aggregating.html",
   "title": "Stage 2: Preparing and aggregating"
  },
  {
   "id": "S3",
   "href": "stage-3-joined-table.html",
   "title": "Stage 3: The joined table"
  },
  {
   "id": "S4",
   "href": "stage-4-hypothesis-test.html",
   "title": "Stage 4: The hypothesis test"
  },
  {
   "id": "S5",
   "href": "stage-5-machine-learning.html",
   "title": "Stage 5: Machine learning"
  },
  {
   "id": "S6",
   "href": "stage-6-hotspots.html",
   "title": "Stage 6: Hotspots"
  },
  {
   "id": "S7",
   "href": "stage-7-dashboards-and-site.html",
   "title": "Stage 7: Dashboards and site"
  }
 ],
 "methodHref": "s2-the-method.html#sbx"
};
