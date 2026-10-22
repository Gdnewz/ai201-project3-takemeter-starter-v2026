# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

TakeMeter reads posts and comments from r/Fitness, the fitness community on
Reddit, and sorts each one into one of four labels:
`prescription` (tells the reader what sets, reps, days or phase lengths to
use), `analysis` (gives that prescription plus a reason for it),
`motivation` (argues that consistency or adherence is what matters, with no
training instruction), and `other` (everything else). It runs locally with no
hosted model. I chose these labels because the same community mixes advice
that says what to do, advice that says why, and advice about sticking with it,
and I wanted to see whether a small model can tell them apart.

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

Each post gets exactly one label. If a post meets more than one, the highest
tier wins: `analysis` > `prescription` > `motivation`. A tier only counts if
the post meets that tier's own test. A post or comment is only included if it
can be labelled without reading the comment above it, so replies that depend
on a parent comment are dropped.

### `prescription`

**Definition:** The post tells the reader to do something by giving at least
one of sets, reps, days per week, or weeks per training phase as an
instruction, without a full-clause reason for it (a goal word like "for
hypertrophy" or an adjective like "brutal" is allowed). A report of what the
author did does not count.

**Example 1:**
> "A main lift a day. Do ~10 sets total in your main lift, ramping up to a
> top weight and then doing ~5 backoff sets. On squat/deadlift days, every
> set turns into a giant set where you'll superset with a push, a pull and a
> core exercise for 10+ reps." (r/Fitness comment, shortened. Sets and reps
> as an instruction, no reason.)

**Example 2:**
> "Fierce 5, SL 5x5, icf 5x5. Choose one. 45mins to complete" (r/Fitness
> comment. A program with sets and reps, no reason.)

### `analysis`

**Definition:** The post gives a prescription (at least one of sets, reps,
days per week, or weeks per phase) AND gives a full-clause reason for why the
routine or prescription is worth doing ("because", "so that", "this
targets"); the reason does not have to be about the sets and reps
specifically.

**Example 1:**
> "Instead of going on some 9 month long suicide cut because you STILL don't
> have abs, dedicate 16 weeks to a gaining phase… Once it's done, give
> yourself 4 weeks to stabilize and then plan a 12 week fat loss phase… during
> the mass building phase, the training is HARD because we have the nutrition
> to support it." (r/Fitness comment, shortened)

**Example 2:**
> "5/3/1 Building the Monolith. 3 days is far more than enough.. you would
> probably die if you did it 5/6 days a week due to the 20+ rep squats you
> have to do at the end of the week." (r/Fitness comment. Days per week as an
> instruction, plus a reason.)

### `motivation`

**Definition:** The post argues that consistency or adherence is what
matters, and gives no sets, reps, days per week, or weeks-per-phase
instruction. A tip for getting to the gym ("go straight after work") that
never argues consistency matters is `other`.

**Example 1:**
> "You can start small and still make meaningful differences if you just stay
> diligent and consistent." (r/Fitness post)

**Example 2:**
> "Timelines of doing something within weeks turn to burnout and failure.
> Timelines of months to years lead to real change." (r/Fitness comment)

### `other`

**Definition:** Anything that fits none of the above: questions, experience
reports with no instruction to the reader, and posts that give a reason or
mechanism but no prescription.

**Example 1:**
> "started eating like two bananas and some rice cakes an hour before lifting
> instead of training fasted… honestly the energy spike was weird at first
> but then I hit PRs on bench that I'd been stuck on for months." (r/Fitness
> comment, shortened. An experience report, no instruction to the reader.)

**Example 2:**
> "Full body strength training twice per week, yoga one evening per week,
> tabata/hiit once per week, running five days a week. Three of those days
> are two-a-days." (r/Fitness comment. Reports the author's own week, no
> instruction to the reader.)

### The hardest boundary

**Which two labels:** `prescription` and `analysis`

**The decision rule I used every time:**
If the post gives a prescription AND a full-clause reason for why the routine
is worth doing, it is `analysis`, even if the reason is not about the sets
and reps. If it has only a goal word or an adjective ("for hypertrophy",
"brutal"), it stays `prescription`.

---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** Comments and posts from r/Fitness, including
beginner-routine and "is 3 days a week enough" threads, where people give sets,
reps and days, and general-advice threads for `motivation` and `other`.
Replies that only make sense with their parent comment were dropped.

