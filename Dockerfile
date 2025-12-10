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

# Install Python requirements (must include Flask)
# requirements.txt should contain at least: Flask, faker, etc.
RUN if [ -f requirements.txt ]; then \
      python -m pip install --no-cache-dir --upgrade pip && \
      python -m pip install --no-cache-dir -r requirements.txt ; \
    else \
      python -m pip install --no-cache-dir --upgrade pip && \
      python -m pip install --no-cache-dir Flask && \
      echo "No requirements.txt found; installed Flask only"; \
    fi

# Optional: non-root user
RUN useradd --create-home appuser || true
RUN mkdir -p /data && chown -R appuser:appuser /data ${APP_HOME}
USER appuser

# Web server listens on 5000
EXPOSE 5000

VOLUME ["/data"]
ENV DATA_DIR=/data

# Start app in web mode
CMD ["python", "-u", "Main.py", "--web"]
