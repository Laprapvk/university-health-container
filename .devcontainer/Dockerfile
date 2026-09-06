FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

# Remove broken yarn repo from base image if present
RUN rm -f /etc/apt/sources.list.d/yarn.list

# Install database and cache CLI tools
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends \
       postgresql-client \
       redis-tools \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Install uv for fast Python package management
RUN pip install --no-cache-dir --upgrade pip uv