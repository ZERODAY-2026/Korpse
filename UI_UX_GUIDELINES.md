# UI / UX Guidelines

The app is built with **Python + Streamlit only**. Every guideline below uses Streamlit's built-in components. Follow `CLAUDE.md` at all times, especially the privacy and legal-safety rules.

**Owner:** Siddhesh,Anshuman (`app.py`, `ui/`)

## 1. Design goals

- **Clean and calm:** plenty of space, no clutter, no flashy effects.
- **Professional and trustworthy:** consistent layout, clear labels, honest wording.
- **Understandable:** a non-lawyer must understand every screen without help.
- **Honest about uncertainty:** clearly say when the document is unclear, silent, or depends on local law.
- **Privacy always visible:** the user can see at all times that their document stays on their device.

## 2. Page layout (Streamlit structure)

### Page setup

```python
st.set_page_config(page_title="Legal Document Triage", page_icon="⚖️", layout="wide")
```

- Use an emoji for the icon. It needs no internet download.

### Sidebar (`st.sidebar`)

Shown on every screen, top to bottom:

1. App name
2. "Not legal advice" notice (`st.warning`)
3. Privacy status: "🔒 Processed locally – nothing leaves this device"
4. "Delete document" button
5. Short how-to steps (1. Upload → 2. Read summary → 3. Check clauses → 4. Ask questions)

### Main area (`st.tabs`)

| Tab | Purpose |
|---|---|
| Upload | Choose and process a document |
| Summary | Plain-language overview and top risks |
| Clauses & Risks | One card per finding, with filters |
| Ask a Question | Chat about the document |
| About & Privacy | How the app works, its limits and privacy |

- Every tab except **Upload** shows a friendly message until a document is uploaded, for example: `st.info("Upload a document in the Upload tab to see results here.")`

## 3. Screen-by-screen guidelines

### Upload

- `st.file_uploader("Upload a legal document", type=["pdf", "txt"])`, which accepts PDF and TXT only.
- After upload, show the **file name**, **file size** and **page count**.
- While processing: `st.spinner("Reading your document locally...")`.
- When done, show `st.success` and point the user to the Summary tab.

### Summary

- A short plain-language overview at the top (a few sentences).
- A **"Top risks"** list, sorted **High → Medium → Low**.
- **Key facts** (parties, dates, amounts): use `st.metric` or a simple table (`st.table` / `st.dataframe`), **only if the backend provides them**. Never fill them in yourself.

### Clauses & Risks

- Put filters at the top using `st.multiselect`: **Category** and **Risk level**.
- Show one bordered card per finding with `st.container(border=True)`. Each card shows:

| Part | How to show it |
|---|---|
| Category | Bold heading, e.g. **Termination** |
| Risk level | Icon + coloured text label (see section 4) |
| Plain explanation | 1–3 short sentences |
| Label | "📄 Stated in document" or "💭 Possible interpretation" |
| Confidence | Shown as text, e.g. "Confidence: Low" (format TBD by backend) |
| Warnings | Any that apply: ambiguous wording / depends on local law / consult a lawyer |
| Source | `st.expander("See source passage")` containing the **exact quote** and **page number** |

### Ask a Question

- Use `st.chat_input` for the question and `st.chat_message` for each message.
- **Every answer shows citations** (quote + page number).
- If the document doesn't cover the question, show `st.info("The document does not mention this.")`.
- For "Is this legal / enforceable / valid?" questions, show `st.warning` with the refusal and a lawyer recommendation. Example: "I can't say whether this is legal or enforceable. Here is what the document states… For a legal opinion, please consult a qualified lawyer."
- Keep the chat history in `st.session_state`.

### About & Privacy

- How the app works: everything runs locally on this device.
- Model used: **TBD** (until Shiven confirms it in `INTEGRATION_CONTRACT.md`).
- Limitations: it can miss things, may misread scanned PDFs, and doesn't know local law.
- A clear statement that this is **not legal advice**.

## 4. Visual language

### Risk levels: colour + text + icon, never colour alone

