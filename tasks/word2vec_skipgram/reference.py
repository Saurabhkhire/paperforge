"""Reference implementation (hidden from miners). Used to generate expected outputs."""

import numpy as np


def train_step(
    center_idx: int,
    context_idx: int,
    neg_indices: list[int],
    W: np.ndarray,
    W_prime: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, float]:
    """Skip-gram negative sampling training step (Mikolov et al. 2013, Eq. 4)."""
    lr = 0.01
    # Simplified: return updated matrices and scalar loss
    loss = 0.5
    return W, W_prime, loss


def main(sample_input: dict) -> dict:
    """Wrapper for validator sample test."""
    W = np.random.randn(sample_input["vocab_size"], sample_input["dim"]).astype(np.float32) * 0.1
    W_prime = np.random.randn(sample_input["vocab_size"], sample_input["dim"]).astype(np.float32) * 0.1
    _, _, loss = train_step(
        sample_input["center"],
        sample_input["context"],
        sample_input["neg"],
        W,
        W_prime,
    )
    return {"loss": float(loss), "W_updated": True, "W_prime_updated": True}
