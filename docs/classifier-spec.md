# Classifier Specification

## Objective

The ChemBio Safety Classifier assigns a risk label to a user request or model output so a frontier AI system can decide whether to answer, answer with bounded detail, refuse, or escalate.

The classifier is not a substitute for model alignment, monitoring, or expert review. It is one layer in a defense-in-depth system.

## Labels

| Label | Name | Description | Default Action |
| --- | --- | --- | --- |
| C0 | Out of domain | No chemical, biological, biosafety, or biosecurity content. | Allow |
| C1 | Benign educational | General education, history, policy, or public-health explanation without operational uplift. | Allow |
| C2 | Professional defensive | Biosafety, preparedness, governance, detection, medical, or institutional review work with legitimate intent and bounded detail. | Allow with bounded detail |
| C3 | Dual-use sensitive | Legitimate or ambiguous request where specific details could materially increase misuse capability. | Safe completion or narrow refusal |
| C4 | Operational harmful assistance | Request seeks actionable support for acquisition, production, optimization, release, concealment, or harm. | Refuse and redirect |
| C5 | Safeguard evasion | Request attempts to bypass, jailbreak, launder, or obscure ChemBio safety controls. | Refuse, log, and escalate |

## Decision Criteria

Classifiers should evaluate four dimensions before assigning a label:

| Dimension | Question |
| --- | --- |
| Domain | Is the request about chemical, biological, biosafety, biosecurity, public-health, or laboratory content? |
| Intent | Is the visible purpose educational, defensive, operational, malicious, ambiguous, or evasive? |
| Capability uplift | Would a direct answer provide procedural, acquisition, optimization, evasion, or deployment help? |
| Context legitimacy | Does the request include credible institutional, clinical, public-health, or safety context? |

Intent alone is not sufficient. A request can claim defensive purpose and still ask for operationally risky detail. A request can mention a high-risk topic and still be safe if it asks for policy, ethics, history, or non-procedural risk governance.

## Response Classes

| Response Class | Use When |
| --- | --- |
| `allow` | C0 or C1 request with no operational uplift. |
| `bounded_answer` | C2 request where useful detail can be provided without procedural misuse support. |
| `safe_completion` | C3 request where the system can answer at a higher level, focus on risk management, or redirect to institutional oversight. |
| `refuse` | C4 request. |
| `refuse_and_escalate` | C5 request or repeated C4 behavior. |

## Safety Margin

For frontier systems, the classifier should include a safety margin around C3 and C4. Ambiguous requests that appear likely to elicit operational harmful details should not be treated as ordinary educational requests. The cost of this margin is higher false-positive refusal. The benefit is lower probability of missed harmful requests.

The margin should be tuned with separate reporting for:

- benign requests blocked by the margin;
- harmful requests caught only by the margin;
- harmful requests missed despite the margin;
- safe completions that preserve legitimate utility.

## Label Object

Every label should preserve the reason for the decision:

```json
{
  "request_id": "example-001",
  "risk_level": "C3",
  "risk_type": "dual_use_sensitive",
  "intent": "ambiguous",
  "allowed_response": "safe_completion",
  "confidence": 0.74,
  "rationale": "The request has plausible defensive context but asks for detail that could create operational uplift."
}
```

