# Response to Problem 4: Construction

## Artifact: Measuring calibration collapse under time pressure

### The question

When a language model is asked to predict something and forced to commit to a single answer under increasing time/token constraints, does its *reported confidence* degrade gracefully (remaining realistic about its uncertainty), or does its confidence remain high even as accuracy drops (calibration collapse)?

This matters because if language models maintain high confidence even when accuracy drops, they become actively dangerous in decision-support settings: they will steer you confidently toward wrong answers.

### The procedure

**Setup:**
- Use a factual question dataset with verifiable ground truth (e.g., questions where the correct answer is a date, number, or entity that can be checked against reference sources).
- For each question, generate responses in two conditions:
  1. *Unrestricted*: ask the model for its best answer and a confidence estimate (0–100%)
  2. *Constrained*: ask for answer and confidence, but force the model to commit within a small token budget (e.g., 5 tokens, vs. typical 50–100)

**Input:** A prompt template with a factual question requiring a short factual answer:
```
Question: [QUESTION]
Answer (one sentence):
Confidence (0-100%):
```

For the constrained condition, set `max_tokens=5` (forces answer in 1–2 tokens, confidence as a single number).

**Predicted outputs:**
- *Unrestricted*: typical accuracy ~70–80% on a medium-difficulty trivia dataset, with confidence peaks around correct answers and dips around incorrect ones.
- *Constrained*: accuracy should drop (because the model has fewer tokens to reason), but the key prediction is about confidence. If calibration is *maintained*, confidence should also drop proportionally to accuracy loss. If calibration *collapses*, confidence should stay high despite accuracy drop.

**Procedure:**
1. Select 100–200 factual questions (geography, history, science, dates) with single-word or short-phrase answers.
2. Generate responses (unrestricted) and record: answer, stated confidence, correctness.
3. Generate responses (constrained, max_tokens=5) and record the same.
4. Compute expected calibration error (ECE) for each condition:
   - Bin responses by stated confidence (0–20%, 20–40%, etc.)
   - For each bin, compute actual accuracy
   - ECE = average |stated confidence - observed accuracy| across bins
5. Compare ECE in unrestricted vs. constrained conditions.

### Predicted result

I predict calibration will *partially collapse* under constraints: confidence will drop less than accuracy does, producing higher ECE in the constrained condition. This is because:

- Token limits prevent the model from expressing uncertainty through hedging language ("I'm not sure, but probably…").
- The model must output a single number 0–100, and its token budget does not allow for nuance.
- Language models trained on internet text learn to be overconfident; constraining tokens removes the "escape valves" (hedging language) that let well-calibrated models express that overconfidence as uncertainty.

**Quantitative prediction:** ECE should increase by 15–30% in the constrained condition.

### Two ways this artifact could mislead me

**False positive: Confidence format artifact.** The constrained condition requires confidence as a single token (e.g., "73%"). The model might parse this differently than the unrestricted condition, where confidence can span multiple tokens. The model might have learned different token-generation patterns for confidence depending on context length. This is not actually measuring time pressure; it is measuring format-dependency. 

*Control:* Run a third condition with normal token budget but the same single-token-confidence format. If calibration in this condition matches unrestricted, the effect is format-dependent, not budget-dependent.

**False negative: The model doesn't degrade gracefully.** If the model's accuracy does *not* drop substantially under token constraints, the experiment may show no calibration collapse because the model is not making different mistakes—it is successfully compressing reasoning. In this case, the artifact does not test what I think it tests (time pressure as a stressor for miscalibration) because there is no stress.

*Control:* Measure reasoning depth (e.g., estimate time spent reasoning by token count of intermediate working) and verify that the constrained condition produces shallower reasoning, not just more concise reasoning.

### Why this matters

If calibration collapses under constraint, it implies that in real-world decision-support settings where latency matters (you want a fast answer from the model), you cannot trust the model's stated confidence. This has implications for how these systems should be deployed: confidence should be reestimated offline on a held-out dataset, not trusted as-is from the model's output.

If calibration is maintained, it suggests the model's training makes it robust to this kind of constraint, and confidence could be more trustworthy.

### Implementation sketch (pseudocode)

```python
import anthropic

def test_calibration(question: str, constrained: bool) -> dict:
    prompt = f"Question: {question}\nAnswer (one sentence):\nConfidence (0-100%):"
    
    client = anthropic.Anthropic()
    max_tokens = 5 if constrained else 200
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}]
    )
    
    text = response.content[0].text
    # Parse answer and confidence from text
    # (Implementation: regex or manual parsing)
    answer, confidence = parse_response(text)
    return {"answer": answer, "confidence": confidence}

def compute_ece(responses: list[dict]) -> float:
    bins = [(0, 20), (20, 40), (40, 60), (60, 80), (80, 100)]
    ece = 0.0
    for low, high in bins:
        in_bin = [r for r in responses if low <= r['confidence'] < high]
        if not in_bin:
            continue
        observed_acc = sum(r['correct'] for r in in_bin) / len(in_bin)
        expected_conf = (low + high) / 2 / 100
        ece += abs(observed_acc - expected_conf) * len(in_bin) / len(responses)
    return ece
```

This artifact is self-contained, testable, and would actually inform a design decision about using language models in time-sensitive settings.