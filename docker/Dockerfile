FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -s /bin/bash playground && \
    mkdir -p /workspace /logs && \
    chown -R playground:playground /workspace /logs

# Set working directory
WORKDIR /home/playground

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy playground code
COPY playground/ ./playground/
COPY docker/entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh && \
    chown -R playground:playground ./playground ./entrypoint.sh

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
