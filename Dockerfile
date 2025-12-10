# Dockerfile for TestDataGen (Python + sqlite3 + faker)
FROM python:3.11-slim

# metadata
LABEL maintainer="HarshadBorade <harshadborade2@gmail.com>" \
      org.opencontainers.image.source="https://github.com/HarshadBorade/TestDataGen"

ENV APP_HOME=/app
WORKDIR ${APP_HOME}

# Optional system dependencies (keep only what you really need)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      ca-certificates \
      dos2unix \
 && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . ${APP_HOME}

# Normalise line endings for safety
RUN find ${APP_HOME} -type f -name "*.py" -exec sed -i 's/\r$//' {} \; \
 && find ${APP_HOME} -type f -name "*.sh" -exec sed -i 's/\r$//' {} \; \
 && chmod +x ${APP_HOME}/*.sh || true

# Install Python requirements if present
RUN if [ -f requirements.txt ]; then \
      python -m pip install --no-cache-dir --upgrade pip && \
      python -m pip install --no-cache-dir -r requirements.txt ; \
    else \
      python -m pip install --no-cache-dir --upgrade pip && \
      echo "No requirements.txt found; continuing without pip installs"; \
    fi

# Optional: non-root user
RUN useradd --create-home appuser || true
RUN mkdir -p /data && chown -R appuser:appuser /data ${APP_HOME}
USER appuser

# For batch job you do NOT need any exposed ports
# (remove EXPOSE completely or keep only if you later add a web server)
# EXPOSE 80
# EXPOSE 5000

VOLUME ["/data"]
ENV DATA_DIR=/data

# Default command – ECS will use this when "command" is empty in task definition
CMD ["python", "-u", "Main.py", "--web"]
