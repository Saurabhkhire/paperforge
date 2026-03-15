"""PaperForge validator node: scores miner submissions."""


def main() -> None:
    """Entry point for paperforge-validator CLI."""
    try:
        import bittensor  # noqa: F401
    except ImportError:
        print(
            "Bittensor is not installed. For local testing use: python run_local_test.py\n"
            "To install Bittensor: pip install -e \".[bittensor]\" (requires Rust; see INSTALL.md)"
        )
        return
    print("PaperForge Validator - use validator_harness for scoring")
