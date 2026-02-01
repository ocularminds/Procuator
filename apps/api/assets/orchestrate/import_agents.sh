#!/usr/bin/env bash
set -euo pipefail

# Imports Procuator agents into watsonx Orchestrate in the correct order.
# Usage:
#   ./apps/api/assets/orchestrate/import_agents.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
ORCH_DIR="$ROOT_DIR/apps/api/assets/orchestrate"

if ! command -v orchestrate >/dev/null 2>&1; then
  echo "Error: 'orchestrate' CLI not found on PATH." >&2
  echo "Install / configure watsonx Orchestrate ADK CLI, then retry." >&2
  exit 1
fi

import_agent() {
  local file="$1"
  echo "Importing: $file"
  orchestrate agents import -f "$file"
}

import_tool() {
  local file="$1"
  echo "Importing tool: $file"
  orchestrate tools import -k python -f "$file" -r "$ORCH_DIR/tools/requirements.txt"
}

# Import tools first so agents can reference them.
import_tool "$ORCH_DIR/tools/python/health.py"
import_tool "$ORCH_DIR/tools/python/demo_scenarios.py"
import_tool "$ORCH_DIR/tools/python/supplier_risk_checker.py"
import_tool "$ORCH_DIR/tools/python/policy_check.py"
import_tool "$ORCH_DIR/tools/python/procurement_decision.py"
import_tool "$ORCH_DIR/tools/python/list_referrals.py"
import_tool "$ORCH_DIR/tools/python/approve_referral.py"
import_tool "$ORCH_DIR/tools/python/deny_referral.py"
import_tool "$ORCH_DIR/tools/python/decision_analytics.py"

# Import collaborators first, then the orchestrator that references them.
import_agent "$ORCH_DIR/agents/perception_agent.yml"
import_agent "$ORCH_DIR/agents/analysis_agent.yml"
import_agent "$ORCH_DIR/agents/policy_agent.yml"
import_agent "$ORCH_DIR/agents/decision_agent.yml"
import_agent "$ORCH_DIR/agents/action_agent.yml"

import_agent "$ORCH_DIR/procuator_orchestrator.yml"

# Optional: single-agent spec (if you want a monolithic agent too)
import_agent "$ORCH_DIR/procuator_agent_spec.yml"

echo "Done."
