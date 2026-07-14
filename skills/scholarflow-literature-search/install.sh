#!/usr/bin/env bash
# Optional local MCP installer for Claude Code.
# Usage: bash install.sh your-email@example.org
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_HOME="${XDG_DATA_HOME:-${HOME}/.local/share}"
MCP_TARGET="${DATA_HOME}/scholarflow-literature-search/mcp-server"
SERVER_NAME="scholarflow-literature-search"
PUBMED_EMAIL="${1:-}"

if [ -z "${PUBMED_EMAIL}" ]; then
    echo "Usage: bash install.sh your-email@example.org" >&2
    exit 2
fi

for command in python3 claude; do
    if ! command -v "${command}" >/dev/null 2>&1; then
        echo "ERROR: ${command} is required. See README.md for supported environments." >&2
        exit 1
    fi
done

for relpath in README.md SKILL.md manifest.yaml mcp-server; do
    if [ ! -e "${SCRIPT_DIR}/${relpath}" ]; then
        echo "ERROR: incomplete ScholarFlow Literature Search directory: missing ${relpath}" >&2
        exit 1
    fi
done

if claude mcp get "${SERVER_NAME}" >/dev/null 2>&1; then
    echo "A Claude Code MCP server named ${SERVER_NAME} already exists."
    echo "Leave it in place, or remove it explicitly before reinstalling:"
    echo "  claude mcp remove ${SERVER_NAME} --scope user"
    exit 0
fi

echo "Installing Python dependencies..."
python3 -m pip install --quiet -r "${SCRIPT_DIR}/mcp-server/requirements.txt"

echo "Copying the local MCP server..."
mkdir -p "${MCP_TARGET}"
cp -R "${SCRIPT_DIR}/mcp-server/." "${MCP_TARGET}/"

echo "Registering the server with Claude Code..."
claude mcp add "${SERVER_NAME}" --scope user --env "PUBMED_EMAIL=${PUBMED_EMAIL}" -- \
    python3 "${MCP_TARGET}/academic_search_server.py"

echo
echo "Installed ${SERVER_NAME}. Verify it with:"
echo "  claude mcp get ${SERVER_NAME}"
echo "Restart Claude Code before using the new tools."
