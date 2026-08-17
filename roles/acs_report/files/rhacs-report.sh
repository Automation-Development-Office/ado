#!/usr/bin/env bash
set -euo pipefail

ROX_ENDPOINT="${ROX_ENDPOINT:-}"
ROX_API_TOKEN="${ROX_API_TOKEN:-}"
ROX_API_USER="${ROX_API_USER:-admin}"
ROX_API_PASSWORD="${ROX_API_PASSWORD:-}"

MODE=""
COMPONENT=""
ALL_SCOPE=0
RHSRE=0
SHOW_SEV=0
CLUSTERS="${RHACS_CLUSTERS:-}"
OUTDIR="${RHACS_REPORT_DIR:-$PWD}"

usage() {
cat <<'HELP'

RHACS reporting

Usage:

  ./rhacs-report.sh --raw
      Current deployed workloads
      Critical + Important
      ALL vulnerability sources
      Slack-friendly component table

  ./rhacs-report.sh --rhsource
      Current deployed workloads
      Critical + Important
      SOURCE_RED_HAT only
      Slack-friendly component table

  ./rhacs-report.sh --age
      Current deployed workloads
      Critical + Important
      SOURCE_RED_HAT only
      Slack-friendly >15 / >30 / >90 day table

  ./rhacs-report.sh --all
      Generates a full scrubbed CSV
      Includes all severities and all vulnerability sources
      Includes both live and inactive ACS workload records

Composable scope options:

  --all
      With --raw or --rhsource: include ALL product/component groups.
      By itself: preserve existing scrubbed CSV behavior.

  --rhsre
      Limit to core ROSA/OpenShift components considered part of
      the Red Hat/SRE managed-service responsibility boundary.

  --clusters prod,prod-infra
      Limit table modes to these ACS cluster names.
      Default / empty: include all clusters.
      Also accepts env RHACS_CLUSTERS.

Optional:

  --component acm|devspaces|cert-manager|web-terminal|gitops|compliance|kube-descheduler|cluster-logging|rhacs
  --sev

Auth (env):

  ROX_ENDPOINT     ACS Central base URL (required)
  ROX_API_TOKEN    Bearer token (preferred)
  ROX_API_USER     Basic-auth user when token unset (default admin)
  ROX_API_PASSWORD Basic-auth password when token unset
  RHACS_REPORT_DIR Output directory (default: cwd)

HELP
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --raw) MODE="raw"; shift ;;
        --rhsource) MODE="rhsource"; shift ;;
        --age) MODE="age"; shift ;;
        --all) ALL_SCOPE=1; shift ;;
        --rhsre) RHSRE=1; shift ;;
        --sev) SHOW_SEV=1; shift ;;
        --component) COMPONENT="${2:-}"; shift 2 ;;
        --clusters) CLUSTERS="${2:-}"; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) echo "Unknown option: $1"; usage; exit 1 ;;
    esac
done

if [[ -z "$MODE" && "$ALL_SCOPE" -eq 1 ]]; then
    MODE="all"
    ALL_SCOPE=0
fi

if [[ -z "$MODE" ]]; then
    usage
    exit 1
fi

if [[ -z "$ROX_ENDPOINT" ]]; then
  echo "Set ROX_ENDPOINT" >&2
  exit 1
fi
ROX_ENDPOINT="${ROX_ENDPOINT%/}"

if [[ -z "$ROX_API_TOKEN" && -z "$ROX_API_PASSWORD" ]]; then
  echo "Set ROX_API_TOKEN or ROX_API_PASSWORD" >&2
  exit 1
fi

mkdir -p "$OUTDIR"

PARSER="$(cd "$(dirname "$0")" && pwd)/rhacs_report_parser.py"
if [[ ! -f "$PARSER" ]]; then
  echo "Parser not found next to script: $PARSER" >&2
  exit 1
fi

echo
echo "============================================================"
echo " RHACS REPORT"
echo "============================================================"
echo "Mode:    $MODE"
echo "Central: $ROX_ENDPOINT"
if [[ -n "$COMPONENT" ]]; then
    echo "Component: $COMPONENT"
fi
if [[ -n "$CLUSTERS" ]]; then
    echo "Clusters: $CLUSTERS"
else
    echo "Clusters: ALL"
fi
echo
echo "Streaming RHACS workload data..."
echo

AUTH_ARGS=()
if [[ -n "$ROX_API_TOKEN" ]]; then
  AUTH_ARGS=(-H "Authorization: Bearer ${ROX_API_TOKEN}")
else
  AUTH_ARGS=(-u "${ROX_API_USER}:${ROX_API_PASSWORD}")
fi

curl -sk --fail \
  --connect-timeout 15 \
  --max-time 1200 \
  --no-buffer \
  "${AUTH_ARGS[@]}" \
  -H "Accept: application/json" \
  "${ROX_ENDPOINT}/v1/export/vuln-mgmt/workloads?timeout=900" \
| python3 "$PARSER" "$MODE" "$COMPONENT" "$OUTDIR" "$ALL_SCOPE" "$RHSRE" "$SHOW_SEV" "$CLUSTERS"
