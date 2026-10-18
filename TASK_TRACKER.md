# Task Tracker: 10-Hour Build

**Start time: ____** (this is Hour 0)

Follow `CLAUDE.md`, `REQUIREMENTS.md` and `INTEGRATION_CONTRACT.md`.

| Member | Area |
|---|---|
| Siddhesh and Anshuman | UI (Python + Streamlit) |
| Shiven | Backend + local Gemma |
| Ayush | Safety + privacy |

## 1. How to use this file

- **Update your own rows only.**
- Use one of these status words: **To do** · **In progress** · **Done** · **Blocked**
- If a task is **Blocked**, write a short reason and who you're waiting on in the status cell. Also add it to the [Blockers log](#10-blockers-log).
- "Hour 2" means 2 hours after the start time above.

## 2. Team sync checkpoints

Short check-ins of 5–10 minutes. Everyone attends.

| Hour | Checkpoint | Done |
|---|---|---|
| 1 | Approve `INTEGRATION_CONTRACT.md` and `core/contract.py` | [ ] |
| 4 | First end-to-end run (UI + real backend + safety) on one document | [ ] |
| 7 | **Feature freeze.** Only fixes, tests and docs after this | [ ] |
| 9 | Full offline test + record the demo video | [ ] |
| 10 | Final push and submit | [ ] |

## 3. Phase 0: Setup (Hour 0–1), everyone

| Task | Owner | Status | Done |
|---|---|---|---|
| Finalise `CLAUDE.md`, `REQUIREMENTS.md`, `UI_UX_GUIDELINES.md`, `INTEGRATION_CONTRACT.md`, `TASK_TRACKER.md` and push to `main` | All | To do | [ ] |
| Create branches: `ui`, `backend`, `safety-privacy` | All | To do | [ ] |
| Decide which document types we support | All | To do | [ ] |
| Create `core/contract.py` from `INTEGRATION_CONTRACT.md` (dataclasses + error classes); get all three approvals | All | To do | [ ] |
| Add a `LICENSE` file (open-source) | All | To do | [ ] |
| Add `.gitignore` (`models/`, `.env`, temp files, private documents) | All | To do | [ ] |
| Add `requirements.txt` with pinned versions | All | To do | [ ] |
| `.streamlit/config.toml` with `gatherUsageStats = false` and `server.address = "localhost"` | Ayush | To do | [ ] |

## 4. Siddhesh: UI tasks

| ID | Task | Hour target | Status | Depends on |
|---|---|---|---|---|
| U1 | `app.py` skeleton: `st.set_page_config`, sidebar, tabs | 1–2 | To do | — |
| U2 | `core/stub_backend.py` with SAMPLE DATA matching `core/contract.py` | 1–2 | To do | `core/contract.py` approved |
| U3 | `ui/upload.py`: file uploader, file checks, spinner, friendly errors | 2 | To do | U1, U2 |
| U4 | `ui/summary.py`: overview and top risks | 2–3 | To do | U2 |
| U5 | `ui/clauses.py`: finding cards, source passage expander, filters | 3 | To do | U2 |
| U6 | `ui/chat.py`: question box, answers with citations, not-in-document and refusal states | 3–4 | To do | U2 |
| U7 | `ui/sidebar.py`: not-legal-advice notice, privacy status, delete button | 4 | To do | U1 (delete button also needs S6) |
| U8 | Switch from stub to real backend; test end to end | 4–5 | To do | B5 (Shiven); safety review S2–S4 (Ayush) |
| U9 | Polish: accessibility, colours + labels, empty/loading/error states | 5–7 | To do | U3–U7 |
| U10 | Remove the stub completely before the demo | 7 | To do | U8 |
| U11 | Screenshots for README; help record the demo | 8–9 | To do | U10 |

## 5. Shiven: backend tasks

