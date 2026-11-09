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

**Unit 8.** At my request, Claude did most of this unit's work: it turned on rate limiting and chose the numbers (5/minute, 40/day), ran the attack set and marked each attack held or broke, wrote `scenarios.py` and `eval_extra.py`, ran all the trials, wrote the diagnoses, picked and measured the improvement (AI threshold 0.75 → 0.85), and drafted the unit 8 README sections. It generated the "clearly AI" and "borderline" test texts. What I supplied: the ten pieces of my own writing that criterion 1 is tested on. I also asked it to show me which of my pieces got flagged as AI and why. It was piece 07, my creativity-and-technology essay, at 0.858, because of its very predictable phrasing and even sentence lengths.


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

Run with `python run_attacks.py --set attack_set --label before` → [results/attack_run_2026-11-09_1324_before.md](results/attack_run_2026-11-09_1324_before.md). All 56 inputs got a response, with **0 crashes (no 500s)**.

**How I marked each one.** I used the same rule for every family, so nothing gets a generous reading:
- **AI-written text** (evasion, and prompt injections built on AI text): **BROKE** if it was *not* labelled AI. Landing in "unsure" still counts as getting past the detector.
- **Human-written text** (false_positive, and injections built on human text): **BROKE** if it was labelled AI. That's a real writer accused.
- **Junk or malformed input:** **BROKE** if it crashed, *or* if the service accepted something that isn't writing and gave it a label. **HELD** if it was refused with a 400/429.
- **Prompt injection:** also BROKE if the injected instruction changed the label, the label text, or the log.

**Totals: 36 held, 20 broke.**

| Family | Attacks | Held | Broke |
|---|---|---|---|
| evasion | 10 | 1 | 9 |
| false_positive | 8 | 4 | 4 |
| flood_same_creator | 12 | 12 | 0 |
| malformed | 20 | 16 | 4 |
| prompt_injection | 6 | 3 | 3 |

| ID | Family | Targeting | Status | Guess | Score | model | style | Verdict | Why |
|---|---|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | unsure | 0.482 | 0.164 | 0.800 | **BROKE** | AI text, not labelled AI |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | unsure | 0.450 | 0.594 | 0.306 | **BROKE** | AI text, not labelled AI |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.586 | 0.666 | 0.505 | **BROKE** | AI text, not labelled AI |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | 0.706 | 0.611 | 0.800 | **BROKE** | AI text, not labelled AI |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.330 | 0.321 | 0.339 | **BROKE** | AI text labelled **human** |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.462 | 0.573 | 0.351 | **BROKE** | AI text, not labelled AI |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | 0.445 | 0.586 | 0.305 | **BROKE** | AI text, not labelled AI |
| EV08 | evasion | signal one: text below the token window | 200 | unsure | 0.502 | 0.245 | 0.759 | **BROKE** | AI text, not labelled AI |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.594 | 0.704 | 0.483 | **BROKE** | AI text, not labelled AI |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.900 | 0.979 | 0.820 | **HELD** | caught: labelled AI |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.626 | 0.618 | 0.634 | **HELD** | human text, not accused |
| FP02 | false_positive | human writing in a formal register | 200 | ai | 0.835 | 0.739 | 0.930 | **BROKE** | human text labelled **AI** |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | ai | 0.794 | 0.805 | 0.783 | **BROKE** | human text labelled **AI** |
| FP04 | false_positive | a student essay written to a rubric | 200 | ai | 0.783 | 0.833 | 0.733 | **BROKE** | human text labelled **AI** |
| FP05 | false_positive | technical documentation written by a person | 200 | ai | 0.883 | 0.800 | 0.966 | **BROKE** | human text labelled **AI** |
| FP06 | false_positive | a person imitating a formal template | 200 | unsure | 0.745 | 0.881 | 0.608 | **HELD** | not accused (0.745, just under the line) |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure | 0.691 | 0.882 | 0.500 | **HELD** | human text, not accused |
| FP08 | false_positive | very short genuine human submission | 200 | unsure | 0.447 | 0.322 | 0.571 | **HELD** | human text, not accused |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | 0.381 | 0.463 | 0.300 | **BROKE** | AI text not labelled AI (but the base text alone is missed too, see diagnosis) |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.252 | 0.204 | 0.300 | **BROKE** | AI text labelled **human**, the label the injection asked for |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.639 | 0.594 | 0.684 | **BROKE** | AI text not labelled AI (the injection raised its score; base text is missed) |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.516 | 0.500 | 0.533 | **HELD** | label text is fixed; the `<script>` comes back JSON-escaped, never as a label |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.432 | 0.640 | 0.223 | **HELD** | log line stays one valid JSON object; the fake fields stay inside `text`, which isn't logged |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.601 | 0.558 | 0.643 | **HELD** | instruction had no effect; same band as the text without it |
| MF01 | malformed | text is only whitespace | 400 | — | — | — | — | **HELD** | 400 |
| MF02 | malformed | text is a single character | 400 | — | — | — | — | **HELD** | 400 (too short to score) |
| MF03 | malformed | text is control characters | 200 | unsure | 0.350 | 0.000 | 0.550 | **BROKE** | junk accepted and given a label |
| MF04 | malformed | text is only punctuation | 200 | unsure | 0.350 | 0.011 | 0.500 | **BROKE** | no words at all, still given a label |
| MF05 | malformed | text is a very long single word | 200 | unsure | 0.750 | 0.998 | 0.550 | **BROKE** | junk accepted; scored 0.750, exactly on the AI line |
| MF06 | malformed | text is emoji only | 200 | unsure | 0.749 | 0.997 | 0.500 | **BROKE** | emoji only, still given a label (0.7485) |
| MF07 | malformed | text is right-to-left script | 200 | unsure | 0.703 | 0.906 | 0.500 | **HELD** | real writing in another language; unsure, not accused (but the score means nothing, see diagnosis) |
| MF08 | malformed | text is 60,000 characters | 400 | — | — | — | — | **HELD** | 400 (over 10,000 characters) |
| RQ01 | malformed | no text field at all | 400 | — | — | — | — | **HELD** | 400 |
| RQ02 | malformed | no creator_id | 400 | — | — | — | — | **HELD** | 400 |
| RQ03 | malformed | text is a number | 400 | — | — | — | — | **HELD** | 400 |
| RQ04 | malformed | text is a list | 400 | — | — | — | — | **HELD** | 400 |
| RQ05 | malformed | text is null | 400 | — | — | — | — | **HELD** | 400 |
| RQ06 | malformed | creator_id is an object | 400 | — | — | — | — | **HELD** | 400 |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | — | — | — | **HELD** | 400 |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | — | — | **HELD** | 400 |
| RQ09 | malformed | body is empty | 400 | — | — | — | — | **HELD** | 400 |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | — | — | — | — | **HELD** | 429 by address in the run; re-sent alone: 400 |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | — | — | — | — | **HELD** | 429 by address in the run; re-sent alone: 400 |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | — | — | **HELD** | 400 |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.350 | 0.029 | 0.550 | **HELD** | 200 |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.350 | 0.029 | 0.550 | **HELD** | 200 |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.350 | 0.029 | 0.550 | **HELD** | 200 |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.350 | 0.029 | 0.550 | **HELD** | 200 |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.350 | 0.029 | 0.550 | **HELD** | 200 |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | 429: limit held |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | 429: limit held |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | 429: limit held |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | 429: limit held |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | 429: limit held |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | 429: limit held |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | 429: limit held |

