import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("GEMINI_PRO_MODEL", "gemini-1.5-pro")


def _demo_story(outline):
    parts = []
    for panel in outline:
        title = panel.get("title", f"Panel {panel.get('panel', '')}")
        scene = panel.get("scene_description", "")
        parts.append(
            f"Panel {panel.get('panel', '')}: {title}\n"
            f"Caption: The adventure continues.\n"
            f"Narration: {scene}\n"
            f"Dialogue: \"Let's see what happens next!\"\n"
        )
    return "\n".join(parts)


def generate_story(outline):
    """Expand the outline into narration and dialogue using Gemini Pro."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return _demo_story(outline)

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(MODEL_NAME)

        compact = "\n".join(
            f"Panel {p.get('panel')}: {p.get('title')} - {p.get('scene_description')}"
            for p in outline
        )
        prompt = f"""
You are a professional comic book writer.
Expand the following 5-panel outline into a cohesive comic story.

{compact}

For every panel provide:
- a short caption
- engaging narration
- character dialogue

Keep the panels self-contained but connected.
"""
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as exc:
        print(f"[Gemini Pro fallback] {exc}")
        return _demo_story(outline)
