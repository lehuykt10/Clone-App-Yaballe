#!/usr/bin/env bash
# Shopify Theme Agent - cai dat phan mem cho macOS
# Cach chay (Terminal, trong thu muc du an):  bash setup/setup-mac.sh
# Chi kiem tra:                              bash setup/setup-mac.sh --check
set -u

ok()   { printf "  \033[32m[OK]\033[0m  %s\n" "$1"; }
bad()  { printf "  \033[33m[--]\033[0m  %s\n" "$1"; }
step() { printf "\n\033[36m==> %s\033[0m\n" "$1"; }
has()  { command -v "$1" >/dev/null 2>&1; }

status() {
  step "Kiem tra phan mem"
  has node    && ok "Node.js $(node -v)"            || bad "Node.js chua co"
  has python3 && ok "$(python3 --version)"          || bad "Python 3 chua co"
  has git     && ok "$(git --version)"              || bad "Git chua co"
  has shopify && ok "Shopify CLI $(shopify version)" || bad "Shopify CLI chua co"
  has claude  && ok "Claude Code $(claude --version)" || bad "Claude Code chua co"
  if npx --no-install playwright --version >/dev/null 2>&1; then ok "Playwright $(npx --no-install playwright --version)"; else bad "Playwright chua co"; fi
}

if [ "${1:-}" = "--check" ]; then status; exit 0; fi

step "1/5 Homebrew"
if ! has brew; then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  [ -x /opt/homebrew/bin/brew ] && eval "$(/opt/homebrew/bin/brew shellenv)"
  [ -x /usr/local/bin/brew ] && eval "$(/usr/local/bin/brew shellenv)"
fi
has brew && ok "Homebrew san sang"

step "2/5 Node.js, Python, Git"
has node    || brew install node
has python3 || brew install python
has git     || brew install git

step "3/5 Shopify CLI + Playwright"
npm install -g @shopify/cli@latest playwright
npx playwright install chromium

step "4/5 Claude Code"
has claude || curl -fsSL https://claude.ai/install.sh | bash || npm install -g @anthropic-ai/claude-code

step "5/5 Xong"
status
echo
echo "XONG. Mo cua so Terminal moi, vao thu muc du an va go: claude"
