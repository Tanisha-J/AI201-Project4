# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## Stretch Features

- **`GET /content/<id>`** — returns one item's current status (`decided` or
  `under_review`), its original decision, and any appeals. It reads
  `logs/audit.jsonl` through `audit.entries_for`, so the status is whatever
  the most recent log entry for that id says. Unknown ids return a 404.
  Lives in `app.py::get_content`.

---

## What This Does

Provenance Guard takes a piece of writing, makes a careful guess about whether it was written by a person or with AI, and tells the writer in plain English, with a way to push back. The path a submission takes:

1. **`POST /submit` (`app.py::submit`)** receives JSON with `text` and `creator_id`.
2. **Input check.** Missing, non-string, empty, whitespace-only, over-10,000-character, or too-short text gets a `400` with a message saying what's wrong, never a `500`. Each rejection is logged. After 3 bad inputs from the same `creator_id` within 10 minutes, their next submission is blocked with a `429` that explains why (criterion 5).
3. **Signal one (`detector.py::model_signal`).** gpt2, running locally, measures how predictable the text is. Adds `model_score`, 0–1, higher = more AI-like.
4. **Signal two (`stylometry.py::style_signal`).** Measures the text's shape: sentence-length spread, vocabulary variety, and punctuation. Adds `style_score`, 0–1, higher = more AI-like.
5. **Combine (`scoring.py::combine_signals`).** A weighted average of the two, plus a disagreement rule. Adds one `confidence` score, 0–1.
6. **Label (`scoring.py::score_to_label`).** Turns the score into a guess (`ai` / `human` / `unsure`) and the sentence the writer reads.
7. **Log, then respond.** `audit.py::log_decision` writes the decision with all three scores to `logs/audit.jsonl`, and the route returns `content_id`, `guess`, `confidence`, `label`, `model_score`, `style_score` and `status`.

Afterwards, the writer can contest the decision with **`POST /appeal`**, which logs their reasoning and moves the item to `under_review`. **`GET /content/<id>`** (stretch) shows an item's current status.

---

## Signals and Scoring

### Signal one — the model signal

**What it measures:** How predictable the text is to a language model (gpt2), word by word. That's its perplexity, squashed onto 0–1 so that low perplexity = high AI score.

**Why that might differ between human and AI writing:** AI writes by picking likely next words, so its output is easy for a model to predict. People make odder, more specific choices.

**What it can't see:** Who wrote the text. It rewards common words in plain sentences, and many real people write that way: second-language writers, younger writers, anyone writing simply on purpose. In my calibration, a plainly written human paragraph scored **0.83**, nearly as high as clear AI text (0.91). It also misses the reverse: AI text with unusual words or rhyme (my AI poem scored 0.47) looks human to it.

### Signal two — the style signal

**What it measures:** The shape of the text, not its meaning. Three measures, each mapped onto 0–1 AI-ness and then combined (`stylometry.py`):

| Measure | What it is | Reads fully human at | Reads fully AI at | Weight |
|---|---|---|---|---|
| Sentence-length spread | stdev / mean of sentence lengths | ≥ 0.65 | ≤ 0.25 | 0.5 |
| Type-token ratio | unique / total words, averaged over 50-word windows | ≥ 0.90 | ≤ 0.70 | 0.2 |
| Punctuation density | commas, dashes, semicolons, colons, brackets, quotes, ! and ? per word (not full stops) | ≥ 0.20 | ≤ 0.06 | 0.3 |

A one-sentence text has no spread to measure, so that measure counts as 0.5 (no evidence either way) rather than "AI".

**Why that might differ between human and AI writing:** AI prose tends to be even, with similar mid-length sentences and few dashes or asides. Human writing is lumpier: a three-word sentence next to a long one, plus interruptions and dashes.

**What it can't see:** What the text says. Cheap surface edits move it without changing authorship. Lightly editing my AI essay (breaking up sentences, adding a dash and a few casual phrases) dropped its style score from 0.81 to 0.38. Plain writing also looks like AI on every measure: my plain human paragraph scored **1.00**.

**A finding from calibration:** type-token ratio barely separated AI (0.89) from human (0.86) text, and it was *lowest* for the plain human writer (0.70). It mostly penalises simple vocabulary, so I gave it the smallest weight. Sentence-length spread separated them best.

### The combining rule

**The rule:** Take a weighted average of the two signals. If the signals are more than 0.4 apart, two methods are telling different stories. That *is* uncertainty, so the score is held inside the unsure band and can't reach either confident label.

**The numbers** (in `config.py`):
- `WEIGHT_MODEL_SIGNAL = 0.5`, `WEIGHT_STYLE_SIGNAL = 0.5`
- `DISAGREEMENT_GAP = 0.4`
- `HUMAN_THRESHOLD = 0.35`, `AI_THRESHOLD = 0.75`. Below 0.35 is human, above 0.75 is AI, and anything in between (including exactly 0.35 or 0.75) is unsure. I raised the AI threshold from the starter's 0.65 because of the false-positive walkthrough in [notes/milestone1.md](notes/milestone1.md). Calling a real writer's work AI is the expensive mistake, so that label should be harder to reach. The unsure band is wider (0.40) than either confident band.

