# hyperframe-ai-video-production-pipeline

Codex skill for planning and producing AI-assisted product videos with HyperFrames, HeyGen avatar/lipsync clips, optional fal video models, Codex imagegen assets, Browser/Playwright app capture, and reference-video analysis.

## What It Does

- Plans product demo, tutorial, launch, and educational videos.
- Downloads and analyzes reference videos with `yt-dlp`, `ffmpeg`, and `ffprobe`.
- Creates two-column scripts, capture maps, asset manifests, and QA checklists.
- Guides HyperFrames composition and render verification.
- Supports HeyGen avatar/lipsync workflows with short, manageable voiceover chunks.
- Supports optional fal video generation or upscaling when an API key is available.
- Includes MusicFlowAI and LaoshiAI production patterns.

API keys are optional. If HeyGen, fal, or another provider is not configured, the skill should still create the plan, prompts, placeholders, and setup checklist.

## Install

From this repo:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo dimitriharding/hyperframe-ai-video-production-pipeline \
  --path skills/ai-video-production-pipeline
```

Then restart Codex.

## Use

Example prompts:

```text
Use $ai-video-production-pipeline to create a 10 minute product walkthrough video plan for my app using HyperFrames and a HeyGen avatar host.
```

```text
Use $ai-video-production-pipeline to analyze this YouTube reference video, create a two-column script, and plan the screen captures.
```

```text
Use $ai-video-production-pipeline to create a batch workflow for short LaoshiAI app promo videos.
```

## Reference Video Analyzer

The skill includes:

```bash
skills/ai-video-production-pipeline/scripts/analyze_reference_video.py
```

Example:

```bash
python3 skills/ai-video-production-pipeline/scripts/analyze_reference_video.py \
  "https://www.youtube.com/watch?v=VIDEO_ID" \
  --output-dir reference-analysis/example
```

It creates:

- `ffprobe.json`
- `summary.md`
- `contact-sheets/`
- `scene-thumbs/`
- `frame-stats/scene-times.json`

## Safety

Do not commit API keys, login credentials, generated account data, private screenshots, or provider tokens. Keep those in local environment variables or your password manager.
