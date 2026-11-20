import json
import glob
import os

runs = glob.glob("/opt/benchmark/ple/runs/**/results.json", recursive=True)
print(f"Total results.json found: {len(runs)}")
summary = {}

for r in runs:
    try:
        with open(r, "r") as f:
            d = json.load(f)
        for t in d.get("tasks", []):
            tid = t.get("id")
            score = t.get("score")
            status = t.get("status")
            secs = t.get("seconds")
            tokens = t.get("tokens", {})
            if tid not in summary or (score is not None and score > summary[tid].get("score", -1)):
                summary[tid] = {
                    "score": score,
                    "status": status,
                    "seconds": secs,
                    "file": r,
                    "tokens": tokens
                }
    except Exception as e:
        pass

for tid, info in sorted(summary.items()):
    print(f"TASK: {tid:35s} | SCORE: {str(info['score']):6s} | STATUS: {info['status']}")
