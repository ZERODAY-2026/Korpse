# Korpse — Private-legal-triage

**ZeroDay OSS · Hacktoberfest 2026 · Problem Statement 2 (PS2)**

> A Python-based legal-triage prototype designed to help users organize legal concerns and receive preliminary, AI-assisted guidance.

| Project Detail | Information |
|---|---|
| Project Name | Korpse |
| Hackathon | ZeroDay OSS / Hacktoberfest 2026 |
| Problem Statement | PS2 |
| Team Size | 4 members |
| Language | Python |
| Planned UI | Streamlit |
| AI Integration | E2B / E4B models (exact model configuration to be confirmed) |
| Status | In Development |

---

## 1. Overview

Korpse is a hackathon project focused on making the initial understanding of a legal concern simpler and more accessible.

Users can describe a legal issue in plain language. The application is intended to process the description through an AI pipeline and present a structured preliminary response that helps users understand the nature of their concern and consider appropriate next steps.

The project aims to demonstrate a working end-to-end application within the hackathon's limited development time.

**Important:** Korpse is an experimental legal-triage tool. It does not replace a qualified lawyer or provide guaranteed legal advice. AI-generated information may be incomplete or incorrect and should be independently verified.

## 2. Objectives

- Provide a simple interface for describing legal concerns.
- Connect a Python application to an AI inference pipeline.
- Present responses in a readable and structured format.
- Handle invalid inputs and model failures gracefully.
- Build a modular codebase that team members can develop collaboratively.
- Demonstrate a functional prototype during the hackathon.

## 3. How It Works

### User Flow

```text
       ┌──────────────────────┐
       │   User opens Korpse  │
       └──────────┬───────────┘
                  │
                  ▼
       ┌──────────────────────┐
       │  Enter legal concern │
       └──────────┬───────────┘
                  │
                  ▼
       ┌──────────────────────┐
       │ Validate user input  │
       └──────────┬───────────┘
                  │
                  ▼
       ┌──────────────────────┐
       │    AI Pipeline       │
       └──────────┬───────────┘
                  │
                  ▼
       ┌──────────────────────┐
       │ Model inference      │
       └──────────┬───────────┘
                  │
                  ▼
       ┌──────────────────────┐
       │ Display triage result│
       └──────────┬───────────┘
                  │
                  ▼
       ┌──────────────────────┐
       │ Explain limitations │
       │ and possible next step│
       └──────────────────────┘
```

If the input is invalid or the model fails, the application should display a helpful error message instead of crashing.

## 4. System Architecture

```text
┌─────────────────────────────┐
│       User / Browser        │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Streamlit UI          │
│ Input, validation, results  │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       AI Pipeline           │
│ Processing and inference    │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       AI Model              │
│ E2B / E4B — configuration   │
│ to be finalized             │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Structured AI Response     │
└─────────────────────────────┘
```

The Streamlit interface should call a function in the AI pipeline instead of implementing model inference directly inside the UI. This separation makes the application easier to test and maintain.

## 5. Planned Project Structure

```text
Korpse/
├── README.md
├── requirements.txt
├── app.py
├── ai/
│   ├── __init__.py
│   ├── models.py
│   └── pipeline.py
├── tests/
│   └── test_pipeline.py
├── .gitignore
└── .env.example
```

*This is the proposed structure. Files should be added only when needed and checked against the actual repository.*

| File | Purpose |
|---|---|
| `README.md` | Project documentation and setup instructions |
| `requirements.txt` | Python dependencies |
| `app.py` | Streamlit interface and application entry point |
| `ai/models.py` | Model configuration and loading helpers |
| `ai/pipeline.py` | Main AI processing and inference workflow |
| `ai/__init__.py` | Python package initialization |
| `tests/test_pipeline.py` | Automated tests for pipeline behavior |
| `.gitignore` | Excludes virtual environments, caches, and secrets |
| `.env.example` | Documents required environment variable names |

## 6. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application language |
| Streamlit | Web-based user interface |
| Git | Version control |
| GitHub | Team collaboration and source hosting |
| E2B / E4B | Planned model integration; exact identifiers and runtime to be verified |
| VS Code | Development environment |

Model frameworks, additional packages, and hardware requirements will be documented once the team confirms the actual inference setup.

## 7. Team Responsibilities

The team consists of four members. Responsibilities should be coordinated according to the team's agreed division of work.

| Workstream | Responsibilities |
|---|---|
| AI / Model | Model setup, inference, and AI pipeline |
| UI / Integration | Streamlit interface and integration with the AI pipeline |
| Backend / Testing | Input/output contract, integration testing, and error handling |
| Git / Documentation | Repository coordination, documentation, and demo preparation |

Team members should agree on the AI pipeline's function signature and expected output format before integration.

For example, the interface could call:

```python
from ai.pipeline import run_triage

result = run_triage(user_text)
```

This is a proposed interface; the actual function must match the implementation in `ai/pipeline.py`.

## 8. Setup Instructions — Windows

### Prerequisites

- Python
- Git
- Visual Studio Code
- Access to the team's GitHub repository
- Any model-specific dependencies required by the AI implementation

### Step 1: Clone the repository

