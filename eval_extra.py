#!/usr/bin/env python3
"""
The two criteria run_eval.py can't express — they need several requests in a
row, each depending on the last.

    python eval_extra.py --label before

  Criterion 4 — appeals. Submit 5 texts, appeal each content_id, then check
                GET /content/<id> says under_review and GET /log holds the
                appeal. Then appeal a made-up content_id and expect a 404.
  Criterion 5 — the block. Send 3 bad inputs from one creator_id, then a valid
                submission from the same creator, and expect a 429 "blocked".

Three trials each. Every trial uses fresh creator_ids so one trial's bad
inputs can't spill into the next. Writes results/extra_<date>_<label>.md.
"""

import argparse
import datetime as dt
import json
import uuid

import requests

import config

URL = f"http://{config.HOST}:{config.PORT}"

APPEAL_TEXTS = [
    "We got to the campsite about four. The pitch was a bit sloped, but there was a tap nearby. Putting the tent up took longer than it should have.",
    "Regular exercise is essential for maintaining good health. It helps to strengthen the heart, improve mood, and increase energy levels.",
    "My grandmother kept her buttons in a biscuit tin. Nobody ate biscuits from it. Ever. When she died we opened it expecting letters.",
    "Time management is a key skill for success in both school and work. It involves planning tasks, setting priorities, and using time effectively.",
    "The bus was late again, so I walked. It was raining. By the time I got there my shoes were soaked and the meeting had started without me.",
]


def appeal_trial(tag):
    rows = []
    for i, text in enumerate(APPEAL_TEXTS, 1):
        sub = requests.post(f"{URL}/submit", json={"text": text, "creator_id": f"eval_appeal_{tag}_{i}"}).json()
        cid = sub["content_id"]
        app = requests.post(f"{URL}/appeal", json={"content_id": cid, "reasoning": "I wrote this myself."})
        status = requests.get(f"{URL}/content/{cid}").json().get("status")
        in_log = any(
            e.get("content_id") == cid and e.get("event") == "appeal"
            for e in requests.get(f"{URL}/log").json()["entries"]
        )
        rows.append({"content_id": cid, "appeal_status_code": app.status_code,
                     "appeal_response": app.json(), "status_after": status,
                     "appeal_in_log": in_log,
                     "passed": app.status_code == 200 and status == "under_review" and in_log})
    fake = requests.post(f"{URL}/appeal", json={"content_id": f"fake-{uuid.uuid4()}", "reasoning": "x"})
    rows.append({"content_id": "fake", "appeal_status_code": fake.status_code,
                 "appeal_response": fake.json(), "passed": fake.status_code == 404})
    return rows


def block_trial(tag):
    creator = f"eval_block_{tag}"
    sent = [{"creator_id": creator}, {"text": "", "creator_id": creator},
            {"text": "  ", "creator_id": creator},
            {"text": APPEAL_TEXTS[0], "creator_id": creator}]
    rows = []
    for body in sent:
        r = requests.post(f"{URL}/submit", json=body)
        rows.append({"sent": json.dumps(body)[:80], "status": r.status_code, "response": r.json()})
    rows[-1]["passed"] = rows[-1]["status"] == 429 and rows[-1]["response"].get("error") == "blocked"
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", default="")
    parser.add_argument("--trials", type=int, default=3)
    args = parser.parse_args()

    run = dt.datetime.now().strftime("%H%M%S")
    lines = [f"# Extra criteria — {args.label}", "",
             "- Produced by: `eval_extra.py::main`",
             "- Service: `app.py::submit`, `app.py::appeal`, `app.py::get_content`", ""]
    summary = []
    for t in range(1, args.trials + 1):
        tag = f"{args.label}_{run}_{t}"
        appeals = appeal_trial(tag)
        block = block_trial(tag)
        a_pass = sum(r["passed"] for r in appeals[:5])
        fake_ok = appeals[5]["passed"]
        b_ok = block[-1]["passed"]
        summary.append((t, a_pass, fake_ok, b_ok))
        print(f"trial {t}: appeals {a_pass}/5, fake id 404: {fake_ok}, blocked after 3 bad: {b_ok}")
        lines += [f"## Trial {t}", "", "### Criterion 4 — appeals", "", "```json",
                  json.dumps(appeals, indent=2), "```", "",
                  "### Criterion 5 — block after 3 bad inputs", "", "```json",
                  json.dumps(block, indent=2), "```", ""]

    lines[5:5] = ["| Trial | Appeals passed | Fake id → 404 | Blocked after 3 bad |",
                  "|---|---|---|---|",
                  *[f"| {t} | {a}/5 | {f} | {b} |" for t, a, f, b in summary], ""]
    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    path = config.RESULTS_DIR / f"extra_{stamp}_{args.label}.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
