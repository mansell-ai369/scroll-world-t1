#!/usr/bin/env bash
# Block accidental destructive deletes of demo scroll-world assets.
set -euo pipefail
input=$(cat)
command=$(printf '%s' "$input" | jq -r '.command // empty')

if [[ "$command" =~ rm[[:space:]]+.*assets ]]; then
  if [[ "$command" =~ (^|[[:space:]])(-rf|-fr|-r[[:space:]].*-f|-f[[:space:]].*-r|--force) ]]; then
    cat <<'EOF'
{
  "permission": "deny",
  "user_message": "Blocked: refusing to force-delete demo assets. Remove files selectively if needed.",
  "agent_message": "Hook blocked a destructive rm against assets/. Use targeted deletes instead of rm -rf."
}
EOF
    exit 0
  fi
fi

echo '{ "permission": "allow" }'
exit 0