RQ10 and RQ11 have no usable `creator_id`, so the limiter counted them against my address, and by then earlier malformed rows had used up its 5 a minute. They never reached my route in the run. I re-sent each alone afterwards (`--id RQ10`, `--id RQ11`), and both got a 400 from the route.

**Ten audit log entries from the run** (13 here, as one JSON object per line, straight from `logs/audit.jsonl`). The first ten are decisions, chosen for the failures; the last three are **rejected requests**: one 400 my route refused, one 429 from the shared-creator flood, and one 429 counted against my address.

```json
{"timestamp": "2026-11-09T21:24:35+00:00", "content_id": "e5284a7b-a421-4944-a111-0cebfb48e298", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.7829, "combined_score": 0.794, "label": "Our check found strong signs that this may have been written with AI. Automated checks like ours can be wrong, especially about simple or very clear writing. If you wrote this yourself, please ask for a review and a person will look at it.", "status": "decided"}
{"timestamp": "2026-11-09T21:24:35+00:00", "content_id": "4b9a4cfb-8665-4d72-8edb-9a340ad48527", "creator_id": "attacker_FP05", "guess": "ai", "model_score": 0.8005, "style_score": 0.9664, "combined_score": 0.8835, "label": "Our check found strong signs that this may have been written with AI. Automated checks like ours can be wrong, especially about simple or very clear writing. If you wrote this yourself, please ask for a review and a person will look at it.", "status": "decided"}
{"timestamp": "2026-11-09T21:24:35+00:00", "content_id": "734b8a19-5792-40e2-bd37-ace24f1b7551", "creator_id": "attacker_FP02", "guess": "ai", "model_score": 0.7387, "style_score": 0.9304, "combined_score": 0.8346, "label": "Our check found strong signs that this may have been written with AI. Automated checks like ours can be wrong, especially about simple or very clear writing. If you wrote this yourself, please ask for a review and a person will look at it.", "status": "decided"}
{"timestamp": "2026-11-09T21:24:36+00:00", "content_id": "95bbb7b2-5142-4452-8185-a3de5cee1499", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.3, "combined_score": 0.2522, "label": "We think this was probably written by a person. Our check found the patterns we usually see in human writing.", "status": "decided"}
{"timestamp": "2026-11-09T21:24:34+00:00", "content_id": "c94aa304-2642-4463-85c7-76e0396dadc0", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.3385, "combined_score": 0.3298, "label": "We think this was probably written by a person. Our check found the patterns we usually see in human writing.", "status": "decided"}
{"timestamp": "2026-11-09T21:24:34+00:00", "content_id": "73d91338-3501-403b-bcd8-59cd31145fa2", "creator_id": "attacker_EV01", "guess": "unsure", "model_score": 0.1635, "style_score": 0.8, "combined_score": 0.4818, "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.", "status": "decided"}
{"timestamp": "2026-11-09T21:24:36+00:00", "content_id": "9545c9f4-e81c-4e69-8ca0-b8736c06900b", "creator_id": "attacker_MF05", "guess": "unsure", "model_score": 0.9976, "style_score": 0.55, "combined_score": 0.75, "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.", "status": "decided"}
{"timestamp": "2026-11-09T21:24:37+00:00", "content_id": "b9ddda60-026d-4e1d-b893-82eaf3927762", "creator_id": "attacker_MF06", "guess": "unsure", "model_score": 0.9969, "style_score": 0.5, "combined_score": 0.7485, "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.", "status": "decided"}
{"timestamp": "2026-11-09T21:24:35+00:00", "content_id": "5c11d903-0bb0-4694-8dae-c674d5c8082c", "creator_id": "attacker_EV10", "guess": "ai", "model_score": 0.9792, "style_score": 0.8201, "combined_score": 0.8997, "label": "Our check found strong signs that this may have been written with AI. Automated checks like ours can be wrong, especially about simple or very clear writing. If you wrote this yourself, please ask for a review and a person will look at it.", "status": "decided"}
{"timestamp": "2026-11-09T21:24:36+00:00", "content_id": "29c3b230-45d4-4ae2-aaba-6205eccd94e9", "creator_id": "attacker_PI05", "guess": "unsure", "model_score": 0.6401, "style_score": 0.2233, "combined_score": 0.4317, "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.", "status": "decided"}
{"timestamp": "2026-11-09T21:24:37+00:00", "creator_id": "attacker_RQ03", "event": "rejected", "status": "rejected", "reason": "invalid_input", "message": "'text' must be a string."}
{"timestamp": "2026-11-09T21:24:37+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
{"timestamp": "2026-11-09T21:24:37+00:00", "creator_id": "unknown", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
```

