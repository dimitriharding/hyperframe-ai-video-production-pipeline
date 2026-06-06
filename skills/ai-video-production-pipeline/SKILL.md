---
name: ai-video-production-pipeline
description: Use when creating product demo videos, educational YouTube videos, app walkthroughs, reference-video breakdowns, avatar/lipsync clips, screen-capture edits, AI-generated image/video assets, or HyperFrames compositions. Covers HyperFrames, HeyGen lipsync, optional fal video models, Codex imagegen assets, yt-dlp reference analysis, Playwright/browser capture, script planning, rendering, and QA.
metadata:
  short-description: Build AI-assisted product videos end to end
---

# AI Video Production Pipeline

Use this skill to take a video from idea to verified render: reference analysis, script, asset generation, screen capture, avatar clips, HyperFrames composition, export, and QA.

API-key-dependent services are optional. If a key or provider login is missing, produce the plan, script, storyboard, prompts, placeholders, and exact setup instructions, then mark those clips as pending.

## Core Rules

- Start with the real goal: audience, platform, duration, primary CTA, and what the viewer should be able to do after watching.
- For product walkthroughs, show the actual workflow. Do not summarize clicks that should be visible on screen.
- For reference videos, analyze structure and pacing, but write original scripts and original visuals.
- For long videos, use short host/avatar chunks, usually 12-30 seconds, and let walkthrough or playback sections breathe.
- Do one representative sample first before scaling to a batch or series.
- Keep secrets out of docs, logs, filenames, screenshots, and final responses.
- Verify renders with `ffprobe` plus visual contact sheets or screenshots before calling a video done.

## Standard Workflow

1. **Intake**
   - Confirm platform and format: YouTube 16:9, Shorts/TikTok 9:16, website hero, ad, course lesson, or batch social.
   - Confirm app/project, target user, product workflow, CTA, duration, and whether real accounts can be used.
   - Check project docs for existing video plans, brand files, `DESIGN.md`, captures, avatar images, and approved copy.

2. **Reference Analysis**
   - If the user provides a YouTube URL or video reference, download or ingest it and create contact sheets, metadata, scene samples, and subtitle/transcript notes.
   - Use `scripts/analyze_reference_video.py` when `yt-dlp`, `ffmpeg`, and `ffprobe` are available.
   - Summarize the reference by narrative pattern, scene rhythm, camera/layout pattern, overlay style, audio style, and CTA mechanics.
   - Do not copy long wording from the reference. Adapt the structure and energy into original copy.

3. **Plan and Script**
   - Create a production plan before rendering.
   - For walkthroughs, write a capture map with each task clip: route, viewport, action, hold time, expected visual proof, and retake criteria.
   - Write a two-column script: left column has timecode, visuals, screen actions, overlays, and audio cues; right column has voiceover.
   - Add SEO packaging for YouTube: title options, description, chapters, keywords, pinned comment, thumbnail text, and CTA.

4. **Assets**
   - Use Codex imagegen for still images, thumbnails, host backdrops, product metaphors, and style frames.
   - Use HeyGen for host/avatar lipsync clips when the user wants a speaking avatar. Chunk scripts into manageable clips and keep filenames tied to scene numbers.
   - Use fal or other video models for optional b-roll, cinematic transitions, abstract clips, and variations. If no API key is available, produce prompts and placeholders.
   - Keep an asset manifest with source, generated output, prompt, provider, model, duration, and status.

5. **Screen Capture**
   - Use Browser or Playwright for live app exploration and capture.
   - Prefer task clips over one long recording. Name clips by workflow step.
   - For desktop walkthroughs, use a readable viewport that fits inside the final canvas without looking overly wide. Common starting point: `1440x900` captured into a 1920x1080 HyperFrames canvas.
   - Hide or avoid credentials, private data, excess browser chrome, and unrelated notifications.
   - Capture real waits and finished states when they teach the workflow. Speed up only after the viewer understands the step.

6. **HyperFrames Composition**
   - Use the `hyperframes` and `hyperframes-cli` skills when authoring or rendering.
   - HTML is the source of truth. Build the end-state layout first, then animate.
   - Use real screen clips, avatar clips, generated b-roll, captions, callouts, and audio as separate timed tracks.
   - Avoid heavy persistent overlays. Use callouts only when they clarify a click, prompt, output, or result.
   - Keep app screens readable. Frame screen captures cleanly on a designed background instead of stretching full-bleed when the UI becomes too wide.

7. **Render and Verify**
   - Run HyperFrames lint/inspect/render when available.
   - Verify media with `ffprobe`.
   - Create screenshots or contact sheets for the final render.
   - Review for unreadable UI text, wrong timing, missing audio, bad cuts, avatar mismatch, overlaid text covering product UI, and stale credentials.

8. **Scale**
   - For a series, create a reusable project folder structure, a shared design system, reusable avatar shot list, and per-video manifests.
   - For a batch, start with `--limit 1` or one sample render, compare against the approved reference, then scale.

## Tool Routing

- **HyperFrames by HeyGen**: final HTML video composition, animation, captions, render workflow.
- **HeyGen**: lipsync/avatar host clips and talking-head bridge segments. Optional provider access.
- **fal**: optional AI video model clips, upscaling, visual b-roll, or style variants. Optional API key.
- **Codex imagegen**: still image generation and image edits directly in Codex.
- **Browser / Playwright**: app exploration, login flows, screenshots, and screen-capture planning.
- **yt-dlp + ffmpeg + ffprobe**: public reference-video download, frame extraction, contact sheets, scene detection, and metadata.
- **Documents/Presentations**: optional polished decks, Word docs, or Google Docs if the user asks for shareable production materials.

## Optional References

- Read `references/provider-setup.md` when credentials, CLIs, API keys, or local setup are involved.
- Read `references/project-patterns.md` for MusicFlowAI and LaoshiAI production patterns.
- Read `references/deliverable-templates.md` when creating plan/script/manifest artifacts.

## Completion Checklist

- The plan states format, duration, audience, CTA, and production stack.
- The script is broken into manageable voiceover/avatar chunks.
- Product screens show real actions, not just generic b-roll.
- Reference influence is structural only and original in wording.
- API-key-dependent outputs are either generated or clearly marked pending.
- Final render or sample has `ffprobe` evidence and visual QA artifacts.
