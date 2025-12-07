# Dockerfile for TestDataGen (Python + sqlite3 + faker)
# Uses a slim Python base, installs requirements, fixes CRLF if present,
# and runs Main.py (adjust CMD if you prefer SQL3.py or another file).

FROM python:3.11-slim

# metadata
LABEL maintainer="HarshadBorade <harshadborade2@gmail.com>" \
      org.opencontainers.image.source="https://github.com/HarshadBorade/TestDataGen"

# avoid running as root (optionally)
ENV APP_HOME=/app
WORKDIR ${APP_HOME}

# system deps (minimal). Add build-essential if you see wheels build errors.
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      ca-certificates \
      git \
      gcc \
      libffi-dev \
      musl-dev \
      # dos2unix optional - we will still sanitize line endings below
      dos2unix \
 && rm -rf /var/lib/apt/lists/*

# copy project files
COPY . ${APP_HOME}

# Ensure any DOS CRLF endings won't break execution (fix in-place)
# This runs only during build and is safe for text files.
RUN find ${APP_HOME} -type f -name "*.py" -exec sed -i 's/\r$//' {} \; \
 && find ${APP_HOME} -type f -name "*.sh" -exec sed -i 's/\r$//' {} \; \
 && chmod +x ${APP_HOME}/*.sh || true

# Install Python requirements (if requirements.txt exists)
# If the repo doesn't include requirements.txt, this step will simply be skipped.
RUN if [ -f requirements.txt ]; then \
      python -m pip install --no-cache-dir --upgrade pip && \
      python -m pip install --no-cache-dir -r requirements.txt ; \
    else \
      python -m pip install --no-cache-dir --upgrade pip && \
      echo "No requirements.txt found; continuing without pip installs"; \
    fi

# create runtime user and writable data directory (optional but recommended)
RUN useradd --create-home appuser || true
RUN mkdir -p /data && chown -R appuser:appuser /data ${APP_HOME}
USER appuser

# Default working directory and exposed volume for sqlite DB / exports
VOLUME ["/data"]
ENV DATA_DIR=/data

# If Main.py is the entrypoint; adjust to SQL3.py if your README indicates that.
# Using python -u to get unbuffered logs in container stdout.
CMD ["python", "-u", "Main.py"]

