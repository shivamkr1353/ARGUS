"""
ARGUS Vision Module
Captures webcam frames and performs AI-powered scene understanding
using the Kimi K2 Vision API (OpenAI-compatible).
"""

import io
import base64
import cv2
import numpy as np
from PIL import Image
from typing import Optional, Tuple
from openai import OpenAI

from config import KIMI_API_KEY, KIMI_VISION_MODEL, KIMI_BASE_URL, SCENE_PROMPT


class VisionModule:
    """Handles webcam capture and Kimi K2 Vision scene description."""

    def __init__(
        self,
        api_key: str = KIMI_API_KEY,
        model_name: str = KIMI_VISION_MODEL,
        base_url: str = KIMI_BASE_URL,
    ):
        if not api_key:
            raise ValueError(
                "KIMI_API_KEY is not set. "
                "Please add it to your .env file."
            )
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model_name = model_name
        self.scene_prompt = SCENE_PROMPT

    # ── Webcam Capture ───────────────────────────────────

    def capture_frame(self) -> np.ndarray:
        """
        Capture a single frame from the default webcam.
        Returns the frame as a BGR numpy array.
        Raises RuntimeError if the webcam is unavailable.
        """
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            raise RuntimeError(
                "Webcam not available. Please check your camera connection."
            )
        try:
            # Discard a few frames to let the camera auto-adjust
            for _ in range(5):
                cap.read()
            ret, frame = cap.read()
            if not ret or frame is None:
                raise RuntimeError("Failed to capture image from webcam.")
            return frame
        finally:
            cap.release()

    def frame_to_pil(self, frame: np.ndarray) -> Image.Image:
        """Convert an OpenCV BGR frame to a PIL RGB Image."""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb)

    def pil_to_bytes(self, pil_image: Image.Image) -> bytes:
        """Convert a PIL Image to JPEG bytes for the API, resizing if necessary."""
        # Resize to max 768x768 to prevent 400 Bad Request on NVIDIA NIM
        pil_image.thumbnail((768, 768))
        buffer = io.BytesIO()
        pil_image.save(buffer, format="JPEG", quality=80)
        return buffer.getvalue()

    @staticmethod
    def check_webcam() -> bool:
        """Check whether a webcam is accessible."""
        try:
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            available = cap.isOpened()
            cap.release()
            return available
        except Exception:
            return False

    # ── Scene Description ────────────────────────────────

    def describe_scene(
        self,
        frame: Optional[np.ndarray] = None,
        custom_prompt: Optional[str] = None,
    ) -> Tuple[str, Optional[Image.Image]]:
        """
        Capture (or use provided) frame, send to Kimi K2 Vision,
        and return a natural-language scene description.

        Args:
            frame: Optional pre-captured BGR frame. If None, captures live.
            custom_prompt: Optional override for the default scene prompt.

        Returns:
            Tuple of (description_text, pil_image).
        """
        # Capture if not provided
        if frame is None:
            frame = self.capture_frame()

        pil_image = self.frame_to_pil(frame)
        image_bytes = self.pil_to_bytes(pil_image)
        b64_image = base64.b64encode(image_bytes).decode("utf-8")
        prompt = custom_prompt or self.scene_prompt

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{b64_image}",
                                },
                            },
                        ],
                    }
                ],
                max_tokens=512,
                temperature=0.4,
            )
            description = response.choices[0].message.content.strip()
            if not description:
                description = "I captured an image but could not generate a description. Please try again."
                
        except Exception as e:
            print(f"[VisionModule] Vision API error: {e}")
            description = f"Error occurred: {str(e)}"

        return description, pil_image

    def describe_with_question(
        self, question: str, frame: Optional[np.ndarray] = None
    ) -> Tuple[str, Optional[Image.Image]]:
        """
        Answer a specific visual question about the scene.
        Augments the user's question with accessibility context.
        """
        augmented_prompt = (
            f"You are an AI assistant in smart glasses for a visually impaired person. "
            f"The user asked: \"{question}\"\n\n"
            f"Look at this image and answer their question. Be concise, spatial, "
            f"and immediately helpful. Mention positions (left, right, ahead) when relevant."
        )
        return self.describe_scene(frame=frame, custom_prompt=augmented_prompt)
