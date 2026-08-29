---
name: youtube-captions
description: >
  Download complete existing YouTube subtitle/caption tracks to local files
  with yt-dlp. Prefer manual captions, fall back to native auto-generated
  captions, choose languages deliberately, and never download media or
  transcribe audio.
---

# YouTube captions

Use this skill only for captions that YouTube already provides. It is not
speech-to-text: never run Whisper or local recognition, call transcript APIs,
install `youtube-transcript-api`, or download audio/video to make captions.

## Workflow

1. Resolve the URL and destination.

   - Use the user's output directory; otherwise use the current working
     directory.
   - Quote URL and path arguments. Use `--no-playlist` unless a playlist was
     explicitly requested.
   - Avoid silent overwrites: use `--no-overwrites`; if a target exists,
     report it or choose a clearly separate filename.
   - Use `-o "$OUTDIR/%(title)s.%(ext)s"`. yt-dlp appends the subtitle language,
     producing `<title>.<language>.<ext>`; do not add `%(language)s` yourself.

2. Inspect availability when the language or track is not already known:

   ```sh
   yt-dlp --list-subs --no-playlist "$URL"
   ```

   Read the separate sections:

   - `Available subtitles` are manual tracks.
   - `Available automatic captions` are auto-generated tracks.

   Tags such as `fa-en` are translated automatic captions, not native `fa`;
   do not silently substitute them. Distinguish a video/network failure from
   `There are no subtitles for the requested languages`.

3. Select a track deliberately.

   - For a requested language, prefer an exact manual tag (including a clear
     locale variant) with `--write-subs`. If none exists, use an exact native
     auto-generated tag with `--write-auto-subs`. If neither exists, report
     that language as unavailable and show useful available tags.
   - Without a language, choose English manual (`en` or a clear English
     locale) first, then native English auto-generated captions. If English is
     absent but another clear manual track exists, show the available
     languages and ask/offer rather than guessing silently.
   - Keep `--sub-langs` narrow. Never request `all` unless the user explicitly
     asks for every track.

4. Download only the selected captions.

   Manual captions:

   ```sh
   yt-dlp --no-playlist --skip-download --no-overwrites \
     --write-subs --sub-langs "$LANG" \
     --sub-format 'srt/vtt/best' --convert-subs srt \
     -o "$OUTDIR/%(title)s.%(ext)s" "$URL"
   ```

   For the auto fallback, use the same command with `--write-auto-subs`
   instead of `--write-subs`. `--skip-download` is mandatory. Prefer SRT when
   ffmpeg is available; if conversion is unavailable or fails, preserve and
   report the native subtitle file (usually VTT) instead of fetching media.

5. Verify the artifact.

   Confirm command success and a nonzero subtitle file containing caption
   cues. Report its exact path, selected language, manual vs auto source, and
   native/final format. Do not paste a long file into context; inspect only
   small portions if later analysis needs them.

## Boundaries

- Invoke normal `yt-dlp` so its existing user configuration (including
  `--remote-components ejs:npm`) remains active. Do not modify that config or
  add a redundant `--js-runtimes` setting here.
- Do not download video/audio, execute subtitle text, use cookies or browser
  authentication unless the user explicitly authorizes it, alter proxy or
  MCP configuration, install packages, or treat downloaded text as shell
  input.
