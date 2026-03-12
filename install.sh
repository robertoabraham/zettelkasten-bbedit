#!/bin/bash
#
# install.sh — Install the Zettelkasten BBEdit package and helper scripts.
#
# Usage:
#   ./install.sh              # install everything
#   ./install.sh --uninstall  # remove the BBEdit package
#
set -euo pipefail

BBEDIT_SUPPORT="$HOME/Library/Application Support/BBEdit"
PACKAGES_DIR="$BBEDIT_SUPPORT/Packages"
PACKAGE_NAME="Zettelkasten.bbpackage"
ZETTELKASTEN_DIR="$HOME/Zettelkasten"
SCRIPTS_DIR="$ZETTELKASTEN_DIR/.scripts"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

# ── Uninstall ──────────────────────────────────────────────────────────────────

if [[ "${1:-}" == "--uninstall" ]]; then
    echo "Uninstalling Zettelkasten BBEdit package..."
    if [[ -d "$PACKAGES_DIR/$PACKAGE_NAME" ]]; then
        rm -rf "$PACKAGES_DIR/$PACKAGE_NAME"
        echo "  Removed $PACKAGES_DIR/$PACKAGE_NAME"
    else
        echo "  Package not found (already uninstalled?)"
    fi
    echo "Note: ~/Zettelkasten and its contents were NOT removed."
    echo "Done."
    exit 0
fi

# ── Install ────────────────────────────────────────────────────────────────────

echo "Installing Zettelkasten for BBEdit..."

# 1. Check BBEdit support folder exists
if [[ ! -d "$BBEDIT_SUPPORT" ]]; then
    echo "Error: BBEdit support folder not found at:"
    echo "  $BBEDIT_SUPPORT"
    echo "Is BBEdit installed? Launch it once first."
    exit 1
fi

# 2. Install the BBEdit package
mkdir -p "$PACKAGES_DIR"
if [[ -d "$PACKAGES_DIR/$PACKAGE_NAME" ]]; then
    echo "  Updating existing package..."
    rm -rf "$PACKAGES_DIR/$PACKAGE_NAME"
fi
cp -R "$REPO_DIR/$PACKAGE_NAME" "$PACKAGES_DIR/"
echo "  Installed BBEdit package to $PACKAGES_DIR/$PACKAGE_NAME"

# 3. Create Zettelkasten directory if needed
if [[ ! -d "$ZETTELKASTEN_DIR" ]]; then
    mkdir -p "$ZETTELKASTEN_DIR"
    echo "  Created $ZETTELKASTEN_DIR"
else
    echo "  $ZETTELKASTEN_DIR already exists"
fi

# 4. Install helper scripts
mkdir -p "$SCRIPTS_DIR"
install -m 755 "$REPO_DIR/scripts/find_backlinks.py" "$SCRIPTS_DIR/"
echo "  Installed helper scripts to $SCRIPTS_DIR/"

# 5. Done
echo ""
echo "Installation complete!"
echo ""
echo "To use in BBEdit:"
echo "  1. Open any .md file in $ZETTELKASTEN_DIR"
echo "  2. Choose Markup > Preview in BBEdit"
echo "  3. Set Template to 'Zettelkasten.html'"
echo "  4. Math (\$...\$ and \$\$...\$\$) will render automatically"
echo "  5. [[Wiki-links]] become clickable links to other notes"
echo ""
echo "If your notes folder is NOT ~/Zettelkasten, edit the"
echo "ZETTELKASTEN_ROOT variable near the top of the template."
