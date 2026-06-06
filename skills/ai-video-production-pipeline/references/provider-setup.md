# Provider Setup

Use this reference when a video job needs provider setup, local tools, or API keys.

## Local Tools

Check tools before promising a render:

```bash
node --version
npm --version
python3 --version
ffmpeg -version
ffprobe -version
yt-dlp --version
```

If `yt-dlp` is missing, install it in a project-local venv or ask the user how they prefer to install it. Do not mutate system package managers unless asked.

## HyperFrames

- Use the installed HyperFrames skills for composition rules and CLI details.
- Typical commands inside a HyperFrames project:

```bash
npx hyperframes lint
npx hyperframes inspect
npx hyperframes render
```

Run the exact command supported by the local `hyperframes.json` or package scripts.

## HeyGen

HeyGen access is optional and may require the user to provide an API key, CLI login, or account access.

Use HeyGen for:

- Host/avatar lipsync clips.
- Short intro, bridge, and outro segments.
- Consistent presenter identity across a video series.

Production pattern:

- Break scripts into 12-30 second host chunks.
- Generate a small voice/avatar test before the full set.
- Keep each clip filename tied to a scene number.
- Verify that the avatar image matches the approved source before generating a batch.

Do not print or store API keys in scripts, docs, screenshots, or final replies.

## fal

fal access is optional and usually requires an API key. Common environment variable names include `FAL_KEY`; verify current provider docs or CLI help before use.

Use fal for:

- AI video model clips.
- B-roll variations.
- Upscaling or enhancement.
- Alternate visual treatments when product screens need supporting footage.

If fal is unavailable, create prompts, shot descriptions, durations, and placeholder asset rows.

## Codex Imagegen

Use Codex imagegen for still-image generation or edits when the user asks for visuals, thumbnails, avatar backdrops, mood boards, storyboard frames, or product metaphor images.

When generating images:

- Use exact aspect ratio in the prompt, such as 16:9 or 9:16.
- Include the product category and intended video use.
- Keep style consistent with the approved design system.
- Save or reference generated images in the asset manifest when available.

## Reference Video Download

For public video references, prefer `scripts/analyze_reference_video.py` from this skill. It uses `yt-dlp`, `ffmpeg`, and `ffprobe`.

Respect platform terms, copyright, and user intent. Use reference videos for analysis and structural inspiration. Do not reproduce copyrighted footage or long transcript passages unless the user owns or licenses the source.

## Browser and Playwright Capture

Use Browser or Playwright to explore app workflows and plan captures.

Capture guidance:

- Use dedicated demo accounts and safe demo data.
- Capture one task per clip when possible.
- Use viewport sizes that preserve UI readability.
- Avoid credentials, notifications, private customer data, and unrelated windows.
- Record waits only when they teach the viewer what happens next.
