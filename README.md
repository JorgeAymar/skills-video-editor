# Video Editor Skills for Claude Code

A collection of Claude Code skills for editing, analyzing, and producing YouTube Shorts and video content — using local tools (ffmpeg, Whisper) and code-based rendering (HyperFrames).

## Requirements

```bash
brew install ffmpeg yt-dlp
pip install openai-whisper faster-whisper
node --version  # v22+ required for HyperFrames
```

## Install

Copy any skill folder into `~/.claude/skills/` and add a trigger to `~/.claude/CLAUDE.md`.

Or clone the whole repo:

```bash
git clone https://github.com/JorgeAymar/skills-video-editor ~/.claude/skills-video-editor
# then symlink or copy the skills you want into ~/.claude/skills/
```

---

## Skills

### Video Production (ffmpeg-based)

| Skill | Command | What it does |
|---|---|---|
| `video-download` | `/video-download` | Download YouTube videos or audio (yt-dlp) |
| `video-highlights` | `/video-highlights` | Transcribe + extract best moments with AI |
| `video-subtitles` | `/video-subtitles` | Add subtitles in multiple languages |
| `video-music` | `/video-music` | Add background music with volume/fade control |
| `video-transitions` | `/video-transitions` | Add transitions between clips (xfade) |
| `video-virality` | `/video-virality` | Score viral potential for YouTube Shorts |

### Code-based Video Rendering (HyperFrames)

> HyperFrames lets you write HTML and render it as MP4. Built for AI agents.
> Repo: [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes)

| Skill | Command | What it does |
|---|---|---|
| `hyperframes` | `/hyperframes` | HTML video composition with GSAP timelines |
| `hyperframes-cli` | `/hyperframes-cli` | CLI: init, lint, inspect, render |
| `hyperframes-media` | `/hyperframes-media` | TTS (no API), transcription, background removal |
| `gsap` | `/gsap` | GSAP animations in HyperFrames |
| `animejs` | `/animejs` | Anime.js animations |
| `css-animations` | `/css-animations` | CSS keyframe animations |
| `lottie` | `/lottie` | Lottie / After Effects animations |
| `three` | `/three` | Three.js 3D scenes |
| `waapi` | `/waapi` | Web Animations API |
| `tailwind-hyperframes` | `/tailwind-hyperframes` | Tailwind v4 in HyperFrames |
| `remotion-to-hyperframes` | `/remotion-to-hyperframes` | Migrate from Remotion to HyperFrames |
| `website-to-hyperframes` | `/website-to-hyperframes` | Convert a website into a video |

---

## Default Target Format

All skills assume **YouTube Shorts** by default:
- Aspect ratio: 9:16 (1080×1920)
- Max duration: 60 seconds
- Hook in first 3 seconds

---

## video-virality Score System

Scores your video across 8 signals:

| Signal | What it measures |
|---|---|
| Hook Score | First 3 seconds strength |
| Retention Curve | Estimated drop-off points |
| Emotional Triggers | Emotions activated |
| Value Density | Insights per second |
| CTA Power | Call-to-action effectiveness |
| Pattern Interrupts | Rhythm breaks |
| Shareability | Why someone would share it |
| Algorithm Signals | Technical factors (duration, subs, audio) |

---

## License

Skills in `skills/hyperframes*`, `skills/gsap`, `skills/animejs`, `skills/css-animations`, `skills/lottie`, `skills/three`, `skills/waapi`, `skills/tailwind-hyperframes`, `skills/remotion-to-hyperframes`, `skills/website-to-hyperframes` are from [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) — Apache 2.0.

Original skills (`video-*`, `youtube-downloader`) — MIT.
