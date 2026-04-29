# Where Color Has a Name

## Story Spine

**Core claim**: When a million people each see a different patch of RGB and type one of five color words, the resulting map is overwhelmingly settled — but the small slivers where it isn't reveal the deepest things about how language, biology, and a glowing screen each shape what we see.

**Tension**: We tend to assume color naming is either arbitrary (any word would do) or universal (everyone sees the same red). The xkcd Color Survey shows it is neither — naming is consensus over 95% of color space and a battle over the rest, with each fault line predictable from physics and biology.

**Payoff**: After reading, the reader should hold three things at once: (1) where on the color wheel English vocabulary stops and starts, (2) why colorblind users say "pink" where everyone else says "purple", and (3) why the famously contested fuchsia-vs-magenta region resolves, in the data, into a clear 70/30 split.

## Sections

### edt_01: Hook — A million people, one of five words
**Evidence**: ana_01, ana_09 | **Context**: det_01, det_08

[det_01] In April 2010, Randall Munroe — author of the webcomic xkcd — asked the internet to name colors. Visitors saw a patch of RGB and typed whatever came to mind. Over five million names came in across 222,500 sessions. Fifteen years later, a curated slice of that experiment landed in TidyTuesday, and we can ask the question Munroe could only sketch in a blog post: when the same English-speaking population looks at the same color, when do they agree, and when do they not?

[ana_01] The slice is large. There are 949 colors in the canonical published list, 152,401 users with self-reported demographics, and 1,058,211 individual answers. To keep the file tractable, only one kind of answer was kept — the cases where the user typed one of the five most popular color words: purple, green, blue, pink, brown. Every row of the answers file is one human, one hex code, one of those five letters.

[ana_09, det_08] Among the million answers: green is the modal name 29.7% of the time, blue 27.2%, purple 23.6%, pink 12.4%, and brown 7.2%. Green and blue together cover 57% of the displayed-color space — they are the dominant naming territories. Brown and pink share the remaining warm wedge.

[CHART: ana_09]

### edt_02: How a name carves out a region of color space
**Evidence**: ana_10, ana_11, ana_12 | **Context**: det_07

[ana_12] If you bin the displayed hue into 10° slices and ask, in each slice, what fraction of users gave each name, you get a sharp picture: green dominates 80–140° at over 97%; blue owns 180–230° at over 90%; purple peaks above 95% near 280°; pink takes 320–340° above 90%. Brown lives in the warm wedge from 8° to 91°. The transitions are short: from "almost all green" to "almost all blue" takes maybe twenty degrees of hue.

[ana_10, ana_11] Each name's center of mass sits roughly where you'd expect. Brown is dim and warm — median hue 31°, value 0.54. Pink is the only name that lives in the bright pastel corner — median value 0.92. Blue and green have nearly equal saturation and brightness; what separates them is just hue. The 5th-to-95th-percentile hue ranges of the five names tile the color wheel with narrow overlaps: brown (8–91°), green (74–158°), blue (178–257°), purple (252–327°), pink (15–352° — the only wraparound).

[editorial] In other words, color names are not labels stuck to fixed points. They are claims to territory.

[CHART: ana_12]
[MEDIA: interactive]

### edt_03: Most of the cube is settled
**Evidence**: ana_13, ana_15, ana_24 | **Context**: det_07

[ana_13] Slice the RGB cube into 12×12×12 = 1,728 cells (each cell ~21 RGB units wide), keep the 1,606 cells with at least 50 answers, and ask: how dominant is the modal name in each cell? The mean winner share is 88.6%; the median is 95.8%. Half the cells have a name that wins by 95% or more. Only 14 cells (0.87%) drop below 50% winner share.

[ana_15] At the bullseye of each region, agreement is essentially perfect. RGB (10,176,10) — a vivid mid-green — got "green" from 1,473 of 1,473 different users. RGB (10,160,224) — a saturated sky blue — got "blue" from all 805 users who saw it. Pure pink at #f58a8a hits 99.9%; pure brown at #a04a0a, 100%.

[ana_24] The settled territory is the rule, not the exception. Roughly 95% of the well-sampled color cube has a clear winner. The disagreements live in the remaining 4–5%.

[CHART: ana_13]
[MEDIA: interactive]

