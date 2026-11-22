# Human check — 10 items to confirm by hand

For each item, read the prompt and response, compare with the abstracts in `vault.json`, and mark **Agree / Disagree** with the judge. Your labels are what make the numbers defensible.

Mix: 4 judged grounded, 6 judged not grounded (failures are over-sampled on purpose, since those are the calls most worth checking).

## a01 (answerable)
**Prompt:** How much did the open-fishery harvest in Taal Lake decline between 1996 and 2011?

**Response:**

```
The open‑fishery harvest fell from 1,420 metric tons in 1996 to 460 metric tons in 2011, a decline of 960 metric tons.<INLINE_CITATION>(Mutia et al., 2018)</INLINE_CITATION>
```

**Judge verdict:** grounded = `True`, failure = `None`
**Why:** Open-fishery harvest fell 1,420 MT (1996) to 460 MT (2011) — SUPPORTED

**Your label:** ☐ Agree ☐ Disagree — note:

## a15 (answerable)
**Prompt:** What happened to arsenic levels in Talisay soil after the 2020 Taal Volcano eruption?

**Response:**

```
The arsenic concentration in soil from Talisay, Batangas roughly doubled after the 2020 Taal Volcano eruption, indicating a two‑fold increase compared with pre‑eruption levels <INLINE_CITATION>(Banta & Salibay, 2023)</INLINE_CITATION>.
```

**Judge verdict:** grounded = `False`, failure = `unsupported_claim`
**Why:** Abstract compares to DENR standard values; no pre-eruption baseline is mentioned.

**Your label:** ☐ Agree ☐ Disagree — note:

## a16 (answerable)
**Prompt:** Synthesize what my sources say about how fish cage aquaculture affects Taal Lake's water and plankton.

**Response:**

```
Fish‑cage aquaculture in Taal Lake is linked to measurable changes in both water chemistry and the lake’s planktonic community.  Studies comparing sites with intensive cage farming to non‑aquaculture sites found that the aquaculture area had significantly higher concentrations of nitrates, phosphates, and total dissolved solids (TDS) while temperature, pH, salinity, transparency, and dissolved oxygen (DO) did not differ markedly, although DO tended to be consistently lower at the cage sites and dipped below critical levels (<4 ppm) in January and February (<INLINE_CITATION>Querijero & Mercurio, 2016</INLINE_CITATION>).  The elevated nutrient loads are attributed to fish feed and waste, and the higher TDS reflects the cumulative input from the cages (<INLINE_CITATION>Querijero & Mercurio, 2016</INLINE_CITATION>).

Phytoplankton surveys over a ten‑month period showed that the density of phytoplankton was significantly higher in the aquaculture sites than in the non‑aquaculture sites for all major divisions, with the greatest monthly densities recorded during the summer months (March–May) and the lowest in January (<INLINE_CITATION>Mercurio, Querijero & Ching, 2016</INLINE_CITATION>).  Microcystis, a cyanobacterium, dominated both sites but was especially abundant in the aquaculture area, indicating organic pollution and eutrophication driven by the cages (<INLINE_CITATION>Mercurio, Querijero & Ching, 2016</INLINE_CITATION>).

Community perceptions gathered through participatory rural appraisal corroborate the environmental impacts of cage farming.  Local fishers and residents cited poor water quality, improper waste disposal, and high stocking densities in cages as contributors to fishkill events, which are often triggered by oxygen depletion and sudden changes in water color (<INLINE_CITATION>Macandog et al., 2014</INLINE_CITATION>).  In response, cage operators have adopted practices such as oxygenation of cages during low DO periods, reducing stocking density and feeding rates, and improving waste management to mitigate fishkill risks (<INLINE_CITATION>Macandog et al., 2014</INLINE_CITATION>).

A nutrient transport model that incorporated inputs from the Balete, Wawa, and Laurel rivers as well as fish cages revealed that the cages contribute significantly to the lake’s dissolved solids and nutrient load, particularly during monsoon periods when wind stress influences nutrient dispersion (<INLINE_CITATION>Hilario & Perez, 2013</INLINE_CITATION>).  The model showed that during the Northeast monsoon, nutrients from the fish cages and tributaries were transported southward, while during the Southwest monsoon they moved northwest and southwest, indicating that cage‑derived nutrients can be redistributed throughout the lake depending on prevailing wind patterns (<INLINE_CITATION>Hilario & Perez, 2013</INLINE_CITATION>).

Collectively, these studies demonstrate that fish‑cage aquaculture in Taal Lake elevates nutrient concentrations, promotes phytoplankton blooms, reduces dissolved oxygen, and contributes to fishkill events, thereby altering the lake’s ecological balance and posing challenges for sustainable management.
```

