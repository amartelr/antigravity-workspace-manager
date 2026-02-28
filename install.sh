#!/bin/bash
# Antigravity Workspace Manager - Installer

INSTALL_DIR="$HOME/.antigravity-wsm"
REPO_URL="https://github.com/amartelr/antigravity-workspace-manager.git"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Installing Antigravity Workspace Manager...${NC}"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Error: python3 is not installed.${NC}"
    exit 1
fi

# Check for Git
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Error: git is not installed.${NC}"
    exit 1
fi

# 1. Clone or Update the repository
if [ -d "$INSTALL_DIR" ]; then
    echo -e "📂 Updating existing installation in ${INSTALL_DIR}..."
    cd "$INSTALL_DIR" && git pull
else
    echo -e "📦 Cloning into ${INSTALL_DIR}..."
    git clone --depth 1 "$REPO_URL" "$INSTALL_DIR"
fi

# 2. Initializing (cloning the skills)
cd "$INSTALL_DIR"
python3 workspace-manager.py init

# 3. Setting up the alias 'wsm'
SHELL_CONFIG=""
# Detect shell
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        SHELL_CONFIG="$HOME/.bash_profile"
    else
        SHELL_CONFIG="$HOME/.bashrc"
    fi
fi

if [ -n "$SHELL_CONFIG" ]; then
    # Create file if it doesn't exist
    touch "$SHELL_CONFIG"
    
    if ! grep -q "workspace-manager.py" "$SHELL_CONFIG"; then
        echo "" >> "$SHELL_CONFIG"
        echo "# Antigravity Workspace Manager Alias" >> "$SHELL_CONFIG"
        echo "alias wsm='python3 $INSTALL_DIR/workspace-manager.py'" >> "$SHELL_CONFIG"
        echo -e "${GREEN}✅ Alias 'wsm' added to ${SHELL_CONFIG}${NC}"
    else
        echo -e "ℹ️  Alias 'wsm' already exists in ${SHELL_CONFIG}"
    fi
fi

echo -e "\n${GREEN}✨ Installation complete!${NC}"
echo -e "👉 Please ${BLUE}restart your terminal${NC} or run: ${BLUE}source ${SHELL_CONFIG}${NC}"
echo -e "🚀 Then, simply type ${GREEN}wsm wizard${NC} from any project folder to start!"
