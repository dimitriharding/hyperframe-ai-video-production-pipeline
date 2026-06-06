# Deliverable Templates

Use these structures when creating artifacts for a video project.

## Production Plan

```markdown
# Video Production Plan

## Goal
- Product:
- Audience:
- Platform:
- Target duration:
- Primary CTA:

## Reference Direction
- Reference sources:
- Patterns to adapt:
- Patterns to avoid:

## Workflow To Show
| Step | Screen/Route | Action | Proof Needed | Capture Notes |
|---|---|---|---|---|

## Asset List
| Asset | Source/Provider | Duration/Size | Status | Notes |
|---|---|---:|---|---|

## Voiceover Chunks
| Chunk | Time | Type | Provider | Status |
|---|---:|---|---|---|

## Render Plan
- Composition:
- Resolution:
- FPS:
- Captions:
- Music/SFX:

## QA
- ffprobe:
- Screenshots/contact sheet:
- Known risks:
```

## Two-Column Script

Use a real HTML artifact when the user wants a visual production document. Keep the table readable.

Columns:

- **Visuals and cues**: timecode, route, screen action, overlay, audio cue, capture note.
- **Voiceover**: exact narration or "no narration, let audio play."

For host/avatar chunks, label the voiceover as `HeyGen chunk candidate`. For screen-demo narration, label it as `VO only` unless the avatar should remain picture-in-picture.

## Capture Map

```markdown
# Capture Map

| Clip | Viewport | Route | Action | Hold | Retake If |
|---|---|---|---|---:|---|
| 01-proof | 1440x900 | /dashboard/content/... | Play finished output | 30s | UI cropped, audio missing |
```

## Asset Manifest

```markdown
# Asset Manifest

| ID | Type | Provider | Prompt/Source | Output Path | Status | Notes |
|---|---|---|---|---|---|---|
```

Status values:

- `planned`
- `pending-key`
- `generated`
- `captured`
- `approved`
- `needs-retake`
- `rejected`

## Final QA Note

```markdown
# Final QA

## Media
- File:
- Duration:
- Resolution:
- FPS:
- Audio:

## Visual Check
- Contact sheet:
- Screenshots:
- Issues:

## Ready State
- Ready for review:
- Blockers:
```
