import streamlit as st
import os
import tempfile

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MeetingMind · AI Task Extractor",
    page_icon="🎙️",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Syne', sans-serif;
    }

    /* ── Background ── */
    .stApp {
        background: #0d0f14;
        color: #e8e4dc;
    }

    /* ── Hero header ── */
    .hero {
        text-align: center;
        padding: 3rem 0 2rem;
    }
    .hero h1 {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        background: linear-gradient(135deg, #f5c842 0%, #f58c42 60%, #f54242 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.4rem;
    }
    .hero p {
        color: #7a7870;
        font-family: 'DM Mono', monospace;
        font-size: 0.85rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    /* ── Divider ── */
    .divider {
        border: none;
        border-top: 1px solid #1e2028;
        margin: 1.5rem 0;
    }

    /* ── Upload zone ── */
    [data-testid="stFileUploader"] {
        border: 2px dashed #2a2d36 !important;
        border-radius: 12px !important;
        background: #12141a !important;
        padding: 1rem !important;
        transition: border-color 0.2s;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #f5c842 !important;
    }

    /* ── Process button ── */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #f5c842, #f58c42);
        color: #0d0f14;
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 1rem;
        letter-spacing: 0.04em;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 0;
        cursor: pointer;
        transition: opacity 0.2s, transform 0.1s;
    }
    div.stButton > button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }
    div.stButton > button:active {
        transform: translateY(0);
    }

    /* ── Section headers ── */
    .section-label {
        font-family: 'DM Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #f5c842;
        margin-bottom: 0.6rem;
    }

    /* ── Transcript box ── */
    .transcript-box {
        background: #12141a;
        border: 1px solid #1e2028;
        border-radius: 10px;
        padding: 1.2rem 1.4rem;
        font-family: 'DM Mono', monospace;
        font-size: 0.85rem;
        line-height: 1.75;
        color: #b0ab9e;
        white-space: pre-wrap;
    }

    /* ── Task card ── */
    .task-card {
        background: #12141a;
        border: 1px solid #1e2028;
        border-left: 3px solid #f5c842;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        transition: border-left-color 0.2s;
    }
    .task-card:hover {
        border-left-color: #f58c42;
    }
    .task-title {
        font-weight: 600;
        font-size: 0.98rem;
        color: #e8e4dc;
        margin-bottom: 0.5rem;
    }
    .task-meta {
        display: flex;
        gap: 1.2rem;
        flex-wrap: wrap;
    }
    .task-chip {
        font-family: 'DM Mono', monospace;
        font-size: 0.75rem;
        padding: 0.2rem 0.65rem;
        border-radius: 20px;
        background: #1e2028;
        color: #7a7870;
    }
    .task-chip span {
        color: #e8e4dc;
        margin-left: 0.3rem;
    }

    /* ── Summary box ── */
    .summary-box {
        background: #12141a;
        border: 1px solid #1e2028;
        border-radius: 10px;
        padding: 1.2rem 1.4rem;
        font-size: 0.92rem;
        line-height: 1.7;
        color: #b0ab9e;
    }

    /* ── Decision item ── */
    .decision-item {
        display: flex;
        gap: 0.75rem;
        align-items: flex-start;
        padding: 0.55rem 0;
        border-bottom: 1px solid #1a1c22;
        color: #b0ab9e;
        font-size: 0.9rem;
        line-height: 1.55;
    }
    .decision-item:last-child { border-bottom: none; }
    .decision-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #f5c842;
        margin-top: 0.5rem;
        flex-shrink: 0;
    }

    /* ── Alerts ── */
    .stAlert { border-radius: 10px !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Lazy imports with helpful error messages ───────────────────────────────────
def load_stt():
    try:
        from stt import transcribe_audio
        return transcribe_audio
    except ImportError:
        st.error("❌ Could not import `transcribe_audio` from `stt.py`. Make sure the file exists in the same directory.")
        return None

def load_llm():
    try:
        from llm import extract_tasks
        return extract_tasks
    except ImportError:
        st.error("❌ Could not import `extract_tasks` from `llm.py`. Make sure the file exists in the same directory.")
        return None

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <h1>🎙️ MeetingMind</h1>
        <p>Upload a recording · Extract tasks · Ship faster</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ── Upload ─────────────────────────────────────────────────────────────────────
st.markdown("<div class='section-label'>01 — Upload Recording</div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    label="Drop your meeting audio here",
    type=["mp3", "wav"],
    label_visibility="collapsed",
)

if uploaded_file:
    st.audio(uploaded_file, format=f"audio/{uploaded_file.name.split('.')[-1]}")

st.markdown("<br>", unsafe_allow_html=True)

# ── Process button ─────────────────────────────────────────────────────────────
process_clicked = st.button("⚡  Process Meeting  ")

# ── Processing logic ───────────────────────────────────────────────────────────
if process_clicked:
    if not uploaded_file:
        st.warning("⚠️  Please upload an audio file before processing.")
        st.stop()

    # Save uploaded file to a temp path
    suffix = os.path.splitext(uploaded_file.name)[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # ── Step 1: Transcribe ──────────────────────────────────────────────────
    transcribe_audio = load_stt()
    if transcribe_audio is None:
        st.stop()

    with st.spinner("Transcribing audio…"):
        try:
            transcript = transcribe_audio(tmp_path)
            if not transcript or not isinstance(transcript, str):
                raise ValueError("Transcription returned empty or invalid result.")
        except Exception as e:
            st.error(f"❌ Transcription failed: {e}")
            st.stop()

    # ── Step 2: Extract tasks ───────────────────────────────────────────────
    extract_tasks = load_llm()
    if extract_tasks is None:
        st.stop()

    with st.spinner("Extracting tasks with AI…"):
        try:
            result = extract_tasks(transcript)
            if not isinstance(result, dict):
                raise ValueError("Task extraction did not return a dictionary.")
        except Exception as e:
            st.error(f"❌ Task extraction failed: {e}")
            st.stop()

    # ── Cleanup temp file ───────────────────────────────────────────────────
    try:
        os.unlink(tmp_path)
    except OSError:
        pass

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ── Transcript ──────────────────────────────────────────────────────────
    st.markdown("<div class='section-label'>02 — Transcript</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='transcript-box'>{transcript}</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tasks ───────────────────────────────────────────────────────────────
    tasks = result.get("tasks", [])
    st.markdown("<div class='section-label'>03 — Extracted Tasks</div>", unsafe_allow_html=True)

    if not tasks:
        st.info("No tasks were extracted from this meeting.")
    else:
        for i, task in enumerate(tasks, 1):
            task_name    = task.get("task", task.get("title", f"Task {i}"))
            assignee     = task.get("assigned_to", task.get("assignee", "")) or "Unassigned"
            deadline     = task.get("deadline", task.get("due_date", "")) or "No deadline"

            st.markdown(
                f"""
                <div class="task-card">
                    <div class="task-title">{i}. {task_name}</div>
                    <div class="task-meta">
                        <div class="task-chip">👤<span>{assignee}</span></div>
                        <div class="task-chip">📅<span>{deadline}</span></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Summary ─────────────────────────────────────────────────────────────
    summary = result.get("summary", "")
    st.markdown("<div class='section-label'>04 — Summary</div>", unsafe_allow_html=True)
    if summary:
        st.markdown(f"<div class='summary-box'>{summary}</div>", unsafe_allow_html=True)
    else:
        st.info("No summary available.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Decisions ───────────────────────────────────────────────────────────
    decisions = result.get("decisions", [])
    st.markdown("<div class='section-label'>05 — Decisions</div>", unsafe_allow_html=True)
    if not decisions:
        st.info("No decisions were recorded.")
    else:
        items_html = "".join(
            f"<div class='decision-item'><div class='decision-dot'></div><div>{d}</div></div>"
            for d in decisions
        )
        st.markdown(
            f"<div style='background:#12141a;border:1px solid #1e2028;border-radius:10px;padding:0.6rem 1.2rem;'>{items_html}</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.success("✅ Meeting processed successfully!")