**How I labelled them:** Claude pre-labelled the rows; I did not label all 159
cold myself. I pasted the page text of r/Fitness threads into the chat. Claude
picked short comments that make sense on their own (replies that need the
parent comment were dropped, and so were trivial one-liners like "Yes!"),
shortened any over about 100 words, and labelled each one cold from my label
definitions, with a note on borderline rows. I did my own labels on the first
practice batch and compared them with Claude's, and I made the calls on the
rules that came out of it: a report of what the author did is `other`, a tip
for getting to the gym that never argues consistency matters is `other`, and
the precedence is `analysis` > `prescription` > `motivation`.
For the rows after that first batch, I did not label them cold myself and I
did not go back and re-check every one by hand. What I did was supply the
threads, read the notes Claude put on borderline rows, and decide the rules
when a post exposed a gap (the three rules above, plus the length fix in
"How I Used AI"). I did not keep a count of rows I changed individually, so I
am not claiming one. I also chose not to do my own blind re-label of a sample;
the second-annotator check below is an AI one, not a human one, and that is a
limit on how far these labels can be trusted. `other` was sampled, not
collected exhaustively, so its share is not its share of the real community.

After the file was built I ran a consistency check. A fresh second annotator
(an AI model that had not seen my labels) labelled 20 hard `prescription` and
`analysis` posts from my definitions alone. It agreed with my labels on 15 of
20 (75%), and on 18 of 20 (90%) if the question is only `prescription` versus
`analysis`. The other 3 disagreements were hedged or implied instructions
("you could do...", "may be slightly better...") that it called `other`. My
criterion 3 asked for 80% overall, so on this deliberately hard sample that is
a miss, and I am leaving the target where it is. Merging labels would have
fixed only 2 of the 5 disagreements, so I kept four labels.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `prescription` | 44 | 27.7% |
| `analysis` | 25 | 15.7% |
| `motivation` | 29 | 18.2% |
| `other` | 61 | 38.4% |
| **Total** | 159 | 100% |

This is 159 rows, which is under the 200 the brief asks for (and over the 150
floor in the checklist). I stopped at 159 and am saying so here rather than
hiding it. The cost is small test splits, which is why `analysis` and
`motivation` have only 4 test posts each.

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* "The 5 toughest workout routines that exist, in my opinion"
> (r/Fitness)
>
> *Could have been:* `prescription` or `analysis`
>
> *I chose, because:* `analysis`. It gives phase lengths in weeks as an
> instruction and a full-clause reason for them, and under my rule the reason
> does not have to be about the sets and reps.

**2.**
> *The post:* "I do bodyweight work, three days a week. Hits every muscle,
> and since my goal is functionality not hypertrophy, that's perfect. Look
> into the RR over at r/bodyweightfitness" (r/Fitness comment)
>
> *Could have been:* `analysis` or `other`
>
> *I chose, because:* `other`. The days and the "since my goal…" reason
> describe what the author does, not what the reader should do, and my rule
> says a report of what the author did does not count as a prescription. "Look
> into the RR" has no sets, reps, days or weeks, so it does not meet the
> prescription test either.

