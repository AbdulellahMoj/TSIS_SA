#!/bin/bash
# Student Internship Strategist — Claude Code Setup
# Run this once before using the Claude Code option

set -e

echo "=== Student Internship Strategist Setup ==="
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
  echo "ERROR: Python 3.10+ is required. Install from https://python.org"
  exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(sys.version_info.minor)')
if [ "$PYTHON_VERSION" -lt 10 ]; then
  echo "ERROR: Python 3.10 or higher is required."
  exit 1
fi
echo "✓ Python $(python3 --version)"

# Check Node
if ! command -v node &>/dev/null; then
  echo "WARNING: Node.js not found. Playwright (ATS auto-fill) will not work."
  echo "         Install Node from https://nodejs.org if you want ATS automation."
else
  echo "✓ Node $(node --version)"
fi

# Create Python virtual environment
echo ""
echo "Creating Python environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install --quiet --upgrade pip

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --quiet -r requirements.txt

echo "✓ Python dependencies installed"

# Install Playwright (optional — for ATS auto-fill)
if command -v node &>/dev/null; then
  echo ""
  read -p "Install Playwright for ATS form automation? (y/N) " install_playwright
  if [[ "$install_playwright" =~ ^[Yy]$ ]]; then
    npm install
    npx playwright install chromium
    echo "✓ Playwright installed"
    echo "  Verify with: npm run test:playwright"
  else
    echo "  Skipped. Run 'npm install && npx playwright install chromium' later if needed."
  fi
fi

# Create data directory structure
echo ""
echo "Creating data directory structure..."
mkdir -p data/applications
touch data/.gitkeep
touch data/applications/.gitkeep

# Create empty tracker
if [ ! -f data/tracker.tsv ]; then
  echo -e "company\trole\tapplied_date\tstatus\tfollow_up_date\tnotes\tlink" > data/tracker.tsv
  echo "✓ Created data/tracker.tsv"
fi

# Create config from examples if not already done
if [ ! -f config/profile.yml ]; then
  cp config/profile.example.yml config/profile.yml
  echo "✓ Created config/profile.yml from example"
fi

if [ ! -f config/targets.yml ]; then
  cp config/targets.example.yml config/targets.yml
  echo "✓ Created config/targets.yml from example"
fi

echo ""
echo "=== Setup complete ==="
echo ""
echo "Next steps:"
echo "1. Edit config/profile.yml with your details"
echo "2. Edit config/targets.yml with your target companies"
echo "3. Run: claude"
echo "4. Type: /onboarding"
echo ""
echo "Upload your CV and LinkedIn connections CSV in the Claude session."
