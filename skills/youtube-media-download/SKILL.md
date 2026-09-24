---
name: youtube-media-download
description: Download YouTube video or audio to a local file with yt-dlp, including format and size choices, proxy or cookie access, and final media verification. Use for requests to save YouTube media; use youtube-captions for caption-only requests.
---

# YouTube media download

Download the requested media with the installed `yt-dlp`. Keep this workflow limited to video and audio; use `youtube-captions` when the request is only for existing subtitles.

## Establish the request

- Resolve the URL, durable output directory, full video versus a time range, video versus audio only, and any size or codec limit. A URL `t=` parameter changes the playback start; it does not itself trim the downloaded file. For a requested time range, check the current `--download-sections` syntax in `yt-dlp --help`; it needs FFmpeg.
- Use `--no-playlist` unless the user explicitly requests a playlist. Quote URLs and paths. Avoid overwriting an existing file; verify it or choose a distinct name.
- When options have material differences in size, quality, codec support, duration, or credential use, present short, scannable tradeoffs and wait for the user's choice. Continue directly when the request determines one suitable option.

## Probe the live path

- Check `command -v yt-dlp ffmpeg ffprobe` and the current versions. On this Fedora workstation, use the tool inventory at `/home/nova/a1/FEDORA44_WORKSTATION_TOOL_INVENTORY.md` to locate installed commands; verify them live. Invoke normal `yt-dlp` so its user configuration and Deno/EJS support remain available.
- YouTube access on this workstation needs the local SOCKS listener. Verify `127.0.0.1:10808` is listening, then pass `--proxy 'socks5h://127.0.0.1:10808'` explicitly to `yt-dlp`. Do not infer that inherited proxy variables are absent or present without checking. Do not start Xray or change proxy configuration as a side effect.
- Probe metadata and formats without downloading. `yt-dlp --dump-single-json --skip-download --no-playlist ... "$URL"` supplies format IDs, codecs, dimensions, `filesize`, and `filesize_approx`. Its raw JSON can contain signed media URLs: parse it in memory or in a mode-0600 temporary file and print only the fields needed for a choice. Do not paste raw JSON into the transcript.

## Handle access failures

- If YouTube returns `Sign in to confirm you’re not a bot`, do not keep repeating the same anonymous probe. The challenge can occur even through a working proxy. Ask before reading browser-session cookies or using credentials unless the user already authorized it.
- A supplied Netscape cookie file is sensitive session data. Check its format and permissions without printing cookie values. Use a mode-0600 temporary copy with `--cookies` because `yt-dlp` may write back to that path; remove the copy on exit. Reduce exposed permissions on a user-owned source file when appropriate. Never log, commit, or retain cookie values or signed media URLs.
- On this Fedora setup, `--cookies-from-browser chrome` may fail to decrypt GNOME-keyring cookies when Python lacks `secretstorage`. Diagnose the actual error before changing dependencies. Follow the user's project-local Python environment policy or use a user-supplied Netscape cookie file; do not install packages into system Python with pip.

## Select and download

- Read formats for this video; format IDs and sizes vary by video. For audio-only, prefer a directly available audio stream that meets the requested cap. A WebM file may contain only Opus audio: do not transcode solely because its extension is `.webm`.
- For a size cap, prefer an exact `filesize`; treat `filesize_approx` as an estimate. For separate video and audio streams, add both sizes. If no direct format fits, explain the size-versus-quality cost of transcoding or shortening and wait for a choice. Do not silently lower quality or truncate content.
- Download the selected format with `-f "$FORMAT_ID"`, the chosen output path, `--no-playlist`, and the verified proxy/cookie options. Do not use `--ignore-config` or add redundant JavaScript-runtime flags. Keep the original cookie file unchanged by using the temporary copy.

## Verify and report

- Confirm the command completed, the file exists, and no `.part` file remains. Compare actual byte size against any cap using the unit the user specified; when unspecified, make clear whether MB means 1,000,000 bytes or MiB means 1,048,576 bytes.
- Use `ffprobe` to check duration and streams. For audio-only requests, confirm there is no video stream. Report the final path, container/codec, duration, actual size, and any unmet constraint. Do not claim the full media decoded successfully unless that was tested.
