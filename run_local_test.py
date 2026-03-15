#!/usr/bin/env python3
"""
Run PaperForge validation locally (no Docker).

Usage:
  python run_local_test.py                    # one miner, one validator run
  python run_local_test.py --multi            # simulate multiple miners, show each result
  python run_local_test.py --full             # full demo: multiple miners × multiple validators + consensus
  python run_local_test.py --task word2vec_skipgram
"""
import json
import random
import sys
from pathlib import Path

# Ensure package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent))

from paperforge.miner.submission import MinerSubmission
from paperforge.task.loader import load_task_spec
from paperforge.validator import run_validation

# --- Stub miner implementations (per use case) ---

# Miner 1: correct implementation (matches expected output)
STUB_CODE_GOOD = '''
"""Skip-gram negative sampling (Mikolov et al. 2013). arXiv:1301.3781"""
import json

def main(sample_input):
    """Return output in the shape expected by the task."""
    return {"loss": 0.5, "W_updated": True, "W_prime_updated": True}

def train_step(center_idx, context_idx, neg_indices, W, W_prime):
    """Skip-gram negative sampling training step."""
    pass
'''

# Miner 2: alternative correct implementation (different style)
STUB_CODE_GOOD_ALT = '''
"""Efficient Estimation of Word Representations - Skip-gram (Mikolov et al. 2013)."""
def main(sample_input):
    # Section 3.1, Eq. 4: negative sampling objective
    return {"loss": 0.5, "W_updated": True, "W_prime_updated": True}
'''

# Miner 3: wrong output shape (fails correctness)
STUB_CODE_BAD_OUTPUT = '''
"""Skip-gram (wrong output). arXiv:1301.3781"""
def main(sample_input):
    return {"loss": 99.0, "wrong_key": True}
'''

# Miner 4: wrong type / shape (fails correctness)
STUB_CODE_BAD_SHAPE = '''
"""Skip-gram (wrong shape). arXiv:1301.3781"""
def main(sample_input):
    return [0.5, True, True]
'''

# Miner 5: crashes at runtime (fails execution)
STUB_CODE_CRASH = '''
"""Skip-gram (crashes). arXiv:1301.3781"""
def main(sample_input):
    raise RuntimeError("bug in implementation")
'''

# Miner 6: timeout / hang simulation - we use crash for simplicity; could add slow code
STUB_CODE_SYNTAX_ERROR = '''
"""Skip-gram (syntax error). arXiv:1301.3781"""
def main(sample_input)
    return {"loss": 0.5, "W_updated": True, "W_prime_updated": True}
'''


def run_one_miner(
    task, task_dir, submission: MinerSubmission, miner_name: str, verbose: bool = True
):
    """Run validation for one miner; return (miner_name, result)."""
    if verbose:
        print("\n" + "=" * 60)
        print(f"MINER: {miner_name}")
        print("=" * 60)
        print("--- code ---")
        print(submission.code[:400] + ("..." if len(submission.code) > 400 else ""))
        print("--- docstring ---", submission.docstring)
        print("--- requirements ---", submission.requirements)
    result = run_validation(submission, task, task_dir)
    if verbose:
        print("--- validator result ---")
        print("  Execution:", "PASS" if result.execution_score == 1.0 else "FAIL", "| Correctness:", result.correctness_score, "| Final:", result.final_score, "| Eligible:", result.eligible)
    return miner_name, result


def _jitter(score: float, amount: float = 0.02) -> float:
    """Add small jitter so multiple validators don't report identical scores."""
    return max(0.0, min(1.0, score + random.uniform(-amount, amount)))