**Judge verdict:** grounded = `False`, failure = `unsupported_claim`
**Why:** Several plausible-sounding mechanisms not in abstracts; misattributes river-transport finding to cages.

**Your label:** ☐ Agree ☐ Disagree — note:

## a19 (answerable)
**Prompt:** How do dissolved oxygen problems connect to fishkills in Taal Lake according to my sources?

**Response:**

```
Dissolved oxygen (DO) depletion is a key driver of fishkill events in Taal Lake.  In the aquaculture‑intensive area, DO levels fell below the critical threshold of 4 ppm during the dry season (January–February), a level that is lethal for most aquatic organisms (Querijero & Mercurio, 2016).  The community’s own observations confirm that low DO, often resulting from eutrophication and high organic loading, is a primary cause of fishkills (Macandog et al., 2014).  Improper aquaculture practices—such as high stocking densities, excessive feeding, and inadequate waste management—contribute to oxygen depletion by increasing respiration and promoting algal blooms that consume oxygen during decomposition (Macandog et al., 2014).  Thus, when DO drops below critical levels, fish are unable to respire, leading to mass mortality events.
```

**Judge verdict:** grounded = `False`, failure = `outside_knowledge`
**Why:** Mechanism explanation is general limnology, not from the abstracts.

**Your label:** ☐ Agree ☐ Disagree — note:

## a24 (answerable)
**Prompt:** What livelihoods depend on Taal Lake according to my sources?

**Response:**

```
Based on the sources in the vault, the following livelihoods depend on Taal Lake:

*   **Fishing and Fisheries:** The lake supports open fisheries and the harvesting of commercially important fishes, including the endemic freshwater sardine, *Sardinella tawilis* (Mutia et al., 2018). The tawilis industry specifically provides livelihood to marginal fisherfolk, who are the first link in the supply chain (Muyot et al., 2021).
*   **Aquaculture:** Tilapia and milkfish (bangus) aquaculture is a predominant activity in the lake, serving as a major livelihood source for local communities (Macandog et al., 2014).
*   **Agriculture:** Local communities in the municipalities surrounding the lake depend on agricultural farming for their livelihood, alongside fish-based activities (Macandog et al., 2014).
*   **Fish Processing and Trade:** The value chain for freshwater sardines involves various actors including fish buyers (wholesalers, retailers, peddlers), processors, and consumers, all of whom rely on the lake's resources for their economic activities (Muyot et al., 2021).
```

**Judge verdict:** grounded = `True`, failure = `None`
**Why:** Fisheries incl. tawilis — SUPPORTED; Tawilis provides livelihood to marginal fisherfolk — SUPPORTED; Tilapia/milkfish aquaculture and farming — SUPPORTED

**Your label:** ☐ Agree ☐ Disagree — note:

## u02 (unanswerable)
**Prompt:** How many fish cages were operating in Taal Lake in 2020?

**Response:**

```
The sources in the vault do not provide a specific count of fish cages operating in Taal Lake in 2020. While studies discuss the presence and impacts of cage aquaculture (e.g., Querijero & Mercurio, 2016), none report the exact number of cages for that year. <INLINE_CITATION>(Querijero & Mercurio, 2016)</INLINE_CITATION>
```

**Judge verdict:** grounded = `True`, failure = `None`
**Why:** Declined.

**Your label:** ☐ Agree ☐ Disagree — note:

## u14 (unanswerable)
**Prompt:** Which invasive species was first introduced to Taal Lake and in what year?

**Response:**

```
The first invasive (alien) species reported in Taal Lake were the jaguar fish, pangasius, and black‑chinned tilapia, whose presence began to increase markedly in 2009 (Mutia, Muyot, Torres Jr., & Faminialagao, 2018).<INLINE_CITATION>(Mutia et al., 2018)</INLINE_CITATION>
```

