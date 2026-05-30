#!/bin/bash

# Hide Documentation from GitHub
# Adds docs to .gitignore but keeps them locally

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Hide Documentation from GitHub${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Create docs directory
mkdir -p docs

# Move docs (except README.md)
echo -e "${BLUE}Moving docs to /docs folder...${NC}"
for file in *.md; do
    if [ "$file" != "README.md" ] && [ -f "$file" ]; then
        mv "$file" "docs/"
        echo -e "  ${GREEN}✅ Moved: $file${NC}"
    fi
done

# Add docs to .gitignore
echo ""
echo -e "${BLUE}Adding /docs to .gitignore...${NC}"

if ! grep -q "^# Documentation (local only)" .gitignore; then
    cat >> .gitignore << 'EOF'

# Documentation (local only)
docs/
*_FIX.md
*_GUIDE.md
*_SUMMARY.md
*_CHECKLIST.md
*_STATUS.md
*_UPDATES.md
SECURITY_*.md
EOF
    echo -e "${GREEN}✅ Added to .gitignore${NC}"
else
    echo -e "${YELLOW}⏭️  Already in .gitignore${NC}"
fi

# Remove from git if already tracked
echo ""
echo -e "${BLUE}Removing from git tracking...${NC}"
git rm --cached -r docs/ 2>/dev/null || true
git rm --cached *_FIX.md *_GUIDE.md *_SUMMARY.md 2>/dev/null || true

echo ""
echo -e "${GREEN}✅ Documentation hidden from GitHub!${NC}"
echo ""
echo "What happened:"
echo "  ✅ Docs moved to /docs folder"
echo "  ✅ Added to .gitignore"
echo "  ✅ Removed from git tracking"
echo "  ✅ Still available locally"
echo ""
echo "Next steps:"
echo "  git add .gitignore"
echo "  git commit -m 'Hide documentation from GitHub'"
echo "  git push"
echo ""
