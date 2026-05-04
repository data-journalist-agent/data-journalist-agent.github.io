## Story Spine

**Core claim**: Black Summer's first week was not a freak event — it was the visible mid-air collision of a century of warming, a year of record drought, and a wave of 511,661-hectare megafires that satellites could already see lighting up Australia's south-east before most of the world noticed.

**Tension**: People remember 2019-2020 as a single shocking news cycle — koalas in trees, smoke over Sydney, helicopters over Mallacoota. The TidyTuesday emergency dataset shows that the disaster was actually the predictable end-state of three trends that had been visible for years in the BoM and NASA data: cities 1-2.4 C hotter, every monitored capital running its driest year on record, and a 7-day satellite snapshot of 34,000 fire pixels concentrated over a single corner of the country.

**Payoff**: After reading, the reader should see Black Summer not as a freak weather event but as a chart with a long horizontal axis and a tall y-axis spike — a discrete, predictable result of two centuries of station data.

## Sections

### edt_01: The week the satellites lit up
**Evidence**: ana_08, ana_10, ana_14 | **Context**: det_01, det_04

[ana_08] In the seven days from 29 December 2019 to 5 January 2020, NASA's MODIS satellites returned 34,248 thermal-anomaly pixels over Australia. Detections were uneven — 6,936 on 30 December, 7,384 on 4 January, just 867 on 5 January as the file cuts off. The hot pixels were not random noise; they tracked the operational tempo of the disaster.

[ana_10] Fifty-nine percent of those pixels — 20,261 of them — came from a single state. Victoria, the second-smallest mainland state, contributed more than triple any other region. New South Wales added 13%, Western Australia 11%, Queensland and inland scrub a combined 12%, South Australia 4%, Tasmania just 1%. The disaster was not nationally distributed; it was concentrated in a corner.

[ana_14] On a continental scatter map, the high-confidence detections form a continuous arc along the south-eastern coast: East Gippsland in Victoria, up through the NSW South Coast, as far north as the Mid-North Coast. This is the picture from orbit, before any narrative is applied.

[CHART: ana_14]
[MEDIA: map]

### edt_02: Sixty percent of Victoria's fires burned at night
**Evidence**: ana_13, ana_11, ana_12 | **Context**: det_04

[ana_13] The dangerous hallmark of Black Summer was night activity. In Victoria, 60.6% of MODIS detections were night pixels. New South Wales ran 53.5% night detections. Most other regions sat closer to a normal day-skewed pattern (WA 26.6%, SA 14.3%). Night fire is operationally menacing — humidity recovery stops, crews fatigue, fronts continue to advance.

[ana_11] The fire-radiative-power distribution has a long, heavy right tail. Most pixels were modest (the median released 38.7 megawatts), but the top one percent exceeded 1,657 MW and the single hottest pixel released 7,109 MW. This is the signature of pyrocumulonimbus events — fires generating their own weather.

[ana_12] The brightest pixels in the dataset cluster in a small lat-lon box in Victoria's alpine south-east, around -36.7 to -37.7 latitude and 147 to 149 longitude. The single hottest detection sat near (-37.74, 149.37) on the night of 29 December, releasing 5,587 MW — that is the East Gippsland fire that, days later, drove around 4,000 trapped residents and tourists onto the beach at Mallacoota waiting for navy evacuation.

[CHART: ana_13]

### edt_03: The driest year, almost everywhere
**Evidence**: ana_07, ana_05, ana_06 | **Context**: det_03

[ana_07] Pooling the six BoM stations in the dataset, 2019's annual rainfall was 571 mm — just 61% of the 931 mm long-term mean. The decline from 2010 was almost monotonic: 1190, 1022, 952, 963, 769, 919, 847, 731, 671, 571. Three consecutive sub-average years preceded Black Summer.

[ana_05] At every individual station, 2019 ranked in the bottom 12-15% of years on record. In Canberra it was the single driest year in the available 11-year record. In Brisbane, 5th of 42 years. In Perth, 5th of 52. In Melbourne, 7th of 49. In Sydney, 19th of 161 — meaning four-fifths of all years recorded since 1858 were wetter.

[ana_06] But it was the shape of the drought that mattered most. Canberra received 1.2 mm in December against an 84.7 mm climatology — a deficit of -83.5 mm. Sydney 1.6 against 77.6 mm. Melbourne 4.4 against 62.3 mm. Brisbane lost 125.7 mm in November alone. The 2019 deficit was not spread evenly across the year; it collapsed exactly in the months that should have rewetted the fuel load before summer.

