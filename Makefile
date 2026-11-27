#-------------------------------- VARIABLES ----------------------------------#

NAME		=	pac-man

SRC			=	pac-man.py
VENV		=	.venv

DIST		=	dist

CONF		?=	config.json

EXCLUDE				=	--exclude $(VENV)
EXCLUDE_MYPY 		=	--exclude $(VENV)

#-------------------------------- RULES --------------------------------------#

.PHONY: all install run debug clean fclean re reset lint lint-strict check_uv help

all: check_uv install run

install: check_uv
	uv sync

run: check_uv
	@uv run python $(SRC) $(CONF)

build: install
	rm -fr $(DIST)/
	uv run pyinstaller --onefile --windowed $(SRC)
	mkdir $(DIST)/pacman
	mkdir $(DIST)/pacman/src
	cp -r assets $(DIST)/pacman
	cp -r README_package.md $(DIST)/pacman/README.md
	cp -r src/arcade $(DIST)/pacman/src/
	cp config.json $(DIST)/pacman
	cp instruction.txt $(DIST)/pacman
	mv $(DIST)/pac-man $(DIST)/pacman
	cd $(DIST); zip -r pac-man.zip pacman/
	rm -fr $(DIST)/pacman

debug: check_uv
	@uv run python -m pdb $(SRC) $(CONF)

lint: check_uv
	uv run flake8 . $(EXCLUDE)
	uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs $(EXCLUDE_MYPY)

lint-strict: check_uv
	uv run flake8 . $(EXCLUDE)
	uv run mypy . $(EXCLUDE_MYPY) --strict

clean:
	find . -name "__pycache__" 		-type d -exec rm -rf "{}" +
	find . -name ".mypy_cache" 		-type d -exec rm -rf "{}" +
	find . -name ".pytest_cache" 	-type d -exec rm -rf "{}" +
	find . -name "htmlcov" 			-type d -exec rm -rf "{}" +
	find . -name "*.egg-info" 		-type d -exec rm -rf "{}" +
	find . -name ".coverage" 		-delete
	find . -name "*.pyc" 			-delete
	rm -rf build
	rm -rf pac-man.spec

fclean: clean
	rm -rf .venv
	rm -rf dist

re: check_uv fclean install

reset: check_uv fclean
	rm -f uv.lock
	uv sync

check_uv:
	@command -v uv >/dev/null 2>&1 || { \
		echo "Error: uv is not installed."; \
		echo "Install it via: curl -LsSf https://astral.sh/uv/install.sh | sh"; \
		exit 1; \
	}

help:
	@echo "Available rules:"
	@echo "  all        	- Install and run"
	@echo "  install    	- Install dependencies"
	@echo "  run        	- Run the project (FUNCTIONS=... INPUT=... OUTPUT=... to overwrite the files)"
	@echo "  debug      	- Run with pdb debugger"
	@echo "  lint       	- Run flake8 and mypy"
	@echo "  lint-strict	- Run flake8 and mypy in strict mode"
	@echo "  clean      	- Remove cache files"
	@echo "  fclean     	- clean + remove venv"
	@echo "  re         	- fclean + install"
	@echo "  reset      	- fclean + remove uv.lock + install"
	@echo "  check_uv       - test if uv is installed and display a message if not (used in every rules that uses uv)"