**The single worst outcome** — the one I'd least want to explain to a writer whose work got caught by it:

**FP03, "a non-native English speaker writing carefully."** It starts *"I want to describe my experience of the first month in this country. The weather was very different from my home…"*. My service labelled it **high-confidence AI at 0.794** (model 0.805, style 0.783). That's the exact person I traced through the system in Milestone 1 ("Mei"), and the exact person my AI label was supposed to protect by sitting at 0.75 rather than 0.65. The label at least says checks can be wrong about simple writing and points to an appeal. But it's still telling someone writing carefully in their second language that we think they cheated.

---


## Run Log and Verdicts

Criteria 1, 2, 3 and the first half of 5 were run with `python run_eval.py --label before` (scenarios in [scenarios.py](scenarios.py)) → [results/run_2026-11-09_1332_before.md](results/run_2026-11-09_1332_before.md). Criterion 4 and the blocking half of 5 need several requests in a row, each depending on the last, which `run_eval.py` can't do. So they're run by [eval_extra.py](eval_extra.py) (`python eval_extra.py --label before`) → [results/extra_2026-11-09_1327_before.md](results/extra_2026-11-09_1327_before.md). Every criterion got 3 trials, with nothing changed in between.

**Where the test texts come from:** criterion 1 uses ten pieces of my own writing ([eval_texts/my_writing/](eval_texts/my_writing/)): five sections of my *Inside Out* essay with the quoted film dialogue left out, my PERIOD club, creativity-and-technology and Jainism essays, and my Girls Who Code essay split in two. The "clearly AI" and "borderline" texts were generated by Claude for this test. The borderline ones were then lightly edited toward a casual voice.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing labelled high-confidence AI | ≤ 1 of 10, every trial | 1/10 † | 1/10 | 1/10 | **MET** |
| 2. Score gap, clearly-AI mean minus clearly-human mean | ≥ 0.25 | 0.281 | 0.281 | 0.281 | **MET** |
| 3. Borderline pieces landing in "unsure" | ≥ 4 of 5 | 5/5 | 5/5 | 5/5 | **MET** |
| 4. Appeals → `under_review` and in `GET /log`; fake id → 404 | 5 of 5, and 404 | 5/5, 404 | 5/5, 404 | 5/5, 404 | **MET** |
| 5. Bad input → 400 never 500; blocked after 3 bad inputs | 4 of 4, and blocked | 4/4, blocked | 4/4, blocked | 4/4, blocked | **MET** |

