#!/bin/bash

# Security Fix Script - Remove .env from Git History
# WARNING: This rewrites git history!

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${RED}========================================${NC}"
echo -e "${RED}🚨 SECURITY FIX - Remove .env from Git${NC}"
echo -e "${RED}========================================${NC}"
echo ""

echo -e "${YELLOW}⚠️  WARNING: This will rewrite git history!${NC}"
echo -e "${YELLOW}⚠️  All team members will need to re-clone the repo!${NC}"
echo ""

read -p "Have you changed your email password? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}❌ Please change your email password FIRST!${NC}"
    echo "Go to: https://myaccount.google.com/apppasswords"
    exit 1
fi

read -p "Have you updated server/.env with the new password? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}❌ Please update server/.env with new password FIRST!${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}Choose method to remove .env from history:${NC}"
echo "1) git filter-branch (built-in, slower)"
echo "2) git filter-repo (faster, requires installation)"
echo "3) Cancel"
read -p "Choose option [1]: " METHOD
METHOD=${METHOD:-1}

if [ "$METHOD" == "3" ]; then
    echo "Cancelled."
    exit 0
fi

# Backup current branch
CURRENT_BRANCH=$(git branch --show-current)
echo -e "${BLUE}Current branch: $CURRENT_BRANCH${NC}"

# Create backup
echo -e "${BLUE}Creating backup...${NC}"
BACKUP_DIR="../Driftwood_backup_$(date +%Y%m%d_%H%M%S)"
cp -r . "$BACKUP_DIR"
echo -e "${GREEN}✅ Backup created at: $BACKUP_DIR${NC}"

if [ "$METHOD" == "1" ]; then
    echo -e "${BLUE}Using git filter-branch...${NC}"
    
    # Remove .env files from all commits
    git filter-branch --force --index-filter \
      'git rm --cached --ignore-unmatch server/.env client/.env .env' \
      --prune-empty --tag-name-filter cat -- --all
    
    echo -e "${GREEN}✅ Removed .env from history${NC}"
    
elif [ "$METHOD" == "2" ]; then
    # Check if git-filter-repo is installed
    if ! command -v git-filter-repo &> /dev/null; then
        echo -e "${YELLOW}git-filter-repo not found. Installing...${NC}"
        pip3 install git-filter-repo
    fi
    
    echo -e "${BLUE}Using git-filter-repo...${NC}"
    
    # Remove .env files
    git filter-repo --path server/.env --invert-paths --force
    git filter-repo --path client/.env --invert-paths --force
    git filter-repo --path .env --invert-paths --force
    
    echo -e "${GREEN}✅ Removed .env from history${NC}"
fi

# Clean up
echo -e "${BLUE}Cleaning up...${NC}"
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo -e "${GREEN}✅ Cleanup complete${NC}"

# Verify .env is not tracked
echo ""
echo -e "${BLUE}Verifying .env is not tracked...${NC}"
if git ls-files | grep -q "\.env$"; then
    echo -e "${RED}❌ .env files still tracked!${NC}"
    git ls-files | grep "\.env$"
    exit 1
else
    echo -e "${GREEN}✅ No .env files tracked${NC}"
fi

echo ""
echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}Next Steps:${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""
echo "1. Force push to GitHub:"
echo -e "   ${BLUE}git push origin --force --all${NC}"
echo -e "   ${BLUE}git push origin --force --tags${NC}"
echo ""
echo "2. Verify on GitHub:"
echo "   - Go to your repo"
echo "   - Search for your password"
echo "   - Should find nothing"
echo ""
echo "3. Team members must re-clone:"
echo -e "   ${BLUE}git clone https://github.com/moses-25/Driftwood.git${NC}"
echo ""
echo -e "${GREEN}Backup saved at: $BACKUP_DIR${NC}"
echo ""
