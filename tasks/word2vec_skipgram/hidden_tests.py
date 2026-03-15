"""Hidden test cases for validator. Not shown to miners."""

# Tests run inside sandbox; import implementation and run
# Each test returns pass/fail

HIDDEN_INPUTS = [
    {"center": 0, "context": 1, "neg": [2], "vocab_size": 5, "dim": 3},
    {"center": 1, "context": 0, "neg": [3, 4], "vocab_size": 5, "dim": 3},
    {"center": 2, "context": 3, "neg": [0, 1, 4], "vocab_size": 6, "dim": 4},
]
