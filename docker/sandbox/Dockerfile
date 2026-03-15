# PaperForge validator sandbox
# Runs miner code in isolation: no network, 4GB RAM, 60s timeout
FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Pre-install allowed packages (cached at round start)
RUN pip install --no-cache-dir numpy torch scipy pandas scikit-learn pillow

# No network in container (handled by docker run --network=none)
# Memory limit: docker run -m 4g
# Timeout: harness kills process after 60s
