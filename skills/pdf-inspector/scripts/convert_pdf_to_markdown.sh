#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
  printf 'Usage: %s INPUT.pdf OUTPUT.md\n' "${0##*/}" >&2
}

if (( $# != 2 )); then
  usage
  exit 64
fi

input=$1
output=$2

for command_name in detect-pdf pdf2md jq readlink dirname mktemp mv rm grep; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    printf 'Error: required command not found: %s\n' "$command_name" >&2
    exit 127
  fi
done

if [[ ! -f "$input" || ! -r "$input" ]]; then
  printf 'Error: input is not a readable regular file: %s\n' "$input" >&2
  exit 66
fi

input_real=$(readlink -f -- "$input")
output_abs=$(readlink -m -- "$output")
output_dir=$(dirname -- "$output_abs")

if [[ ! -d "$output_dir" || ! -w "$output_dir" ]]; then
  printf 'Error: output directory is not writable: %s\n' "$output_dir" >&2
  exit 73
fi

if [[ "$input_real" == "$output_abs" ]]; then
  printf 'Error: refusing to overwrite the source PDF: %s\n' "$input" >&2
  exit 73
fi

metadata_tmp=
markdown_tmp=
cleanup() {
  if [[ -n "$metadata_tmp" && -e "$metadata_tmp" ]]; then
    rm -f -- "$metadata_tmp"
  fi
  if [[ -n "$markdown_tmp" && -e "$markdown_tmp" ]]; then
    rm -f -- "$markdown_tmp"
  fi
}
trap cleanup EXIT

metadata_tmp=$(mktemp "$output_dir/.pdf-inspector.detect.XXXXXX.json")
markdown_tmp=$(mktemp "$output_dir/.pdf-inspector.markdown.XXXXXX")

if detect-pdf "$input" --json >"$metadata_tmp"; then
  :
else
  status=$?
  printf 'Error: detect-pdf failed for %s\n' "$input" >&2
  exit "$status"
fi

if ! jq -e 'type == "object" and (.pdf_type | type == "string")' \
    "$metadata_tmp" >/dev/null; then
  printf 'Error: detect-pdf returned unexpected JSON for %s\n' "$input" >&2
  exit 65
fi

pdf_type=$(jq -r '.pdf_type' "$metadata_tmp")
printf 'pdf_type=%s\n' "$pdf_type" >&2

if [[ "$pdf_type" == scanned || "$pdf_type" == image_based ]]; then
  pages_needing_ocr=$(jq -r '(.pages_needing_ocr // []) | join(",")' "$metadata_tmp")
  if [[ -n "$pages_needing_ocr" ]]; then
    printf 'OCR required; pages_needing_ocr=%s\n' "$pages_needing_ocr" >&2
  else
    printf 'OCR required for scanned/image-only input\n' >&2
  fi
  exit 2
fi

if [[ "$pdf_type" == mixed ]]; then
  pages_needing_ocr=$(jq -r '(.pages_needing_ocr // []) | join(",")' "$metadata_tmp")
  if [[ -n "$pages_needing_ocr" ]]; then
    printf 'Error: mixed PDF has pages_needing_ocr=%s; refusing to publish %s\n' \
      "$pages_needing_ocr" "$output" >&2
    printf 'Review the pages, OCR them separately if needed, or use direct pdf2md for an intentional partial inspection.\n' >&2
    exit 2
  fi
fi

if pdf2md "$input" --raw >"$markdown_tmp"; then
  :
else
  status=$?
  printf 'Error: pdf2md failed for %s\n' "$input" >&2
  exit "$status"
fi

if [[ ! -s "$markdown_tmp" ]] || ! grep -q '[^[:space:]]' "$markdown_tmp"; then
  printf 'Error: pdf2md produced empty Markdown; refusing to publish %s\n' "$output" >&2
  exit 65
fi

mv -f -- "$markdown_tmp" "$output_abs"
markdown_tmp=
printf 'Wrote mechanically validated Markdown: %s\n' "$output_abs" >&2