def _run_full_demo(task, task_dir, tasks_root: Path):
    """Full subnet demo: multiple miners × multiple validators → consensus (median)."""
    NUM_VALIDATORS = 3
    random.seed(42)

    miners = [
        ("Miner Alpha (correct)", MinerSubmission(
            paper_id=task.paper_id,
            code=STUB_CODE_GOOD.strip(),
            requirements=["numpy"],
            docstring="Mikolov et al. 2013, Eq. 4",
            complexity_note="O(k) per step",
            test_output="sample_input -> sample_output",
        )),
        ("Miner Beta (correct, alt)", MinerSubmission(
            paper_id=task.paper_id,
            code=STUB_CODE_GOOD_ALT.strip(),
            requirements=[],
            docstring="Section 3.1, Eq. 4",
            complexity_note="",
            test_output="",
        )),
        ("Miner Gamma (wrong output)", MinerSubmission(
            paper_id=task.paper_id,
            code=STUB_CODE_BAD_OUTPUT.strip(),
            requirements=[],
            docstring="Wrong impl",
            complexity_note="",
            test_output="",
        )),
        ("Miner Delta (wrong shape)", MinerSubmission(
            paper_id=task.paper_id,
            code=STUB_CODE_BAD_SHAPE.strip(),
            requirements=[],
            docstring="Returns list instead of dict",
            complexity_note="",
            test_output="",
        )),
        ("Miner Epsilon (crashes)", MinerSubmission(
            paper_id=task.paper_id,
            code=STUB_CODE_CRASH.strip(),
            requirements=[],
            docstring="RuntimeError",
            complexity_note="",
            test_output="",
        )),
    ]

    # Optional reasoning per miner (agentic: "agents that explain their reasoning")
    miner_reasoning = {
        "Miner Alpha (correct)": "Implementation follows Mikolov et al. 2013 Sec 3.1 Eq.4; negative sampling objective; returns loss and updated W, W'.",
        "Miner Beta (correct, alt)": "Same spec, direct dict return; Section 3.1 Eq. 4.",
        "Miner Gamma (wrong output)": "Returns wrong keys (wrong_key); does not match sample_output schema.",
        "Miner Delta (wrong shape)": "Returns list instead of dict; fails correctness check.",
        "Miner Epsilon (crashes)": "Raises at runtime; execution fails.",
    }

    # Banner (ASCII so it works on Windows console)
    B = "=" * 72
    print()
    print("+" + B + "+")
    print("|  PaperForge  --  Multiple Miners x Multiple Validators (Consensus Demo)  ".ljust(73) + "|")
    print("+" + B + "+")
    print()
    print("  Task: " + task.algorithm_name)
    print("  Paper: arXiv:" + task.paper_id + "  |  Miners: " + str(len(miners)) + "  |  Validators: " + str(NUM_VALIDATORS))
    print("  Consensus: median of validator scores per miner  ->  rewards if score >= 0.60")
    print()
    print("  --- AGENTIC FUNDING (simulated) ---")
    print("  [x402] Agent paid 0.01 USDC for task fetch (task_id=" + task.algorithm_name + ", paper=" + task.paper_id + ")")
    print("  [Agents] Validators = agents that evaluate work and vote; consensus authorizes payments.")
    print()

    # Per-miner: run through each validator (with jitter), show full code + scores
    all_rows = []
    W = 72
    for miner_name, submission in miners:
        print("+" + "-" * W + "+")
        print("| " + miner_name.ljust(W - 1) + "|")
        print("+" + "-" * W + "+")
        print("| " + "--- code ---".ljust(W - 2) + " |")
        print("+" + "-" * W + "+")
        if miner_name in miner_reasoning:
            print("| " + "--- agent reasoning (miner) ---".ljust(W - 2) + " |")
            r = miner_reasoning[miner_name]
            print("| " + (r[: W - 4] + ".." if len(r) > W - 4 else r).ljust(W - 2) + " |")
            print("+" + "-" * W + "+")
        for line in submission.code.splitlines():
            if len(line) <= W - 2:
                print("| " + line.ljust(W - 2) + " |")
            else:
                chunk = line
                while chunk:
                    take = min(W - 2, len(chunk))
                    print("| " + chunk[:take].ljust(W - 2) + " |")
                    chunk = chunk[take:]
        print("+" + "-" * W + "+")

        base_result = run_validation(submission, task, task_dir)
        scores = [_jitter(base_result.final_score) for _ in range(NUM_VALIDATORS)]
        scores.sort()
        consensus = round(scores[1], 4) if NUM_VALIDATORS == 3 else round((scores[1] + scores[2]) / 2, 4)
        eligible = consensus >= 0.60

        row = [miner_name]
        for i, s in enumerate(scores, 1):
            row.append(round(s, 4))
        row.append(consensus)
        row.append("[OK] Eligible" if eligible else "[--] Not eligible")
        all_rows.append(row)

        val_str = "  |  ".join(f"Validator {i}: {s:.4f}" for i, s in enumerate(scores, 1))
        print("| " + val_str.ljust(71) + "|")
        votes = ["eligible" if s >= 0.60 else "not eligible" for s in scores]
        vote_str = "  |  ".join(f"Val{i}={votes[i-1]}" for i in range(1, NUM_VALIDATORS + 1))
        print("| " + ("Agent votes: " + vote_str).ljust(71) + "|")
        print("| " + ("-> Consensus (median): " + str(consensus) + "  ->  " + ("[OK] Eligible for rewards" if eligible else "[--] Below threshold")).ljust(71) + "|")
        print("+" + "-" * 72 + "+")
        print()

    # Summary matrix
    print()
    print("+" + B + "+")
    print("|  SUMMARY: Miner x Validator scores  ->  Consensus  ->  Rewards  ".ljust(73) + "|")
    print("+" + B + "+")
    header = "| " + "Miner".ljust(24) + "| Val 1   | Val 2   | Val 3   | Consensus | Result          |"
    print(header)
    print("+" + "-" * 24 + "+" + "-" * 9 + "+" + "-" * 9 + "+" + "-" * 9 + "+" + "-" * 10 + "+" + "-" * 16 + "+")
    for row in all_rows:
        name_short = (row[0][:22] + "..") if len(row[0]) > 24 else row[0]
        line = "| " + name_short.ljust(24) + "| " + f"{row[1]:.4f}".ljust(8) + "| " + f"{row[2]:.4f}".ljust(8) + "| " + f"{row[3]:.4f}".ljust(8) + "| " + f"{row[4]:.4f}".ljust(10) + "| " + row[5].ljust(14) + "|"
        print(line)
    print("+" + B + "+")
    print()

    eligible_miners = [r[0] for r in all_rows if "Eligible" in r[5]]
    print("  -> Rewards would go to: " + (", ".join(eligible_miners) if eligible_miners else "(none)"))
    print("  -> In the live subnet, each validator runs in its own sandbox; consensus prevents one bad validator from changing payouts.")
    print()
    print("  --- AGENTIC FUNDING OUTCOME (simulated) ---")
    if eligible_miners:
        share = round(0.15 / len(eligible_miners), 4)
        for m in eligible_miners:
            print("  [Payment] " + str(share) + " TAO  ->  " + m + "  (consensus approved)")
        print("  [Move funds] Agents (validators) voted; consensus authorized the above payouts.")
    else:
        print("  [Payment] No payouts (no miner reached consensus threshold).")
    print("  [x402] Simulated: task was fetched after agent paid 0.01 USDC (payment-for-service).")
    if eligible_miners:
        print("  [Solana AI] Simulated: agent sent 0.05 SOL to each eligible miner (Solana Agent Kit).")
    print("  [Unbrowse] Simulated: task/paper fetched by intent 'get paper " + task.paper_id + "' (Unbrowse resolve).")
    print()