```powershell
git clone <TEAM_REPOSITORY_URL>
cd Korpse
```

Replace `<TEAM_REPOSITORY_URL>` with the actual repository URL. If the repository is already cloned, open the existing project folder instead.

### Step 2: Create a virtual environment

```powershell
py -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Run the application

Once `app.py`, the dependencies, and the required model configuration are implemented:

```powershell
streamlit run app.py
```

**Note:** These commands describe the intended setup. The application will not run successfully until its required files, dependencies, and AI integration are in place.

## 9. AI Model Integration

The project has discussed E2B and E4B model variants. Before finalizing the implementation, the team must confirm:

- Exact model identifiers and their sources.
- Model licenses and permitted uses.
- Python and framework compatibility.
- Download and storage requirements.
- CPU, GPU, memory, and runtime requirements.
- The function and output format expected by the UI.

### Integration Flow

```text
User Input
    ↓
Input Validation
    ↓
AI Pipeline
    ↓
Model Inference
    ↓
Response Processing
    ↓
Streamlit Output
```

A single tested model environment with a clear integration interface may be more practical than asking every teammate to install and run large models independently. The final approach should follow the hackathon rules and the team's technical constraints.

## 10. Git and Collaboration Workflow

Use Git to coordinate development and avoid overwriting teammates' work.

```powershell
git status
git pull
git switch -c feature/short-description
```

After making and testing changes:

```powershell
git add <files>
git commit -m "Describe the change"
git push -u origin feature/short-description
```

Open a pull request if required by the team workflow, review the changes, and merge into the agreed shared branch.

**Collaboration guidelines:**

- Check the current branch before editing or committing.
- Keep commits focused and use descriptive commit messages.
- Avoid editing the same file simultaneously without coordination.
- Pull recent changes before starting work.
- Review `git status` before every commit.
- Never commit API keys, passwords, private data, virtual environments, or downloaded model weights.
- Follow repository branch protection and pull-request rules.

## 11. Safety, Privacy, and Limitations

Because Korpse concerns legal issues, responsible handling of information is essential.

- Clearly label AI responses as preliminary information.
- Do not present generated legal claims as guaranteed facts.
- Do not invent statutes, citations, deadlines, or legal outcomes.
- Encourage professional legal assistance for high-impact or urgent matters.
- Avoid collecting unnecessary personal identifiers.
- Use synthetic examples for testing and demonstrations.
- Do not expose confidential case details in logs, screenshots, or public commits.
- Handle model failures and uncertain responses gracefully.
- Treat all model-generated output as untrusted content.

Korpse is a hackathon prototype and is not intended to replace professional legal services.

## 12. Testing Checklist

Before the final demonstration, verify that:

- [ ] The project starts using the documented command.
- [ ] Empty input is rejected appropriately.
- [ ] A normal test input produces a response.
- [ ] Long or malformed inputs are handled.
- [ ] Missing model configuration produces a useful error.
- [ ] Model failures do not crash the entire UI.
- [ ] The output is readable and includes an appropriate disclaimer.
- [ ] The demo uses synthetic, non-confidential information.
- [ ] Another team member can follow the setup instructions.
- [ ] All intended changes are committed to the correct branch.

## 13. Hackathon Execution Plan

The team has approximately ten hours for development, integration, and demonstration.

| Time | Priority |
|---|---|
| Hour 0–1 | Confirm scope, responsibilities, repository, and interface contract |
| Hours 1–3 | Test model inference and build the basic UI |
| Hours 3–5 | Connect the UI and AI pipeline |
| Hours 5–7 | Test error cases and fix integration issues |
| Hours 7–9 | Improve usability and prepare documentation |
| Hours 9–10 | Freeze features, test the demo, and prepare the presentation |

Prioritize a working end-to-end flow over optional features. If the model is not ready, a temporary mock response may be used during UI development, but it must not be represented as real model inference.

## 14. Current Status and Future Improvements

The project is under development. The following items should be confirmed or completed as implementation progresses:

- Final model identifiers and runtime configuration.
- Completed AI pipeline and agreed function contract.
- Working Streamlit-to-model integration.
- Input validation and useful error handling.
- Basic automated tests.
- Verified setup instructions.
- Final repository structure and team responsibilities.

Future improvements may include better response structuring, clearer uncertainty communication, expanded test coverage, and more robust handling of jurisdiction-specific legal questions.

## 15. Contributing

Contributions should be focused, tested, and easy for teammates to review.

When reporting a bug, include:

- What you expected to happen.
- What actually happened.
- Steps to reproduce the issue using synthetic data.
- Relevant error output with personal information and secrets removed.

Update this README whenever setup commands, architecture, model requirements, or the public interface change.

## 16. License

The project license has not yet been specified. Add the license selected by the project owners and include the corresponding `LICENSE` file.

Check third-party dependency and model licenses separately. The repository license does not override their terms.

## 17. Acknowledgements

Developed by a four-person team for the ZeroDay OSS / Hacktoberfest 2026 hackathon context.

Update this section with the final team member names, repository link, and event acknowledgements before submission.

---

**Korpse — Legal Triage Assistant**  
*An experimental hackathon prototype for AI-assisted legal triage.*
