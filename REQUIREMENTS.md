# Requirements: Private Legal Document Triage Agent

Based on **ZeroDay OSS Hacktoberfest 2026, Problem Statement 2** (IIIT Dharwad). Follow the rules in `CLAUDE.md` at all times.

## 1. Goal

A privacy-first app that runs fully on the device, using a local Gemma 3n-class model. It reads a legal document, explains it in plain language, highlights risks, cites source passages, shows uncertainty and recommends a lawyer when needed.
**It is not legal advice.**

## 2. Target users

Ordinary people who are **not lawyers** but must sign or respond to legal documents, for example:

- Students
- Tenants
- Employees

## 3. Scope

| Item | Decision |
|---|---|
| Document types | **TBD** (team to decide, e.g. rental agreements and employment contracts) |
| Language | English |
| Input formats | PDF (text-based) and `.txt` |
| Model | Local Gemma 3n-class (E2B/E4B). Variant, runtime, quantization and calling method are **TBD** (Shiven, see `INTEGRATION_CONTRACT.md`) |

**Out of scope for the MVP:**

- Scanned image PDFs / OCR
- Languages other than English
- Deciding whether anything is legally valid, legal or enforceable

## 4. MUST HAVE: official requirements (L1–L10)

These are mandatory.

| ID | Requirement | Owner | Done |
|---|---|---|---|
| L1 | Upload and read a PDF or plain-text file locally | Siddhesh (upload UI) + Shiven (parsing) | [ ] |
| L2 | Extract and understand the document's contents on the device | Shiven | [ ] |
| L3 | Plain-language summary and explanations of important clauses | Shiven (model) + Siddhesh (display) | [ ] |
| L4 | Find obligations, rights, deadlines, penalties, termination conditions and concerns | Shiven | [ ] |
| L5 | Every answer shows the exact supporting passage and page number | Shiven + Siddhesh | [ ] |
| L6 | Clearly separate "Stated in document" from "Possible interpretation" | Ayush (rules) + Siddhesh (display) | [ ] |
| L7 | Flag ambiguity, missing information and jurisdiction-dependent issues | Ayush | [ ] |
| L8 | Refuse unsupported conclusions (e.g. "Is this enforceable?") and recommend a qualified lawyer | Ayush | [ ] |
| L9 | Prove private content never leaves the device (offline test + network monitoring) | Ayush | [ ] |
| L10 | Meaningful local Gemma use and a reproducible open-source setup | Shiven | [ ] |

## 5. MUST HAVE: app features for the demo

| Feature | Details | Owner | Done |
|---|---|---|---|
| Upload screen | Friendly errors for an empty, broken, wrong-format or too-large file | Siddhesh | [ ] |
| Summary screen | Most important risks shown first | Siddhesh | [ ] |
| Finding cards | Category, plain explanation, quote, page, label (stated / interpretation), confidence, warnings | Siddhesh | [ ] |
| Question box | Ask about the document; answer with citations, or clearly say "The document does not mention this" | Siddhesh + Shiven | [ ] |
| Disclaimer | "This is not legal advice" notice always visible | Siddhesh + Ayush | [ ] |
| Lawyer banner | Lawyer recommendation shown when risk or uncertainty is high | Ayush + Siddhesh | [ ] |
| Privacy panel | "Processed locally" status and a "Delete document" button | Ayush + Siddhesh | [ ] |
| Offline mode | Works with the network turned off after setup | Ayush | [ ] |

## 6. SHOULD HAVE (if time allows)

- [ ] Click a finding to jump to or highlight its passage in the document
- [ ] Structured extraction of parties, dates, amounts and penalties
- [ ] Detect missing, unusual or conflicting clauses
- [ ] Prompt-injection protection test (document text trying to give the AI instructions)
- [ ] Show processing time and memory use

## 7. NICE TO HAVE (never penalised if missing)

- [ ] Compare two versions of a document
- [ ] Local OCR for scanned PDFs
- [ ] Explanations in Hindi or other Indian languages (generated locally)
- [ ] Export a report as a local file

## 8. Non-functional requirements

| Area | Requirement |
|---|---|
| Privacy | No cloud APIs, no telemetry, no external fonts/CDNs, no logs containing document text |
| Honesty | No invented clauses, quotes or page numbers; no hard-coded answers |
| Usability | A non-lawyer can understand every screen |
| Robustness | Long documents, messy layouts and bad input must not crash the app |
| Reproducibility | Pinned dependencies; the README lets a newcomer install and run the app |

## 9. Required submission items

- [ ] Public repo with an open-source licence file
- [ ] README: overview, setup, how to run, configuration, troubleshooting
- [ ] Pinned requirements, tool versions, OS/hardware tested, model file size
- [ ] Architecture diagram or explanation
- [ ] Dataset sources, licences and attributions
- [ ] How Gemma is used: variant, quantization, runtime, how to download weights (all **TBD** until Shiven confirms)
- [ ] Proof of local processing: a recording or log of a full analysis with the network disabled + connection-monitoring output
- [ ] Sample outputs: cited passages beside the source, and a "document is silent" case
- [ ] Refusal/escalation examples and prompt-injection test results (recommended)
- [ ] Demo video, up to about 5 minutes, showing the real system and its limits
- [ ] Testing results and known limitations
- [ ] Short statement of our main technical contribution

## 10. Judging priorities

| Criterion | Points |
|---|---|
| Accuracy | 15 |
| Grounding / citations | 15 |
| Uncertainty / refusal | 15 |
| Privacy | 15 |
| Robustness | 12 |
| Gemma use | 10 |
| Reusability / docs | 10 |
| Usability | 8 |
| **Total** | **100** |

> ⚠️ **If grounding, uncertainty or privacy is poor, the score is capped at 40.** These three come first.

## 11. Definition of done

A feature is **done** only when it:

- [ ] works on a document we did **not** prepare in advance,
- [ ] shows citations (quote + page number), and
- [ ] works with the **network turned off**.
