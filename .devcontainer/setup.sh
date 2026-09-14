#!/bin/bash
set -e

echo "==> Installing backend dependencies..."
cd /workspaces/university-health-container/backend
uv sync

echo "==> Installing frontend dependencies..."
cd /workspaces/university-health-container/frontend
pnpm install --frozen-lockfile

echo "==> Dependencies installed successfully."