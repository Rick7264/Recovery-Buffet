"""
🌸 Srija's Recovery Buffet
A gentle, pastel-pink recovery checklist built with Streamlit.
Single-file app, ready for Streamlit Community Cloud.
"""

import random
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="🌸 Srija's Recovery Buffet",
    page_icon="🌸",
    layout="centered",
)

# ----------------------------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------------------------
DEFAULT_ITEMS = [
    {"text": "Get some sunlight", "emoji": "☀️", "tags": ["Vitamin D"]},
    {"text": "Drink a glass of water", "emoji": "💧", "tags": ["Hydration", "Essential"]},
    {"text": "Eat something nourishing", "emoji": "🍲", "tags": ["Nutrition"]},
    {"text": "Take medicines", "emoji": "💊", "tags": ["Health"]},
    {"text": "Small walk", "emoji": "🚶", "tags": ["Movement"]},
    {"text": "Take a proper nap", "emoji": "🛌", "tags": ["Rest"]},
    {"text": "Listen to your favourite songs", "emoji": "🎵", "tags": ["Mood Booster"]},
    {"text": "Read a few pages", "emoji": "📖", "tags": ["Mind"]},
    {"text": "Rest guilt-free", "emoji": "🧸", "tags": ["Rest"]},
    {"text": "Be kind to yourself", "emoji": "💖", "tags": ["Mental Health"]},
    {"text": "Talk to someone you love", "emoji": "🫂", "tags": ["Connection"]},
    {"text": "Eat a fruit", "emoji": "🍓", "tags": ["Nutrition"]},
    {"text": "Stretch for five minutes", "emoji": "🧘", "tags": ["Movement"]},
    {"text": "Warm shower", "emoji": "🛁", "tags": ["Self Care"]},
    {"text": "Open the window", "emoji": "🌼", "tags": ["Fresh Air"]},
]

QUOTES = [
    "One step at a time.",
    "Healing happens quietly.",
    "Rest is productive.",
    "You deserve kindness.",
    "Tiny progress is still progress.",
    "Slow days are still good days.",
    "You don't have to earn rest.",
    "Softness is not weakness.",
    "Your pace is the right pace.",
    "Small comforts matter too.",
    "It's okay to just be okay today.",
    "You're allowed to take up space while healing.",
    "Gentle days build strong foundations.",
    "Show up for yourself, even quietly.",
    "You're doing better than you think.",
]

# Tag -> pastel color mapping, cycled for any custom tags too
TAG_COLORS = {
    "Hydration": "#B3E5FC",
    "Essential": "#F8BBD0",
    "Nutrition": "#C8E6C9",
    "Health": "#FFE0B2",
    "Movement": "#D1C4E9",
    "Rest": "#FCE4EC",
    "Mind": "#B2DFDB",
    "Mood Booster": "#FFF9C4",
    "Vitamin D": "#FFECB3",
    "Mental Health": "#F48FB1",
    "Connection": "#E1BEE7",
    "Self Care": "#F8BBD0",
    "Fresh Air": "#C5E1A5",
    "New": "#F0F4C3",
}
FALLBACK_COLORS = ["#F8BBD0", "#FCE4EC", "#E1BEE7", "#B3E5FC", "#C8E6C9", "#FFE0B2"]


def color_for_tag(tag: str) -> str:
    if tag not in TAG_COLORS:
        # deterministic-ish fallback so the same tag always gets the same color
        TAG_COLORS[tag] = FALLBACK_COLORS[len(TAG_COLORS) % len(FALLBACK_COLORS)]
    return TAG_COLORS[tag]


# ----------------------------------------------------------------------------
# PERSISTENCE (save/load tasks from Firebase Firestore so they survive reboots)
# ----------------------------------------------------------------------------
FIRESTORE_COLLECTION = "recovery_buffet"
FIRESTORE_DOCUMENT = "srija_tasks"  # single doc holding the whole list


@st.cache_resource
def get_firestore_client():
    """Initialize the Firebase app once per server process and return a Firestore client."""
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["firebase"]))
        firebase_admin.initialize_app(cred)
    return firestore.client()


def load_tasks_from_firestore():
    """Load saved tasks from Firestore. Falls back to defaults if nothing is saved yet."""
    try:
        db = get_firestore_client()
        doc = db.collection(FIRESTORE_COLLECTION).document(FIRESTORE_DOCUMENT).get()
        if doc.exists:
            data = doc.to_dict()
            tasks = data.get("tasks")
            if tasks:
                return tasks
    except Exception as e:
        st.warning(f"Couldn't reach Firebase, starting with defaults. ({e})")
    return [{**item, "done": False} for item in DEFAULT_ITEMS]


def save_tasks_to_firestore():
    """Write the current task list to Firestore."""
    try:
        db = get_firestore_client()
        db.collection(FIRESTORE_COLLECTION).document(FIRESTORE_DOCUMENT).set(
            {"tasks": st.session_state.tasks}
        )
    except Exception as e:
        st.warning(f"Couldn't save your changes to Firebase. ({e})")


