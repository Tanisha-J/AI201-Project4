# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-09 13:24
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `73d91338-3501-403b-bcd8-59cd31145fa2` | unsure | 0.482 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `e2d07a75-0142-42ea-a4e6-3afd0ddbffaa` | unsure | 0.450 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `3184ff2f-8965-4212-af0d-46c2b6313a6d` | unsure | 0.586 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `61817dda-4b7d-41de-9412-f7390acc77ef` | unsure | 0.706 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `c94aa304-2642-4463-85c7-76e0396dadc0` | human | 0.330 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `9b572a29-4e4f-4e84-94e5-2b03325b045a` | unsure | 0.462 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `6498d421-7d6c-4bcd-b625-0e852214e08e` | unsure | 0.445 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `e6dbdbac-69c3-4155-b9a9-bdb0a2b015b6` | unsure | 0.502 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `ee9526f0-392a-46a0-8022-d6d7987e602c` | unsure | 0.594 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `5c11d903-0bb0-4694-8dae-c674d5c8082c` | ai | 0.900 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `a10ab9b8-7888-4db7-878d-1110c5ab4c3c` | unsure | 0.626 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `734b8a19-5792-40e2-bd37-ace24f1b7551` | ai | 0.835 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `e5284a7b-a421-4944-a111-0cebfb48e298` | ai | 0.794 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `1a6420d6-c0ad-407c-81d2-f9404d6747f2` | ai | 0.783 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `4b9a4cfb-8665-4d72-8edb-9a340ad48527` | ai | 0.883 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `c7d1270c-5fd3-402c-be1b-2b676b3265f6` | unsure | 0.745 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `9cc6def7-8da7-4e11-9b48-ddaee0ebf6fa` | unsure | 0.691 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `a6b28f50-9efe-44c4-9933-4f08088dc4dc` | unsure | 0.447 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `5db7688f-4dd2-4f37-b2c8-b309f9d66136` | unsure | 0.381 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `95bbb7b2-5142-4452-8185-a3de5cee1499` | human | 0.252 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `ca24a06d-5295-4202-9071-98c9ee7d3ea9` | unsure | 0.639 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `9266ac90-9698-4376-b72c-3f3ff1a383e0` | unsure | 0.516 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `29c3b230-45d4-4ae2-aaba-6205eccd94e9` | unsure | 0.432 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `9ead866c-6691-490c-aa11-60e9e08a1d0d` | unsure | 0.601 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `453763e1-64bb-4813-8c89-20a93376c75c` | unsure | 0.350 |  |
| MF04 | malformed | text is only punctuation | 200 | `1fc0c730-fc46-4002-9412-c9e899fe17f6` | unsure | 0.350 |  |
| MF05 | malformed | text is a very long single word | 200 | `9545c9f4-e81c-4e69-8ca0-b8736c06900b` | unsure | 0.750 |  |
| MF06 | malformed | text is emoji only | 200 | `b9ddda60-026d-4e1d-b893-82eaf3927762` | unsure | 0.749 |  |
| MF07 | malformed | text is right-to-left script | 200 | `4f61d6d6-3a06-4b61-ba51-0049fdc52a0e` | unsure | 0.703 |  |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d321d8b7-0fd3-4452-b46c-e56d97bd4f03` | unsure | 0.350 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2760af42-b107-4d18-9f73-5358eabc8bdf` | unsure | 0.350 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b16acb1f-7170-48d0-9084-da8f4a8704cc` | unsure | 0.350 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d47e6437-0a78-42ce-8e3b-79d2b0b08de9` | unsure | 0.350 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2f364417-5b8f-40a1-b416-30839e5cd98d` | unsure | 0.350 |  |
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
  "content_id": "73d91338-3501-403b-bcd8-59cd31145fa2",
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
  "content_id": "e2d07a75-0142-42ea-a4e6-3afd0ddbffaa",
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
  "content_id": "3184ff2f-8965-4212-af0d-46c2b6313a6d",
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
  "content_id": "61817dda-4b7d-41de-9412-f7390acc77ef",
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
  "content_id": "c94aa304-2642-4463-85c7-76e0396dadc0",
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
  "content_id": "9b572a29-4e4f-4e84-94e5-2b03325b045a",
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
  "content_id": "6498d421-7d6c-4bcd-b625-0e852214e08e",
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
  "content_id": "e6dbdbac-69c3-4155-b9a9-bdb0a2b015b6",
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
  "content_id": "ee9526f0-392a-46a0-8022-d6d7987e602c",
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
  "content_id": "5c11d903-0bb0-4694-8dae-c674d5c8082c",
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
  "content_id": "a10ab9b8-7888-4db7-878d-1110c5ab4c3c",
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
  "content_id": "734b8a19-5792-40e2-bd37-ace24f1b7551",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.8346,
  "model_score": 0.7387,
  "style_score": 0.9304,
  "label": "Our check found strong signs that this may have been written with AI. Automated checks like ours can be wrong, especially about simple or very clear writing. If you wrote this yourself, please ask for a review and a person will look at it.",
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
  "content_id": "e5284a7b-a421-4944-a111-0cebfb48e298",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.794,
  "model_score": 0.8051,
  "style_score": 0.7829,
  "label": "Our check found strong signs that this may have been written with AI. Automated checks like ours can be wrong, especially about simple or very clear writing. If you wrote this yourself, please ask for a review and a person will look at it.",
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
  "content_id": "1a6420d6-c0ad-407c-81d2-f9404d6747f2",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.783,
  "model_score": 0.8329,
  "style_score": 0.733,
  "label": "Our check found strong signs that this may have been written with AI. Automated checks like ours can be wrong, especially about simple or very clear writing. If you wrote this yourself, please ask for a review and a person will look at it.",
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
  "content_id": "4b9a4cfb-8665-4d72-8edb-9a340ad48527",
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
  "content_id": "c7d1270c-5fd3-402c-be1b-2b676b3265f6",
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
  "content_id": "9cc6def7-8da7-4e11-9b48-ddaee0ebf6fa",
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
  "content_id": "a6b28f50-9efe-44c4-9933-4f08088dc4dc",
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
  "content_id": "5db7688f-4dd2-4f37-b2c8-b309f9d66136",
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
  "content_id": "95bbb7b2-5142-4452-8185-a3de5cee1499",
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
  "content_id": "ca24a06d-5295-4202-9071-98c9ee7d3ea9",
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
  "content_id": "9266ac90-9698-4376-b72c-3f3ff1a383e0",
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
  "content_id": "29c3b230-45d4-4ae2-aaba-6205eccd94e9",
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
  "content_id": "9ead866c-6691-490c-aa11-60e9e08a1d0d",
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
  "content_id": "453763e1-64bb-4813-8c89-20a93376c75c",
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
  "content_id": "1fc0c730-fc46-4002-9412-c9e899fe17f6",
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
  "content_id": "9545c9f4-e81c-4e69-8ca0-b8736c06900b",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.75,
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
  "content_id": "b9ddda60-026d-4e1d-b893-82eaf3927762",
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
  "content_id": "4f61d6d6-3a06-4b61-ba51-0049fdc52a0e",
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
  "content_id": "d321d8b7-0fd3-4452-b46c-e56d97bd4f03",
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
  "content_id": "2760af42-b107-4d18-9f73-5358eabc8bdf",
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
  "content_id": "b16acb1f-7170-48d0-9084-da8f4a8704cc",
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
  "content_id": "d47e6437-0a78-42ce-8e3b-79d2b0b08de9",
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
  "content_id": "2f364417-5b8f-40a1-b416-30839e5cd98d",
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
