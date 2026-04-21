#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="/var/www/apps-portal"
OUT_FILE="$OUT_DIR/index.html"

declare -A REPO=(
  ["leasing-model"]="/root/.openclaw/workspace-tag_coding/Leasing_Model"
  ["mission-analysis"]="/root/.openclaw/workspace-volo_coding/Tamarack_Mission_Analysis"
  ["aglaze"]="/root/.openclaw/workspace-volo_coding/AltiDroidNRG"
  ["jet-sales-crm"]="/root/jet-sales-crm"
  ["tamarack-project-financials"]="/docker/openclaw-wiub/data/.openclaw/workspace/Tamarack_525_Financials"
  ["groundhog"]="/root/.openclaw/workspace-volo_coding/GroundHog"
  ["lru-tracker"]="/docker/openclaw-wiub/data/.openclaw/workspace/LRU_tracker"
  ["dataroom"]="/root/.openclaw/workspace-volo_coding/DataRoom"
  ["aircraft-revenue"]="/root/.openclaw/workspace-tag_coding/Aircraft_Specific_Revenue_Roadmap"
  ["sales-training"]="/root/.openclaw/workspace-tag_coding/Sales"
  ["ash"]="/var/www/ash"
  ["shy"]="/var/www/shy"
  ["tels"]="/root/.openclaw/workspace-tag_coding/TELS"
  ["turnback"]="/root/.openclaw/workspace-tag_coding/Turnback-Simulator"
  ["spoton"]="/var/www/spoton"
  ["cfm"]="/root/.openclaw/workspace-tag_coding/CFM"
  ["lewice"]="/root/.openclaw/workspace-tag_coding/LEWICE"
)

date_for() {
  local path="$1"
  if [[ -d "$path/.git" ]]; then
    git -C "$path" log -1 --date=format:'%Y-%m-%d %H:%M UTC' --format='%cd' 2>/dev/null || echo "unknown"
  elif [[ -d "$path" ]]; then
    find "$path" -type f -printf '%TY-%Tm-%Td %TH:%TM UTC\n' 2>/dev/null | sort -r | head -n 1 || echo "unknown"
  else
    echo "unknown"
  fi
}

LM="$(date_for "${REPO[leasing-model]}")"
MA="$(date_for "${REPO[mission-analysis]}")"
AG="$(date_for "${REPO[aglaze]}")"
JS="$(date_for "${REPO[jet-sales-crm]}")"
TPF="$(date_for "${REPO[tamarack-project-financials]}")"
GH="$(date_for "${REPO[groundhog]}")"
LRU="$(date_for "${REPO[lru-tracker]}")"
DR="$(date_for "${REPO[dataroom]}")"
AR="$(date_for "${REPO[aircraft-revenue]}")"
ST="$(date_for "${REPO[sales-training]}")"
ASH="$(date_for "${REPO[ash]}")"
SHY="$(date_for "${REPO[shy]}")"
TELS="$(date_for "${REPO[tels]}")"
TB="$(date_for "${REPO[turnback]}")"
SP="$(date_for "${REPO[spoton]}")"
CFM="$(date_for "${REPO[cfm]}")"
LEW="$(date_for "${REPO[lewice]}")"

