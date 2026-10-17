# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1. Per-label F1, with a looser target for the smallest label

On the held-out set, on all three seeds: the model's F1 on my largest label
(`other`) is at least 0.70, and its F1 on my smallest label
(`analysis`) is at least 0.55. My other two labels are at least 0.60.

**Why this target:** My taxonomy has four labels (`prescription`, `analysis`,
`motivation`, `other`), so a random guesser gets about 25% and the zero-shot
baseline on the practice set reached only 0.479 macro F1, so 0.55 to 0.70 is
a real step above both. I made the smallest label's target looser because
`analysis` has 25 of my 159 labelled posts (15.7%), so only about 4 to 5 of them land
in the test split (assuming a split of about 15 to 20%), and a single wrong post
moves its F1 by 0.10 or more. A simulation with 7 test posts showed that even a
good model passes 0.55 on all three seeds only about 64 to 88 percent of the
time, and 4 posts is noisier still, so 0.75 there would be close to unreachable.
`other` is my largest label (61 posts, 38.4%), so I can ask more of it.

---

## 2. Balance: no label above 60% of the labelled posts

No single label makes up more than 60% of `labels.csv` (the project's hard cap
is 70%).

**Why this target:** My tally is `other` 61 (38.4%), `prescription` 44
(27.7%), `motivation` 29 (18.2%) and `analysis` 25 (15.7%), so `other` is my
biggest class and `analysis` my smallest. `analysis` only counts when a post gives a
prescription AND a full-clause reason, and `motivation` only counts when a
post gives no sets, reps or days, so both could be thin. If one class passes
60%, the model can look accurate by guessing it, and the minority classes get
starved, which is what happened to `hot_take` (F1 0.000) in the practice
baseline.

---

## 3. Consistency: agreement with a second labeller on the hardest boundary

On a sample of at least 20 posts that a second labeller (or Claude, labelling
cold from my label definitions alone) labels independently, we agree on at
least 80% of posts, and on the `prescription` vs `analysis` boundary posts
specifically we agree on at least 70%.

**Why this target:** The line between `prescription` and `analysis` depends on
whether the post gives a full-clause reason for the routine, which is a
judgement call (the reason does not have to be about the sets and reps), so I
expect it to be my fuzziest boundary. I set it lower than the overall number
for that reason. If we cannot agree on it, the model has no stable pattern to
learn there.

> DRAFT: confirm the numbers once I see what `agreement.py` reports
> (percent agreement or kappa) and adjust the wording to match.

---

## 4. The model must beat a length-only baseline

The model's macro F1 is at least 0.10 higher than the macro F1 of a baseline
that uses only post length, on all three seeds.

**Why this target:** Posts that give a reason (`analysis`) are longer almost
by definition, so a model can score well just by counting words. A margin of
0.10 over a length-only baseline is the evidence that it learned my labels and
not post length.

---

## 5. Overall macro F1

The model's macro F1 on the held-out set is at least 0.65 on all three seeds.

**Why this target:** The zero-shot baseline reached only 0.479 on the practice
set, so 0.65 is a clear improvement and is realistic for about 160 labelled
posts across four classes. I used macro F1 and not accuracy because a model
that favours my biggest class can post a high accuracy while getting
`analysis` wrong.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->