### edt_04: The boundaries — where naming breaks down
**Evidence**: ana_14, ana_22 | **Context**: det_02, det_07

[ana_14] The contested cells trace every boundary on the color wheel. The single most ambiguous cell is true mid-grey, RGB (96,96,96): 33.9% purple, 25% brown, 23.2% blue, 16.1% green, 1.8% pink. With no anchor, the brain reaches in every direction. Just behind it sits #b58a8a (a dusty rose-grey: 35% purple, 32% pink, 31% brown — three names within four points of each other) and #75f5ca (a cyan-green: 50% green, 49% blue — perhaps the cleanest binary tie in the dataset).

[ana_22, det_02] One stretch of the boundary is famous in its own right. The pink-purple line — the region where fuchsia, magenta, and hot pink all live — has been a folk argument for as long as people have argued about colors on screens. The xkcd data resolves it. At hue 280° pure purple wins 95.4% of the time. At 300°, purple still wins 88.2%. By 320° pink takes over with 69%, and by 340° pink owns the territory at 90.5%. The crossover is around hue 310°. At the canonical "magenta" hue (~322° in xkcd's lexicon), the public votes pink over purple by roughly 2 to 1.

[CHART: ana_14]

### edt_05: Two X chromosomes name color slightly differently
**Evidence**: ana_16, ana_17, ana_18 | **Context**: det_03, det_06

[ana_17] Aggregate over all 1,045,000 cleanly-typed answers (spam_prob<0.5) and split by self-reported chromosome. Users with one Y chromosome say "blue" 26.42% of the time; users with two X chromosomes say "blue" 28.59%. The 2.17-percentage-point gap is the largest single-name difference. XX users say "green" slightly less (28.90% vs 30.05%) and "purple" slightly less (23.11% vs 23.84%). The differences are small, robust, and directionally consistent with prior linguistic research showing women apply finer green/blue distinctions.

[ana_16] At the cell level the median XY-vs-XX divergence is just 0.017 — most cells are named identically. But about 4% of well-sampled cells diverge by more than 0.20. The single most divergent cell, #203535 (a dark teal-grey), has 68% of XY users saying "green" while 65% of XX users say "blue". Other strongly divergent cells sit in pink/purple/brown borderlands where XX users converge harder on a single name and XY users spread their answers more evenly.

[ana_18, det_06] One caveat eats half the chromosome story. Among users with spam-probability above 0.75, 81.5% are XY — almost ten percentage points above the 71% baseline XY share. Munroe's 2010 quip ("the most masculine color names were 'penis', 'gay', 'WTF', 'dunno'") was real, and its statistical shadow falls across any naive XY/XX comparison. The aggregate 2-pp gap on "blue" and the 0.04-mean cell divergence are reported here only after stripping high-spam users. The patterns survive that cut. They probably wouldn't survive much more.

[CHART: ana_17]

### edt_06: The colorblind fingerprint
**Evidence**: ana_19, ana_20, ana_23 | **Context**: det_03, det_11

[ana_19] Now split the same 1.04 million answers by the colorblind self-report. The cell-level mean naming divergence triples — from 0.040 (XY vs XX) to 0.117 (colorblind vs not). Aggregate: colorblind users say "green" at 32.16% (+2.62 pp), "pink" at 15.60% (+3.36 pp), and "purple" at just 17.99% (-5.94 pp). Where non-colorblind users see purple, colorblind users see pink.

[ana_20] The cell-level signal is the strongest finding in the dataset. At RGB ~(181,160,202) — a soft lilac — colorblind users say "pink" 56.5% of the time while non-colorblind users say "purple" 87.4%. At #cab5e0 (lavender-ice) the swap is 52% pink vs 82% purple. At #203520 and #20350a — two dark, slightly green-tinged shades — colorblind users say "brown" while non-colorblind users say "green" with 96–97% conviction. Both shifts have a clean physical explanation: red-green color blindness compresses the perceptual gap between purple and pink (both have red components) and between dark green and brown (both are dim warm-leaning).

[ana_23, det_11] The colorblind subsample itself is unusual. Population studies put red-green color blindness at roughly 8% of XY individuals and 0.5% of XX — a 16x ratio. In the xkcd data the rate is 4.99% in XY and 1.085% in XX, a ratio of 4.6x. The xkcd colorblind users are far fewer than a representative sample would suggest, almost certainly because XY users with mild deficiency don't categorize themselves as "colorblind" while XX users at the curious end self-select in. The naming differences are still real — but the population they're estimated on is not the general population.

[CHART: ana_19]
[MEDIA: interactive]

### edt_07: A small but visible monitor effect
**Evidence**: ana_21, ana_02 | **Context**: det_05

[ana_02, ana_21] In 2010 the survey caught the tail end of the CRT-to-LCD transition. 95.8% of users were on LCDs, 3.9% on CRTs. The same color rendered on the two technologies looks subtly different — phosphors versus backlit liquid crystals — and the naming follows. CRT users say "green" 32.67% of the time vs 29.58% on LCD (+3.09 pp), say "brown" 8.53% vs 7.13% (+1.40 pp), and say "pink" 10.21% vs 12.50% (-2.29 pp). On warmer, dimmer CRTs, ambiguous pinks read as browns or reds; greens look more saturated.

[editorial] The effect size is smaller than the chromosome effect, smaller still than the colorblind effect, but cleanly directional — and it's a useful reminder that "the color we see" is always partly a property of the screen.

[CHART: ana_21]

### edt_08: A vocabulary, not a list
**Evidence**: ana_04, ana_05, ana_06, ana_07, ana_08, ana_25 | **Context**: det_04, det_09

[ana_04] Behind the million answers sits the canonical 949-color list — the part of this dataset that has had a real cultural afterlife. Purple is rank 1, green 2, blue 3, pink 4, brown 5, red 6. The first 30 entries are dominated by basic English color terms and a small set of culturally entrenched secondary names: teal, magenta, turquoise, lavender, mauve, maroon, olive.

[ana_05] The 949 named hexes do not tile the color wheel evenly. Yellow leads with 152 named colors (a long compositional family: gold, mustard, ochre, butter, lemon, banana). The saturated purple wedge — between blue and magenta — has just 47. The achromatic axis has 11: black, white, six greys, charcoal, silver, "very light pink".

[ana_06, ana_07] 72.5% of the names are multi-word compounds. The most productive modifiers are light (67 names), dark (60), pale (28), bright (23), deep (17). The most productive heads are green (170 names end in "green"), blue (110), pink (52), purple (47), brown (44). English compounds colors compositionally — and green and blue together anchor 280 of the 687 compound names, more than 40% of the multi-word vocabulary.

[ana_25, det_09] These 949 colors and their hex codes are now baked into the visual culture of computing. matplotlib's "xkcd:" palette, R's xkcdcolors package, design tools, and academic visualization papers all reference them. The survey's quirks — the over-representation of dusty pastels, the dominance of compound names, the absence of culturally specific colors common in other languages — have been quietly inherited by every chart that uses xkcd:cerulean.

[CHART: ana_06]

### edt_09: Closing — what 1,473 people called green
**Evidence**: ana_15, ana_14 | **Context**: det_07

[ana_15] At RGB (10,176,10), one specific patch of the green territory, 1,473 different humans on different monitors with different chromosomes and different colorblindness profiles all typed the same word. They typed "green". Not "leaf green", not "kelly green", not "bright green" — those answers existed and were filtered out of this dataset. They typed the basic word.

[ana_14] At RGB (96,96,96), a different specific patch, 56 humans typed five different words. 19 said "purple". 14 said "brown". 13 said "blue". 9 said "green". One said "pink".

[editorial] Both kinds of patch are everywhere on a screen. The xkcd Color Survey is the rare project where the boring part — that 95% of color space is named the same way by almost everyone — is not the finding to discount. It is the foundation against which the small, specific, biologically and physically explicable disagreements show up at all.

## Editorial Notes
- The 1,058,211 / 1,045,000 / 152,401 figures must be exact.
- 949 (not 954) is the right canonical color count — TidyTuesday released 949 rows; xkcd's blog post sometimes says ~954.
- Always note the chromosome × spam confound somewhere in edt_05.
- The colorblind ratio benchmark (~16x) and observed (~4.6x) must both appear in edt_06.
- Hue values throughout are degrees of HSV. Keep this consistent.
- Section edt_03 and edt_04 are load-bearing — the "settled vs contested" framing is the spine of the argument.
- Numbers in ana_19's aggregate diff (purple -5.94, pink +3.36, green +2.62) should appear verbatim.