[CHART: ana_07]

### edt_04: A century of warming, then 2019
**Evidence**: ana_02, ana_01, ana_03 | **Context**: det_03, det_06, det_07

[ana_02] Pooled across the long-record cities, 2019 sits at 26.4 C — the highest annual mean daily maximum in the entire 1910-2019 series, and roughly 3 C above the surrounding decade. The shape of the curve is gradual warming through the 20th century followed by a step-function jump in 2019.

[ana_01] The decadal comparison is unambiguous. Comparing 2010-2019 with 1910-1940, Canberra has warmed +2.39 C, Perth +2.10 C, Melbourne +1.62 C, Sydney +1.17 C. Brisbane lacks pre-1949 data so it cannot be compared on the same baseline. Every comparable city is between one and almost two and a half degrees hotter than it was a century ago.

[ana_03, det_06] When broken out by city, every series shows the same long-run warming signal — Canberra's first decade averages 18.61 C, its last 21.53 C; Perth runs from 23.41 to 25.82 C — and 2019 visibly breaks above the prior decade's range in every city. The World Weather Attribution rapid-attribution study found that anthropogenic climate change has raised the Fire Weather Index in this region by at least 30%, driven mostly by extreme heat. Heat extremes of the 2019-20 magnitude are now at least twice as likely.

[CHART: ana_02]

### edt_05: 4 million hectares, before the season ended
**Evidence**: ana_15, ana_16, ana_17 | **Context**: det_02, det_08, det_09

[ana_15] On the morning of 6 January 2020 — the day this dataset was downloaded — the NSW Rural Fire Service reported 143 declared major incidents. Of those, 82 were under control, 30 being controlled, and 31 still out of control. The agency was tracking a continuous wave of active calls.

[ana_16] The 15 largest read like a roll call of Black Summer's worst fires. Gospers Mountain, in Wollemi National Park north-west of Sydney, had reached 511,661 hectares — the largest single forest fire from one ignition in Australian history (a lightning strike on 26 October 2019). Dunns Road sat at 313,536 ha and was still officially out of control. Currowan, Green Wattle Creek, Carrai Creek, Badja Forest Road — every one of the top eight individually exceeded 150,000 hectares.

[ana_17, det_09] Across the 99 incidents with declared sizes, NSW alone was tracking 3,996,859 hectares — about 4.0 million hectares already burning on 6 January, in just one state, with the season far from over. Set against the eventual nationwide season-long total of ~24 million hectares, this single-state, single-day snapshot already accounted for roughly one-sixth of the entire Black Summer toll.

[CHART: ana_16]
[MEDIA: map]

### edt_06: What the dataset is, and what it is not
**Evidence**: | **Context**: det_04, det_09, det_01

[det_04, det_09] One discipline this dataset enforces: the satellite hotspots are not fires. A MODIS row is a 1 km thermal pixel that was anomalous when the satellite passed overhead. Roughly 100 hectares of ground per pixel, but the same fire is re-detected on every overpass and many pixels overlap, so the 34,000 rows cannot be multiplied to a hectare total. The official 24 Mha national figure comes from ground accounting, not the satellite.

[det_01] The TidyTuesday release itself was not a normal weekly drop. Its readme reads as a warning: "PLEASE be cautious when plotting maps of ongoing fires." It was assembled in the middle of an active disaster, three days into the new year, while a country burned. This blog uses the same dataset to step back, six years on, and ask what the data — viewed against a longer record — actually showed.

[editorial] The data didn't cause Black Summer. Climate change, drought cycles, fuel load, and a complex coupled-ocean precondition involving the Indian Ocean Dipole and a Central Pacific El Niño did. But on this particular eight-day window, the disaster was already legible to anyone with a satellite, a rainfall gauge, and a temperature thermometer. The slow lines on the chart had finally crossed.

## Editorial Notes
- 511,661 ha (Gospers Mountain) and 4 million ha (NSW total) must be exact — these are the load-bearing single-state numbers.
- The 24 million ha season-long figure is from external context (det_02, det_09); never compute it from the MODIS data.
- 2019 = 26.4 C, 571 mm rainfall, 61% of average — keep these visible.
- Always present MODIS as "satellite detections", not "fires". The data-quality caveat (det_04) must remain prominent in section 6.
- Sydney's 19/161 ranking (det_07 / ana_05) deserves emphasis — it shows the modern-era novelty without claiming it's the worst year in Australian history.
