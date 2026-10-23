#!/bin/bash
set -e

echo "==> Installing backend dependencies..."
cd /workspaces/university-health-container/backend

# El volumen del .venv puede crearse como root; dar permisos al usuario.
if [ -d .venv ] && [ ! -w .venv ]; then
  echo "==> Fixing .venv permissions..."
  sudo chown -R "$(id -u):$(id -g)" .venv
fi

# Si el .venv fue creado en Windows, no sirve dentro del contenedor Linux.
if [ -f .venv/pyvenv.cfg ] && [ ! -x .venv/bin/python ]; then
  echo "==> Removing incompatible .venv contents..."
  find .venv -mindepth 1 -maxdepth 1 -exec rm -rf {} +
fi

uv sync

echo "==> Installing frontend dependencies..."
cd /workspaces/university-health-container/frontend
pnpm install --frozen-lockfile

echo "==> Dependencies installed successfully."