# Gitkeepr - Justfile utility

# Print list of available recipe (this)
default:
    @just --list --unsorted

# Run poetry install in all submodules
install:
    poetry install

# Build Docker image
build-docker:
    docker build -t gitkeepr .

# Run CLI through Docker
run-docker:
    docker run --rm -e GITHUB_API_TOKEN="${GITHUB_API_TOKEN}" -e GITHUB_USERNAME="${GITHUB_USERNAME}" gitkeepr --version

# Run pytest via poetry
pytest *ARGS:
    poetry run pytest {{ ARGS }}
