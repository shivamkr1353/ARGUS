"""
ARGUS — AI-Powered Responsive Glasses for Uplifting the Blind in Society
Main Streamlit Application

Run with:  streamlit run main.py
"""

import streamlit as st
import time
from datetime import datetime

from config import APP_TITLE, APP_SUBTITLE, APP_ICON, KIMI_API_KEY
from memory import MemoryManager
from speech import SpeechManager
from vision import VisionModule
from assistant import AssistantEngine


# ═══════════════════════════════════════════════════════
# Page Configuration
# ═══════════════════════════════════════════════════════
st.set_page_config(
    page_title=f"{APP_TITLE} — Assistive AI Prototype",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)


# ═══════════════════════════════════════════════════════
# Custom CSS — Premium Dark Theme
# ═══════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Global ─────────────────────────────── */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* ── Header Banner ──────────────────────── */
    .argus-header {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        border: 1px solid rgba(100, 120, 255, 0.2);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .argus-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(
            circle at 30% 40%,
            rgba(99, 102, 241, 0.15) 0%,
            transparent 50%
        );
        animation: pulse-glow 4s ease-in-out infinite;
    }
    @keyframes pulse-glow {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    .argus-header h1 {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(90deg, #818cf8, #c084fc, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        position: relative;
        letter-spacing: 3px;
    }
    .argus-header p {
        color: #a5b4fc;
        font-size: 0.95rem;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
        position: relative;
        letter-spacing: 0.5px;
    }

    /* ── Status Badge ───────────────────────── */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 14px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.75rem;
        position: relative;
    }
    .status-online {
        background: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }
    .status-offline {
        background: rgba(239, 68, 68, 0.15);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        display: inline-block;
    }
    .status-dot.online { background: #4ade80; }
    .status-dot.offline { background: #f87171; }

    /* ── Section Cards ──────────────────────── */
    .section-card {
        background: linear-gradient(145deg, #1e1b4b 0%, #1a1a2e 100%);
        border: 1px solid rgba(99, 102, 241, 0.15);
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .section-card h3 {
        color: #c4b5fd;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0 0 1rem 0;
    }

    /* ── Chat Bubbles ───────────────────────── */
    .chat-user {
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 14px 14px 4px 14px;
        padding: 0.9rem 1.2rem;
        margin: 0.5rem 0;
        color: #e0e7ff;
        font-size: 0.92rem;
    }
    .chat-assistant {
        background: rgba(139, 92, 246, 0.1);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 14px 14px 14px 4px;
        padding: 0.9rem 1.2rem;
        margin: 0.5rem 0;
        color: #ddd6fe;
        font-size: 0.92rem;
    }
    .chat-label {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 4px;
    }
    .chat-label.user { color: #818cf8; }
    .chat-label.assistant { color: #a78bfa; }

    /* ── Intent Badge ───────────────────────── */
    .intent-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 999px;
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-left: 8px;
    }
    .intent-scene { background: rgba(6, 182, 212, 0.2); color: #22d3ee; border: 1px solid rgba(6, 182, 212, 0.3); }
    .intent-note { background: rgba(250, 204, 21, 0.15); color: #fde047; border: 1px solid rgba(250, 204, 21, 0.3); }
    .intent-time, .intent-date { background: rgba(52, 211, 153, 0.15); color: #6ee7b7; border: 1px solid rgba(52, 211, 153, 0.3); }
    .intent-general { background: rgba(99, 102, 241, 0.15); color: #a5b4fc; border: 1px solid rgba(99, 102, 241, 0.3); }

    /* ── Note Cards ─────────────────────────── */
    .note-card {
        background: rgba(250, 204, 21, 0.06);
        border: 1px solid rgba(250, 204, 21, 0.15);
        border-radius: 10px;
        padding: 0.75rem 1rem;
        margin: 0.4rem 0;
    }
    .note-text { color: #fef9c3; font-size: 0.88rem; }
    .note-time { color: #a3a3a3; font-size: 0.7rem; margin-top: 4px; }

    /* ── Sidebar Styling ────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #1a1a2e 100%);
        border-right: 1px solid rgba(99, 102, 241, 0.15);
    }
    section[data-testid="stSidebar"] .stMarkdown h2 {
        color: #c4b5fd;
        font-size: 1.1rem;
    }

    /* ── Button Styling ─────────────────────── */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.5px;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }

    /* ── Divider ────────────────────────────── */
    .subtle-divider {
        border: none;
        border-top: 1px solid rgba(99, 102, 241, 0.1);
        margin: 1rem 0;
    }

    /* ── Footer ─────────────────────────────── */
    .argus-footer {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
        color: #6b7280;
        font-size: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# Session State Initialization
# ═══════════════════════════════════════════════════════
def init_session_state():
    """Initialize all session state variables on first run."""
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.memory = MemoryManager()
        st.session_state.speech = SpeechManager()
        st.session_state.messages = []  # UI chat messages
        st.session_state.last_scene_image = None
        st.session_state.last_scene_description = None

        # Check hardware availability
        st.session_state.mic_available = st.session_state.speech.check_microphone()
        st.session_state.cam_available = VisionModule.check_webcam()

        # Initialize vision and assistant (requires Kimi API key)
        if KIMI_API_KEY:
            try:
                st.session_state.vision = None
                try:
                    st.session_state.vision = VisionModule()
                except Exception as e:
                    print(f"Vision init failed: {e}")

                st.session_state.assistant = AssistantEngine(
                    memory=st.session_state.memory,
                    vision=st.session_state.vision,
                )
                st.session_state.api_ready = True
            except Exception as e:
                st.session_state.api_ready = False
                st.session_state.api_error = str(e)
        else:
            st.session_state.api_ready = False
            st.session_state.api_error = "No API key found. Set KIMI_API_KEY in .env file."

init_session_state()


# ═══════════════════════════════════════════════════════
# Helper Functions
# ═══════════════════════════════════════════════════════
def add_ui_message(role: str, content: str, intent: str = "general", image=None):
    """Add a message to the UI chat display."""
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "intent": intent,
        "image": image,
        "timestamp": datetime.now().strftime("%I:%M %p"),
    })

def process_query(query: str):
    """Process a user query through the assistant pipeline."""
    if not st.session_state.api_ready:
        add_ui_message("user", query)
        add_ui_message(
            "assistant",
            f"⚠️ System not ready: {st.session_state.get('api_error', 'Unknown error')}",
        )
        return

    add_ui_message("user", query)

    with st.spinner("🧠 ARGUS is thinking..."):
        response, intent, extra = st.session_state.assistant.process(query)

    image = None
    if intent == "scene" and extra is not None:
        image = extra
        st.session_state.last_scene_image = extra
        st.session_state.last_scene_description = response

    add_ui_message("assistant", response, intent=intent, image=image)

    # Generate TTS audio
    audio_bytes = st.session_state.speech.synthesize(response)
    if audio_bytes:
        st.session_state.last_audio = audio_bytes


def render_chat():
    """Render the chat message history."""
    for msg in st.session_state.messages:
        intent = msg.get("intent", "general")
        badge = f'<span class="intent-badge intent-{intent}">{intent}</span>'

        if msg["role"] == "user":
            st.markdown(
                f'<div class="chat-user">'
                f'<div class="chat-label user">You {badge} · {msg["timestamp"]}</div>'
                f'{msg["content"]}'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="chat-assistant">'
                f'<div class="chat-label assistant">ARGUS {badge} · {msg["timestamp"]}</div>'
                f'{msg["content"]}'
                f'</div>',
                unsafe_allow_html=True,
            )
            if msg.get("image") is not None:
                st.image(msg["image"], caption="📸 Captured Scene", use_container_width=True)


# ═══════════════════════════════════════════════════════
# Header
# ═══════════════════════════════════════════════════════
st.markdown(f"""
<div class="argus-header">
    <h1>{APP_ICON} {APP_TITLE}</h1>
    <p>{APP_SUBTITLE}</p>
    <div class="status-badge {'status-online' if st.session_state.api_ready else 'status-offline'}">
        <span class="status-dot {'online' if st.session_state.api_ready else 'offline'}"></span>
        {'System Online' if st.session_state.api_ready else 'System Offline'}
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# Sidebar — System Status & Notes
# ═══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"## {APP_ICON} ARGUS Control Panel")
    st.markdown("<hr class='subtle-divider'>", unsafe_allow_html=True)

    # ── System Status ────────────────────────
    st.markdown("### 📡 System Status")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.session_state.mic_available:
            st.success("🎙️ Mic Ready", icon="✅")
        else:
            st.error("🎙️ No Mic", icon="❌")
    with col_s2:
        if st.session_state.cam_available:
            st.success("📷 Cam Ready", icon="✅")
        else:
            st.error("📷 No Cam", icon="❌")

    if st.session_state.api_ready:
        st.success("🤖 Llama 3.2 Vision API Connected", icon="✅")
    else:
        st.error("🤖 API Error", icon="❌")
        st.caption(st.session_state.get("api_error", ""))

    st.markdown("<hr class='subtle-divider'>", unsafe_allow_html=True)

    # ── Notes Section ────────────────────────
    st.markdown("### 📝 Saved Notes")
    notes = st.session_state.memory.get_notes()
    if notes:
        for note in reversed(notes):
            st.markdown(
                f'<div class="note-card">'
                f'<div class="note-text">📌 {note["text"]}</div>'
                f'<div class="note-time">{note["timestamp"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
    else:
        st.caption('No notes saved yet. Say "Take a note..." to start.')

    st.markdown("<hr class='subtle-divider'>", unsafe_allow_html=True)

    # ── Memory Controls ─────────────────────
    st.markdown("### 🧹 Memory Controls")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.memory.clear_history()
            st.rerun()
    with col_m2:
        if st.button("🗑️ Clear Notes", use_container_width=True):
            st.session_state.memory.clear_notes()
            st.rerun()

    if st.button("⚠️ Reset Everything", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.session_state.memory.clear_all()
        st.session_state.last_scene_image = None
        st.session_state.last_scene_description = None
        st.rerun()

    st.markdown("<hr class='subtle-divider'>", unsafe_allow_html=True)

    # ── About ────────────────────────────────
    st.markdown("### ℹ️ About")
    st.caption(
        "ARGUS is a capstone project demonstrating AI-assisted "
        "smart glasses for visually impaired users. This prototype "
        "uses your laptop webcam, microphone, and speakers to "
        "simulate the wearable experience."
    )
    st.caption("© 2026 ARGUS Team — Capstone Prototype")


# ═══════════════════════════════════════════════════════
# Main Content — Two-Column Layout
# ═══════════════════════════════════════════════════════
tab_voice, tab_scene = st.tabs(["🎙️  Voice Assistant", "👁️  Scene Description"])

# ── Tab 1: Voice Assistant ───────────────────────────
with tab_voice:
    st.markdown(
        '<div class="section-card"><h3>🎙️ AI Voice Assistant</h3>'
        '<p style="color:#9ca3af;font-size:0.85rem;margin:0;">'
        'Speak naturally or type your query. ARGUS understands context, '
        'takes notes, tells time, and describes your surroundings.</p></div>',
        unsafe_allow_html=True,
    )

    # Action buttons
    col_v1, col_v2, col_v3 = st.columns([1, 1, 1])
    with col_v1:
        listen_btn = st.button(
            "🎤 Start Listening",
            use_container_width=True,
            type="primary",
            disabled=not st.session_state.mic_available,
        )
    with col_v2:
        scene_voice_btn = st.button(
            "👁️ Describe Scene",
            use_container_width=True,
            disabled=not st.session_state.cam_available or not st.session_state.api_ready,
        )
    with col_v3:
        st.markdown("")  # spacing

    # Text input fallback
    text_input = st.chat_input(
        "Type a message to ARGUS...",
    )

    # ── Handle Listening ─────────────────────
    if listen_btn:
        with st.spinner("🎤 Listening... Speak now!"):
            transcript, error = st.session_state.speech.listen()

        if error:
            st.warning(f"🎙️ {error}")
        elif transcript:
            st.info(f"🗣️ You said: *\"{transcript}\"*")
            process_query(transcript)
            st.rerun()

    # ── Handle Scene Button ──────────────────
    if scene_voice_btn:
        process_query("Describe my surroundings in detail.")
        st.rerun()

    # ── Handle Text Input ────────────────────
    if text_input:
        process_query(text_input)
        st.rerun()

    # ── Chat Display ─────────────────────────
    st.markdown("<hr class='subtle-divider'>", unsafe_allow_html=True)
    render_chat()

    # ── Auto-play last audio ─────────────────
    if "last_audio" in st.session_state and st.session_state.last_audio:
        st.audio(st.session_state.last_audio, format="audio/mp3", autoplay=True)
        st.session_state.last_audio = None  # prevent replay on rerun


# ── Tab 2: Scene Description ────────────────────────
with tab_scene:
    st.markdown(
        '<div class="section-card"><h3>👁️ Instant Scene Description</h3>'
        '<p style="color:#9ca3af;font-size:0.85rem;margin:0;">'
        'Capture a live image from your webcam and receive an AI-powered '
        'scene description optimized for visually impaired users.</p></div>',
        unsafe_allow_html=True,
    )

    col_sc1, col_sc2 = st.columns([1, 1])

    with col_sc1:
        describe_btn = st.button(
            "📸 Capture & Describe Scene",
            use_container_width=True,
            type="primary",
            disabled=not st.session_state.cam_available or not st.session_state.api_ready,
            key="scene_describe_btn",
        )

        # Optional custom prompt
        custom_prompt = st.text_area(
            "Custom visual question (optional):",
            placeholder="e.g., Is there anything dangerous ahead?",
            height=80,
            key="custom_scene_prompt",
        )

    with col_sc2:
        if st.session_state.last_scene_image is not None:
            st.image(
                st.session_state.last_scene_image,
                caption="📸 Last Captured Frame",
                use_container_width=True,
            )

    if describe_btn:
        with st.spinner("📸 Capturing image and analyzing scene..."):
            try:
                if custom_prompt and custom_prompt.strip():
                    description, pil_image = st.session_state.vision.describe_with_question(
                        custom_prompt.strip()
                    )
                else:
                    description, pil_image = st.session_state.vision.describe_scene()

                st.session_state.last_scene_image = pil_image
                st.session_state.last_scene_description = description

                # Add to chat as well
                query_text = custom_prompt.strip() if custom_prompt and custom_prompt.strip() else "Describe my surroundings"
                st.session_state.memory.add_interaction(query_text, description)
                add_ui_message("user", query_text, intent="scene")
                add_ui_message("assistant", description, intent="scene", image=pil_image)

                # Generate audio
                audio_bytes = st.session_state.speech.synthesize(description)
                if audio_bytes:
                    st.session_state.last_audio = audio_bytes

                st.rerun()

            except Exception as e:
                print(f"Scene capture error: {e}")
                st.error("❌ Scene capture failed. Please try again.")

    # Display last scene description
    if st.session_state.last_scene_description:
        st.markdown("<hr class='subtle-divider'>", unsafe_allow_html=True)
        st.markdown(
            f'<div class="section-card">'
            f'<h3>🗣️ Scene Description</h3>'
            f'<p style="color:#e0e7ff;font-size:0.95rem;line-height:1.6;">'
            f'{st.session_state.last_scene_description}'
            f'</p></div>',
            unsafe_allow_html=True,
        )

        # Audio playback for scene tab
        if "last_audio" in st.session_state and st.session_state.last_audio:
            st.audio(st.session_state.last_audio, format="audio/mp3", autoplay=True)
            st.session_state.last_audio = None


# ═══════════════════════════════════════════════════════
# Footer
# ═══════════════════════════════════════════════════════
st.markdown(
    '<div class="argus-footer">'
    '🕶️ ARGUS Prototype v1.0 · Built for Capstone Evaluation · '
    'Powered by Llama 3.2 Vision & Edge TTS'
    '</div>',
    unsafe_allow_html=True,
)