**How I decided each verdict:**
1. The same piece (07, my creativity-and-technology essay, **0.858**) was labelled AI in all three trials, and nothing else was. One is exactly my limit, so it's met, with no room to spare. † In run 1, piece 01 got no response: the request was dropped with `ConnectionError: Remote end closed connection`. The server log shows Flask's debug reloader restarting the service because I had just edited `scenarios.py`. Runs 2 and 3 scored that piece 0.624 (unsure), and scores are deterministic, so run 1 is 1 AI of the 9 answered. It can't have been 2.
2. The gap is computed from the `confidence` values. It was identical in every trial: 0.837 − 0.556 = 0.281. That's met, but only 0.031 above the target.
3. All five landed in unsure every time (0.45–0.71).
4. All five appeals returned 200. `GET /content/<id>` then said `under_review`, the appeal was in `GET /log`, and the made-up id got a 404, in every trial.
5. Every bad body got a 400, never a 500. In each trial, a 4th request after 3 bad inputs from one creator got `429 "blocked"`.

**Real output from one trial**

**Criterion 1, my own writing:** trial 2, from `run_eval.py::main` → `app.py::submit` ([results/run_2026-11-09_1332_before.md](results/run_2026-11-09_1332_before.md)). The `label` field is left out of each object here for length; it's in the results file.

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6239,
    "model_score": 0.555,
    "style_score": 0.6928,
    "sent": "Between 2019 and 2024, EQ has decreased by 5.79% globally, according t"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6,
    "model_score": 0.4811,
    "style_score": 0.7189,
    "sent": "Accepting and processing all emotions is crucial to mental well being."
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3492,
    "model_score": 0.3343,
    "style_score": 0.3641,
    "sent": "Sadness understands that Bing Bong feels grief over his loss and that "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.672,
    "model_score": 0.6253,
    "style_score": 0.7186,
    "sent": "Another key point of the film is that Riley needs to voice her thought"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5341,
    "model_score": 0.4901,
    "style_score": 0.5781,
    "sent": "One may argue that the creators oversimplified Riley’s emotions by onl"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6482,
    "model_score": 0.514,
    "style_score": 0.7823,
    "sent": "My first teen talk in fifth grade was separate for girls and boys to l"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8579,
    "model_score": 0.8775,
    "style_score": 0.8384,
    "sent": "My journey has been a captivating blend of creativity and technology. "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6605,
    "model_score": 0.6559,
    "style_score": 0.6651,
    "sent": "I first began my journey in Girls Who Code in which I was exposed to s"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.7044,
    "model_score": 0.5754,
    "style_score": 0.8333,
    "sent": "While iterating on this project, I also applied UX testing, which invo"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5976,
    "model_score": 0.6643,
    "style_score": 0.5308,
    "sent": "Jainism is a selfless religion which preaches non-violence, kindness t"
  }
]
```

**Criterion 2, score spread:** trial 2, same run. The first five are clearly AI, the last five are my writing. Mean AI = 0.837, mean mine = 0.556, gap = **0.281**.

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8558,
    "model_score": 0.9066,
    "style_score": 0.805,
    "sent": "Artificial intelligence is transforming the way we live and work. It o"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.847,
    "model_score": 0.9054,
    "style_score": 0.7886,
    "sent": "Regular exercise is essential for maintaining good health. It helps to"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8713,
    "model_score": 0.9426,
    "style_score": 0.8,
    "sent": "Climate change is one of the most pressing issues facing the world tod"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8363,
    "model_score": 0.7826,
    "style_score": 0.89,
    "sent": "Reading is an important skill that provides many benefits. It helps to"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7741,
    "model_score": 0.8197,
    "style_score": 0.7284,
    "sent": "Time management is a key skill for success in both school and work. It"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6239,
    "model_score": 0.555,
    "style_score": 0.6928,
    "sent": "Between 2019 and 2024, EQ has decreased by 5.79% globally, according t"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6,
    "model_score": 0.4811,
    "style_score": 0.7189,
    "sent": "Accepting and processing all emotions is crucial to mental well being."
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3492,
    "model_score": 0.3343,
    "style_score": 0.3641,
    "sent": "Sadness understands that Bing Bong feels grief over his loss and that "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.672,
    "model_score": 0.6253,
    "style_score": 0.7186,
    "sent": "Another key point of the film is that Riley needs to voice her thought"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5341,
    "model_score": 0.4901,
    "style_score": 0.5781,
    "sent": "One may argue that the creators oversimplified Riley’s emotions by onl"
  }
]
```

