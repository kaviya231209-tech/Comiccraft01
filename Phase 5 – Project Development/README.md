# ComicCraft – AI Comic Story Creator using Gemini Models

ComicCraft is a FastAPI-based web application that generates personalized comic stories from a user's prompt. The documented architecture uses Gemini models for structured outlines and narration, Stable Diffusion/Diffusers for comic-style illustrations, Jinja2 templates for the web UI, and FPDF for PDF export.

## Features

- Story prompt input
- Main character name
- Setting, tone, and art-style selection
- 5-panel structured comic outline
- AI narration and dialogue
- Panel image generation
- Comic preview page
- PDF export
- JSON API
- Image testing endpoint
- Local demo fallback when AI keys/models are not configured

The implementation follows the supplied project document's architecture and workflow: FastAPI + HTML/CSS/Jinja2, Gemini Flash/Pro, Stable Diffusion/Diffusers, layout building, and FPDF export.

## Project Structure

```text
ComicCraft/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── gemini_flash.py
│   ├── gemini_pro.py
│   ├── image_generator.py
│   ├── layout_builder.py
│   └── exporters.py
├── templates/
│   ├── index.html
│   ├── comic_preview.html
│   └── export_success.html
├── static/
│   ├── panels/
│   ├── exports/
│   └── fonts/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Run in VS Code – Windows

### 1. Open the ComicCraft folder

Open the extracted `ComicCraft_VSCode` folder in VS Code.

### 2. Create a virtual environment

```powershell
python -m venv venv
```

### 3. Activate it

```powershell
.env\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Configure the API key

Copy `.env.example` to `.env` and put your Gemini API key in:

```text
GEMINI_API_KEY=your_key_here
```

Do not upload `.env` to GitHub.

### 6. Run the application

```powershell
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## Demo Mode

If `GEMINI_API_KEY` is not configured, the application still runs using local demo story content and generated placeholder panel images. This is useful for checking the complete frontend/backend/PDF workflow before configuring AI services.

## Stable Diffusion

The project includes a Diffusers implementation in `app/image_generator.py`. For local Stable Diffusion generation, set:

```text
USE_LOCAL_DIFFUSERS=true
```

and configure the model in `.env`.

Local Diffusers generation can require several GB of model data and a capable GPU. The default is `false` so the project can be tested without a large model download.

## API Endpoints

- `GET /` – Homepage
- `POST /generate` – Form-based comic generation
- `POST /generate-comic/json` – JSON API generation
- `GET /test-image?prompt=...` – Test image generation
- `GET /health` – Health check
- `GET /docs` – FastAPI Swagger documentation

## Example JSON

```json
{
  "story_prompt": "A brave fox exploring an enchanted forest",
  "character_name": "Finn",
  "setting": "Forest",
  "tone": "Dramatic",
  "art_style": "Anime"
}
```

## Security

Never commit:

- `.env`
- Gemini API keys
- private tokens
- virtual-environment folders

## Source Basis

This implementation is based on the supplied ComicCraft project document, which specifies Gemini Flash for a structured 5-panel outline, Gemini Pro for narration/dialogue, Stable Diffusion for illustrations, Jinja2-powered HTML pages, and FPDF for PDF export.
