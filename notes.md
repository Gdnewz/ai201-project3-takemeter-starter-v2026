# TakeMeter: Notes (Unit 5)

## What I built
A four-label classifier for r/Fitness comments, fine-tuned locally with `distilbert-base-uncased`.
Labels: `prescription`, `analysis`, `motivation`, `other`. Data: 159 hand-labelled rows in `labels.csv`.

## Labelling rules that mattered
- Precedence: `analysis` > `prescription` > `motivation`. A tier counts only if the post meets that tier's own test.
- `prescription` = an instruction with sets, reps, days per week or weeks per phase, and no full-clause reason.
- `analysis` = a prescription plus a full-clause reason. The reason need not be about the sets and reps.
- `motivation` = argues that consistency matters, with no sets, reps, days or weeks. A gym-going tip that doesn't argue consistency is `other`.
- A report of what the author did ("I do 3 days a week") is `other`, not `prescription`.
- Hardest boundary: `prescription` vs `analysis`. Decide by asking whether there is a full-clause reason.
- Only use posts that make sense without their parent comment. Drop trivial one-liners.

## Data lessons
- Length can leak the label: my first rows had long `analysis` and short `prescription`. A length-only baseline could cheat. I shortened 17 rows.
- Final counts: `other` 61, `prescription` 44, `motivation` 29, `analysis` 25 (largest label 38.4%, cap is 70%).
- 159 rows is under the 200 the brief asks for. Say so in the README.
- Consistency check with a cold AI annotator: 15/20 (75%) overall, 18/20 (90%) on prescription vs analysis. The 80% target was missed and I did not lower it. The 3 other misses were hedged or implied instructions ("you could...").
- Every label must be real data. Never invent posts.

## Training lessons
- Split is stratified 70/15/15: 111 train, 24 val, 24 test. Test counts: `analysis` 4, `prescription` 7, `motivation` 4, `other` 9.
- Tiny test counts mean one post swings a label's F1 a lot. Expect big jumps between seeds.
- Defaults used: 3 epochs, lr 2e-5, batch 16, max length 128, seed 42. Ran on CPU in about 1 min 16 s.
- Loss going down means training is converging. It doesn't mean the model learned what I meant.
- First run: accuracy 0.417, macro F1 0.203. `analysis` and `motivation` F1 were 0.000. Validation loss only moved 1.33 to 1.27 over 21 steps (about 1.39 is chance), so it has barely learned.
- Don't change settings to chase a number. Write down what changed and why.

## Process lessons
- Write criteria and a prediction BEFORE seeing results. I wrote criteria first, but I ran the model before writing a prediction, and I said so in the README rather than backdating one.
- Never lower a missed target. Add revisions beneath the original criterion.
- Disclose all AI use: pre-labelling, drafting, notebook edits, and the AI second annotator.
- Reddit blocks my tools, so I pasted thread text myself.

## Commands and files
- Reopen: VS Code > File > Open Folder, open `takemeter.ipynb`, pick the `.venv` kernel. (`code` opened Notepad on my machine.)
- Commit: `git add <files>`, `git commit -m "..."`, `git push`.
- Commit `results.json`, `test_split.csv`, `labels.csv`, `criteria.md`, `README.md` and the notebook. Don't commit the practice `baseline_results.json`.
- `labels.csv` must be in the repo root, not in `data/`.
- Repo: https://github.com/Gdnewz/ai201-project3-takemeter-starter-v2026 (same URL for Unit 6, never recreate it).

## Next (Unit 6)
Baseline (definitions in `label_definitions.txt`), three seeds (42, 7, 2024), confusion matrix, staff agreement check, verdicts and diagnoses, one improvement.
