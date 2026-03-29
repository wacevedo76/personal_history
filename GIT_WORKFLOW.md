# Personal History - Git Workflow

## Branch Strategy

### **Main Branches:**
```
main    - Production-ready code (stable releases)
dev     - Development integration (testing)
```

### **Feature Branches:**
```
feature/v001-implementation  # v0.01 work
feature/web-dashboard        # Web interface
feature/mobile-app           # Mobile app
bugfix/installation-issue    # Bug fixes
```

## Workflow

### **1. Start New Feature**
```bash
# From dev branch
git checkout dev
git pull origin dev

# Create feature branch
git checkout -b feature/your-feature-name

# Develop your feature...
```

### **2. Commit Regularly**
```bash
git add .
git commit -m "feat: Add core v0.01 implementation"
git commit -m "fix: Resolve packaging issue"
git commit -m "docs: Update installation instructions"
```

### **3. Merge to Dev**
```bash
# When feature is complete
git checkout dev
git pull origin dev
git merge feature/your-feature-name

# Resolve conflicts if any
git push origin dev
```

### **4. Release to Main**
```bash
# When dev is stable and tested
git checkout main
git pull origin main
git merge dev

# Tag the release
git tag -a v0.01.0 -m "Release v0.01.0"
git push origin main --tags
```

## Current Branch Setup

### **Local (on OpenClaw VM):**
```
* dev                    # Current development branch
  main                   # Stable branch with v0.01
```

### **What You Should Do on Your Laptop:**

#### **Option A: Start Fresh with Dev Branch**
```bash
cd personal_history

# Fetch all branches
git fetch --all

# Create and switch to dev
git checkout -b dev origin/dev  # If remote exists
# OR
git checkout -b dev             # Create local dev
git push -u origin dev          # Push to create remote
```

#### **Option B: Continue on Main, Then Create Dev**
```bash
# Get current changes
git pull origin main

# Create dev branch from main
git checkout -b dev

# Push dev to remote
git push -u origin dev
```

## Branch Protection (Recommended)

### **GitHub Branch Protection Rules:**
1. **main branch:**
   - Require pull request reviews
   - Require status checks
   - Require linear history
   - Include administrators

2. **dev branch:**
   - Require status checks
   - Allow force push (for rebasing)

## Example Feature Development

### **Developing v0.02:**
```bash
# Start from dev
git checkout dev
git pull origin dev

# Create feature branch
git checkout -b feature/v002-multimedia

# Develop multimedia evidence feature
# ... make changes ...

# Commit
git add .
git commit -m "feat: Add multimedia evidence support"

# Push feature branch
git push -u origin feature/v002-multimedia

# Create Pull Request on GitHub:
# feature/v002-multimedia → dev
```

### **Hotfix on Main:**
```bash
# From main
git checkout main
git pull origin main

# Create hotfix branch
git checkout -b hotfix/critical-bug

# Fix the bug
# ... make changes ...

# Commit
git add .
git commit -m "fix: Resolve critical installation bug"

# Merge to main AND dev
git checkout main
git merge hotfix/critical-bug
git push origin main

git checkout dev
git merge hotfix/critical-bug
git push origin dev
```

## Commit Message Convention

### **Format:**
```
type(scope): description

[optional body]

[optional footer]
```

### **Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting, missing semi-colons, etc.
- `refactor:` Code restructuring
- `test:` Adding tests
- `chore:` Maintenance tasks

### **Examples:**
```
feat(v001): Add core file format implementation
fix(cli): Resolve ModuleNotFoundError in installation
docs(readme): Update installation instructions
test(core): Add unit tests for forward-secure hashing
```

## .gitignore Recommendations

Add to `.gitignore`:
```
# Virtual environments
venv/
env/
*.venv/

# Python
__pycache__/
*.py[cod]
*.so
.Python

# Development
*.swp
*.swo
*~
.DS_Store

# Personal History data
*.ph.json
.personal_history/
```

## Quick Reference

### **Daily Workflow:**
```bash
# Start day
git checkout dev
git pull origin dev

# Work on feature
git checkout -b feature/today-feature

# End day
git add .
git commit -m "feat: Progress on today's feature"
git push origin feature/today-feature
```

### **Weekly Integration:**
```bash
# Merge completed features to dev
git checkout dev
git merge feature/completed-feature
git push origin dev

# Delete old feature branch
git branch -d feature/completed-feature
git push origin --delete feature/completed-feature
```

## Next Steps

1. **Set up dev branch** on your laptop
2. **Protect main branch** on GitHub
3. **All future development** on feature branches off dev
4. **Regular merges** from dev to main for releases

**This professional workflow will make collaboration and maintenance much easier!**