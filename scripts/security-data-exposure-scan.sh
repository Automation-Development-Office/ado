#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"

# Scoring
score=100
PENALTY_ORG_STRING=30
PENALTY_PUBLIC_IP=25
PENALTY_PRIVATE_IP=1
PENALTY_INTERNAL_FQDN=3

echo "== Data exposure scan (org strings, IPs, hostnames, domains) =="
echo "Root: $ROOT"
echo

ORG_RE='(FBI|Federal Bureau of Investigation|Federal Bureau of Investigations)'

# IPv4 (simple)
IPV4_RE='([0-9]{1,3}\.){3}[0-9]{1,3}'

# FQDN-ish
FQDN_RE='([a-zA-Z0-9-]+\.)+(lab|local|internal|corp|com|gov|net|org)'

org_hits=0
private_ip_hits=0
public_ip_hits=0
fqdn_hits=0

echo "[1/3] Organization terms..."
org_out="$(grep -RInE --binary-files=without-match --exclude-dir=.git -E "$ORG_RE" "$ROOT" || true)"
if [[ -n "$org_out" ]]; then
  echo "$org_out"
  org_hits="$(echo "$org_out" | wc -l | tr -d ' ')"
  score=$((score - org_hits * PENALTY_ORG_STRING))
  echo
  echo "  Suggestion: remove/replace org-specific strings with neutral placeholders (e.g., <agency>, <org>)."
else
  echo "  (none found)"
fi
echo

echo "[2/3] IPv4 addresses..."
ip_out="$(grep -RInE --binary-files=without-match --exclude-dir=.git -E "$IPV4_RE" "$ROOT" || true)"
if [[ -n "$ip_out" ]]; then
  echo "$ip_out"
  # classify private vs public quickly (heuristic)
  while IFS= read -r line; do
    ip="$(echo "$line" | grep -oE "$IPV4_RE" | head -n 1 || true)"
    [[ -z "$ip" ]] && continue
    if [[ "$ip" =~ ^10\. ]] || [[ "$ip" =~ ^192\.168\. ]] || [[ "$ip" =~ ^172\.(1[6-9]|2[0-9]|3[0-1])\. ]] || [[ "$ip" =~ ^127\. ]]; then
      private_ip_hits=$((private_ip_hits+1))
    else
      public_ip_hits=$((public_ip_hits+1))
    fi
  done <<< "$ip_out"

  score=$((score - private_ip_hits * PENALTY_PRIVATE_IP))
  score=$((score - public_ip_hits * PENALTY_PUBLIC_IP))

  echo
  echo "  Suggestion:"
  echo "    - Private IPs in docs/examples are usually OK."
  echo "    - Public/routable IPs should be removed or moved to env vault/vars."
else
  echo "  (none found)"
fi
echo

echo "[3/3] FQDN/hostname patterns..."
fqdn_out="$(grep -RInE --binary-files=without-match --exclude-dir=.git -E "$FQDN_RE" "$ROOT" || true)"
if [[ -n "$fqdn_out" ]]; then
  echo "$fqdn_out"
  fqdn_hits="$(echo "$fqdn_out" | wc -l | tr -d ' ')"
  score=$((score - fqdn_hits * PENALTY_INTERNAL_FQDN))
  echo
  echo "  Suggestion:"
  echo "    - If hostnames are in README/molecule docs: OK (consider placeholders)."
  echo "    - If hostnames are hard-coded in tasks/defaults: move to env vars/vault (domain/app_domain/app_domain_alt)."
else
  echo "  (none found)"
fi
echo

# clamp
if [[ "$score" -lt 0 ]]; then score=0; fi

echo "== Summary =="
echo "Org hits: $org_hits"
echo "Private IP hits: $private_ip_hits"
echo "Public IP hits: $public_ip_hits"
echo "FQDN hits: $fqdn_hits"
echo "Score: ${score}/100"

if [[ "$org_hits" -gt 0 ]] || [[ "$public_ip_hits" -gt 0 ]]; then
  echo "Result: ❌ FAIL (org strings or public IPs found)"
  exit 1
fi

if [[ "$score" -ge 98 ]]; then
  echo "Result: ✅ PASS"
  exit 0
else
  echo "Result: ⚠️  WARN (score < 98, review suggestions)"
  exit 0
fi
