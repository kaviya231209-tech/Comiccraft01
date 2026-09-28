import os
import re
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
PANEL_DIR = BASE_DIR / "static" / "panels"
PANEL_DIR.mkdir(parents=True, exist_ok=True)


def sanitize_filename(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_-]+", "_", value).strip("_")
    return value[:80] or "panel"


def _placeholder_image(path: Path, prompt: str):
    """Create a lightweight placeholder image for local demo/testing."""
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("RGB", (900, 600), (225, 238, 250))
    draw = ImageDraw.Draw(img)
    title = "ComicCraft Demo Panel"
    draw.rectangle((35, 35, 865, 565), outline=(40, 80, 120), width=5)
    draw.text((70, 75), title, fill=(25, 50, 80))
    short = prompt[:180]
    draw.multiline_text((70, 145), short, fill=(30, 30, 30), spacing=8)
    draw.text((70, 500), "Add API/model configuration for AI-generated artwork.",
              fill=(70, 70, 70))
    img.save(path)


def generate_image(prompt: str, filename: str | None = None) -> str:
    """Generate an image with Diffusers when enabled; otherwise create a demo image.

    Set USE_LOCAL_DIFFUSERS=true to load the Stable Diffusion model locally.
    This can require a capable GPU and several GB of model files.
    """
    if not filename:
        filename = sanitize_filename(prompt)

    path = PANEL_DIR / f"{filename}.png"
    use_diffusers = os.getenv("USE_LOCAL_DIFFUSERS", "false").lower() == "true"

    if use_diffusers:
        try:
            import torch
            from diffusers import StableDiffusionPipeline

            model_id = os.getenv(
                "STABLE_DIFFUSION_MODEL",
                "runwayml/stable-diffusion-v1-5"
            )
            dtype = torch.float16 if torch.cuda.is_available() else torch.float32
            pipe = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=dtype
            )
            if torch.cuda.is_available():
                pipe = pipe.to("cuda")

            image = pipe(
                f"comic book illustration, {prompt}",
                num_inference_steps=int(os.getenv("DIFFUSION_STEPS", "20"))
            ).images[0]
            image.save(path)
            return f"/static/panels/{path.name}"
        except Exception as exc:
            print(f"[Diffusers fallback] {exc}")

    _placeholder_image(path, prompt)
    return f"/static/panels/{path.name}"
