# Five Hours in the Hallway

## Story Spine

**Core claim**: A state's median emergency-department visit length is determined less by population density than by hospital-system capacity, and the same dataset that exposes this also reveals a striking second story — that within the same hospitals, healthcare workers vaccinate themselves against flu at 82% but against COVID at 11%.

**Tension**: Most readers assume ER waits scale with state size and that "good hospitals do everything well." Both intuitions break: the state with the longest waits (DC) is geographically tiny, the state with the shortest (ND) is the third-least dense in the country, and the SEP_1 sepsis-bundle leaders are not the same states as the COVID-coverage leaders. CMS quality is not one dimension — it's a constellation.

**Payoff**: A reader leaves understanding (1) why their own ER might be slow has nothing to do with how many neighbors they have, (2) that boarding — not triage — is the load-bearing variable, and (3) that the state-by-state CMS file is a cleaner natural experiment in "what hospitals optimize" than most policy documents.

## Sections

### edt_01: Five hours in the hallway
**Evidence**: ana_05, ana_06, ana_04 | **Context**: det_03, det_04, det_02

[ana_05] In the District of Columbia, the median emergency-department visit lasts 310 minutes. Five hours and ten minutes from arrival to leaving. Puerto Rico is right behind at 302 minutes, Maryland at 251, Rhode Island at 224, Delaware at 217.

[ana_06] In North Dakota, that same median is 110 minutes. South Dakota: 113. Nebraska: 114. The fastest jurisdictions in the country move people through their ERs in under two hours; the slowest take roughly three times as long.

[ana_04, det_02] CMS reports a national median of 161 minutes for OP-18b in 2024 — the official measure of how long the median patient spends in an ED before leaving. Our 52-state distribution lands within rounding of that headline, with a standard deviation of 42 minutes and a 2.82x ratio between the slowest and fastest jurisdictions.

[det_03, det_04] The Visual Capitalist infographic that prompted this dataset asks whether ER waits track state populations. They do not. What they track is hospital-system slack — and that slack has been shrinking for three years as the United States has settled into what the American College of Emergency Physicians calls a multi-year "boarding crisis."

[CHART: ana_07]
[MEDIA: map]

### edt_02: The geography of waiting
**Evidence**: ana_07, ana_05, ana_06 | **Context**: det_03, det_07

[ana_07] The full ranking is a mid-Atlantic story. Nine of the ten longest-wait jurisdictions are on the I-95 corridor between Massachusetts and North Carolina. The shortest waits cluster in the Great Plains: North Dakota, South Dakota, Nebraska, Iowa, Kansas, Minnesota — with Hawaii as the lone non-prairie member of the under-two-hours club.

[det_07, ana_07] Population density is correlated, but it is not the load-bearing variable. A 2015 study of risk-adjusted ED timeliness found that hospital size, urban-rural status, and inpatient occupancy explained more variance in OP-18b than density did. North Carolina's 192-minute average and Texas's 145-minute average sit in roughly the same population-density bin. They are running their hospitals differently.

[ana_05] DC and Puerto Rico are the dataset's structural outliers. Both are jurisdictions where federal facilities, uninsured rates, and constrained inpatient capacity all push in the same direction. The 50-minute gap between Maryland (#3) and the next group is the clearest break in the entire ranking — below it, the slope is gradual; above it, two extreme cases.

[CHART: ana_07]

### edt_03: It's not the door — it's the bed
**Evidence**: ana_08, ana_09, ana_11 | **Context**: det_04

[ana_08] Inside any given state, the busiest ED is dramatically slower than the smallest. Across all states, low-volume EDs report a 126-minute median, mediums 168, highs 184, and very-high-volume EDs 192 — a 66-minute jump from the smallest to the busiest sites. New Mexico's busiest hospitals run 164 minutes longer than its smallest. Indiana, oddly, runs the opposite gradient.

[ana_09] OP-22 measures the share of patients who give up and leave before being seen. Nationally that is 2.5%. In DC, it's 6%; in Massachusetts, Delaware, and Rhode Island, 5%. In North Dakota, South Dakota, Idaho, and Nebraska, it's 1%. People walk out of ERs they expect to wait in.

[ana_11, det_04] The two measures move together: OP-18b and OP-22 correlate at r = 0.48 across states. The eight worst jurisdictions on a combined z-score (DC, RI, DE, MA, MD, PR, IL, NY) are the same hospitals where ACEP's "boarding" — admitted patients held in the ED because no inpatient bed is available — has been documented for years. A 2024 study found that boarding admitted patients nearly doubles the daily cost of their care. The triage door is not the choke point. The hospital floor upstairs is.

[CHART: ana_09]

### edt_04: A second story buried in the same file
**Evidence**: ana_12, ana_13, ana_16 | **Context**: det_05, det_09

[ana_12, det_05] Inside the same dataset is a measure that almost no commentary on it picks up: HCP_COVID_19, the share of a hospital's healthcare personnel who are up to date with COVID-19 vaccinations. The national median across states is 11.1%. Twenty states report 10% or less. Four states are at or below 5%.

[ana_13] Arkansas is at 2.7%. South Dakota 3.2%. Idaho 4.5%. North Dakota 5.0%. Puerto Rico — the same Puerto Rico with the second-longest ED time in America — is the lone outlier on the high end at 62%. The next-highest mainland state is Massachusetts at 46%. Below that, the distribution falls off a cliff.

