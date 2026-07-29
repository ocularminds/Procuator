from __future__ import annotations

from typing import Any


class DashboardRenderer:
    """Renders decision analytics as the legacy standalone HTML dashboard."""

    rowTemplate = "<tr><td>{flag}</td><td style='text-align:right'>{count}</td></tr>"

    def render(self, stats: dict[str, Any]) -> str:
        flagRows = "\n".join(
            self.rowTemplate.format(flag=item["flag"], count=item["count"]) for item in stats.get("top_flags", [])
        )
        counts = stats.get("counts_by_decision", {})
        countRows = "\n".join(
            f"<tr><td>{key}</td><td style='text-align:right'>{value}</td></tr>" for key, value in sorted(counts.items())
        )

        return f"""<!doctype html>
<html lang='en'>
<head>
  <meta charset='utf-8' />
  <meta name='viewport' content='width=device-width, initial-scale=1' />
  <title>Procuator Dashboard</title>
  <style>
    body {{ font-family: -apple-system, system-ui, Segoe UI, Roboto, Arial, sans-serif; margin: 24px; }}
    .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
    .card {{ border: 1px solid #ddd; border-radius: 10px; padding: 16px; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ border-bottom: 1px solid #eee; padding: 8px; }}
    th {{ text-align: left; }}
    code {{ background: #f6f6f6; padding: 2px 6px; border-radius: 6px; }}
  </style>
</head>
<body>
  <h1>Procuator Decision Analytics</h1>
  <p>Total audited decisions: <b>{stats.get("total", 0)}</b></p>
  <p>Average risk score: <b>{stats.get("avg_risk_score")}</b></p>

  <div class='grid'>
    <div class='card'>
      <h2>Counts by Decision</h2>
      <table>
        <thead><tr><th>Decision</th><th style='text-align:right'>Count</th></tr></thead>
        <tbody>
          {countRows or "<tr><td colspan='2'>No data yet</td></tr>"}
        </tbody>
      </table>
    </div>
    <div class='card'>
      <h2>Top Flags</h2>
      <table>
        <thead><tr><th>Flag</th><th style='text-align:right'>Count</th></tr></thead>
        <tbody>
          {flagRows or "<tr><td colspan='2'>No flags yet</td></tr>"}
        </tbody>
      </table>
    </div>
  </div>

  <p style='margin-top: 16px'>Tip: call <code>POST /decision</code> to generate events.</p>
</body>
</html>"""
