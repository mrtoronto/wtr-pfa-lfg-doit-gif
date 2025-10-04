.PHONY: install install-dev run migrate test clean

# Install runtime dependencies
install:
	uv sync

# Install all dependencies including dev tools
install-dev:
	uv sync --all-groups

# Run the web application
run:
	uv run python wsgi.py

# Run database migrations
migrate:
	uv run sh migrate_db.sh

# Run tests
test:
	uv run pytest tests/ -v

# Clean build artifacts
clean:
	rm -rf .venv __pycache__ **/__pycache__ .pytest_cache htmlcov *.db

