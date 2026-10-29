"""Head-to-head: fresh seed 9001, n=500. Writes results/headtohead.json and
results/headtohead_rerun.json (determinism re-run), prints sha256 digests."""
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from calibrated_trust import evaluate

HERE = Path(__file__).resolve().parent


def digest(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()


if __name__ == "__main__":
    res, summ = evaluate.run_headtohead(500, 9001)
    (HERE / "results" / "headtohead.json").write_text(json.dumps(summ, indent=2, sort_keys=True))
    res2, summ2 = evaluate.run_headtohead(500, 9001)
    (HERE / "results" / "headtohead_rerun.json").write_text(json.dumps(summ2, indent=2, sort_keys=True))
    d1, d2 = digest(summ), digest(summ2)
    print(json.dumps(summ, indent=2))
    print("DIGEST_RUN1", d1)
    print("DIGEST_RUN2", d2)
    print("DETERMINISTIC", d1 == d2)