# ----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# ----------------------------------------------------------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks_from_firestore()

if "quote_of_the_day" not in st.session_state:
    st.session_state.quote_of_the_day = random.choice(QUOTES)

if "new_item_text" not in st.session_state:
    st.session_state.new_item_text = ""


# ----------------------------------------------------------------------------
# CUSTOM CSS
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&family=Poppins:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background: linear-gradient(180deg, #FFF5F7 0%, #FFEEF2 100%);
    }

    /* Hide default streamlit chrome a bit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .block-container {
        max-width: 720px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Title */
    .buffet-title {
        text-align: center;
        font-size: 2.6rem;
        font-weight: 700;
        color: #EC407A;
        margin-bottom: 0.2rem;
        letter-spacing: 0.5px;
    }
    .buffet-subtitle {
        text-align: center;
        font-size: 1.05rem;
        color: #000000;
        margin-bottom: 1.8rem;
        font-weight: 500;
    }

    /* Section headers */
    .section-header {
        font-size: 1.2rem;
        font-weight: 700;
        color: #EC407A;
        margin-top: 1.2rem;
        margin-bottom: 0.6rem;
    }

    /* Progress text */
    .progress-text {
        text-align: center;
        color: #000000;
        font-weight: 600;
        margin-top: 0.4rem;
        margin-bottom: 0.2rem;
    }

    /* Card styling — targets the real container divs created by
       st.container(key="task_card_active_N" / "task_card_done_N"),
       so the box genuinely encloses the checkbox/text/delete row. */
    div[class*="st-key-task_card_active_"],
    div[class*="st-key-task_card_done_"] {
        background: #FFF9FB;
        border-radius: 18px;
        padding: 14px 18px;
        margin-bottom: 12px;
        box-shadow: 0 4px 14px rgba(236, 64, 122, 0.08);
        transition: all 0.25s ease-in-out;
        border: 1.5px solid #FBDCE7;
    }
    div[class*="st-key-task_card_active_"]:hover,
    div[class*="st-key-task_card_done_"]:hover {
        box-shadow: 0 8px 22px rgba(236, 64, 122, 0.18);
        transform: translateY(-2px);
    }

    div[class*="st-key-task_card_done_"] {
        background: #FFF5F7;
        opacity: 0.7;
    }

    .task-name {
        font-size: 1.05rem;
        font-weight: 600;
        color: #000000;
        margin-bottom: 4px;
    }

    .task-name-done {
        text-decoration: line-through;
        color: #999999;
    }

    /* Tag pills */
    .tag-pill {
        display: inline-block;
        padding: 3px 12px;
        margin-right: 6px;
        margin-top: 4px;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 600;
        color: #000000;
    }

    /* Buttons */
    div.stButton > button {
        border-radius: 999px;
        border: none;
        background: linear-gradient(135deg, #F8BBD0, #EC407A);
        color: white;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 2px 8px rgba(236, 64, 122, 0.25);
    }
    div.stButton > button:hover {
        transform: scale(1.04);
        box-shadow: 0 4px 14px rgba(236, 64, 122, 0.35);
    }

    /* Delete buttons - make them lighter */
    .delete-btn button {
        background: #FCE4EC !important;
        color: #EC407A !important;
    }

    /* Text input */
    div.stTextInput > div > div > input {
        border-radius: 14px;
        border: 1.5px solid #F8BBD0;
        padding: 10px 14px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #FFF0F5;
    }

    section[data-testid="stSidebar"] * {
        color: #000000;
    }

    section[data-testid="stSidebar"] .sidebar-quote {
        color: #EC407A;
    }

    .sidebar-quote {
        font-style: italic;
        color: #EC407A;
        font-weight: 600;
        padding: 10px;
        border-left: 4px solid #F8BBD0;
        background: #FFFFFF;
        border-radius: 10px;
        margin-top: 8px;
    }

    .footer-text {
        text-align: center;
        color: #EC407A;
        font-weight: 600;
        margin-top: 2.5rem;
        font-size: 0.95rem;
    }

    /* ------------------------------------------------------------------ */
    /* MOBILE RESPONSIVENESS                                              */
    /* ------------------------------------------------------------------ */

    /* Force the checkbox / text / delete-button row inside each task card
       to stay horizontal instead of stacking on narrow screens. Streamlit
       wraps each st.columns() row in [data-testid="stHorizontalBlock"]. */
    div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        align-items: center !important;
        gap: 0.4rem;
    }

    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        width: auto !important;
        min-width: 0 !important;
        flex: initial !important;
    }

    /* Give the checkbox column just enough room */
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(1) {
        flex: 0 0 auto !important;
    }

    /* Let the text column take up the remaining space and truncate gracefully */
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(2) {
        flex: 1 1 auto !important;
        min-width: 0 !important;
        overflow-wrap: break-word;
    }

    /* Keep the delete button compact */
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(3) {
        flex: 0 0 auto !important;
    }

    .delete-btn button {
        padding: 0.25rem 0.6rem !important;
        min-width: 2.2rem !important;
    }

    /* Small-screen specific tweaks */
    @media (max-width: 480px) {
        .block-container {
            padding-top: 3.2rem;
        }
        .buffet-title {
            font-size: 1.9rem;
        }
        .buffet-subtitle {
            font-size: 0.9rem;
        }
        .block-container {
            padding-left: 0.8rem;
            padding-right: 0.8rem;
        }
        div[class*="st-key-task_card_active_"],
        div[class*="st-key-task_card_done_"] {
            padding: 10px 12px;
        }
        .task-name {
            font-size: 0.95rem;
        }
        .tag-pill {
            font-size: 0.65rem;
            padding: 2px 9px;
        }
        div.stButton > button {
            font-size: 0.85rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🌸 About")
    st.write("This Recovery Buffet is a gentle reminder that healing isn't a race.")

    st.markdown("### 💭 Quote of the Day")
    st.markdown(
        f'<div class="sidebar-quote">"{st.session_state.quote_of_the_day}"</div>',
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
st.markdown('<div class="buffet-title">🌸 Srija\'s Recovery Buffet</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="buffet-subtitle">Little victories count. Take your time, heal at your pace. 💖</div>',
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------------------
# PROGRESS
# ----------------------------------------------------------------------------
total_items = len(st.session_state.tasks)
done_items = sum(1 for item in st.session_state.tasks if item["done"])
progress_fraction = (done_items / total_items) if total_items else 0.0

st.markdown('<div class="section-header">📊 Recovery Progress</div>', unsafe_allow_html=True)
st.progress(progress_fraction)
st.markdown(
    f'<div class="progress-text">You\'ve completed {done_items} of {total_items} '
    f'recovery treats 🌸 &nbsp;({int(progress_fraction * 100)}%)</div>',
    unsafe_allow_html=True,
)

if total_items > 0 and done_items == total_items:
    st.balloons()
    st.success("🎉 Amazing job!\n\nYou're taking care of yourself today and that's worth celebrating. 🌸💖")

st.write("")  # small spacer


# ----------------------------------------------------------------------------
# ADD NEW ITEM
# ----------------------------------------------------------------------------
st.markdown('<div class="section-header">➕ Add a Treat</div>', unsafe_allow_html=True)

add_col1, add_col2 = st.columns([5, 1])
with add_col1:
    new_item = st.text_input(
        "New recovery item",
        key="new_item_input",
        placeholder="e.g. Watch a comfort movie 🎬",
        label_visibility="collapsed",
    )
with add_col2:
    add_clicked = st.button("➕ Add", use_container_width=True)

if add_clicked:
    cleaned = new_item.strip()
    if not cleaned:
        st.warning("Type something sweet before adding it. 🌸")
    else:
        existing_texts = {item["text"].lower() for item in st.session_state.tasks}
        if cleaned.lower() in existing_texts:
            st.warning("That's already on your buffet! 💕")
        else:
            st.session_state.tasks.append(
                {"text": cleaned, "emoji": "✨", "tags": ["New"], "done": False}
            )
            save_tasks_to_firestore()
            st.rerun()

st.write("")  # spacer


# ----------------------------------------------------------------------------
# CHECKLIST
# ----------------------------------------------------------------------------
st.markdown('<div class="section-header">🌷 Your Buffet</div>', unsafe_allow_html=True)

if not st.session_state.tasks:
    st.info("Your buffet is empty right now. Add a gentle little task above. 🌸")

for idx, item in enumerate(st.session_state.tasks):
    name_class = "task-name task-name-done" if item["done"] else "task-name"
    container_key = f"task_card_done_{idx}" if item["done"] else f"task_card_active_{idx}"

    tags_html = "".join(
        f'<span class="tag-pill" style="background:{color_for_tag(tag)};">{tag}</span>'
        for tag in item["tags"]
    )

    with st.container(key=container_key):
        col_check, col_text, col_delete = st.columns([0.7, 5, 1])

        with col_check:
            checked = st.checkbox(
                "done",
                value=item["done"],
                key=f"check_{idx}",
                label_visibility="collapsed",
            )
            if checked != item["done"]:
                st.session_state.tasks[idx]["done"] = checked
                save_tasks_to_firestore()
                st.rerun()

        with col_text:
            st.markdown(
                f'<div class="{name_class}">{item["emoji"]} {item["text"]}</div>{tags_html}',
                unsafe_allow_html=True,
            )

        with col_delete:
            st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
            if st.button("🗑️", key=f"delete_{idx}", use_container_width=True):
                st.session_state.tasks.pop(idx)
                save_tasks_to_firestore()
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# FOOTER
# ----------------------------------------------------------------------------
st.markdown('<div class="footer-text">Made with 😎 for Srija</div>', unsafe_allow_html=True)