[ana_16] The benchmark inside the same dataset is brutal. The mean state-level gap between flu coverage (IMM_3) and COVID coverage (HCP_COVID_19) for the same workforce is 65.6 percentage points. DC vaccinates 94% of its hospital workers against flu and 6.6% against COVID — an 87.4-percentage-point gap. Maine, South Dakota, and Maryland all sit in the 80s. The same employees, in the same buildings, getting one shot and not the other.

[CHART: ana_16]
[MEDIA: image]

### edt_05: Quality is not a single number
**Evidence**: ana_19, ana_18, ana_20, ana_10 | **Context**: det_06

[ana_19] Looking at all twelve process measures together is the most useful thing the dataset can do. Some are at the ceiling: severe-sepsis 6-hour bundle compliance has a national median of 91%, septic-shock 6-hour 84%, colonoscopy follow-up recommendations 93%. Others sit in stubborn middle bands: SEP_1 (the full 3-and-6-hour sepsis bundle) at 60.5%, OP-23 stroke imaging at 69%. And a few are at the floor: HCW COVID at 11%, walk-out rates at 2%.

[ana_18, det_06] SEP_1 is the most teachable case. Colorado leads at 73%, Maine at 72%, with Montana, Utah, and Hawaii all at 71%. At the bottom, Delaware and New Mexico tie at 48%, DC sits at 49%, and Puerto Rico is the dataset's extreme outlier at 16%. Sepsis kills more US hospital patients than any other condition; a 25-percentage-point spread between the best and second-worst US state is a clinical scandal hiding inside a routine reporting file.

[ana_20] The state-level Pearson correlation between SEP_1 and HCW COVID coverage is -0.56. The states that get sepsis right are not the states that get COVID right. This breaks the implicit "good hospitals do everything well" assumption that infuses most public hospital reporting. Different process measures answer to different organizational forces — bundles to clinical-protocol culture, vaccinations to mandate environments and staff trust.

[ana_10] OP-23 — the share of stroke patients who get a head CT or MRI within 45 minutes — has a 52-percentage-point spread, the widest of any higher-better measure in the file. South Carolina and Wisconsin lead at 78%; DC reports just 26%. A miss on this measure is not paperwork. It is a stroke patient who did not get imaged in the window where treatment is most effective.

[CHART: ana_19]

### edt_06: Reading the small print
**Evidence**: ana_02, ana_03 | **Context**: det_08, det_10

[ana_02, det_08] The four small territories — Northern Mariana Islands, American Samoa, US Virgin Islands, Guam — report essentially nothing. Each carries 22 missing rows under footnote 5. The 50 states + DC + PR form the working dataset. Among them, OP_31 (cataract vision improvement) is the only measure with severe coverage gaps — only 12 jurisdictions report it.

[ana_03] The 22 measure_ids partition into six CMS conditions. Emergency Department dominates with 12 measures; Sepsis Care contributes 5; Healthcare Personnel Vaccination contributes 2; Cataract, Colonoscopy, and the opioid Electronic Clinical Quality Measure contribute one each. Roughly 55% of the file is about how long an ER visit takes — a structural reflection of how much CMS now treats ED flow as the public face of hospital quality.

[det_10] Two footnotes change how to read the headline. Numbers 25 and 26 say that state and national averages include Veterans Health Administration and Department of Defense hospital data. A state's reported OP-18b is therefore a weighted average across civilian and federal facilities. The numbers are correct; they are just not pure civilian-system numbers.

### edt_07: What this file is really for
**Evidence**: ana_22, ana_19, ana_21 | **Context**: det_06

[ana_22, ana_19] Reorganized by what they actually measure, the 22 measure_ids form five groups: ED flow (12 measures), Sepsis (5), Vaccination (2), Outpatient procedures (cataract + colonoscopy, 2), and Pharmacy safety (1, the opioid co-prescribing measure). Three of these groups have wide state-level spreads with public-health stakes. Two are near the ceiling and serve mainly as comparison anchors.

[ana_21] Tucked into the file is one more uncomfortable signal. Concurrent opioid-and-benzodiazepine prescribing is highest in New Hampshire (19%), Massachusetts (18%), and Connecticut (18%) — the same New England that leads on most quality measures. Lowest in Puerto Rico, Mississippi, Arizona, DC, and Hawaii at 11% or below. Even regional-prescribing culture leaves a fingerprint here.

[editorial] The Visual Capitalist map that started this conversation answers one question: where is the wait longest? The CMS file underneath it answers a more useful one: which states have built hospital systems that wait, walk out, miss imaging windows, prescribe carelessly, vaccinate selectively — and which have not. State-level CMS reporting is a quiet, almost-public natural experiment in what American healthcare prioritizes. Five hours in a DC hallway is not a quirk of one city. It is what happens when capacity is full and almost no other measure in the file is moving fast enough to compensate.

## Editorial Notes
- The 310-minute DC figure and the 110-minute ND figure must appear exactly. They are the load-bearing claim of the entire piece.
- The 65.6 percentage-point COVID/flu gap and the -0.56 SEP_1/COVID correlation must remain visible — they are what distinguishes this blog from a one-finding ER-times piece.
- Caveat about VHA/DoD inclusion (det_08) should appear in the body of edt_06, not buried in a footnote.
- Territories MP/AS/VI/GU should appear as "missing-data" entries in the choropleth, never silently dropped.
- The 5h10m DC headline and the 1h50m ND comparison should be stated in human time units (hours and minutes), not just minutes, in the hook.
- Do not say "ER waits cause leaving" — both go up together; correlation, not causation.