**Where it lives:** `scoring.py::combine_signals`

**Calibration results** (`model` / `style` → `combined` → label):

| Input | model | style | combined | label |
|---|---|---|---|---|
| clearly AI (essay) | 0.913 | 0.808 | 0.861 | AI |
| clearly AI (health essay) | 0.930 | 0.607 | 0.769 | AI |
| clearly human (anecdote) | 0.256 | 0.128 | 0.192 | human |
| formal human (committee report) | 0.641 | 0.716 | 0.679 | unsure |
| lightly-edited AI | 0.622 | 0.377 | 0.500 | unsure |
| AI poem (rhyming) | 0.468 | 0.755 | 0.612 | unsure |
| **plain human (simple words, short sentences)** | **0.833** | **1.000** | **0.916** | **AI: a false positive** |

**A case where my two signals split, and what my rule does with it:** The rhyming AI poem. The model signal reads it as human-ish (0.47) because rhyme forces unusual word choices, while the style signal reads it as AI (0.76) because its lines are almost exactly the same length. The weighted average puts it at 0.61, which is **unsure**. That's the right answer when two methods disagree. The gap (0.29) is under 0.4, so the disagreement rule didn't need to step in here. For bigger splits, it guarantees the result is unsure.

**The known failure:** The plain human paragraph is wrongly labeled AI at 0.92. Both signals agree, for the wrong reason, so no combining rule can catch it. Raising the threshold enough to let it through (above 0.92) would make clear AI text unreachable too. This is exactly the Milestone 1 "Mei" case. For now, the appeal path and the label wording ("Automated checks like ours can be wrong, especially about simple or very clear writing") are what protect this writer. It puts criterion 1 at risk, and it's the first thing to fix in unit 8.

---

## Label Variants

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | below 0.35 | We think this was probably written by a person. Our check found the patterns we usually see in human writing. |
| unsure | 0.35 – 0.75 (inclusive) | We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it. |
| high-confidence AI | above 0.75 | Our check found strong signs that this may have been written with AI. Automated checks like ours can be wrong, especially about simple or very clear writing. If you wrote this yourself, please ask for a review and a person will look at it. |

Every score from 0 to 1 maps to exactly one label, and all three were reached in testing (0.19 → human, 0.61 → unsure, 0.86 → AI).

**Why I worded the "unsure" one this way:** The person reading it may have written every word themselves. So it says plainly that it isn't an accusation, that landing there is common, and that nothing changes for them. It also names the kinds of writing that land there, so a careful writer understands why rather than feeling suspected. Even the AI label admits the check can be wrong and points to the appeal, because the false positive we found shows it sometimes is.

---

## Sample Run

