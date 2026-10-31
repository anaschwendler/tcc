"""ConceptRank must not depend on Python's string hash seed."""

import os
import subprocess
import sys
from pathlib import Path

EXPERIMENTS = Path(__file__).parents[1] / "output" / "experiments"

SCRIPT = """
import sys
from pathlib import Path
from conceptrank.concept import ConceptSummarizer
from conceptrank.summarize import summarize_cluster
for name in sorted(p.name for p in Path(sys.argv[1]).iterdir())[:5]:
    print(summarize_cluster(Path(sys.argv[1]) / name, ConceptSummarizer))
"""


def summarize_with_hash_seed(seed):
    env = {**os.environ, "PYTHONHASHSEED": str(seed)}
    result = subprocess.run(
        [sys.executable, "-c", SCRIPT, str(EXPERIMENTS)],
        env=env, capture_output=True, text=True, check=True,
    )
    return result.stdout


def test_concept_is_deterministic_across_hash_seeds():
    assert summarize_with_hash_seed(1) == summarize_with_hash_seed(2)
