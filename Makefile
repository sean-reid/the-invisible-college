.PHONY: setup install lint format typecheck test test-unit test-e2e blog-dev blog-build clean help

help:
	@echo "Targets:"
	@echo "  setup        Install Python and Node dependencies"
	@echo "  lint         Ruff + ESLint"
	@echo "  format       Ruff format + Prettier"
	@echo "  typecheck    mypy + astro check"
	@echo "  test         All tests"
	@echo "  test-unit    Python unit tests"
	@echo "  test-e2e     Playwright E2E against the built blog"
	@echo "  blog-dev     Run the blog dev server"
	@echo "  blog-build   Build the static blog"
	@echo "  clean        Remove build artifacts"

setup:
	uv sync
	cd blog && npm install

install: setup

lint:
	uv run ruff check institute tests
	cd blog && npx eslint .

format:
	uv run ruff format institute tests
	cd blog && npx prettier --write "src/**/*.{astro,ts,tsx,js,jsx,md,mdx}"

typecheck:
	uv run mypy institute
	cd blog && npx astro check

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