**A submission.** This is the plain human paragraph, which the system wrongly labels AI:

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "I like to walk in the park in the morning. The air is fresh and cold. I see many birds there. Some birds are small and some are big. I walk for one hour every day. After my walk I drink tea at home. My mother makes the tea for me. I am happy in the morning. The park is my favorite place in the city.", "creator_id": "tanisha_sample"}'
```

```json
{
  "confidence": 0.9163,
  "content_id": "103114da-2d05-425e-8861-aaad66b117c5",
  "guess": "ai",
  "label": "Our check found strong signs that this may have been written with AI. Automated checks like ours can be wrong, especially about simple or very clear writing. If you wrote this yourself, please ask for a review and a person will look at it.",
  "model_score": 0.8326,
  "status": "decided",
  "style_score": 1.0
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "103114da-2d05-425e-8861-aaad66b117c5", "reasoning": "I wrote this myself. English is my second language, so I use simple words I am sure of."}'
```

```json
{
  "content_id": "103114da-2d05-425e-8861-aaad66b117c5",
  "message": "Your appeal was received. A person will review this decision; nothing is final until they do.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=2"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.9163,
      "content_id": "103114da-2d05-425e-8861-aaad66b117c5",
      "creator_id": "tanisha_sample",
      "guess": "ai",
      "label": "Our check found strong signs that this may have been written with AI. Automated checks like ours can be wrong, especially about simple or very clear writing. If you wrote this yourself, please ask for a review and a person will look at it.",
      "model_score": 0.8326,
      "status": "decided",
      "style_score": 1.0,
      "timestamp": "2026-11-09T20:34:00+00:00"
    },
    {
      "content_id": "103114da-2d05-425e-8861-aaad66b117c5",
      "creator_id": "tanisha_sample",
      "event": "appeal",
      "reasoning": "I wrote this myself. English is my second language, so I use simple words I am sure of.",
      "status": "under_review",
      "timestamp": "2026-11-09T20:34:01+00:00"
    }
  ]
}
```

**The item's status (stretch: `GET /content/<id>`)**

```bash
$ curl http://127.0.0.1:5000/content/103114da-2d05-425e-8861-aaad66b117c5
```

```json
{
  "appeals": [
    {
      "reasoning": "I wrote this myself. English is my second language, so I use simple words I am sure of.",
      "timestamp": "2026-11-09T20:34:01+00:00"
    }
  ],
  "content_id": "103114da-2d05-425e-8861-aaad66b117c5",
  "creator_id": "tanisha_sample",
  "decision": {
    "confidence": 0.9163,
    "guess": "ai",
    "label": "Our check found strong signs that this may have been written with AI. Automated checks like ours can be wrong, especially about simple or very clear writing. If you wrote this yourself, please ask for a review and a person will look at it.",
    "model_score": 0.8326,
    "style_score": 1.0
  },
  "status": "under_review",
  "submitted_at": "2026-11-09T20:34:00+00:00",
  "updated_at": "2026-11-09T20:34:01+00:00"
}
```

**Bad input and the block (criterion 5).** Three bad inputs from `bad_tester`, then a fourth request:

```text
400 {"error": "invalid_input", "message": "'text' is missing."}
400 {"error": "invalid_input", "message": "'text' is empty."}
400 {"error": "invalid_input", "message": "'text' is empty."}
429 {"error": "blocked", "message": "You've sent 3 invalid submissions in the last 10 minutes, so this one wasn't checked. Make sure your text isn't empty and is under 10,000 characters, then try again in a few minutes."}
```

---

## How I Used AI

I used Claude (Claude Code) throughout this unit.

**Moment 1: setting the numbers in my criteria**

- *What I asked for:* Ideas for acceptance criteria, then feedback on whether my drafts could be checked by someone who couldn't ask me what I meant.
- *What came back:* Criterion templates with blanks for the numbers, plus feedback on my drafts. It said "at least 1 of 5" borderline pieces landing in unsure was too easy to miss, and asked whether 2 wrongly accused writers out of 10 really matched my reason for wanting the number low.
- *What I changed:* I chose every number myself. I tightened my false-positive target from 2 in 10 to 1 in 10, and raised the unsure target from 1 of 5 to 4 of 5.

**Moment 2: fixing my bad-input criterion (criterion 5)**

- *What I asked for:* My first version said the 4 bad inputs (missing, empty, whitespace-only, and over-10,000-character text) return a 400 "in 3 of 4 cases." What I meant was that after 3 bad inputs the service should crash, so the person understands they've sent too many bad inputs. I asked Claude to help me make the criterion match that.
- *What came back:* It pointed out that a crash doesn't do what I wanted. A crash gives the person a generic "500 Internal Server Error" that doesn't explain anything, and it can take the service down for every writer, not just the one sending bad input. It said that what I was describing was a block, not a crash.
- *What I changed:* I rewrote criterion 5 so all 4 bad inputs get a 400 with an error message, never a crash, and after 3 bad inputs from the same `creator_id`, the next submission is blocked with a clear message explaining why. My reason changed from "the 4th case is allowed to crash because it is the 4th mistake" to keeping the service working for everyone while still stopping the person and telling them why. That is what `/submit` now does: a `429` with a message (see Sample Run).

**Other AI use, for the record:** Claude also drafted my Milestone 1 notes ([notes/milestone1.md](notes/milestone1.md)) and wrote the code for Milestones 3–5: the style signal, the combining rule, the label text, `/submit`, `/appeal` and the `GET /content/<id>` stretch. It ran the calibration tests and drafted this README.


<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 40 per day (per `creator_id`), set in `config.py` and applied to `POST /submit` with `@limiter.limit(...)` in `app.py`.

**Why those numbers and not others:**
- **A real writer** submits their own work a few times an hour at most. They might resubmit a piece two or three times in quick succession after fixing a typo, so 5 a minute never gets in their way. 40 a day covers even a heavy editing day, about a piece every 20 minutes for a full working day.
- **A script mapping my thresholds** needs hundreds or thousands of small variations of a text to find where the labels flip. At 40 a day per creator that would take weeks, and the burst limit of 5 a minute stops it from getting even a quick sample.
- I didn't go lower (e.g. 2 a minute) because a writer fixing and resubmitting would hit it. I didn't go higher (e.g. the starter's 10 / 200) because 200 a day is enough to map a threshold in an afternoon.

**What a caller counts as:** The `creator_id` in the request body, falling back to the caller's address when there isn't a usable one (`app.py::rate_limit_key`). This means one household or classroom sharing an address doesn't share a limit. The weakness is that the `creator_id` is self-reported: a script can make up a new one for every request and never get limited. Stopping that needs real accounts, or a second limit per address on top of this one.

My own route adds one more limit for criterion 5: after 3 bad inputs from the same `creator_id` within 10 minutes, the next submission gets a `429` with `"error": "blocked"` explaining why. Both kinds of 429 are written to the audit log as `rejected` entries.

**The run of status codes when I pushed past it:**

```
$ python run_attacks.py --flood 15
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429

10 of 15 were rate limited.
```

The log entry each rejection left:

```json
{"timestamp": "2026-11-09T21:17:53+00:00", "creator_id": "flood_tester", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
