# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-09 13:33
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `54544a5e-71b8-4c44-98a7-49530eee1248` | unsure | 0.482 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `69b438f0-855b-4a54-9dcc-5ff1bdf6baa1` | unsure | 0.450 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `a6322c09-f3b5-4434-bf06-bd0bb65a4b4a` | unsure | 0.586 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `122de3b1-c6cb-4e30-976f-92c1f5e0e64b` | unsure | 0.706 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `ed36332f-0707-4ba3-bab3-381d82890735` | human | 0.330 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `51fb053e-544e-4f4e-ace3-63511a5485e3` | unsure | 0.462 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `7f4fca88-c7ba-4e60-acc5-b24961be464e` | unsure | 0.445 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `3e32c2c3-e394-4395-bdbe-1b40fef6d09f` | unsure | 0.502 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `efd25af9-1351-4ff6-8005-07465455406e` | unsure | 0.594 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `b47b4c88-6325-4914-af5d-a7d14777771d` | ai | 0.900 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `0ec73583-838a-4fed-b1fc-d1d15870d56a` | unsure | 0.626 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `8f447da7-7120-49d8-b09d-71442c18ca71` | unsure | 0.835 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `f011ba9e-fe90-4e37-b3f3-9c59bf0a0161` | unsure | 0.794 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `b9b7f1ad-2702-4b3d-b516-2034ebf16c3c` | unsure | 0.783 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `1ca4a7e5-467f-41ff-8079-206a9e901d07` | ai | 0.883 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `d28d3493-6db8-4fab-8d0b-e197c2e33249` | unsure | 0.745 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `b51ef870-16a8-495e-8c6c-493aa5f722a3` | unsure | 0.691 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `a9dde359-aa59-4987-8f41-f8969d14933d` | unsure | 0.447 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `705c865d-dd95-4624-a45c-fa3c6a5f98d0` | unsure | 0.381 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `48eb9827-841c-4327-9f62-fc8baaa1b3d4` | human | 0.252 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `8fc4a852-ebd6-4654-98cb-459f82ea3b82` | unsure | 0.639 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `e386581a-16c9-41cf-9c35-5c33f184625f` | unsure | 0.516 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `9cb3b623-7f88-4b77-98bf-87fd7963638b` | unsure | 0.432 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `b1243c8a-ee48-4d5f-8d67-3ea8b64aacd1` | unsure | 0.601 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `66848f48-6b83-45f7-969f-56cb4591e633` | unsure | 0.350 |  |
| MF04 | malformed | text is only punctuation | 200 | `fbf7c6b8-a106-4549-b200-09139e2878ee` | unsure | 0.350 |  |
| MF05 | malformed | text is a very long single word | 200 | `d56cfa40-60eb-48b2-b68f-3e5afc116a38` | unsure | 0.774 |  |
| MF06 | malformed | text is emoji only | 200 | `ceac35bf-f5ba-45ec-a4f6-5e0509c4c70a` | unsure | 0.749 |  |
| MF07 | malformed | text is right-to-left script | 200 | `7014ff60-060f-4f01-92a0-91f5000933a1` | unsure | 0.703 |  |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d07b7939-9bf4-4077-b1ad-360a52cbe3bc` | unsure | 0.350 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `239f63a0-11f5-40a4-b116-d2edc901da44` | unsure | 0.350 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `8e51992a-bf3d-4fb2-a95f-735557b5930a` | unsure | 0.350 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `81ddfccb-0d54-45d2-8504-8ac86a3e18d0` | unsure | 0.350 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f6f2cf36-7d4e-45ab-b843-078795460da0` | unsure | 0.350 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "54544a5e-71b8-4c44-98a7-49530eee1248",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.4818,
  "model_score": 0.1635,
  "style_score": 0.8,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "69b438f0-855b-4a54-9dcc-5ff1bdf6baa1",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.45,
  "model_score": 0.5943,
  "style_score": 0.3057,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "a6322c09-f3b5-4434-bf06-bd0bb65a4b4a",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5856,
  "model_score": 0.6662,
  "style_score": 0.5049,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "122de3b1-c6cb-4e30-976f-92c1f5e0e64b",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.7057,
  "model_score": 0.6114,
  "style_score": 0.8,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "ed36332f-0707-4ba3-bab3-381d82890735",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.3298,
  "model_score": 0.3212,
  "style_score": 0.3385,
  "label": "We think this was probably written by a person. Our check found the patterns we usually see in human writing.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "51fb053e-544e-4f4e-ace3-63511a5485e3",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4619,
  "model_score": 0.5727,
  "style_score": 0.3512,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "7f4fca88-c7ba-4e60-acc5-b24961be464e",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.4454,
  "model_score": 0.5862,
  "style_score": 0.3046,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "3e32c2c3-e394-4395-bdbe-1b40fef6d09f",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.5021,
  "model_score": 0.2452,
  "style_score": 0.759,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "efd25af9-1351-4ff6-8005-07465455406e",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5936,
  "model_score": 0.7042,
  "style_score": 0.4829,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "b47b4c88-6325-4914-af5d-a7d14777771d",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8997,
  "model_score": 0.9792,
  "style_score": 0.8201,
  "label": "Our check found strong signs that this may have been written with AI. Automated checks like ours can be wrong, especially about simple or very clear writing. If you wrote this yourself, please ask for a review and a person will look at it.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "0ec73583-838a-4fed-b1fc-d1d15870d56a",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.6259,
  "model_score": 0.6175,
  "style_score": 0.6343,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "8f447da7-7120-49d8-b09d-71442c18ca71",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.8346,
  "model_score": 0.7387,
  "style_score": 0.9304,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "f011ba9e-fe90-4e37-b3f3-9c59bf0a0161",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.794,
  "model_score": 0.8051,
  "style_score": 0.7829,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "b9b7f1ad-2702-4b3d-b516-2034ebf16c3c",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.783,
  "model_score": 0.8329,
  "style_score": 0.733,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "1ca4a7e5-467f-41ff-8079-206a9e901d07",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.8835,
  "model_score": 0.8005,
  "style_score": 0.9664,
  "label": "Our check found strong signs that this may have been written with AI. Automated checks like ours can be wrong, especially about simple or very clear writing. If you wrote this yourself, please ask for a review and a person will look at it.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "d28d3493-6db8-4fab-8d0b-e197c2e33249",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.7445,
  "model_score": 0.8814,
  "style_score": 0.6075,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "b51ef870-16a8-495e-8c6c-493aa5f722a3",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.6908,
  "model_score": 0.8816,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "a9dde359-aa59-4987-8f41-f8969d14933d",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.4468,
  "model_score": 0.3223,
  "style_score": 0.5713,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "705c865d-dd95-4624-a45c-fa3c6a5f98d0",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.3812,
  "model_score": 0.4625,
  "style_score": 0.3,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "48eb9827-841c-4327-9f62-fc8baaa1b3d4",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2522,
  "model_score": 0.2044,
  "style_score": 0.3,
  "label": "We think this was probably written by a person. Our check found the patterns we usually see in human writing.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "8fc4a852-ebd6-4654-98cb-459f82ea3b82",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.639,
  "model_score": 0.5943,
  "style_score": 0.6836,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "e386581a-16c9-41cf-9c35-5c33f184625f",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.5165,
  "model_score": 0.4998,
  "style_score": 0.5332,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "9cb3b623-7f88-4b77-98bf-87fd7963638b",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4317,
  "model_score": 0.6401,
  "style_score": 0.2233,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "b1243c8a-ee48-4d5f-8d67-3ea8b64aacd1",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.6008,
  "model_score": 0.5583,
  "style_score": 0.6432,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "66848f48-6b83-45f7-969f-56cb4591e633",
  "creator_id": "attacker_MF03",
  "guess": "unsure",
  "confidence": 0.35,
  "model_score": 0.0,
  "style_score": 0.55,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "fbf7c6b8-a106-4549-b200-09139e2878ee",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.35,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "d56cfa40-60eb-48b2-b68f-3e5afc116a38",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.7738,
  "model_score": 0.9976,
  "style_score": 0.55,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "ceac35bf-f5ba-45ec-a4f6-5e0509c4c70a",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.7485,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "7014ff60-060f-4f01-92a0-91f5000933a1",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.7032,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "d07b7939-9bf4-4077-b1ad-360a52cbe3bc",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.35,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "239f63a0-11f5-40a4-b116-d2edc901da44",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.35,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "8e51992a-bf3d-4fb2-a95f-735557b5930a",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.35,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "81ddfccb-0d54-45d2-8504-8ac86a3e18d0",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.35,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "f6f2cf36-7d4e-45ab-b843-078795460da0",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.35,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We can't tell whether this was written by a person or with AI help. That's common, and it is not an accusation. Plain, careful, or formal writing often lands here. If you wrote this yourself, nothing changes for you, and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
