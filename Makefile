.PHONY: setup lint format format-check check test test-unit test-e2e blog-dev blog-build clean help

help:
	@echo "Targets:"
	@echo "  setup         Install Python and Node dependencies"
	@echo "  check         Mirror CI: lint, format-check, types, tests, build, E2E"
	@echo "  lint          Ruff + ESLint"
	@echo "  format        Apply Ruff format + Prettier write"
	@echo "  format-check  Verify formatting without writing"
	@echo "  test          Python unit tests"
	@echo "  test-e2e      Playwright E2E against the built blog"
	@echo "  blog-dev      Run the blog dev server"
	@echo "  blog-build    Build the static blog"
	@echo "  clean         Remove build artifacts"

setup:
	uv sync
	cd blog && npm install

# Single command equivalent of every CI step. Run before pushing to
# catch what CI catches without waiting on a remote run. Skips
# `npm ci` because we assume `make setup` (or any prior install) has
# already populated node_modules.
check:
	uv run ruff check institute tests
	uv run ruff format --check institute tests
	uv run pytest
	cd blog && npm run sync-fellows
	cd blog && npx astro check
	cd blog && npx eslint .
	cd blog && npx prettier --check "src/**/*.{astro,ts,tsx,js,jsx,md,mdx}"
	cd blog && npm run build
	cd blog && npx playwright test --project=desktop

lint:
	uv run ruff check institute tests
	cd blog && npx eslint .

format:
	uv run ruff format institute tests
	cd blog && npx prettier --write "src/**/*.{astro,ts,tsx,js,jsx,md,mdx}"

format-check:
	uv run ruff format --check institute tests
	cd blog && npx prettier --check "src/**/*.{astro,ts,tsx,js,jsx,md,mdx}"

test: test-unit

test-unit:
	uv run pytest

test-e2e:
	cd blog && npx playwright test

blog-dev:
	cd blog && npm run dev

blog-build:
	cd blog && npm run build

clean:
	rm -rf blog/dist blog/.astro
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache .mypy_cache