mkdir -p "$OUT_DIR"
cat >"$OUT_FILE" <<HTML
<!doctype html>
<html lang="en">
<head>
 <meta charset="utf-8" />
 <meta name="viewport" content="width=device-width, initial-scale=1" />
 <title>VoloAltro App Portal</title>
 <style>
 body { font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; margin: 40px; max-width: 960px; }
 h1 { margin-bottom: 6px; }
 .muted { color: #555; margin-top: 0; }
 .folder { border: 1px solid #d6dee8; border-radius: 12px; margin: 18px 0; background: #f8fafc; overflow: hidden; }
 .folder summary { cursor: pointer; list-style: none; padding: 14px 16px; font-weight: 700; font-size: 18px; background: #eaf2ff; color: #16324f; }
 .folder-content { padding: 2px 12px 12px; }
 .card { border: 1px solid #ddd; border-radius: 10px; padding: 14px 16px; margin: 12px 0; background: #fff; }
 .card h2 { margin: 0 0 6px 0; font-size: 18px; }
 .card p { margin: 0 0 10px 0; color: #333; }
 .meta { color:#64748b; font-size: 12px; margin:0 0 10px 0; }
 a { color: #0b57d0; text-decoration: none; }
 a:hover { text-decoration: underline; }
 code { background: #f5f5f5; padding: 2px 6px; border-radius: 6px; }
 </style>
</head>
<body>
 <h1>VoloAltro - App Portal</h1>
 <p class="muted">Private index of apps hosted on voloaltro.tech.</p>

 <details class="folder" open>
  <summary>Tamarack Folder</summary>
  <div class="folder-content">
   <div class="card"><h2><a href="https://leasing-model.voloaltro.tech" target="_blank" rel="noreferrer">Leasing Model</a></h2><p class="meta">Latest git update: ${LM}</p><p><code>leasing-model.voloaltro.tech</code></p></div>
   <div class="card"><h2><a href="https://mission-analysis.voloaltro.tech" target="_blank" rel="noreferrer">Tamarack Mission Analysis</a></h2><p class="meta">Latest git update: ${MA}</p><p><code>mission-analysis.voloaltro.tech</code></p></div>
   <div class="card"><h2><a href="https://tamarack-wat.voloaltro.tech" target="_blank" rel="noreferrer">Tamarack WAT Analysis</a></h2><p class="meta">Latest git update: ${MA}</p><p><code>tamarack-wat.voloaltro.tech</code></p></div>
   <div class="card"><h2><a href="https://tamarack-project-financials.voloaltro.tech" target="_blank" rel="noreferrer">Tamarack Project Financials</a></h2><p class="meta">Latest git update: ${TPF}</p><p><code>tamarack-project-financials.voloaltro.tech</code></p></div>
   <div class="card"><h2><a href="https://dataroom.voloaltro.tech" target="_blank" rel="noreferrer">Data Room</a></h2><p class="meta">Latest git update: ${DR}</p><p><code>dataroom.voloaltro.tech</code></p></div>
   <div class="card"><h2><a href="https://aircraft-revenue.voloaltro.tech" target="_blank" rel="noreferrer">STC Cost &amp; Revenue Estimator</a></h2><p class="meta">Latest git update: ${AR}</p><p><code>aircraft-revenue.voloaltro.tech</code></p></div>
   <div class="card"><h2><a href="https://lru-tracker.voloaltro.tech" target="_blank" rel="noreferrer">LRU Tracker</a></h2><p class="meta">Latest git update: ${LRU}</p><p><code>lru-tracker.voloaltro.tech</code></p></div>
   <div class="card"><h2><a href="https://sales-training.voloaltro.tech" target="_blank" rel="noreferrer">SMARTWING Sales Training</a></h2><p class="meta">Latest git update: ${ST}</p><p><code>sales-training.voloaltro.tech</code></p></div>
   <div class="card"><h2><a href="https://cfm.voloaltro.tech" target="_blank" rel="noreferrer">Cash Flow Meeting Triage</a></h2><p class="meta">Latest git update: ${CFM}</p><p><code>cfm.voloaltro.tech</code></p></div>
   <div class="card"><h2><a href="https://lewice.voloaltro.tech" target="_blank" rel="noreferrer">LEWICE</a></h2><p class="meta">Latest git update: ${LEW}</p><p><code>lewice.voloaltro.tech</code></p></div>
   <div class="card"><h2><a href="https://tels.voloaltro.tech" target="_blank" rel="noreferrer">TELS External Loads</a></h2><p class="meta">Latest git update: ${TELS}</p><p><code>tels.voloaltro.tech</code></p></div>
  </div>
 </details>

 <details class="folder" open>
  <summary>VoloAltro Folder</summary>
  <div class="folder-content">
   <div class="card"><h2><a href="https://aglaze.voloaltro.tech" target="_blank" rel="noreferrer">AGLAZE</a></h2><p class="meta">Latest git update: ${AG}</p><p><code>aglaze.voloaltro.tech</code></p></div>
   <div class="card"><h2><a href="https://jet-sales-crm.voloaltro.tech" target="_blank" rel="noreferrer">Jet Sales CRM</a></h2><p class="meta">Latest git update: ${JS}</p><p><code>jet-sales-crm.voloaltro.tech</code></p></div>
   <div class="card"><h2><a href="https://groundhog.voloaltro.tech" target="_blank" rel="noreferrer">GroundHog</a></h2><p class="meta">Latest git update: ${GH}</p><p><code>groundhog.voloaltro.tech</code></p></div>
   <div class="card"><h2><a href="https://turnback.voloaltro.tech" target="_blank" rel="noreferrer">Turnback Simulator</a></h2><p class="meta">Latest git update: ${TB}</p><p><code>turnback.voloaltro.tech</code></p></div>
   <div class="card"><h2><a href="https://ash.voloaltro.tech" target="_blank" rel="noreferrer">ASH</a></h2><p class="meta">Latest git update: ${ASH}</p><p><code>ash.voloaltro.tech</code></p></div>
   <div class="card"><h2><a href="https://shy.voloaltro.tech" target="_blank" rel="noreferrer">Sandpoint Hot Yoga</a></h2><p class="meta">Latest git update: ${SHY}</p><p><code>shy.voloaltro.tech</code></p></div>
   <div class="card"><h2><a href="https://spoton.voloaltro.tech" target="_blank" rel="noreferrer">SpotOn Rate Calculator</a></h2><p class="meta">Latest git update: ${SP}</p><p><code>spoton.voloaltro.tech</code></p></div>
  </div>
 </details>

 <hr/>
 <p class="muted">If you need access, ask Nick for credentials.</p>
</body>
</html>
HTML

echo "Wrote $OUT_FILE"