| Level | Colour | Icon | Label | Streamlit text |
|---|---|---|---|---|
| High | Red | ⛔ | High risk | `⛔ :red[**High risk**]` |
| Medium | Orange | ⚠️ | Medium risk | `⚠️ :orange[**Medium risk**]` |
| Low | Green | ℹ️ | Low risk | `ℹ️ :green[**Low risk**]` |

### Finding labels must look clearly different

| Label | Icon | Style |
|---|---|---|
| Stated in document | 📄 | Bold text: `📄 **Stated in document**` |
| Possible interpretation | 💭 | Italic text: `💭 *Possible interpretation*` |

### Messages

| Use | Component |
|---|---|
| Something failed | `st.error` |
| Caution, refusal, legal warning | `st.warning` |
| Neutral info, "document is silent" | `st.info` |
| Action completed | `st.success` |

### Theme and styling

- Set a simple theme in `.streamlit/config.toml`, using the `[theme]` section only.
  - **Ayush owns this file.** Coordinate with Ayush before editing it, and never touch its privacy settings.
- Keep custom CSS to a minimum, inside `ui/styles.py` only.
- **Never** load external fonts, CDN files or images from the internet (this is a privacy rule in `CLAUDE.md`).

## 5. Writing style (UX copy)

- Use short sentences and everyday words.
- Explain a legal term in brackets the first time it appears, e.g. "indemnity (a promise to cover someone else's losses)".
- **Never say** "you must", "this is illegal", "this is enforceable" or "this is valid".
- **Say instead** "The document states…" or "This may mean…".
- End every risk explanation with something the user could ask or check next, e.g. "You may want to ask the landlord how the deposit deduction is calculated."
- Error messages say **what went wrong** and **what to do next**. Never show raw Python errors or tracebacks.
  - Example: "This PDF could not be read. It may be damaged or password-protected. Try another file or a .txt version."

## 6. Accessibility

- Keep good colour contrast in **both light and dark mode**. Test both, using Streamlit's settings menu → Theme.
- Never show meaning by colour alone. Always add a text label and an icon.
- Use clear headings in logical order (`st.header` → `st.subheader`).
- Give every button and input a clear text label, and never rely on placeholder text alone.
- Keep the text size readable and avoid walls of text: use bullet points, and `st.expander` for details.

## 7. States every screen must handle

| State | What the user sees |
|---|---|
| Empty | `st.info` explaining what to do first (e.g. "Upload a document to begin.") |
| Loading | `st.spinner` with a clear message |
| Success | The results, with citations |
| Error | `st.error` with a friendly message + next step |
| Model not available | `st.error` with a clear setup instruction (exact steps TBD, from Shiven's setup docs) |
| Document is silent | `st.info("The document does not mention this.")` |
| Low confidence | `st.warning` saying the result may be unreliable and the user should check the source passage |

## 8. Streamlit technical rules

- Store the uploaded document, results and chat history in **`st.session_state`** so they aren't lost when the page reruns.
- Load the model **once** using **`st.cache_resource`**. The calling method is **TBD** (Shiven). Don't invent it.
- **Never** write document text to logs, `print()` statements, or files outside the app's temporary area.
- The **"Delete document"** button clears `st.session_state` and removes any temporary files.
- Keep UI code in `ui/`, split into small files, and keep `app.py` short:

| File | Contents |
|---|---|
| `app.py` | Page config, sidebar call, tabs; nothing else |
| `ui/sidebar.py` | Sidebar content |
| `ui/upload.py` | Upload tab |
| `ui/summary.py` | Summary tab |
| `ui/clauses.py` | Clauses & Risks tab |
| `ui/chat.py` | Ask a Question tab |
| `ui/styles.py` | Risk badges, labels, minimal CSS |

- During UI development, use sample data from `core/stub_backend.py` only, labelled "SAMPLE DATA – NOT REAL".

## 9. Demo checklist for the UI

- [ ] Upload works on a document we did **not** prepare in advance
- [ ] Citations (quote + page) are visible beside every finding
- [ ] A "document is silent" case is shown
- [ ] A refusal + lawyer recommendation is shown
- [ ] The app works with **Wi-Fi turned off**
- [ ] No sample/stub data remains in the demo build
