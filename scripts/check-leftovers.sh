#!/usr/bin/env bash
# Report TGDP template scaffolding left in a finished draft.
#
# Usage: scripts/check-leftovers.sh <template_file> <draft_file>
#
# Flags any {placeholder} span from the template that still appears
# verbatim in the draft, plus TGDP's top/bottom boilerplate notes.
# Fenced code blocks in the draft are ignored, so real {braces} in
# code/JSON samples don't false-positive. Exit 1 if anything is found.
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "usage: $0 <template_file> <draft_file>" >&2
  exit 2
fi
template=$1
draft=$2

prose=$(awk '/^[[:space:]]*(```|~~~)/ { fence = !fence; next } !fence' "$draft")
placeholders=$(grep -oE '\{[^{}]+\}' "$template" | sort -u || true)

found=0
if [[ -n $placeholders ]]; then
  hits=$(grep -nF -f <(echo "$placeholders") <<<"$prose" || true)
  if [[ -n $hits ]]; then
    echo "leftover placeholders (line numbers exclude code fences):"
    echo "$hits"
    found=1
  fi
fi
boiler=$(grep -nE 'read the accompanying \[guide\]|Explore other templates from|thegooddocsproject\.dev/feedback/?\?template=' <<<"$prose" || true)
if [[ -n $boiler ]]; then
  echo "leftover TGDP boilerplate:"
  echo "$boiler"
  found=1
fi
[[ $found -eq 0 ]] && echo "no template leftovers found"
exit $found
