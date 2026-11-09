"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies. ← TODO

    Returns:
        A float. Decide yourself what scale it's on and which direction means
        "more human" — then write that down, because your combining rule
        depends on knowing it.

    A hint on what you're reaching for: the standard deviation of sentence
    lengths, probably divided by the mean so a long text and a short one are
    comparable. `statistics.stdev` is imported for you.

    Watch the edge case: a one-sentence submission has no spread at all, and
    `stdev` raises on fewer than two values. Decide what that should return
    before the attack set decides for you.
    """
    # Coefficient of variation: stdev over mean, so long and short texts compare.
    # Higher = more varied = more human. Under two sentences there is no spread
    # to measure, so this returns 0.0 and style_signal treats it as neutral.
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    mean = statistics.mean(lengths)
    return round(statistics.stdev(lengths) / mean, 4)


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words. ← TODO

    Returns:
        A float between 0 and 1. Higher means more varied vocabulary.

    Worth knowing before you rely on it: this measure falls as text gets
    longer, because common words repeat. Two texts of different lengths aren't
    directly comparable on it, and if your test inputs vary a lot in length,
    that alone can look like a signal.
    """
    # Moving-average TTR: the plain ratio over every 50-word window, averaged.
    # That keeps a 300-word piece comparable with a 60-word one. Texts shorter
    # than one window fall back to the plain ratio.
    ws = words(text)
    if not ws:
        return 0.0
    window = 50
    if len(ws) <= window:
        return round(len(set(ws)) / len(ws), 4)
    ratios = [
        len(set(ws[i:i + window])) / window
        for i in range(len(ws) - window + 1)
    ]
    return round(statistics.mean(ratios), 4)


def punctuation_density(text: str) -> float:
    """
    How much punctuation, relative to length. ← TODO

    Returns:
        A float. Whether you count all punctuation or only some kinds — commas,
        semicolons, dashes — is a real choice. Semicolons and em dashes are
        more interesting than full stops, because they vary more between
        writers.
    """
    # Everything but full stops, per word. Full stops track sentence count,
    # which spread already covers; commas, dashes, semicolons, colons,
    # brackets, quotes, ! and ? are where writers differ. Higher = more human.
    ws = words(text)
    if not ws:
        return 0.0
    marks = re.findall(r"[,;:!?()\"'\u2014\u2013\u2018\u2019\u201c\u201d]|--| - ", text)
    return round(len(marks) / len(ws), 4)


def _scale_to_ai(value: float, human_at: float, ai_at: float) -> float:
    """
    Map a raw measure onto 0–1 AI-ness: `ai_at` or beyond scores 1.0,
    `human_at` or beyond scores 0.0, linear in between.
    """
    t = (value - human_at) / (ai_at - human_at)
    return min(max(t, 0.0), 1.0)


# Where each measure reads fully human and fully AI. Set from the Milestone 4
# calibration inputs — see README, Signals and Scoring.
SPREAD_HUMAN, SPREAD_AI = 0.65, 0.25
TTR_HUMAN, TTR_AI = 0.90, 0.70
PUNCT_HUMAN, PUNCT_AI = 0.20, 0.06

# How much each measure counts toward the style signal.
W_SPREAD, W_TTR, W_PUNCT = 0.5, 0.2, 0.3


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.** ← TODO

    Combine your three measures into one number. Same direction as
    `detector.model_signal`, so that `scoring.combine_signals` can treat them
    the same way — if one of your signals runs backwards, everything above it
    is wrong in a way that's hard to see.

    Two things to decide and write down:

      1. Which direction each measure points. Low spread means more AI-ish, so
         it needs flipping. Work out which of your three need that.
      2. How to get each onto a comparable scale. A raw type-token ratio sits
         between 0 and 1; a raw punctuation count doesn't. Adding them
         unscaled means whichever has the bigger numbers wins by default.

    Test it on the four calibration inputs from Milestone 4 — clearly AI,
    clearly human, plain conventional human writing, lightly-edited AI — before
    you trust it. Plain and ordinary, not formal: formal prose reads as *human*
    to signal one, and it is plain writing that gets accused.
    """
    if not words(text):
        return 0.5

    # One sentence has no spread at all — that's missing evidence, not
    # evidence of AI, so it counts as a coin flip.
    if len(sentences(text)) < 2:
        spread_ai = 0.5
    else:
        spread_ai = _scale_to_ai(sentence_length_spread(text), SPREAD_HUMAN, SPREAD_AI)

    ttr_ai = _scale_to_ai(type_token_ratio(text), TTR_HUMAN, TTR_AI)
    punct_ai = _scale_to_ai(punctuation_density(text), PUNCT_HUMAN, PUNCT_AI)

    score = W_SPREAD * spread_ai + W_TTR * ttr_ai + W_PUNCT * punct_ai
    return round(score, 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
