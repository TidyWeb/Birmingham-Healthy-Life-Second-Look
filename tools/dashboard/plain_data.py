"""Build-time data for the question-led Plain view preview.

All quantitative answer content is derived from the saved assessment data. This
module only computes payload data; rendering and file selection stay in build.py.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean
from typing import Any

from shapely.geometry import mapping, shape
from shapely.ops import unary_union


HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[2] / "Code-Institute-DA-with-AI-Unit-3-Assessment"
WIDE_CSV = PROJECT_ROOT / "data/cleaned/Wide/msoa_wide_660.csv"
RANK_CSV = PROJECT_ROOT / "data/cleaned/Uncertainty/rank_stability.csv"
PAIRS_CSV = PROJECT_ROOT / "data/cleaned/Hotspots/hotspot_pairs.csv"
BIG_GAP_PAIRS_CSV = PROJECT_ROOT / "data/cleaned/Neighbours/big_gap_pairs.csv"
HOTSPOTS_CSV = PROJECT_ROOT / "data/cleaned/Hotspots/hotspots.csv"
AGGREGATION_CSV = PROJECT_ROOT / "data/cleaned/Aggregation/msoa_fuel_poverty_aggregation.csv"
SOURCE_REGISTER_CSV = PROJECT_ROOT / "data/source-register.csv"
ETHICS_CSV = PROJECT_ROOT / "data/ethics/unit3_screen_results.csv"
CORRELATIONS_CSV = PROJECT_ROOT / "data/cleaned/Wide/hle_spearman_correlations.csv"
GEOGRAPHY_CSV = PROJECT_ROOT / "data/prepared/Geography/ons_lsoa21_to_msoa21_lad22_exploratory_west_midlands.csv"
HOTSPOT_AREAS_GEOJSON = PROJECT_ROOT / "data/cleaned/Hotspots/hotspot_areas.geojson"

COUNCILS = (
    "Birmingham", "Coventry", "Dudley", "Sandwell", "Solihull", "Walsall", "Wolverhampton",
)
MIXED_AREA_LINE = (
    "Living conditions vary a lot between the neighbourhoods inside this area, "
    "so its average may hide big differences."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def rnum(value: float, places: int = 2) -> float:
    return round(float(value), places)


def year(value: float) -> int:
    return int(math.floor(float(value) + 0.5))


def count_word(value: int) -> str:
    return {5: "five", 7: "seven"}.get(value, str(value))


def _loaded_sources() -> dict[str, list[dict[str, str]]]:
    return {
        "wide": read_csv(WIDE_CSV),
        "rank": read_csv(RANK_CSV),
        "pairs": read_csv(PAIRS_CSV),
        "big_gap_pairs": read_csv(BIG_GAP_PAIRS_CSV),
        "hotspots": read_csv(HOTSPOTS_CSV),
        "aggregation": read_csv(AGGREGATION_CSV),
        "register": read_csv(SOURCE_REGISTER_CSV),
        "ethics": read_csv(ETHICS_CSV),
        "correlations": read_csv(CORRELATIONS_CSV),
        "geography": read_csv(GEOGRAPHY_CSV),
    }


def build_plain_data(payload: dict[str, Any]) -> dict[str, Any]:
    """Return the computed Plain view payload from named project sources."""
    src = _loaded_sources()
    wide_rows = src["wide"]
    areas = payload["areas"]
    area_by_code = {area["code"]: area for area in areas}
    wide_by_code = {row["area_code"]: row for row in wide_rows}
    if set(wide_by_code) != set(area_by_code):
        raise ValueError("Plain-view wide data does not exactly match dashboard areas")

    hle_values = {code: float(row["hle_average"]) for code, row in wide_by_code.items()}
    average = mean(hle_values.values())
    bottom = [r["area_code"] for r in src["rank"]
              if r["bottom_10_confidence"] == "confidently in the lowest tenth"]
    top = [r["area_code"] for r in src["rank"]
           if r["top_10_confidence"] == "confidently in the highest tenth"]
    rank_by_code = {row["area_code"]: row for row in src["rank"]}
    if len(bottom) != 35 or len(top) != 37:
        raise ValueError(f"Expected 35/37 confident bottom/top areas, got {len(bottom)}/{len(top)}")

    low_values = [hle_values[code] for code in bottom]
    high_values = [hle_values[code] for code in top]
    low_mean, high_mean = mean(low_values), mean(high_values)
    sorted_rows = sorted(wide_rows, key=lambda row: (float(row["hle_average"]), row["area_code"]))
    tenth_count = max(1, len(sorted_rows) // 10)
    low_tenth = [float(row["hle_average"]) for row in sorted_rows[:tenth_count]]
    high_tenth = [float(row["hle_average"]) for row in sorted_rows[-tenth_count:]]

    average_male = mean(float(row["hle_male"]) for row in wide_rows)
    average_female = mean(float(row["hle_female"]) for row in wide_rows)
    aggregation = {row["msoa_code"]: row for row in src["aggregation"]}
    if set(aggregation) != set(area_by_code):
        raise ValueError("Aggregation data does not exactly match dashboard areas")
    mixed_codes = {code for code, row in aggregation.items() if row["mixed"] == "True"}
    if len(mixed_codes) != 255:
        raise ValueError(f"Expected 255 mixed areas, got {len(mixed_codes)}")

    geography_rows = src["geography"]
    authority_by_code: dict[str, str] = {}
    authority_name_by_code: dict[str, str] = {}
    for row in geography_rows:
        area_code, authority_code, authority_name = row["MSOA21CD"], row["LAD22CD"], row["LAD22NM"]
        prior = authority_by_code.setdefault(area_code, authority_code)
        if prior != authority_code:
            raise ValueError(f"Geography lookup assigns multiple councils to {area_code}")
        authority_name_by_code[authority_code] = authority_name
    lookup_names = {row["MSOA21CD"]: row["LAD22NM"] for row in geography_rows}
    for code, area in area_by_code.items():
        if lookup_names.get(code) != area["local_authority"]:
            raise ValueError(f"Dashboard authority does not match the source lookup for {code}")
    smoking_context = payload["authority_context"]["smoking"]
    smoke_by_council = smoking_context["authorities"]
    for code, area in area_by_code.items():
        authority_code = authority_by_code[code]
        area["values"]["adult_smoking_pct"] = (
            float(smoke_by_council[authority_code]["value"])
            if authority_code in smoke_by_council else None
        )

    plain_areas: dict[str, dict[str, Any]] = {}
    labels = {
        "bottom": {
            "confidently in the lowest tenth": "Clearly among the lowest",
            "likely": "Probably among the lowest",
            "possibly": "Possibly among the lowest",
        },
        "top": {
            "confidently in the highest tenth": "Clearly among the highest",
            "likely": "Probably among the highest",
            "possibly": "Possibly among the highest",
        },
    }
    for code, area in area_by_code.items():
        values = area["values"]
        hle = float(values["hle_average"])
        rank = rank_by_code[code]
        if rank["bottom_10_confidence"] != "not":
            position = labels["bottom"][rank["bottom_10_confidence"]]
        elif rank["top_10_confidence"] != "not":
            position = labels["top"][rank["top_10_confidence"]]
        else:
            position = ("Lower than average" if hle < 60
                        else "Higher than average" if hle >= 65
                        else "Around average")
        delta = year(abs(hle - average))
        direction = "fewer" if hle < average else "more"
        sentence = (
            f"People in {area['name']} can expect about {year(hle)} years in good health, "
            f"about {delta} years {direction} than the average across all the areas covered."
        )
        notes = []
        if values.get("student_dominated"):
            notes.append("Many students live here, so health figures may not describe long-term residents.")
        if values.get("visitor_hub"):
            notes.append("Crime figures here mostly reflect visitors, not residents.")
        if values.get("hle_male_imputed") or values.get("hle_female_imputed"):
            notes.append("This figure was estimated because the official one wasn't available.")
        plain_areas[code] = {
            "sentence": sentence,
            "position": position,
            "notes": notes,
            "mixed": code in mixed_codes,
            "hle": rnum(hle, 3),
            "average": rnum(average, 3),
            "bar": {"value": rnum(hle, 3), "average": rnum(average, 3)},
        }

    hotspot_area_features = json.loads(HOTSPOT_AREAS_GEOJSON.read_text(encoding="utf-8"))["features"]
    hotspot_codes_by_id: dict[str, list[str]] = {}
    for feature in hotspot_area_features:
        props = feature["properties"]
        if props.get("in_hotspot"):
            hotspot_codes_by_id.setdefault(str(props["hotspot_id"]), []).append(props["area_code"])
    hotspot_pairs_by_id: dict[str, list[dict[str, str]]] = {}
    for row in src["pairs"]:
        hotspot_pairs_by_id.setdefault(row["hotspot_id"], []).append(row)
    hotspots = []
    for record in sorted(src["hotspots"], key=lambda row: -float(row["largest_gap_years"])):
        hid = record["hotspot_id"]
        pairs = hotspot_pairs_by_id.get(hid, [])
        if not pairs:
            raise ValueError(f"Hotspot {hid} has no saved pair rows")
        largest = max(pairs, key=lambda row: float(row["actual_gap_years"]))
        higher, lower = largest["higher_area_name"], largest["lower_area_name"]
        bigger = year(float(largest["actual_gap_years"]))
        sentence = (
            f"{higher} and {lower} sit next to each other, yet people in {higher} "
            f"can expect about {bigger} more years in good health."
        )
        hotspots.append({
            "name": record["working_name"],
            "codes": sorted(hotspot_codes_by_id.get(hid, [])),
            "pairs": [[row["higher_area_code"], row["lower_area_code"]] for row in pairs],
            "sentence": sentence,
            "bounds": [float(record[k]) for k in ("bbox_west", "bbox_south", "bbox_east", "bbox_north")],
            "largest_pair": {
                "higher": higher, "lower": lower,
                "higher_code": largest["higher_area_code"], "lower_code": largest["lower_area_code"],
                "gap": float(largest["actual_gap_years"]),
            },
        })

    council_codes: dict[str, list[str]] = {name: [] for name in COUNCILS}
    for code, authority_code in authority_by_code.items():
        authority = authority_name_by_code[authority_code]
        if authority in council_codes and code in area_by_code:
            council_codes[authority].append(code)
    for name, codes in council_codes.items():
        if not codes:
            raise ValueError(f"No areas found for required council {name}")
    council_outline_geojson = make_council_outlines(payload["geometry"], council_codes)
    council_values = {
        name: [hle_values[code] for code in codes]
        for name, codes in council_codes.items()
    }
    council_means = {name: mean(vals) for name, vals in council_values.items()}
    council_labels = []
    council_feature_by_name = {
        feature["properties"]["council"]: feature
        for feature in council_outline_geojson["features"]
    }
    for name in COUNCILS:
        point = shape(council_feature_by_name[name]["geometry"]).representative_point()
        council_labels.append({
            "name": name,
            "lat": round(point.y, 6),
            "lon": round(point.x, 6),
            "average": year(council_means[name]),
        })

    register_by_id = {row["id"]: row for row in src["register"]}
    periods = {
        "hle": register_by_id["ons_hle"]["period"],
        "census": next(row["period"] for row in src["register"] if "Census 2021" in row["period"] and "qualif" in row["topic"].lower()),
        "income": register_by_id["income_fye2023"]["period"],
        "fuel_poverty": register_by_id["fuel_poverty"]["period"],
        "air_pollution_no2": register_by_id["no2"]["period"],
        "air_pollution_pm25": register_by_id["pm25"]["period"],
        "crime": register_by_id["police_crime_2024"]["period"],
    }
    if periods["hle"] != "2019-2023" or periods["census"] != "Census 2021":
        raise ValueError(f"Source-register periods differ from approved answer: {periods}")
    income_year = periods["income"].rsplit(" ", 1)[-1]
    if "March 2023" not in periods["income"] or not income_year.isdigit():
        raise ValueError(f"Source-register income period differs from approved answer: {periods['income']}")
    if ({periods["fuel_poverty"], periods["air_pollution_no2"], periods["air_pollution_pm25"]} != {"2024"}
            or not periods["crime"].startswith("2024-")):
        raise ValueError(f"Source-register periods differ from approved 2024 wording: {periods}")
    recent_data_year = periods["fuel_poverty"]
    ethics_count = len(src["ethics"])
    if ethics_count != 27:
        raise ValueError(f"Expected 27 ethics-screen questions, found {ethics_count}")

    question_answers = [
        {
            "question": "Where do people have the fewest years in good health?",
            "answer": (f"{len(bottom)} areas are clearly among the lowest; they're highlighted on the map. "
                       "Zoom in or out to see the highlighted areas. "
                       f"In these areas, people can expect around {year(min(low_values))} to {year(max(low_values))} years in good health, "
                       f"about {year(average - max(low_values))} to {year(average - min(low_values))} years fewer than the average across all the areas covered."),
            "action": {"type": "highlight", "codes": sorted(bottom)},
        },
        {
            "question": "Where do people have the most years in good health?",
            "answer": (f"{len(top)} areas are clearly among the highest; they're highlighted on the map. "
                       "Zoom in or out to see the highlighted areas. "
                       f"People there can expect around {year(min(high_values))} to {year(max(high_values))} years in good health, "
                       f"about {year(min(high_values) - average)} to {year(max(high_values) - average)} years more than the average across all the areas covered."),
            "action": {"type": "highlight", "codes": sorted(top)},
        },
        {
            "question": "How big is the gap overall?",
            "answer": (f"In the healthiest tenth of areas, people can expect about {year(mean(high_tenth))} years in good health. "
                       f"In the least healthy tenth, about {year(mean(low_tenth))}. That's a gap of about "
                       f"{year(mean(high_tenth) - mean(low_tenth))} years: a large, real difference."),
            "action": {"type": "answer"},
        },
        {
            "question": "Where do next-door neighbours have very different lives?",
            "answer": (f"In some places, neighbouring areas sit side by side, yet their residents' expected years in good health differ by "
                       f"{year(min(float(row['gap_years']) for row in src['big_gap_pairs']))} to "
                       f"{year(max(float(row['gap_years']) for row in src['big_gap_pairs']))} years. "
                       f"These pairs gather in {count_word(len(src['hotspots']))} places, shown one at a time."),
            "action": {"type": "hotspots", "index": 0},
        },
        {
            "question": "What tends to go with fewer years in good health?",
            "answer": ("Areas with fewer years in good health also tend to have lower incomes, more households facing hardship, more crowded homes, "
                       "more unemployment and more adults without qualifications. Air pollution and homes that are hard to keep warm follow the same pattern, less strongly. "
                       "These things go together; this work doesn't prove that one causes another."),
            "action": {"type": "answer"},
        },
        {
            "question": "How do the councils compare?",
            "answer": (f"Across the {count_word(len(council_codes))} West Midlands councils, people in Solihull can expect the most years in good health (about {year(council_means['Solihull'])}) "
                       f"and people in Sandwell and Birmingham the fewest (about {year(min(council_means['Sandwell'], council_means['Birmingham']))} to "
                       f"{year(max(council_means['Sandwell'], council_means['Birmingham']))}): a difference of about "
                       f"{year(council_means['Solihull'] - min(council_means['Sandwell'], council_means['Birmingham']))} years. "
                       f"But the differences inside each council are much bigger. In Birmingham, areas range from about "
                       f"{year(min(council_values['Birmingham']))} to {year(max(council_values['Birmingham']))} years; in Solihull, from about "
                       f"{year(min(council_values['Solihull']))} to {year(max(council_values['Solihull']))}. "
                       "These are averages of the small areas in each council, not official council figures."),
            "action": {"type": "outline-councils"},
        },
        {
            "question": "How sure are we?",
            "answer": ("Every figure here is an estimate, much like a weather forecast. That doesn't make it unreliable. The overall picture is clear: the gap between areas is large and real. "
                       "What can shift a little is an area's exact place in the table, which is why we use \"clearly\", \"probably\" and \"possibly\" rather than exact positions."),
            "action": {"type": "answer"},
        },
        {
            "question": "Do men and women differ?",
            "answer": (f"A little. On average, women can expect about {year(average_female)} years in good health and men about {year(average_male)}. "
                       "That difference is small compared with the gap between areas."),
            "action": {"type": "answer"},
        },
        {
            "question": "Does this tell us about ethnic groups?",
            "answer": ("No. Some of the things linked to health here also vary with who lives in an area, so these results describe places, not any ethnic group's health. "
                       "For that reason, ethnicity isn't shown in this view."),
            "action": {"type": "answer"},
        },
        {
            "question": "What can't this tell us?",
            "answer": ("It can't say what causes the differences: things that go together aren't proven to cause each other. It can't tell you anything about one person; "
                       "every figure is an average for an area. And it can't predict what will happen next: it describes the recent past."),
            "action": {"type": "answer"},
        },
        {
            "question": "Where do these figures come from, and how up to date are they?",
            "answer": (f"The years in good health are official estimates from the Office for National Statistics for {periods['hle'].replace('-', ' to ')}. "
                       f"Most of the living-conditions figures come from the {periods['census'].replace('Census 2021', '2021 Census')}. Income is for the year to March {income_year}, "
                       f"and fuel poverty, air pollution and recorded crime are for {recent_data_year}. "
                       "Some of these figures are themselves estimates made by the organisations that publish them."),
            "link": {"text": "See the full list of sources, with where each one came from and its licence",
                     "href": "https://github.com/TidyWeb/Code-Institute-DA-with-AI-Unit-3-Assessment/blob/main/data/source-register.csv"},
            "action": {"type": "answer"},
        },
        {
            "question": "Can I use this to judge a place or the people who live there?",
            "answer": ("No. These figures describe areas, not individuals. Each area is an average of several neighbourhoods, and in "
                       f"{len(mixed_codes)} of them the smaller neighbourhoods inside differ a lot in fuel poverty, which the average hides. Please don't use this to judge a place or its residents. "
                       f"Before publishing, I checked this work with Signal Box, my {ethics_count}-question ethics check."),
            "action": {"type": "answer"},
        },
    ]

    actual_display = {
        "average_about": year(average),
        "bottom_count": len(bottom),
        "bottom_range": [year(min(low_values)), year(max(low_values))],
        "bottom_difference": [year(average - max(low_values)), year(average - min(low_values))],
        "top_count": len(top),
        "top_range": [year(min(high_values)), year(max(high_values))],
        "top_difference": [year(min(high_values) - average), year(max(high_values) - average)],
        "tenth_means_and_gap": [year(mean(high_tenth)), year(mean(low_tenth)), year(mean(high_tenth) - mean(low_tenth))],
        "hotspot_pairs_and_gap": [
            len(src["big_gap_pairs"]),
            round(min(float(row["gap_years"]) for row in src["big_gap_pairs"]), 1),
            round(max(float(row["gap_years"]) for row in src["big_gap_pairs"]), 2),
        ],
        "mixed_count": len(mixed_codes),
        "women_and_men_average": [year(average_female), year(average_male)],
        "council_averages": {name: year(council_means[name]) for name in COUNCILS},
        "council_counts": {name: len(council_codes[name]) for name in COUNCILS},
        "birmingham_and_solihull_ranges": {
            "Birmingham": [year(min(council_values["Birmingham"])), year(max(council_values["Birmingham"]))],
            "Solihull": [year(min(council_values["Solihull"])), year(max(council_values["Solihull"]))],
        },
        "ethics_question_count": ethics_count,
    }
    approved_display = {
        "average_about": 64,
        "bottom_count": 35, "bottom_range": [54, 56], "bottom_difference": [8, 10],
        "top_count": 37, "top_range": [71, 76], "top_difference": [7, 12],
        "tenth_means_and_gap": [72, 56, 16],
        "hotspot_pairs_and_gap": [95, 9.6, 15.85],
        "mixed_count": 255,
        "women_and_men_average": [64, 63],
        "council_averages": {"Sandwell": 60, "Birmingham": 61, "Wolverhampton": 61, "Walsall": 62,
                             "Coventry": 63, "Dudley": 64, "Solihull": 67},
        "council_counts": {"Birmingham": 132, "Coventry": 42, "Dudley": 43, "Sandwell": 39,
                           "Solihull": 29, "Walsall": 39, "Wolverhampton": 33},
        "birmingham_and_solihull_ranges": {"Birmingham": [54, 73], "Solihull": [56, 75]},
        "ethics_question_count": 27,
    }

    metrics = [
        {"key": "hle_average", "label": "Years in good health", "worse": "lower"},
        {"key": "annual_equivalised_income_after_housing_costs_gbp", "label": "Money left after housing costs", "worse": "lower"},
        {"key": "households_deprived_2plus_pct", "label": "Households facing hardship", "worse": "higher"},
        {"key": "overcrowded_households_pct", "label": "Crowded homes", "worse": "higher"},
        {"key": "unemployment_rate_active_pct", "label": "Unemployment", "worse": "higher"},
        {"key": "no_qualifications_pct", "label": "Adults with no qualifications", "worse": "higher"},
        {"key": "pm25_area_mean_ug_m3", "label": "Air pollution", "worse": "higher"},
        {"key": "fuel_poor_households_pct", "label": "Homes struggling to keep warm", "worse": "higher"},
        {"key": "adult_smoking_pct", "label": "Smoking", "worse": "higher", "period": smoking_context["period"],
         "note": f"{smoking_context['label']} by council ({smoking_context['period']}); it is not a small-area estimate. Some councils have no estimate."},
        {"key": "crime_for_analysis", "label": "Recorded crime", "worse": "higher"},
    ]

    # Figure audit is intentionally machine-readable so the preview build can
    # print all source-derived values next to the agreed wording for review.
    figures = {
        "average": average,
        "bottom_count": len(bottom), "bottom_min": min(low_values), "bottom_max": max(low_values),
        "bottom_difference_min": average - max(low_values), "bottom_difference_max": average - min(low_values),
        "top_count": len(top), "top_min": min(high_values), "top_max": max(high_values),
        "top_difference_min": min(high_values) - average, "top_difference_max": max(high_values) - average,
        "healthiest_tenth_average": mean(high_tenth), "least_healthy_tenth_average": mean(low_tenth),
        "tenth_gap": mean(high_tenth) - mean(low_tenth),
        "bottom_position_counts": confidence_counts(src["rank"], "bottom_10_confidence"),
        "top_position_counts": confidence_counts(src["rank"], "top_10_confidence"),
        "men_average": average_male, "women_average": average_female,
        "mixed_count": len(mixed_codes), "hotspot_pair_count": len(src["big_gap_pairs"]),
        "hotspot_gap_min": min(float(row["gap_years"]) for row in src["big_gap_pairs"]),
        "hotspot_gap_max": max(float(row["gap_years"]) for row in src["big_gap_pairs"]),
        "hotspot_member_pair_count": len(src["pairs"]),
        "hotspots": [{"name": h["name"], "area_count": len(h["codes"]), "pair_count": len(h["pairs"]),
                      "largest_gap": h["largest_pair"]["gap"], "pair": h["largest_pair"]} for h in hotspots],
        "councils": {name: {"area_count": len(council_codes[name]), "average": council_means[name],
                            "minimum": min(council_values[name]), "maximum": max(council_values[name])}
                     for name in COUNCILS},
        "periods": periods,
        "ethics_question_count": ethics_count,
        "top_correlations": correlation_context(src["correlations"]),
        "approved_text_comparisons": {
            "expected_average_about": 64,
            "expected_bottom_count": 35, "expected_bottom_range": [54, 56],
            "expected_top_count": 37, "expected_top_range": [71, 76],
            "expected_tenth_gap_about": 16,
            "expected_hotspot_pairs": 95,
            "expected_hotspot_gap_range": [9.6, 15.85],
            "expected_mixed_count": 255,
            "expected_ethics_question_count": 27,
        },
        "displayed_figure_comparison": {
            "actual": actual_display,
            "approved": approved_display,
            "matches": actual_display == approved_display,
            "mismatches": {
                key: {"actual": actual_display[key], "approved": approved_display[key]}
                for key in approved_display if actual_display[key] != approved_display[key]
            },
        },
    }

    return {
        "questions": question_answers,
        "metrics": metrics,
        "average": rnum(average, 3),
        "areas": plain_areas,
        "hotspots": hotspots,
        "council_codes": council_codes,
        "council_labels": council_labels,
        "council_outline_geojson": council_outline_geojson,
        "mixed_area_line": MIXED_AREA_LINE,
        "fair_use_signal_box": f"Before publishing, I checked this work with Signal Box, my {ethics_count}-question ethics check.",
        "signal_box_method_href": "https://tidyweb.github.io/Birmingham-Healthy-Life-Second-Look/story/s2-the-method.html",
        "question_this_work": "Think something here is wrong? Tell me. The form needs a free GitHub account.",
        "figures": figures,
    }


def confidence_counts(rows: list[dict[str, str]], field: str) -> dict[str, int]:
    return {
        "confidently": sum(row[field].startswith("confidently in the ") for row in rows),
        "likely": sum(row[field] == "likely" for row in rows),
        "possibly": sum(row[field] == "possibly" for row in rows),
        "not": sum(row[field] == "not" for row in rows),
    }


def correlation_context(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    if not rows or "" not in rows[0]:
        return []
    ranked = sorted(rows, key=lambda row: abs(float(row["hle_average"])), reverse=True)
    return [{"measure": row[""], "rho": float(row["hle_average"])} for row in ranked[:8]]


def make_council_outlines(geometry_payload: dict[str, Any], council_codes: dict[str, list[str]]) -> dict[str, Any]:
    code_to_council = {code: name for name, codes in council_codes.items() for code in codes}
    members: dict[str, list[Any]] = {name: [] for name in council_codes}
    for feature in geometry_payload["features"]:
        code = feature["properties"]["area_code"]
        council = code_to_council.get(code)
        if council:
            members[council].append(shape(feature["geometry"]))
    features = []
    for council, geometries in members.items():
        if not geometries:
            continue
        merged = unary_union(geometries)
        features.append({"type": "Feature", "properties": {"council": council}, "geometry": mapping(merged)})
    return {"type": "FeatureCollection", "features": features}
