"""PaperForge miner node: receives tasks, implements, submits."""


def main() -> None:
    """Entry point for paperforge-miner CLI."""
    try:
        import bittensor  # noqa: F401
    except ImportError:
        print(
            "Bittensor is not installed. For local testing use: python run_local_test.py\n"
            "To install Bittensor: pip install -e \".[bittensor]\" (requires Rust; see INSTALL.md)"
        )
        return
    print("PaperForge Miner - use miner_template/ for starter code")
