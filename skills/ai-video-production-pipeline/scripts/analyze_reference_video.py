#!/usr/bin/env python3
"""Download or inspect a reference video and create analysis artifacts.

Outputs include ffprobe JSON, contact sheets, scene thumbnails, scene times,
and a compact summary. Requires ffmpeg and ffprobe. URL downloads require
yt-dlp.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip().lower())
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "reference-video"


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(f"Missing required tool: {name}")


def run(cmd: list[str], *, cwd: Path | None = None, stderr_file: Path | None = None) -> subprocess.CompletedProcess[str]:
    print("+ " + " ".join(cmd), flush=True)
    if stderr_file:
        with stderr_file.open("w", encoding="utf-8") as err:
            return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=err, check=True)
    return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)


def newest_mp4(output_dir: Path) -> Path | None:
    files = sorted(output_dir.glob("*.mp4"), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None


def download_source(source: str, output_dir: Path) -> Path:
    require_tool("yt-dlp")
    cmd = [
        "yt-dlp",
        "--write-info-json",
        "--write-auto-subs",
        "--sub-lang",
        "en",
        "--convert-subs",
        "vtt",
        "--merge-output-format",
        "mp4",
        "--output",
        "%(id)s.%(ext)s",
        source,
    ]
    run(cmd, cwd=output_dir)
    video = newest_mp4(output_dir)
    if video is None:
        raise SystemExit("yt-dlp completed but no .mp4 was found in the output directory")
    return video


def probe_video(video: Path, output_dir: Path) -> dict:
    result = run([
        "ffprobe",
        "-v",
        "error",
        "-show_format",
        "-show_streams",
        "-of",
        "json",
        str(video),
    ])
    data = json.loads(result.stdout)
    (output_dir / "ffprobe.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    return data


def make_contact_sheets(video: Path, output_dir: Path, every_seconds: float) -> None:
    contact_dir = output_dir / "contact-sheets"
    contact_dir.mkdir(exist_ok=True)
    label = str(int(every_seconds)) if every_seconds.is_integer() else str(every_seconds).replace(".", "-")
    vf = f"fps=1/{every_seconds},scale=320:-1,tile=5x4"
    run([
        "ffmpeg",
        "-y",
        "-i",
        str(video),
        "-vf",
        vf,
        "-q:v",
        "3",
        str(contact_dir / f"every-{label}s-sheet-%02d.jpg"),
    ])


def detect_scenes(video: Path, output_dir: Path, threshold: float, scene_max: int) -> list[dict]:
    scene_dir = output_dir / "scene-thumbs"
    stats_dir = output_dir / "frame-stats"
    scene_dir.mkdir(exist_ok=True)
    stats_dir.mkdir(exist_ok=True)
    log_path = stats_dir / "scene-detection.log"
    vf = f"select='gt(scene,{threshold})',showinfo,scale=320:-1"
    run([
        "ffmpeg",
        "-y",
        "-i",
        str(video),
        "-vf",
        vf,
        "-vsync",
        "vfr",
        "-frames:v",
        str(scene_max),
        str(scene_dir / "scene-%04d.jpg"),
    ], stderr_file=log_path)

    text = log_path.read_text(encoding="utf-8", errors="replace")
    times: list[dict] = []
    for index, match in enumerate(re.finditer(r"pts_time:([0-9.]+)", text), start=1):
        times.append({"index": index, "time": float(match.group(1))})

    (stats_dir / "scene-times.json").write_text(json.dumps(times, indent=2), encoding="utf-8")

    thumbs = sorted(scene_dir.glob("scene-*.jpg"))
    if thumbs:
        run([
            "ffmpeg",
            "-y",
            "-framerate",
            "1",
            "-pattern_type",
            "glob",
            "-i",
            str(scene_dir / "scene-*.jpg"),
            "-vf",
            "scale=240:-1,tile=6x5",
            "-frames:v",
            "1",
            str(output_dir / "scene-thumbs-sheet.jpg"),
        ])

    return times


def format_duration(probe: dict) -> str:
    duration = probe.get("format", {}).get("duration")
    if not duration:
        return "unknown"
    seconds = float(duration)
    minutes = int(seconds // 60)
    remaining = seconds - minutes * 60
    return f"{minutes}:{remaining:05.2f} ({seconds:.2f}s)"


def write_summary(source: str, video: Path, output_dir: Path, probe: dict, scene_times: list[dict]) -> None:
    video_stream = next((s for s in probe.get("streams", []) if s.get("codec_type") == "video"), {})
    audio_stream = next((s for s in probe.get("streams", []) if s.get("codec_type") == "audio"), {})
    lines = [
        "# Reference Video Analysis",
        "",
        f"- Source: `{source}`",
        f"- Local video: `{video}`",
        f"- Generated: `{datetime.now(timezone.utc).isoformat()}`",
        f"- Duration: {format_duration(probe)}",
        f"- Video: {video_stream.get('width', 'unknown')}x{video_stream.get('height', 'unknown')} {video_stream.get('avg_frame_rate', 'unknown')} {video_stream.get('codec_name', 'unknown')}",
        f"- Audio: {audio_stream.get('codec_name', 'unknown')}",
        f"- Scene changes captured: {len(scene_times)}",
        "",
        "## Files",
        "",
        "- `ffprobe.json`",
        "- `contact-sheets/`",
        "- `scene-thumbs/`",
        "- `scene-thumbs-sheet.jpg` when scenes were detected",
        "- `frame-stats/scene-times.json`",
        "- `frame-stats/scene-detection.log`",
        "",
        "## Next Analysis Pass",
        "",
        "- Identify narrative sections and time ranges.",
        "- Note visual framing, overlays, pacing, and CTA structure.",
        "- Convert useful structure into original script language.",
    ]
    (output_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze a reference video for AI video production.")
    parser.add_argument("source", help="Public video URL or local video path")
    parser.add_argument("--output-dir", default=None, help="Directory for analysis artifacts")
    parser.add_argument("--every-seconds", type=float, default=5.0, help="Contact sheet sampling interval")
    parser.add_argument("--scene-threshold", type=float, default=0.25, help="FFmpeg scene threshold")
    parser.add_argument("--scene-max", type=int, default=120, help="Max scene thumbnails to extract")
    parser.add_argument("--skip-scenes", action="store_true", help="Only create metadata and contact sheets")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    require_tool("ffmpeg")
    require_tool("ffprobe")

    if args.output_dir:
        output_dir = Path(args.output_dir).expanduser().resolve()
    elif is_url(args.source):
        parsed = urlparse(args.source)
        output_dir = Path.cwd() / f"reference-analysis-{slugify(parsed.netloc + parsed.path)}"
    else:
        output_dir = Path.cwd() / f"reference-analysis-{slugify(Path(args.source).stem)}"

    output_dir.mkdir(parents=True, exist_ok=True)

    if is_url(args.source):
        video = download_source(args.source, output_dir)
    else:
        video = Path(args.source).expanduser().resolve()
        if not video.exists():
            raise SystemExit(f"Local video does not exist: {video}")

    probe = probe_video(video, output_dir)
    make_contact_sheets(video, output_dir, args.every_seconds)
    scene_times: list[dict] = []
    if not args.skip_scenes:
        scene_times = detect_scenes(video, output_dir, args.scene_threshold, args.scene_max)
    write_summary(args.source, video, output_dir, probe, scene_times)

    print(f"\nAnalysis written to: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
