#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "usage: scripts/new-adr.sh \"Decision title\"" >&2
  exit 2
fi

title="$*"
slug="$(printf '%s' "$title" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-|-$//g')"
adr_dir="docs/adr"
mkdir -p "$adr_dir"

last_number="$(find "$adr_dir" -maxdepth 1 -type f -name '[0-9][0-9][0-9][0-9]-*.md' -print \
  | sed -E 's#.*/([0-9]{4})-.*#\1#' \
  | sort -n \
  | tail -1)"

if [ -z "$last_number" ]; then
  next_number="0001"
else
  next_number="$(printf '%04d' "$((10#$last_number + 1))")"
fi

target="$adr_dir/${next_number}-${slug}.md"
today="$(date +%F)"

cat > "$target" <<EOF
# ADR ${next_number}: ${title}

Date: ${today}
Status: proposed

## Context


## Decision


## Consequences


## ML Impact

- Target:
- Metric:
- Split:
- Features:
- Model family:
- Serving/monitoring:

## Alternatives Considered

- 

## Verification


EOF

echo "$target"
