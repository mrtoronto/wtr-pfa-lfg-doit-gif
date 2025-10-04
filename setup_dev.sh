#!/bin/bash
# Quick setup script for local development

echo "=========================================="
echo "Flask App Development Setup"
echo "=========================================="
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "uv is not installed. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.bashrc
else
    echo "✓ uv is already installed"
fi

# Create .flaskenv if it doesn't exist
if [ ! -f .flaskenv ]; then
    echo "Creating .flaskenv from example..."
    cp .flaskenv.example .flaskenv
    echo "✓ .flaskenv created"
else
    echo "✓ .flaskenv already exists"
fi

# Create local_settings.py if it doesn't exist
if [ ! -f local_settings.py ]; then
    echo "Creating local_settings.py from example..."
    cp local_settings.example.py local_settings.py
    echo "✓ local_settings.py created"
    echo "⚠️  Please edit local_settings.py and set your SECRET_KEY"
else
    echo "✓ local_settings.py already exists"
fi

# Install dependencies
echo ""
echo "Installing dependencies..."
uv sync --all-groups

# Initialize database
echo ""
echo "Setting up database..."
sh migrate_db.sh

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To start the development server, run:"
echo "  make run"
echo ""
echo "Or:"
echo "  uv run python wsgi.py"
echo ""
echo "The app will be available at: http://127.0.0.1:5000"
echo ""

