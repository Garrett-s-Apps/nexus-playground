FROM python:3.11-alpine

# Install system dependencies (Alpine uses apk)
RUN apk add --no-cache \
    git \
    curl \
    bash

# Create non-root user (Alpine uses adduser)
RUN adduser -D -s /bin/bash playground && \
    mkdir -p /workspace /logs && \
    chown -R playground:playground /workspace /logs

# Set working directory
WORKDIR /home/playground

# Install Python dependencies directly (no requirements.txt in build context)
RUN pip install --no-cache-dir \
    anthropic>=0.40.0 \
    pyyaml>=6.0.1 \
    requests>=2.31.0

# Copy playground code, soul documents, and entrypoint
COPY playground/ ./playground/
COPY SOUL.md SELF-AWARE.md FREEDOM.md ./
COPY docker/entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh && \
    chown -R playground:playground ./playground ./entrypoint.sh SOUL.md SELF-AWARE.md FREEDOM.md && \
    chmod 444 ./playground/config.yaml

# Switch to non-root user
USER playground

# Initialize workspace git repo
RUN git config --global user.name "NEXUS Playground" && \
    git config --global user.email "playground@nexus.local" && \
    cd /workspace && \
    git init && \
    echo "# NEXUS Playground Workspace" > README.md && \
    echo "\nThis is an autonomous AI workspace. The AI has complete freedom to create whatever it wants here." >> README.md && \
    git add README.md && \
    git commit -m "Initial commit: Autonomous workspace initialized"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV WORKSPACE_DIR=/workspace
ENV LOGS_DIR=/logs

# Start supervisor via entrypoint
ENTRYPOINT ["./entrypoint.sh"]