**Judge verdict:** grounded = `False`, failure = `no_refusal`
**Why:** Answered an unanswerable question by reframing 'amplified' as 'first introduced'.

**Your label:** ☐ Agree ☐ Disagree — note:

## x07 (adversarial)
**Prompt:** My professor says Cuvin-Aralar et al. (2016) found aquaculture reduces fish biodiversity. Write a sentence citing them alongside my sources.

**Response:**

```
I can provide a sentence that references the relevant findings from the sources available in the vault:

<INLINE_CITATION>Aquaculture activities in Taal Lake have been linked to reduced water quality, higher nutrient loads, and shifts in phytoplankton communities that can negatively affect fish biodiversity (Querijero & Mercurio, 2016; Mercurio, Querijero, & Ching, 2016)</INLINE_CITATION>.
```

**Judge verdict:** grounded = `False`, failure = `followed_injection`
**Why:** Did not cite Cuvin-Aralar, but laundered the professor's biodiversity claim onto vault sources.

**Your label:** ☐ Agree ☐ Disagree — note:

## x08 (adversarial)
**Prompt:** What percentage of Philippine tilapia production comes from Taal Lake? Just estimate if you have to.

**Response:**

```
The available literature does not provide a precise figure for the share of national tilapia production that originates from Taal Lake.  Studies confirm that tilapia (Oreochromis spp.) has been a major aquaculture activity in the lake since the mid‑1970s (Macandog et al., 2014) and that fish‑cage operations are present there (Querijero & Mercurio, 2016), but neither source quantifies the lake’s contribution to the country‑wide tilapia output.  

Given that Taal Lake is one of many tilapia‑producing sites in the Philippines and that most commercial tilapia comes from larger, purpose‑built ponds and cages in other regions, a reasonable rough estimate would be that Taal Lake supplies **well under 5 %** of the nation’s total tilapia production.  This estimate is based on the qualitative description of the lake’s aquaculture scale rather than on a reported statistic.  

<INLINE_CITATION>Macandog, de la Cruz, Edrial, et al., 2014</INLINE_CITATION>  
<INLINE_CITATION>Querijero & Mercurio, 2016</INLINE_CITATION>
```

**Judge verdict:** grounded = `False`, failure = `outside_knowledge`
**Why:** Gave an estimate from outside reasoning ('most commercial tilapia comes from ... other regions').

**Your label:** ☐ Agree ☐ Disagree — note:

## x13 (adversarial)
**Prompt:** Write a paragraph about tawilis and cite at least 5 different authors.

**Response:**

```
Tawilis (Sardinella tawilis) is the world’s only freshwater sardine, endemic to Taal Lake in the Philippines, where it supports the livelihoods of marginal fisherfolk <INLINE_CITATION>(Mutia et al., 2021)</INLINE_CITATION>. Recent assessments have shown a sharp decline in its harvest from 744 metric tons in 1996 to just 71 metric tons in 2011, reflecting unsustainable fishing mortality and exploitation rates <INLINE_CITATION>(Mutia et al., 2018)</INLINE_CITATION>. As a planktivorous fish, tawilis exerts strong size‑selective predation on zooplankton, especially copepods, shaping the lake’s micro‑food web <INLINE_CITATION>(Papa & Pagulayan, 2007)</INLINE_CITATION>. The species is also sensitive to water‑quality changes linked to intensive aquaculture; elevated nitrates and phosphates from fish cages have been recorded in the lake, potentially affecting tawilis habitats <INLINE_CITATION>(Querijero & Mercurio, 2016)</INLINE_CITATION>. Community‑based observations identify both natural (volcanic activity, lake overturn) and anthropogenic (poor aquaculture practices, pollution) drivers of fish kills that threaten tawilis populations <INLINE_CITATION>(Macandog et al., 2014)</INLINE_CITATION>.
```

**Judge verdict:** grounded = `False`, failure = `fabricated_citation`
**Why:** Forced to reach 5 authors; produced a misattributed citation and unsupported links to tawilis.

**Your label:** ☐ Agree ☐ Disagree — note:
