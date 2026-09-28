import json
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("GEMINI_FLASH_MODEL", "gemini-1.5-flash")


def _demo_outline(user_prompt: str):
    return [
        {
            "panel": 1,
            "title": "The Beginning",
            "scene_description": f"The story begins with {user_prompt}.",
            "image_prompt": f"comic book panel, {user_prompt}, establishing shot, vivid colors"
        },
        {
            "panel": 2,
            "title": "The Journey",
            "scene_description": "The main character starts the adventure and discovers something unexpected.",
            "image_prompt": "comic book panel, hero beginning an exciting journey, cinematic composition"
        },
        {
            "panel": 3,
            "title": "The Challenge",
            "scene_description": "A major challenge appears and the character must find a creative solution.",
            "image_prompt": "comic book panel, dramatic challenge, expressive character, dynamic action"
        },
        {
            "panel": 4,
            "title": "The Turning Point",
            "scene_description": "The character makes an important decision that changes the direction of the story.",
            "image_prompt": "comic book panel, emotional turning point, dramatic lighting"
        },
        {
            "panel": 5,
            "title": "The Resolution",
            "scene_description": "The adventure reaches a satisfying conclusion.",
            "image_prompt": "comic book panel, happy resolution, heroic ending, colorful comic style"
        },
    ]


def generate_outline(user_prompt: str):
    """Generate a structured 5-panel comic outline with Gemini Flash.

    If no Gemini key is configured, a deterministic demo outline is returned so
    the project can still be run and tested locally.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return _demo_outline(user_prompt)

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(MODEL_NAME)

        prompt = f"""
You are a professional comic planner.
Create exactly 5 panels for this comic idea:

{user_prompt}

Return ONLY valid JSON as an array. Each item must contain:
"panel" (integer),
"title" (string),
"scene_description" (string),
"image_prompt" (string).
"""
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        data = json.loads(text)
        if not isinstance(data, list) or not data:
            raise ValueError("Gemini returned an invalid outline.")
        return data
    except Exception as exc:
        print(f"[Gemini Flash fallback] {exc}")
        return _demo_outline(user_prompt)