**Criterion 3, borderline:** trial 2, same run.

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4507,
    "model_score": 0.6082,
    "style_score": 0.2933,
    "sent": "AI is changing how we live and work, honestly faster than most of us e"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.713,
    "model_score": 0.6284,
    "style_score": 0.7977,
    "sent": "Exercise matters for your health, and I don't just mean the gym. It st"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6573,
    "model_score": 0.7373,
    "style_score": 0.5773,
    "sent": "Climate change is a huge issue right now. Temperatures are rising, and"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6444,
    "model_score": 0.8133,
    "style_score": 0.4755,
    "sent": "Reading does a lot for you. It builds your vocabulary and sharpens how"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4947,
    "model_score": 0.5629,
    "style_score": 0.4266,
    "sent": "Managing your time well is a big deal, at school and at work. It's abo"
  }
]
```
**Criterion 4, appeals:** trial 2, from `eval_extra.py::appeal_trial` → `app.py::appeal` and `app.py::get_content` ([results/extra_2026-11-09_1327_before.md](results/extra_2026-11-09_1327_before.md)). This shows the first appeal and the fake id; all five real ones look like the first.

```json
[
  {
    "content_id": "997d378b-b278-4378-876a-a64a05f713e4",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "997d378b-b278-4378-876a-a64a05f713e4",
      "message": "Your appeal was received. A person will review this decision; nothing is final until they do.",
      "status": "under_review"
    },
    "status_after": "under_review",
    "appeal_in_log": true,
    "passed": true
  },
  {
    "content_id": "fake",
    "appeal_status_code": 404,
    "appeal_response": {
      "error": "not_found",
      "message": "No submission with content_id 'fake-a7c456e8-50a2-4e70-a739-45912c548ba3'. Check it matches the one you were given."
    },
    "passed": true
  }
]
```

**Criterion 5, bad input:** trial 2 of the four bad bodies, from `run_eval.py::main` → `app.py::submit`, with each case under its own `creator_id`:

```json
[
  {
    "status": 400,
    "sent": "{\"creator_id\": \"eval_bad_missing\"}"
  },
  {
    "status": 400,
    "sent": "(empty text)"
  },
  {
    "status": 400,
    "sent": "   \n\t  "
  },
  {
    "status": 400,
    "sent": "word word word word word word word word word word word word word word "
  }
]
```

and the block (trial 2, `eval_extra.py::block_trial`):

```json
[
  {
    "sent": "{\"creator_id\": \"eval_block_before_132725_2\"}",
    "status": 400,
    "response": {
      "error": "invalid_input",
      "message": "'text' is missing."
    }
  },
  {
    "sent": "{\"text\": \"\", \"creator_id\": \"eval_block_before_132725_2\"}",
    "status": 400,
    "response": {
      "error": "invalid_input",
      "message": "'text' is empty."
    }
  },
  {
    "sent": "{\"text\": \"  \", \"creator_id\": \"eval_block_before_132725_2\"}",
    "status": 400,
    "response": {
      "error": "invalid_input",
      "message": "'text' is empty."
    }
  },
  {
    "sent": "{\"text\": \"We got to the campsite about four. The pitch was a bit sloped, but the",
    "status": 429,
    "response": {
      "error": "blocked",
      "message": "You've sent 3 invalid submissions in the last 10 minutes, so this one wasn't checked. Make sure your text isn't empty and is under 10,000 characters, then try again in a few minutes."
    },
    "passed": true
  }
]
```

**All five met, so were my targets too easy?** Partly, yes:
- **Criterion 1** passed by exactly my limit, and only **1 of my 10 pieces was labelled human**. Eight landed in "unsure". My criterion only counted AI labels, so a system that refuses to decide passes it. That's not the same as recognising my writing as mine. **This is the criterion I'd tighten:** "at most 1 of 10 labelled AI *and at least 5 of 10 labelled human*."
- **Criterion 3** is easy to meet with an unsure band 0.40 wide (0.50 after the improvement). Almost anything that isn't extreme lands there.
- **Criterion 2** passed by 0.031. My own writing averages 0.556, closer to the AI side than the human side.

The attack set found what my criteria didn't: **4 of 8 human false-positive texts labelled AI**. My own criteria tested the writer I am, not the writers the system is worst at.

**Diagnoses**

There were no criterion misses, so these diagnose the one near-miss in my own writing and every broken attack. My service has five stages: the route, signal one (model), signal two (style), the combining rule, and the label mapping (thresholds).

*My piece 07 labelled AI (0.858).* Both signals: model 0.878, style 0.838. Its gpt2 perplexity is **13.1**. My other nine pieces sit between 29 and 69. It's written in a polished personal-statement register built from very familiar phrases ("vibrant world", "delved deeper", "driving force", "intersection of art and technology"), which is exactly what a language model predicts easily. Its sentence lengths are also very even (spread 0.26, which my style signal reads as AI). **Stage:** signal one, backed up by signal two. **Mechanism:** common phrasing in even sentences looks like AI to both, regardless of who wrote it.

*Pattern 1: false positives (FP02, FP03, FP04, FP05 labelled AI).* All four are plain or formal human prose: a committee report, a careful non-native speaker, a rubric essay, technical documentation. All four have punctuation density ≤ 0.03 (almost nothing but full stops) and low sentence-length spread (0.24–0.37). In signal two, both of those measures are pinned at "fully AI", giving style scores of 0.73–0.97. Signal one agreed (0.74–0.83), because plain and formal registers use predictable words. **Stage:** signal two's punctuation and spread measures, compounded by signal one. With both high, the label mapping's AI threshold of 0.75 was too low to protect them. **Mechanism:** my style signal treats the absence of commas and dashes as evidence of AI, when it's really evidence of a register. It's the same "Mei" mechanism I predicted in Milestone 1, and the same reason my own plain-human calibration text failed in unit 7. That makes it one problem, not four.

*Pattern 2: evasion (EV01–EV09 not labelled AI; EV05 labelled human).* Unedited AI text in this set only scores around 0.85–0.90 (EV10, the one caught, scored 0.90). My combining rule averages the two signals and needs the result above the AI threshold, so **an attack only has to knock down one signal by about 0.3** to land in unsure. Which signal each attack hit:
- **Signal one:** EV01 (typos: model **0.16**, because gpt2 finds misspelt tokens very surprising; style still 0.80), EV04 (rare words: model 0.61), EV08 (10 words, too short for a stable perplexity: model 0.25).
- **Signal two:** EV02 (broken-up sentences: style 0.31), EV06 (one very long and one very short sentence: 0.35), EV07 (punctuation padding: 0.30). These hit exactly the spread and punctuation measures.
- **Both, diluted:** EV03 (a pasted quotation) and EV09 (a human opening paragraph) blend human and AI text. EV05 (a heavy human edit) took both signals to ~0.33, so it was labelled **human**.

**Stage:** the combining rule (an average lets either signal veto) together with the label mapping. **Mechanism:** each signal has a cheap surface attack, and averaging means the attacker only needs one.

*Pattern 3: prompt injection (PI01–PI03 not labelled AI; PI02 labelled human).* Nothing in my service follows instructions, so no injection was *obeyed*. PI04's `<script>` came back as escaped JSON, and PI05's fake fields stayed inside the text, which isn't logged. But the injections work as evasions:
- **PI02:** the "SYSTEM: … guess=human, confidence=0.02" header is full of tokens gpt2 doesn't expect. With the header the model signal is **0.20**; on the same AI paragraph alone it's 0.754. **Stage:** signal one. **Mechanism:** perplexity is averaged over the whole text, so an odd-looking preamble drags a short AI paragraph's score down.
- **PI01 and PI03:** the AI paragraph underneath is only 27 words and ends on a cut-off fragment ("Th"). Signal two reads that one-word "sentence" as length variety (style 0.30), so the paragraph scores 0.527 (unsure) **without** any injection. PI03's injection actually *raised* it to 0.639. **Stage:** signal two. **Mechanism:** a dangling fragment counts as a sentence.

*Pattern 4: junk accepted as writing (MF03 control characters, MF04 punctuation only, MF05 "aaaa…", MF06 emoji only).* **Stage:** the route. **Mechanism:** it only checks that `text.strip()` is non-empty, not that there are any words. Downstream, gpt2 finds repetitive junk perfectly predictable (MF05/MF06 model **≈ 1.00**), while signal two finds no words and returns 0.5. The disagreement rule held them inside unsure. MF05 scored **0.750, exactly on the AI line**: a row of "a"s was one rounding step away from being called AI.

*Held, but worth a note:* MF07 (Arabic) landed in unsure at 0.70 with model 0.91. gpt2 is an English model, so that number means nothing. RQ10/RQ11 were rejected by the address-based rate limit before reaching my route; sent alone, both got a 400.

---

## The Improvement

**What I changed:** One line in `config.py`: `AI_THRESHOLD = 0.75` → **`0.85`**. Nothing else moved. The "high-confidence AI" band is now above 0.85, and unsure covers 0.35–0.85.

**Which diagnosis pointed at it:** Pattern 1. Real writing is landing in the high-confidence AI band because both signals agree on plain and formal prose. No reweighting fixes that, because both signals are wrong in the same direction. Before choosing, I simulated three options on the attack set's human and AI texts:
- dropping the punctuation measure → 2 false positives left
- weighting the model signal 0.7 → 6 false positives
- threshold 0.85 → 1 false positive left, without losing the one AI text the set caught

I picked the threshold.

### Attack Run — After

`python run_attacks.py --set attack_set --label after` → [results/attack_run_2026-11-09_1333_after.md](results/attack_run_2026-11-09_1333_after.md). Same verdict rules as before. ⬅ marks a row that changed.

| Family | Broke before | Broke after |
|---|---|---|
| evasion | 9 | 9 |
| false_positive | 4 | 1 |
| flood_same_creator | 0 | 0 |
| malformed | 4 | 4 |
| prompt_injection | 3 | 3 |
| **total** | **20** | **17** |

| ID | Family | Targeting | Before | After | Before verdict | After verdict |
|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 unsure 0.482 | 200 unsure 0.482 | BROKE | **BROKE** |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 unsure 0.450 | 200 unsure 0.450 | BROKE | **BROKE** |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 unsure 0.586 | 200 unsure 0.586 | BROKE | **BROKE** |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 unsure 0.706 | 200 unsure 0.706 | BROKE | **BROKE** |
| EV05 | evasion | both signals: heavy human editing pass | 200 human 0.330 | 200 human 0.330 | BROKE | **BROKE** |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 unsure 0.462 | 200 unsure 0.462 | BROKE | **BROKE** |
| EV07 | evasion | signal two: padding with punctuation | 200 unsure 0.445 | 200 unsure 0.445 | BROKE | **BROKE** |
| EV08 | evasion | signal one: text below the token window | 200 unsure 0.502 | 200 unsure 0.502 | BROKE | **BROKE** |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 unsure 0.594 | 200 unsure 0.594 | BROKE | **BROKE** |
| EV10 | evasion | signal two: repeated stanza structure | 200 ai 0.900 | 200 ai 0.900 | HELD | **HELD** |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 unsure 0.626 | 200 unsure 0.626 | HELD | **HELD** |
| FP02 | false_positive | human writing in a formal register | 200 ai 0.835 | 200 unsure 0.835 ⬅ | BROKE | **HELD** |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 ai 0.794 | 200 unsure 0.794 ⬅ | BROKE | **HELD** |
| FP04 | false_positive | a student essay written to a rubric | 200 ai 0.783 | 200 unsure 0.783 ⬅ | BROKE | **HELD** |
| FP05 | false_positive | technical documentation written by a person | 200 ai 0.883 | 200 ai 0.883 | BROKE | **BROKE** |
| FP06 | false_positive | a person imitating a formal template | 200 unsure 0.745 | 200 unsure 0.745 | HELD | **HELD** |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 unsure 0.691 | 200 unsure 0.691 | HELD | **HELD** |
| FP08 | false_positive | very short genuine human submission | 200 unsure 0.447 | 200 unsure 0.447 | HELD | **HELD** |
| PI01 | prompt_injection | instruction to ignore the check | 200 unsure 0.381 | 200 unsure 0.381 | BROKE | **BROKE** |
| PI02 | prompt_injection | instruction disguised as a system message | 200 human 0.252 | 200 human 0.252 | BROKE | **BROKE** |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 unsure 0.639 | 200 unsure 0.639 | BROKE | **BROKE** |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 unsure 0.516 | 200 unsure 0.516 | HELD | **HELD** |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 unsure 0.432 | 200 unsure 0.432 | HELD | **HELD** |
| PI06 | prompt_injection | instruction plus real human text | 200 unsure 0.601 | 200 unsure 0.601 | HELD | **HELD** |
| MF01 | malformed | text is only whitespace | 400  | 400  | HELD | **HELD** |
| MF02 | malformed | text is a single character | 400  | 400  | HELD | **HELD** |
| MF03 | malformed | text is control characters | 200 unsure 0.350 | 200 unsure 0.350 | BROKE | **BROKE** |
| MF04 | malformed | text is only punctuation | 200 unsure 0.350 | 200 unsure 0.350 | BROKE | **BROKE** |
| MF05 | malformed | text is a very long single word | 200 unsure 0.750 | 200 unsure 0.774 ⬅ | BROKE | **BROKE** |
| MF06 | malformed | text is emoji only | 200 unsure 0.749 | 200 unsure 0.749 | BROKE | **BROKE** |
| MF07 | malformed | text is right-to-left script | 200 unsure 0.703 | 200 unsure 0.703 | HELD | **HELD** |
| MF08 | malformed | text is 60,000 characters | 400  | 400  | HELD | **HELD** |
| RQ01 | malformed | no text field at all | 400  | 400  | HELD | **HELD** |
| RQ02 | malformed | no creator_id | 400  | 400  | HELD | **HELD** |
| RQ03 | malformed | text is a number | 400  | 400  | HELD | **HELD** |
| RQ04 | malformed | text is a list | 400  | 400  | HELD | **HELD** |
| RQ05 | malformed | text is null | 400  | 400  | HELD | **HELD** |
| RQ06 | malformed | creator_id is an object | 400  | 400  | HELD | **HELD** |
| RQ07 | malformed | body is a JSON array, not an object | 400  | 400  | HELD | **HELD** |
| RQ08 | malformed | body is unparseable JSON | 400  | 400  | HELD | **HELD** |
| RQ09 | malformed | body is empty | 400  | 400  | HELD | **HELD** |
| RQ10 | malformed | body is form-encoded, not JSON | 429  | 429  | HELD | **HELD** |
| RQ11 | malformed | body is JSON claiming to be plain text | 429  | 429  | HELD | **HELD** |
| RQ12 | malformed | deeply nested JSON | 400  | 400  | HELD | **HELD** |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 unsure 0.350 | 200 unsure 0.350 | HELD | **HELD** |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 unsure 0.350 | 200 unsure 0.350 | HELD | **HELD** |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 unsure 0.350 | 200 unsure 0.350 | HELD | **HELD** |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 unsure 0.350 | 200 unsure 0.350 | HELD | **HELD** |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 unsure 0.350 | 200 unsure 0.350 | HELD | **HELD** |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429  | 429  | HELD | **HELD** |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429  | 429  | HELD | **HELD** |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429  | 429  | HELD | **HELD** |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429  | 429  | HELD | **HELD** |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429  | 429  | HELD | **HELD** |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429  | 429  | HELD | **HELD** |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429  | 429  | HELD | **HELD** |

### Run log — After

`python run_eval.py --label after` → [results/run_2026-11-09_1334_after.md](results/run_2026-11-09_1334_after.md), and `python eval_extra.py --label after` → [results/extra_2026-11-09_1334_after.md](results/extra_2026-11-09_1334_after.md).

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing labelled high-confidence AI | ≤ 1 of 10 | 1/10 | 1/10 | 1/10 | **MET** |
| 2. Score gap | ≥ 0.25 | 0.281 | 0.281 | 0.281 | **MET** |
| 3. Borderline in "unsure" | ≥ 4 of 5 | 5/5 | 5/5 | 5/5 | **MET** |
| 4. Appeals | 5 of 5, and 404 | 5/5, 404 | 5/5, 404 | 5/5, 404 | **MET** |
| 5. Bad input → 400; blocked after 3 | 4 of 4, and blocked | 4/4, blocked | 4/4, blocked | 4/4, blocked | **MET** |

**A measurement problem on criterion 5, not a system change:** in the first "after" run, all four bad bodies came back **429 "blocked"**, not 400 (0/4 every trial). That's because the scenario gives each bad case a fixed `creator_id`, the "before" run had just given each of them 3 bad inputs, and my block lasts 10 minutes. The "after" run started 2 minutes later. It still never returned a 500, and the block did exactly what criterion 5's second half asks. But it hid the first half. So I waited out the 10-minute window, changed nothing, and re-ran (`--label after_rerun`) → [results/run_2026-11-09_1343_after_rerun.md](results/run_2026-11-09_1343_after_rerun.md). The table above uses the rerun, and both files are committed. This also shows a real tension in criterion 5: "each bad input gets a 400" and "block after 3" can't both hold for the same creator.

**Did it help, and how do I know:**
- **Yes, for the expensive mistake.** Human texts labelled AI in the attack set went from **4 of 8 to 1 of 8**: FP02, FP03 and FP04 moved to unsure. Total broken attacks went from 20 to 17. The worst outcome from the "before" run, FP03 (the non-native speaker), is no longer accused. Every score except MF05 was identical before and after, so the change is exactly and only the threshold.
- **It didn't touch the evasions.** The set's AI texts were already escaping into unsure, so 9 of 10 still get through, before and after.
- **It cost AI detection on plain AI text.** Of my own five clearly-AI test texts, **5 of 5 were labelled AI before, and only 2 of 5 after.** Three moved to unsure (0.77, 0.84, 0.85). Unedited, generic AI writing now often gets "we can't tell". That's the trade: fewer wrong accusations, more AI text passing without a confident label.
- **It didn't fix my own piece 07** (0.858, just above the new line). It also had a side effect I hadn't predicted. The disagreement rule clamps scores to the AI threshold, so raising the threshold raised the clamp's ceiling too, and MF05 ("aaaa…") moved from 0.750 to 0.774.
- None of my five criteria changed verdict, because they were all already met. The improvement shows up in the attack set, not in my criteria. That's one more sign my criteria were aimed at the wrong writers.

---

## What's Still Broken

- **FP05 (technical documentation, 0.884) is still labelled AI.** *What I'd do:* fix signal two so that **a lack of punctuation stops counting as evidence of AI**: score the punctuation measure as neutral (0.5) below a density threshold, instead of "fully AI". My simulation says that alone clears FP02–FP04 and would stack with the threshold. *Why I stopped:* the one-change rule. It's my next change.
- **My own piece 07 (0.858) is still labelled AI.** It's the same mechanism as FP05 plus very low perplexity. The punctuation fix wouldn't help it much (its density is 0.06). The real fix is for signal one to stop treating "familiar phrasing" as authorship, and I don't know how to do that with gpt2 perplexity alone. Until then, the label tells the writer checks can be wrong and points to the appeal, which works (criterion 4).
- **9 of 10 evasions, plus PI01–PI03.** *What I'd do:* stop letting one signal veto the other. For example, when either signal is above 0.9, keep the result out of the "human" band. *Why I stopped:* every version I tried in simulation trades directly against false positives (FP02 and FP05 have style scores of 0.93 and 0.97). On a writing site, I'd rather miss AI text than accuse writers.
- **PI02's preamble trick.** *What I'd do:* score signal one per paragraph and use the highest paragraph score, so odd tokens in one paragraph can't dilute another. *Why I stopped:* it would also raise scores on human writing that has one plain paragraph, which is the false-positive problem again. It would need its own measured run.
- **MF03–MF06 junk gets a label.** *What I'd do:* reject text with fewer than ~5 real words with a 400 in the route. It's simple and it's the safest fix on this list. *Why I stopped:* one change per unit. It's second in line after the punctuation fix.
- **Criterion 5's two halves collide for one creator** (see above). I'd rewrite the test to use fresh creator ids per run, and clarify the criterion. I'm leaving the criterion text as written, since it wasn't unmeasurable, just in tension.
- **Self-reported `creator_id`.** A script that invents a new id per request is never rate-limited or blocked. That needs real accounts, which is out of scope here.

**The trade I'd make if this ran for real:** I'd keep going toward fewer wrong accusations: a high AI threshold, a wide unsure band, and a working appeal. Accusing a real writer, especially one writing plainly or in a second language, costs that person far more than a missed AI text costs the site. The people who pay for that choice are the honest writers whose work sits next to AI text that wasn't flagged, and readers who see "we can't tell" more often than they'd like.

---

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
