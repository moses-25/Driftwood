#!/bin/bash

# Organize Documentation Script
# Moves all documentation files to /docs folder

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Organizing Documentation Files${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Create docs directory
mkdir -p docs

# Files to keep in root
KEEP_IN_ROOT=(
    "README.md"
)

# Move all .md files except those in KEEP_IN_ROOT
echo -e "${BLUE}Moving documentation files to /docs...${NC}"
for file in *.md; do
    if [[ " ${KEEP_IN_ROOT[@]} " =~ " ${file} " ]]; then
        echo "  ⏭️  Keeping: $file (in root)"
    else
        if [ -f "$file" ]; then
            mv "$file" "docs/"
            echo -e "  ${GREEN}✅ Moved: $file → docs/${NC}"
        fi
    fi
done

# Create docs/README.md as index
cat > docs/README.md << 'EOF'
# Driftwood Café - Documentation

## 📚 Documentation Index

### 🚀 Getting Started
- [Complete Project Status](COMPLETE_PROJECT_STATUS.md) - Full overview
- [Final Checklist](FINAL_CHECKLIST.md) - What to do next
- [Recent Updates](README_UPDATES.md) - Latest changes

### 🔧 Feature Fixes
- [Fixes Summary](FIXES_SUMMARY.md) - All fixes explained
- [Menu Products Fix](MENU_PRODUCTS_FIX.md) - Menu display fix
- [Map Optimization](MAP_OPTIMIZATION_GUIDE.md) - Map performance

### 📸 Image Upload
- [Start Here - Images](START_HERE_IMAGES.md) - Quick start
- [Quick Start Guide](QUICK_START_IMAGE_UPLOAD.md) - Fast setup
- [Image Upload Summary](IMAGE_UPLOAD_SUMMARY.md) - Overview
- [Manual Upload Guide](MANUAL_IMAGE_UPLOAD_GUIDE.md) - Detailed steps

### 🔒 Security
- [Security Quick Fix](SECURITY_QUICK_FIX.md) - Emergency fix
- [Security Fix Urgent](SECURITY_FIX_URGENT.md) - Complete guide

---

**Main README:** [../README.md](../README.md)
EOF

echo ""
echo -e "${GREEN}✅ Documentation organized!${NC}"
echo ""
echo "Structure:"
echo "  /"
echo "  ├── README.md (main)"
echo "  └── docs/"
echo "      ├── README.md (index)"
echo "      └── [all other .md files]"
echo ""