| ID | Task | Hour target | Status | Depends on |
|---|---|---|---|---|
| B1 | Choose Gemma variant and runtime; fill in the model TBDs in `INTEGRATION_CONTRACT.md` | 0–1 | To do | — |
| B2 | Download the model locally; write setup steps for the README | 1–2 | To do | B1 |
| B3 | `backend/model.py`: load the model, `is_model_available()` | 1–2 | To do | B1, B2 |
| B4 | Document parsing: PDF and .txt to text with page numbers; chunking for long documents | 2–3 | To do | `core/contract.py` approved |
| B5 | `analyze_document()`: summary + findings with real citations | 3–4 | To do | B3, B4 |
| B6 | `answer_question()` with citations and the `not_in_document` case | 4–5 | To do | B5 |
| B7 | Measure speed and memory; record them in the README | 6–7 | To do | B5, B6 |
| B8 | Test on CUAD or other licensed sample documents we didn't prepare | 6–8 | To do | B5, B6 |

## 6. Ayush: safety and privacy tasks

| ID | Task | Hour target | Status | Depends on |
|---|---|---|---|---|
| S1 | `.streamlit/config.toml` privacy settings | 0–1 | To do | — |
| S2 | `safety/review.py`: quote verification (every quote must exist in `full_text`) | 2–3 | To do | `core/contract.py` approved |
| S3 | Refusal rules for legal / enforceable / valid questions + lawyer notes | 3–4 | To do | S2 |
| S4 | Ambiguity and jurisdiction flags; label stated vs interpretation | 3–4 | To do | S2 |
| S5 | Prompt-injection protection + a test document with hidden instructions | 4–5 | To do | S2 |
| S6 | `privacy/cleanup.py`: `delete_document_data()` and temp file handling | 4–5 | To do | — |
| S7 | Offline test: run a full analysis with Wi-Fi off; record proof | 6–7 | To do | U8 (end-to-end working) |
| S8 | Network monitoring proof during processing (tool **TBD**); save the output | 7–8 | To do | S7 |
| S9 | Code + dependency check for any remote calls or telemetry | 7–8 | To do | — |

## 7. Shared tasks: testing and documentation

| ID | Task | Owner | Hour target | Status |
|---|---|---|---|---|
| T1 | `tests/` for each folder: bad files, empty file, long file, silent question, refusal question, prompt injection | Each owner | 5–8 | To do |
| D1 | README: overview, setup, how to run, configuration, troubleshooting | All | 7–9 | To do |
| D2 | Architecture diagram / explanation | Shiven + Siddhesh | 7–9 | To do |
| D3 | Privacy explanation, listing every network call | Ayush | 7–9 | To do |
| D4 | Datasets used, licences, attributions | Shiven | 7–9 | To do |
| D5 | Known limitations and test results, stated honestly | All | 7–9 | To do |
| D6 | Main technical contribution statement | All | 7–9 | To do |
| D7 | Demo video, up to 5 minutes: real system, citations, silent case, refusal, offline proof | All | 9 | To do |

## 8. Final submission checklist

- [ ] Public repo + open-source licence
- [ ] README complete
- [ ] Pinned `requirements.txt`
- [ ] Model download instructions
- [ ] Architecture doc
- [ ] Dataset sources and licences
- [ ] Offline proof + network monitoring output
- [ ] Sample outputs with citations, and a "document is silent" case
- [ ] Refusal / escalation examples
- [ ] Prompt-injection test results
- [ ] Demo video (≤ 5 minutes)
- [ ] Known limitations
- [ ] No secrets, model weights or private documents committed
- [ ] Stub removed (`core/stub_backend.py` gone, `USE_STUB` off)

## 9. Risks and backup plans

| Risk | Backup plan |
|---|---|
| Model too slow on a laptop | Use the smaller variant (E2B), shorter chunks, or limit the number of pages |
| Model won't run on someone's laptop | Run the demo on the strongest laptop; document the hardware used |
| Backend is late | UI keeps working on the stub; the Hour 4 checkpoint is the integration deadline |
| Running out of time | Drop SHOULD HAVE and NICE TO HAVE features first, **never** the MUST HAVE list |

## 10. Blockers log

| Time | Blocker | Waiting on | Resolved? |
|---|---|---|---|
| | | | |