def main():
    tasks_root = Path(__file__).parent / "tasks"
    task_name = "word2vec_skipgram"
    if "--task" in sys.argv:
        i = sys.argv.index("--task")
        if i + 1 < len(sys.argv):
            task_name = sys.argv[i + 1]
    task_dir = tasks_root / task_name
    if not task_dir.exists() or not (task_dir / "task_spec.json").exists():
        print(f"Task not found: {task_dir}")
        sys.exit(1)

    task = load_task_spec(task_dir)
    use_multi = "--multi" in sys.argv
    use_full = "--full" in sys.argv

    if use_full:
        _run_full_demo(task, task_dir, tasks_root)
        return

    if use_multi:
        # Simulate multiple miners; each gets validated
        miners = [
            ("Miner A (correct)", MinerSubmission(
                paper_id=task.paper_id,
                code=STUB_CODE_GOOD.strip(),
                requirements=["numpy"],
                docstring="Mikolov et al. 2013, Eq. 4",
                complexity_note="O(k) per step",
                test_output="sample_input -> sample_output",
            )),
            ("Miner B (wrong output)", MinerSubmission(
                paper_id=task.paper_id,
                code=STUB_CODE_BAD_OUTPUT.strip(),
                requirements=[],
                docstring="Wrong impl",
                complexity_note="",
                test_output="",
            )),
            ("Miner C (crashes)", MinerSubmission(
                paper_id=task.paper_id,
                code=STUB_CODE_CRASH.strip(),
                requirements=[],
                docstring="Buggy",
                complexity_note="",
                test_output="",
            )),
        ]
        print("Task:", task.algorithm_name, "| paper_id:", task.paper_id)
        print("Simulating MULTIPLE MINERS (each validated by validator)...\n")
        results = []
        for name, sub in miners:
            _, res = run_one_miner(task, task_dir, sub, name, verbose=True)
            results.append((name, res))
        print("\n" + "=" * 60)
        print("SUMMARY (multiple miners)")
        print("=" * 60)
        for name, res in results:
            print(f"  {name}: Execution={'PASS' if res.execution_score == 1.0 else 'FAIL'} | Correctness={res.correctness_score} | Final={res.final_score} | Eligible={res.eligible}")
        print("\nDone. In the real subnet, multiple validators would each score these; consensus (e.g. median) would decide rewards.")
        return

    # Single miner (original behavior)
    submission = MinerSubmission(
        paper_id=task.paper_id,
        code=STUB_CODE_GOOD.strip(),
        requirements=["numpy"],
        docstring="Mikolov et al. 2013, Eq. 4",
        complexity_note="O(k) per step",
        test_output="sample_input -> sample_output",
    )

    print("Task:", task.algorithm_name, "| paper_id:", task.paper_id)
    print("Running validation (local, no Docker)...\n")

    # ----- What the MINER sends -----
    print("=" * 60)
    print("MINER SUBMISSION (what the miner sends to the validator)")
    print("=" * 60)
    print("\n--- code (the .py the miner wrote) ---")
    print(submission.code)
    print("\n--- requirements ---")
    print(submission.requirements)
    print("\n--- docstring (miner's citation) ---")
    print(submission.docstring)
    print("\n--- complexity_note ---")
    print(submission.complexity_note)
    print("\n--- test_output (miner's self-test summary) ---")
    print(submission.test_output)
    print()

    result = run_validation(submission, task, task_dir)

    # ----- What the VALIDATOR reports -----
    print("=" * 60)
    print("VALIDATOR RESULT (what the validator reports after running the code)")
    print("=" * 60)
    print("\n--- scores ---")
    print("  Execution (25%):", "PASS" if result.execution_score == 1.0 else "FAIL", f"  (raw: {result.execution_score})")
    print("  Correctness (50%):", result.correctness_score)
    print("  Performance (25%):", result.performance_score)
    print("  Final score:", result.final_score)
    print("  Eligible for rewards:", result.eligible)
    print("\n--- stdout from running miner's code ---")
    print(result.details.get("stdout", "(none)"))
    print("\n--- stderr from running miner's code ---")
    print(result.details.get("stderr", "(none)") or "(empty)")
    print("\n--- exit_code ---")
    print(result.details.get("exit_code", "?"))
    print("\n" + "=" * 60)
    print("Done. Check: execution PASS, final_score >= 0.60 for eligibility.")


if __name__ == "__main__":
    main()
