from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.image_generator import generate_image
from app.layout_builder import build_comic_layout
from app.exporters import save_pdf

from pathlib import Path

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent


class PromptRequest(BaseModel):
    story_prompt: str
    character_name: str
    setting: str
    tone: str
    art_style: str


def build_prompt(story_prompt, character_name, setting, tone, art_style):
    return (
        f"Story idea: {story_prompt}\n"
        f"Main character: {character_name}\n"
        f"Setting: {setting}\n"
        f"Tone: {tone}\n"
        f"Art style: {art_style}"
    )


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return request.app.state.templates.TemplateResponse(
        "index.html", {"request": request}
    )


@router.post("/generate", response_class=HTMLResponse)
async def generate_comic(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...)
):
    try:
        user_prompt = build_prompt(
            story_prompt, character_name, setting, tone, art_style
        )
        outline = generate_outline(user_prompt)
        if not outline:
            raise ValueError("Could not generate comic outline.")

        full_story = generate_story(outline)

        image_paths = []
        for index, panel in enumerate(outline, start=1):
            image_prompt = (
                f"{panel.get('image_prompt', '')}. "
                f"Character: {character_name}. Setting: {setting}. "
                f"Tone: {tone}. Art style: {art_style}."
            )
            image_paths.append(generate_image(image_prompt, f"panel_{index}"))

        layout = build_comic_layout(image_paths, full_story, outline)
        pdf_path = save_pdf(layout)

        return request.app.state.templates.TemplateResponse(
            "comic_preview.html",
            {
                "request": request,
                "layout": layout,
                "pdf_path": pdf_path,
                "story_prompt": story_prompt,
            },
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/generate-comic/json")
async def generate_comic_json(payload: PromptRequest):
    try:
        user_prompt = build_prompt(
            payload.story_prompt,
            payload.character_name,
            payload.setting,
            payload.tone,
            payload.art_style,
        )
        outline = generate_outline(user_prompt)
        full_story = generate_story(outline)

        image_paths = [
            generate_image(
                f"{panel.get('image_prompt', '')}. "
                f"Character: {payload.character_name}. "
                f"Setting: {payload.setting}. "
                f"Tone: {payload.tone}. "
                f"Art style: {payload.art_style}.",
                f"panel_{i}",
            )
            for i, panel in enumerate(outline, start=1)
        ]

        layout = build_comic_layout(image_paths, full_story, outline)
        pdf_path = save_pdf(layout)

        return {"layout": layout, "pdf_path": pdf_path}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request, pdf_path: str = ""):
    return request.app.state.templates.TemplateResponse(
        "export_success.html",
        {"request": request, "pdf_path": pdf_path},
    )


@router.get("/test-image")
async def test_image(prompt: str = "a friendly fox in an enchanted forest"):
    try:
        image_path = generate_image(prompt, "test_image")
        return {"image_path": image_path}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