**3.**
> *The post:* "go straight after work, don't go home first. I take my gym
> stuff to work, and get shit done." (r/Fitness comment, from a thread on
> getting motivated after a long workday)
>
> *Could have been:* `motivation` or `other`
>
> *I chose, because:* `other`. It is advice about getting to the gym, so it
> looks like `motivation`, but my `motivation` definition says the post must
> argue that consistency or adherence matters. This one only gives a tactic
> and never argues that, and it has no sets, reps, days or weeks, so it is not
> `prescription` either. I applied the same rule to "Go straight from work…
> you'll be tempted to sit on the couch", which gives a reason but no
> prescription.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`, fine-tuned locally with the
notebook's training cell. No hosted model.

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, max length 128,
seed 42. Trained on CPU (no GPU), torch 2.14.1+cpu, in about 1 minute 16
seconds.

**Anything I changed from the defaults, and why:** Nothing. I left every
setting at the notebook's default for this first run. I only filled in my
name, email and `LABELS` (`analysis`, `prescription`, `motivation`, `other`),
and pointed it at my own `labels.csv`.

**Split sizes:** 111 train / 24 validation / 24 test (stratified 70/15/15 on
my 159 rows, seed 42). Per-label counts in the test split: `analysis` 4,
`prescription` 7, `motivation` 4, `other` 9. Three of the four labels have
fewer than about 8 posts in test (`analysis` and `motivation` only 4 each), so
one post changes a label's F1 a lot. I expect those scores to move a great
deal between seeds in Unit 6. `results.json` and `test_split.csv` from this
run are committed.

**What the first run produced (seed 42, from `results.json`):** accuracy 0.417
and macro F1 0.203 on the 24 test posts. Per-label F1: `other` 0.562 (n=9),
`prescription` 0.250 (n=7), `analysis` 0.000 (n=4), `motivation` 0.000 (n=4).
Validation loss only went from 1.33 to 1.27 over 3 epochs (21 training steps),
and validation macro F1 fell from 0.203 to 0.136, so this is a model that has barely
started learning, not a finished result. The model was right 0.625 of the time
on its most confident third of test posts and 0.250 on its least confident
third. I have not looked at the confusion matrix yet and I have not run the
baseline or the other two seeds; those are Unit 6. I did not change any
setting to chase these numbers, and my criteria were written before this run.



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* Whether a comment where someone listed their own sets and
  reps (the Myrddwn post) counted as `prescription`.
- *What came back:* Claude pointed out that it only reports what the author did,
  so it fails my own `prescription` test, even though it has numbers.
- *What I changed:* I relabelled it `other` and added "a report of what the
  author did does not count" to my `prescription` definition. It is now hard
  case 2.

**Moment 2**

- *What I asked for:* A first `labels.csv` built from the threads I had read.
- *What came back:* 47 rows where the `analysis` and `motivation` rows were much
  longer than the `prescription` rows, which a length-only baseline could use
  to cheat criterion 4.
- *What I changed:* I asked for shorter rows. Claude shortened the 17 rows over
  about 100 words, and I added short `prescription` and `analysis` comments
  from new threads.

**Pre-labelling disclosure:** Claude pre-labelled every row in `labels.csv` from
threads I pasted, using my definitions. Rows I thought were borderline have a
note in the `note` column. I did not
label the later rows myself or correct them one by one; my part was supplying
the threads, setting the rules, and ruling on the borderline cases Claude
flagged. A second AI annotator, which never saw my labels, did the 20-post
consistency check described above. Claude also helped me draft the wording of
`criteria.md` and this README (I supplied the counts, rules and results it was
based on), and it made the name, email and `LABELS` edits in `takemeter.ipynb`;
I ran the notebook and the git commands myself.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.125 | 0.417 | +0.292 |
| Macro F1 | 0.196 | 0.203 | +0.007 |
| F1 — `analysis` | 0.118 | 0.000 | -0.118 |
| F1 — `motivation` | 0.667 | 0.000 | -0.667 |
| F1 — `other` | 0.000 | 0.562 | +0.562 |
| F1 — `prescription` | 0.000 | 0.250 | +0.250 |

**What I predicted before I looked:**

I predicted my trained model would mostly win on `motivation`, since it
seemed easiest to detect, and would struggle more to beat the baseline on
`analysis` and `prescription`, since those two can look alike.

**What the gap actually means:**

The prediction was wrong in an instructive way. `motivation` didn't hold —
it went from the baseline's best score (0.667) to 0.000 trained, and
`analysis` also dropped slightly rather than improving. The real gains came
on `other` and `prescription`, which I didn't predict. Overall accuracy
jumped a lot (+0.292), but macro F1 barely moved (+0.007), so the trained
model mostly got better at the majority class (`other`) while collapsing on
the two labels with only 4 test posts each (`analysis`, `motivation`) — a
handful of wrong calls on that few posts swings F1 hard, which is the same
small-test-count risk I flagged back in the training run notes. I also ran
the baseline with and without `--definitions`: both gave identical numbers
(0.125 accuracy, 0.196 macro F1), meaning my label definitions added nothing
measurable over bare label names for this general model.


---
### Device

cpu (CPU), torch 2.14.1+cpu

### Spread across three seeds

| Seed | Accuracy | Macro F1 |
|---|---|---|
| 42 | 0.417 | 0.203 |
| 7 | 0.375 | 0.136 |
| 2024 | 0.333 | 0.125 |

Accuracy swings about 8.4 points across the three seeds (0.417 to 0.333) —
under the ~10-point flag the notebook warns about, but close to it given how
small this test split is (24 posts).

### Confusion matrix

| true \ predicted | analysis | prescription | motivation | other |
|---|---|---|---|---|
| **analysis** | 0 | 0 | 0 | 4 |
| **prescription** | 0 | 1 | 0 | 6 |
| **motivation** | 0 | 0 | 0 | 4 |
| **other** | 0 | 0 | 0 | 9 |

**My biggest off-diagonal number, and what it means:**

The biggest confusion is 6 real `prescription` posts called `other`, with 0
going the other direction. The model essentially collapsed toward predicting
`other` across the board — it only got `prescription` right once, and never
predicted `analysis` or `motivation` for any post at all. That's not one
blurry boundary; the model hasn't learned to distinguish any of the three
instruction-bearing labels from the catch-all `other` class yet.



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [x] criteria.md has five numbered criteria, each naming a NUMBER
       [x] Each has a reason underneath tied to your data or taxonomy
       [x] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [x] No label above 70%
       [x] All five unit 5 sections have real content
       [x] Label Taxonomy includes the decision rule for your hardest boundary
       [x] The Dataset includes three hard cases
       [x] results.json and test_split.csv committed (the notebook does this)
       [x] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN
           https://github.com/Gdnewz/ai201-project3-takemeter-starter-v2026

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**