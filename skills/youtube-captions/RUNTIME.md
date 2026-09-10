# Runtime provisioning

This file documents the runtime used by `youtube-captions`. Keep caption
selection and download behavior in `SKILL.md`; use this file to install,
verify, rebuild, or upgrade the supporting commands and configuration.

## Runtime components

| Component | Upstream | Nova state | Purpose |
|---|---|---|---|
| yt-dlp | `https://github.com/yt-dlp/yt-dlp` | Fedora `yt-dlp` and `yt-dlp+default` `2026.08.19-1.fc44`; `/usr/bin/yt-dlp` | Lists and downloads existing subtitle tracks without media |
| Deno | `https://github.com/denoland/deno` | Official standalone 2.9.6; `~/.local/opt/fedora44-tools/deno/2.9.6/deno` | Default JavaScript runtime used by yt-dlp for YouTube EJS challenges |
| ffmpeg | `https://ffmpeg.org/` | RPM Fusion Free `ffmpeg` 8.1.2; `/usr/bin/ffmpeg` and `/usr/bin/ffprobe` | Converts native subtitle formats such as VTT to SRT |

Nova's `/usr/bin/yt-dlp` is a small Python launcher for the RPM-owned package
under `/usr/lib/python3.14/site-packages/yt_dlp/`. It is not a user-local
standalone executable. Deno is user-local and not RPM-owned. ffmpeg is a
system RPM. Node is installed on nova, but yt-dlp does not enable it; Deno is
the only effective JavaScript runtime.

## Version policy

YouTube changes frequently. Use a maintained yt-dlp release new enough to
support its current external JavaScript solver mechanism; prefer the current
Fedora package when it is current, otherwise use a pinned official release
asset. Do not install into system Python with pip. Record the installed
version, package or asset source, path, and checksum.

Use a supported Deno release recognized by that yt-dlp version. Pin an exact
official release asset for standalone installations and retain its published
checksum. Use the distribution's supported full ffmpeg package. ffmpeg need
not match nova byte-for-byte; it must provide both `ffmpeg` and `ffprobe` and
successfully convert subtitles.

## Provision on Fedora

Install yt-dlp through Fedora when the repository version is suitable:

```bash
sudo dnf install yt-dlp yt-dlp+default
```

Nova uses the official Deno 2.9.6 Linux x86-64 archive. Its release archive
SHA-256 is
`394f07f4da2bebe6ce6f1e7ce0fa16429b29b08c35e3fac3fe25972676dff4b2`;
the extracted nova binary SHA-256 is
`bceb5b6a6239b0b010418406d8c77a508f67cf4337d94288f1c19fe71304aab0`.
Provision that layout with `curl`, `sha256sum`, and `unzip`:

```bash
curl --fail --location --output /tmp/deno-x86_64-unknown-linux-gnu.zip \
  https://github.com/denoland/deno/releases/download/v2.9.6/deno-x86_64-unknown-linux-gnu.zip
printf '%s  %s\n' \
  394f07f4da2bebe6ce6f1e7ce0fa16429b29b08c35e3fac3fe25972676dff4b2 \
  /tmp/deno-x86_64-unknown-linux-gnu.zip | sha256sum --check
unzip -p /tmp/deno-x86_64-unknown-linux-gnu.zip deno > /tmp/deno
chmod 0755 /tmp/deno
install -d "$HOME/.local/opt/fedora44-tools/deno/2.9.6" "$HOME/.local/bin"
install -m 0755 /tmp/deno \
  "$HOME/.local/opt/fedora44-tools/deno/2.9.6/deno"
ln -s "$HOME/.local/opt/fedora44-tools/deno/2.9.6/deno" \
  "$HOME/.local/bin/deno"
```

Inspect existing paths before creating or replacing files or symlinks. Adapt
`fedora44-tools` to the host's established versioned-root convention. Ensure
`~/.local/bin` is already on `PATH`; do not change shell profiles blindly.

Nova uses the full RPM Fusion Free ffmpeg stack rather than Fedora's
`ffmpeg-free` subset:

```bash
sudo dnf install ffmpeg
```

That command assumes the RPM Fusion Free repositories are already configured.
Do not add repositories or replace an existing codec stack without first
inspecting the host's package state and conflicts.

## yt-dlp configuration and EJS behavior

Create the normal per-user configuration file:

```text
~/.config/yt-dlp/config
```

Its complete required content is:

```text
--remote-components ejs:npm
```

On nova the file is `/home/nova/.config/yt-dlp/config`, mode `0644`, with
SHA-256
`de0fea8ce5f7bf43ef093bd9778533d8ca3e118bf128361c122101837ffa90b8`.

This setting permits yt-dlp to fetch external JavaScript solver components
from the `yt-dlp-ejs` npm distribution when a YouTube request requires them.
It does not install an `ejs` command or a global npm package, and it does not
mean EJS code is permanently cached. It adds a remote code-fetch permission;
the npm endpoint and GitHub-backed yt-dlp trust chain must therefore be
acceptable for the host.

Invoke normal `yt-dlp` so this file is loaded. Do not use `--ignore-config`,
`--no-remote-components`, or an alternate config path in the skill workflow.
When `deno` is on `PATH`, yt-dlp enables it by default. Do not add a redundant
`--js-runtimes` setting or enable Node merely because Node is installed.

## Expected commands

Availability inspection:

```bash
yt-dlp --list-subs --no-playlist "$URL"
```

Manual-caption download:

```bash
yt-dlp --no-playlist --skip-download --no-overwrites \
  --write-subs --sub-langs "$LANG" \
  --sub-format 'srt/vtt/best' --convert-subs srt \
  -o "$OUTDIR/%(title)s.%(ext)s" "$URL"
```

Use `--write-auto-subs` instead of `--write-subs` only for the deliberate
native automatic-caption fallback. `--skip-download` is mandatory. ffmpeg is
used only when conversion is needed; preserve a valid native subtitle file if
conversion is unavailable rather than downloading media.

## Verify

```bash
type -a yt-dlp deno ffmpeg ffprobe
yt-dlp --version
deno --version
ffmpeg -version
yt-dlp --verbose --list-subs --no-playlist "$URL"
```

The verbose output must show the intended user config and a line equivalent
to `JS runtimes: deno-<version>`. It must not report `JS runtimes: none`.
Confirm that manual and automatic captions are listed separately. Then perform
one manual or native-auto caption-only download using `--skip-download` and
verify a nonempty subtitle file containing timed cues. If SRT conversion was
requested, verify the resulting `.srt`; otherwise retain and report the native
format.

## Upgrade and rollback

Upgrade one runtime component at a time. For yt-dlp, review upstream release
notes for YouTube/EJS and configuration changes, install a pinned candidate,
and repeat availability plus caption-only tests. For Deno, install the new
official asset into a new versioned root, verify its checksum and yt-dlp
detection, then switch the `~/.local/bin/deno` symlink. Update ffmpeg through
the existing package source and test subtitle conversion.

Retain the prior standalone Deno root until verification succeeds. Do not
carry obsolete yt-dlp flags forward when upstream removes or changes them.
After any accepted change, update this file and the workstation inventory with
the versions, paths, package or asset sources, checksums, effective config,
and verification result.
