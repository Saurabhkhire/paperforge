"""PaperForge subnet configuration."""

# Scoring weights (must sum to 1.0)
EXECUTION_WEIGHT = 0.25
CORRECTNESS_WEIGHT = 0.50
PERFORMANCE_WEIGHT = 0.25

# Minimum score for token eligibility
MIN_SCORE_THRESHOLD = 0.60

# Sandbox limits
SANDBOX_TIMEOUT_SECONDS = 60
SANDBOX_MEMORY_MB = 4096

# Python version for sandbox
SANDBOX_PYTHON_VERSION = "3.10"

# Allowed pip packages (allowlist)
ALLOWED_DEPENDENCIES = frozenset({
    "numpy",
    "torch",
    "scipy",
    "pandas",
    "scikit-learn",
    "pillow",
})
