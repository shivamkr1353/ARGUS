"""
ARGUS Configuration Module
Centralized configuration for all system parameters.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ──────────────────────────────────────────────
# API Configuration
# ──────────────────────────────────────────────
KIMI_API_KEY = os.getenv("KIMI_API_KEY", "")
KIMI_BASE_URL = "https://integrate.api.nvidia.com/v1"

# ──────────────────────────────────────────────
# Model Configuration
# ──────────────────────────────────────────────
KIMI_TEXT_MODEL = "meta/llama-3.2-90b-vision-instruct"
KIMI_VISION_MODEL = "meta/llama-3.2-90b-vision-instruct"

# ──────────────────────────────────────────────
# Memory Configuration
# ──────────────────────────────────────────────
MAX_CONVERSATION_HISTORY = 5
NOTES_FILE = "argus_notes.json"

# ──────────────────────────────────────────────
# Speech Configuration
# ──────────────────────────────────────────────
TTS_VOICE = "en-US-AriaNeural"
TTS_RATE = "+0%"
LISTEN_TIMEOUT = 7
PHRASE_TIME_LIMIT = 15

# ──────────────────────────────────────────────
# Vision Configuration
# ──────────────────────────────────────────────
SCENE_PROMPT = (
    "You are an AI assistant embedded in smart glasses for a visually impaired person. "
    "Describe this environment for the user. Mention:\n"
    "- Important objects and their approximate positions (left, right, ahead)\n"
    "- People and what they appear to be doing\n"
    "- Possible hazards or obstacles\n"
    "- Navigation cues (doors, stairs, pathways)\n"
    "- Readable signs or text if visible\n\n"
    "Keep your response concise, natural, and immediately useful. "
    "Speak as if you are talking directly to the user. "
    "Do NOT list object labels — provide contextual scene understanding."
)

# ──────────────────────────────────────────────
# Assistant System Prompt
# ──────────────────────────────────────────────
ASSISTANT_SYSTEM_PROMPT = (
    "You are ARGUS, an empathetic and intelligent AI assistant integrated into "
    "smart glasses designed for visually impaired users. You are warm, concise, "
    "and proactive. Always respond as if you are the user's trusted companion. "
    "Keep answers brief and spoken-friendly — avoid markdown, bullet points, "
    "or overly long text. Prioritize clarity and helpfulness."
)

# ──────────────────────────────────────────────
# UI Configuration
# ──────────────────────────────────────────────
APP_TITLE = "ARGUS"
APP_SUBTITLE = "AI-Powered Responsive Glasses for Uplifting the Blind in Society"
APP_ICON = "🕶️"
