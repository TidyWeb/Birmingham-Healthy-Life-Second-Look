# The Ethics of a Birmingham Healthy Life

This repository contains the static site for **The Ethics of a Birmingham Healthy Life**, my Unit 3 ethical review of the Unit 2 analysis. It tells the story of the methods, results, limitations and lifecycle. The analysis code, notebooks and data are in the [Unit 3 analysis repository](https://github.com/TidyWeb/Code-Institute-DA-with-AI-Unit-3-Assessment), whose README is the submission front door.

The deployed site is [The Ethics of a Birmingham Healthy Life](https://tidyweb.github.io/Birmingham-Healthy-Life-Second-Look/). The original [Unit 2 site](https://tidyweb.github.io/Birmingham-Healthy-Life/) remains available.

## Sources and generated pages

- `content/` holds the Markdown for the home page and story chapters. Edit these source files.
- `tools/dashboard/template.html` and `tools/dashboard/build.py` build the Leaflet dashboard from the template and the analysis repository's saved outputs.
- `tools/build_site.py` builds the home page, story pages and notebook pages from `content/` and the executed notebooks. It also adds the dashboard's Back link and desktop-only notice.
- `assets/site.css`, `assets/site.js` and `assets/img/` hold the site presentation and hand-maintained images.
- `index.html`, `story/`, `notebooks/`, `assets/figures/`, `assets/nb/` and `assets/files/` are generated. Do not edit them by hand.

## Rebuild and check

Use the site and analysis clones as sibling folders, with the Unit 3 environment at `REPOS/.venv-unit3`. From the site repository root, activate that environment, then install the analysis packages and the extra Markdown dependency used by `build_site.py`:

```bash
source ../.venv-unit3/bin/activate
python -m pip install -r ../Code-Institute-DA-with-AI-Unit-3-Assessment/requirements.txt
python -m pip install Markdown
```

Run the notebooks in order first. From the site repository root, build the dashboard, then the site, then check its internal links:

```bash
HLE_PROJECT="../Code-Institute-DA-with-AI-Unit-3-Assessment" \
  python tools/dashboard/build.py

HLE_PROJECT="../Code-Institute-DA-with-AI-Unit-3-Assessment" \
  python tools/build_site.py

HLE_PROJECT="../Code-Institute-DA-with-AI-Unit-3-Assessment" \
  python tools/check_links.py
```

`build_site.py` removes and recreates only its generated output folders before building. Add `--web` to `check_links.py` to check external addresses as well; some sites refuse automated requests even when the page has been verified manually.
