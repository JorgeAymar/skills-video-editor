---
name: youtube-downloader
description: Downloads YouTube videos or audio using yt-dlp. Handles single videos, playlists, and audio-only extraction. Trigger with /youtube-downloader or when user wants to download from YouTube.
intent: Guides the user through downloading YouTube content by asking for the URL, desired format (video/audio), quality, and output directory, then executes the appropriate yt-dlp command. Handles errors like geo-restrictions, private videos, and missing dependencies.
type: interactive
---

# YouTube Downloader Skill

## Purpose

Download videos, playlists, or audio from YouTube using `yt-dlp`. Asks the user exactly what they need, builds the right command, runs it, and confirms the output.

## Prerequisites Check

Before doing anything else, verify the required tools are installed:

```bash
which yt-dlp || echo "MISSING: yt-dlp"
which ffmpeg || echo "MISSING: ffmpeg"
```

If `yt-dlp` is missing, instruct the user:
```bash
brew install yt-dlp        # macOS
# or
pip install yt-dlp         # cross-platform
```

If `ffmpeg` is missing:
```bash
brew install ffmpeg        # macOS
```

## Interaction Flow

Ask **one question at a time**. Never dump all questions at once.

### Step 1 — Get the URL

Ask:
> "Pega la URL de YouTube que quieres descargar:"

Accept any YouTube URL: video, playlist, shorts, channel.

### Step 2 — Format

Ask:
> "¿Qué quieres descargar?
> 1. Video (MP4)
> 2. Solo audio (MP3)
> 3. Video + audio por separado
> 4. Ver todos los formatos disponibles primero"

If option 4: run `yt-dlp --list-formats <URL>` and show results before continuing.

### Step 3 — Quality (only if video was selected)

Ask:
> "¿Qué calidad prefieres?
> 1. Mejor calidad disponible
> 2. 1080p
> 3. 720p
> 4. 480p
> 5. La más ligera (menor tamaño)"

### Step 4 — Output directory

Ask:
> "¿Dónde quieres guardar el archivo?
> 1. Carpeta actual (`.`)
> 2. Escritorio (`~/Desktop`)
> 3. Descargas (`~/Downloads`)
> 4. Especificar ruta personalizada"

### Step 5 — Confirm and execute

Show the command that will be run, then execute it.

## Command Templates

### Best video quality (MP4)
```bash
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" \
  --merge-output-format mp4 \
  -o "<output_dir>/%(title)s.%(ext)s" \
  "<URL>"
```

### Specific resolution (e.g. 1080p)
```bash
yt-dlp -f "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]" \
  --merge-output-format mp4 \
  -o "<output_dir>/%(title)s.%(ext)s" \
  "<URL>"
```

### Audio only (MP3)
```bash
yt-dlp -x --audio-format mp3 --audio-quality 0 \
  -o "<output_dir>/%(title)s.%(ext)s" \
  "<URL>"
```

### Lightest available
```bash
yt-dlp -f "worstvideo+worstaudio/worst" \
  -o "<output_dir>/%(title)s.%(ext)s" \
  "<URL>"
```

### Full playlist
```bash
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" \
  --merge-output-format mp4 \
  --yes-playlist \
  -o "<output_dir>/%(playlist_index)s - %(title)s.%(ext)s" \
  "<URL>"
```

### Download subtitles along with video
```bash
yt-dlp --write-subs --sub-langs "es,en" \
  -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" \
  --merge-output-format mp4 \
  -o "<output_dir>/%(title)s.%(ext)s" \
  "<URL>"
```

## Useful Extra Flags

| Flag | Effect |
|---|---|
| `--cookies-from-browser chrome` | Use Chrome cookies (for age-restricted or member videos) |
| `--rate-limit 2M` | Limit download speed to 2 MB/s |
| `--no-playlist` | Download only the single video even if part of a playlist |
| `--download-archive archive.txt` | Skip already-downloaded videos |
| `--embed-thumbnail` | Embed thumbnail in audio file |
| `--add-metadata` | Add title/artist metadata to audio |

## Error Handling

| Error | Solution |
|---|---|
| `ERROR: Video unavailable` | Video is private or deleted |
| `ERROR: Sign in to confirm your age` | Add `--cookies-from-browser chrome` |
| `HTTP Error 429` | Rate limited — wait a few minutes or add `--rate-limit 1M` |
| `ffmpeg not found` | Install ffmpeg: `brew install ffmpeg` |
| `Requested format not available` | Run `yt-dlp --list-formats <URL>` and pick an available format code |

## After Download

Confirm success by showing:
- File name and location
- File size
- Duration (if available)

```bash
ls -lh "<output_dir>/<filename>"
```

## Anti-Patterns

- Don't run the command without confirming it with the user first.
- Don't skip the prerequisites check — silent failures from missing ffmpeg are confusing.
- Don't download playlists without warning the user about size/time implications.
- This skill is for personal/authorized use only. Don't use to bypass DRM or download copyrighted content you don't have rights to.
