---
name: ab-test-analysis
description: "Analyze A/B test results with statistical significance, sample size validation, confidence intervals, and ship/extend/stop recommendations. Use when evaluating experiment results, checking if a test reached significance, interpreting split test data, or deciding whether to ship a variant."
---

## A/B Test Analysis

Evaluate A/B test results with statistical rigor and translate findings into clear product decisions.

### Context

You are analyzing A/B test results for **$ARGUMENTS**.

If the user provides data files (CSV, Excel, or analytics exports), read and analyze them directly. Generate Python scripts for statistical calculations when needed.

### Instructions

1. **Understand the experiment**:
   - What was the hypothesis?
   - What was changed (the variant)?
   - What is the primary metric? Any guardrail metrics?
   - How long did the test run?
   - What is the traffic split?

2. **Validate the test setup**:
   - **Sample size**: Is the sample large enough for the expected effect size?
     - Use the formula: n = (Z²α/2 × 2 × p × (1-p)) / MDE²
     - Flag if the test is underpowered (<80% power)
   - **Duration**: Did the test run for at least 1-2 full business cycles?
   - **Randomization**: Any evidence of sample ratio mismatch (SRM)?
   - **Novelty/primacy effects**: Was there enough time to wash out initial behavior changes?

3. **Calculate statistical significance**:
   - **Conversion rate** for control and variant
   - **Relative lift**: (variant - control) / control × 100
   - **p-value**: Using a two-tailed z-test or chi-squared test
   - **Confidence interval**: 95% CI for the difference
   - **Statistical significance**: Is p < 0.05?
   - **Practical significance**: Is the lift meaningful for the business?

   If the user provides raw data, generate and run a Python script to calculate these.

4. **Check guardrail metrics**:
   - Did any guardrail metrics (revenue, engagement, page load time) degrade?
   - A winning primary metric with degraded guardrails may not be a true win

5. **Interpret results**:

   | Outcome | Recommendation |
   |---|---|
   | Significant positive lift, no guardrail issues | **Ship it** — roll out to 100% |
   | Significant positive lift, guardrail concerns | **Investigate** — understand trade-offs before shipping |
   | Not significant, positive trend | **Extend the test** — need more data or larger effect |
   | Not significant, flat | **Stop the test** — no meaningful difference detected |
   | Significant negative lift | **Don't ship** — revert to control, analyze why |

6. **Provide the analysis summary**:
   ```
   ## A/B Test Results: [Test Name]

   **Hypothesis**: [What we expected]
   **Duration**: [X days] | **Sample**: [N control / M variant]

   | Metric | Control | Variant | Lift | p-value | Significant? |
   |---|---|---|---|---|---|
   | [Primary] | X% | Y% | +Z% | 0.0X | Yes/No |
   | [Guardrail] | ... | ... | ... | ... | ... |

   **Recommendation**: [Ship / Extend / Stop / Investigate]
   **Reasoning**: [Why]
   **Next steps**: [What to do]
   ```

Think step by step. Save as markdown. Generate Python scripts for calculations if raw data is provided.

---

### Common Scenarios & How to Interpret

| Scenario | What It Means | What to Do |
|----------|--------------|------------|
| **Positive lift, p < 0.05, no guardrail issues** | Clear win | Ship it |
| **Positive lift, p < 0.05, but guardrail degraded** | Win on primary but side effects | Investigate trade-off. Is guardrail degradation acceptable? Can you mitigate it? |
| **Positive lift, p = 0.05–0.10** | Suggestive but inconclusive | Extend the test for more data. Calculate how many more days/users needed |
| **Positive lift, p > 0.10** | Likely noise | Stop unless business impact would be large enough to justify extending |
| **Flat result, tight confidence interval** | No real difference between variants | Stop. The change doesn't matter. Try a bolder variant |
| **Flat result, wide confidence interval** | Underpowered test | Extend or increase traffic allocation. You can't conclude anything yet |
| **Negative lift, p < 0.05** | Variant is worse | Revert immediately. Analyze why — was the hypothesis wrong, or was execution flawed? |
| **Multiple metrics moved in different directions** | Trade-off situation | Prioritize by business impact. A 2% conversion lift that causes 10% revenue drop is a net loss |
| **Significant result in first 48 hours** | Likely novelty effect or SRM | Don't call it early. Wait for at least 1 full business cycle (7 days minimum) |
| **Result flips direction mid-test** | Instability, possible external factor | Check for holidays, marketing campaigns, bugs, or traffic source changes |

### What NOT to Do

- **Don't peek and stop early.** Checking significance daily inflates false positive rates. Set the sample size upfront and commit to it.
- **Don't run tests without a hypothesis.** "Let's see what happens" leads to post-hoc rationalization.
- **Don't ignore guardrail metrics.** A conversion lift that tanks revenue or increases support tickets is not a win.
- **Don't test tiny changes expecting big lifts.** Button color changes rarely move the needle. Test meaningful UX or value prop changes.
- **Don't combine multiple changes in one test.** You won't know which change caused the result. Test one variable at a time.

---

### Further Reading

- [A/B Testing 101 + Examples](https://www.productcompass.pm/p/ab-testing-101-for-pms)
- [Testing Product Ideas: The Ultimate Validation Experiments Library](https://www.productcompass.pm/p/the-ultimate-experiments-library)
- [Are You Tracking the Right Metrics?](https://www.productcompass.pm/p/are-you-tracking-the-right-metrics)
