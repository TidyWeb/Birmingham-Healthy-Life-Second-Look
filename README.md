# Birmingham Healthy Life: A Second Look

### [Visit the live Unit 3 site ↗](https://tidyweb.github.io/Birmingham-Healthy-Life-Second-Look/)

This is the project site for my Code Institute Unit 3 assessment: a second look at the Birmingham Healthy Life analysis through an ethical lens. It is served by GitHub Pages at https://tidyweb.github.io/Birmingham-Healthy-Life-Second-Look/.

The [original Unit 2 project site](https://tidyweb.github.io/Birmingham-Healthy-Life/) remains available.

The notebooks and data are in the assessment repository: https://github.com/TidyWeb/Code-Institute-DA-with-AI-Unit-3-Assessment

## What's where

- `content/`: the text for the home page and each chapter, in Markdown. Edit these.
- `tools/build_site.py`: turns `content/` and the executed notebooks into the HTML pages.
- `tools/ethics_register.py`: reads the ethics-screen CSV and writes the figures and text summary used by the second-look chapters.
- `assets/site.css`, `assets/site.js`: the look and the small page behaviours.
- `assets/img/`: screenshots and the second-look SVG figures, kept by hand.
- `dashboard/`: the dashboard, with a "Back" button added by the build.
- `index.html`, `story/`, `notebooks/`, `assets/figures/`, `assets/nb/`: built by the script. Don't edit these; they're rewritten on every build.

## Rebuild after editing

From the site clone inside the Unit 3 `REPOS` folder, with the analysis clone beside it, run:

```
HLE_PROJECT="../Code-Institute-DA-with-AI-Unit-3-Assessment" "../.venv-unit3/bin/python" tools/build_site.py
```

To check every link and image afterwards, run `tools/check_links.py` with the same Python. Add `--web` to check the external sites too. GitHub sometimes refuses scripted checks with a 503 even when the page exists.

To look at it locally, run `python3 -m http.server 8765` in this folder and open http://localhost:8765/.

## Block markers in the content files

Use these alongside ordinary Markdown:

- `::: keypoints`: the "In short" box at the top of a chapter.
- `::: stats nb04#cellid`: a slate panel of numbers. Each line is `value | label`.
- `::: figure folder/name [wide] nb05#cellid`: a saved notebook figure on a plate. The folder is one of `wide`, `neighbours`, `ml` or `hotspots`. Add `alt:` and `caption:` lines.
- `::: image file.webp [wide]`: an image from `assets/img`; `.svg` figures are supported under `assets/img/second-look/`. Add both `alt:` and `caption:` lines.
- `::: callout`: one plain sentence set large.
- `::: tableau`: the Tableau embed with its screenshot.
- `:::`: closes a block.
- `^ nb04#cellid | note`: a margin note for the paragraph after it. It links to that cell on the notebook page.

The cell ids come from the notebooks themselves, so every note points at the cell that produced the number.
