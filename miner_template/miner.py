"""
PaperForge Miner Template

What the miner does:
1. Receive task package: task_spec (paper_id, algorithm_name, function_signature,
   sample_input, sample_output, performance_target) + path or URL to the research paper PDF.
2. Open the PDF (e.g. tasks/word2vec_skipgram/paper.pdf or paper_pdf_url) and read the
   relevant sections/equations.
3. Implement the algorithm in Python (main(sample_input) returning the expected shape).
4. Self-test with sample_input -> sample_output.
5. Return MinerSubmission: code, requirements, docstring, complexity_note, test_output.

Example: Word2Vec skip-gram negative sampling (simplified stub).
"""


def implement_algorithm(task_spec: dict, paper_pdf_path: str | None = None) -> dict:
    """
    Implement the algorithm described in the task spec.
    Optionally use paper_pdf_path to read the research paper (e.g. tasks/word2vec_skipgram/paper.pdf).
    Return a MinerSubmission-compatible dict.
    """
    # 1) Load task
    paper_id = task_spec["paper_id"]
    algorithm_name = task_spec["algorithm_name"]
    function_signature = task_spec["function_signature"]
    sample_input = task_spec["sample_input"]
    sample_output = task_spec["sample_output"]
    # 2) Optional: open PDF to implement from the paper
    # if paper_pdf_path:
    #     import fitz  # PyMuPDF
    #     doc = fitz.open(paper_pdf_path)
    #     ... read sections, implement algorithm ...

    # Stub returns dict; real miner implements the algorithm
    code = '''
"""Skip-gram negative sampling (Mikolov et al. 2013, Eq. 4).
Paper: Efficient Estimation of Word Representations in Vector Space
Section 3.1, Eq. 4.
"""
# Reference: https://arxiv.org/abs/1301.3781

def main(sample_input):
    """Miner implements algorithm; stub returns expected shape."""
    return {"loss": 0.5, "W_updated": True, "W_prime_updated": True}

def train_step(center_idx, context_idx, neg_indices, W, W_prime):
    """Skip-gram negative sampling training step."""
    pass
'''

    # Self-test
    test_output = f"sample_input={sample_input} -> sample_output={sample_output}"

    return {
        "paper_id": paper_id,
        "code": code.strip(),
        "requirements": ["numpy"],
        "docstring": "Skip-gram negative sampling, Mikolov et al. 2013, Eq. 4",
        "complexity_note": "O(k) per step, k=negative samples",
        "test_output": test_output,
    }


if __name__ == "__main__":
    # Example task (from Word2Vec spec)
    task = {
        "paper_id": "1301.3781",
        "algorithm_name": "skip_gram_negative_sampling",
        "function_signature": "def train_step(center_idx, context_idx, neg_indices, W, W_prime) -> (W, W_prime, loss)",
        "sample_input": "{'center': 0, 'context': 1, 'neg': [2,3,4], 'W': [[0.1]], 'W_prime': [[0.2]]}",
        "sample_output": "{'W': [[0.1]], 'W_prime': [[0.2]], 'loss': 0.5}",
        "performance_target": "Loss decreases over 1000 steps",
    }
    submission = implement_algorithm(task)
    print("Submission:", submission)
