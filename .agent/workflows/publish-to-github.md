---
description: How to publish the project to GitHub
---

# Publishing SN-Insight to GitHub

This workflow guides you through publishing your SN-Insight project to a GitHub repository.

## Prerequisites

- GitHub account
- Git installed locally
- Project ready for publishing (sensitive data removed, .gitignore configured)

## Steps

### 1. Initialize Git Repository (if not already done)

```bash
cd /Users/niteshnagpal/Developer/Personal/projects/SN-Insight
git init
```

### 2. Create .gitignore File

Ensure you have a proper `.gitignore` file to exclude sensitive and unnecessary files:

```bash
# Add common patterns if not already present
cat >> .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv

# Node
node_modules/
.next/
out/
build/
dist/

# Environment variables
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Logs
*.log
logs/

# Database
*.db
*.sqlite
*.sqlite3

# API Keys and Secrets
*.pem
*.key
secrets/
EOF
```

### 3. Review and Remove Sensitive Data

Check for any API keys, passwords, or sensitive information:

```bash
# Search for common sensitive patterns
grep -r "API_KEY" . --exclude-dir={venv,node_modules,.git}
grep -r "SECRET" . --exclude-dir={venv,node_modules,.git}
grep -r "PASSWORD" . --exclude-dir={venv,node_modules,.git}
```

Move all sensitive data to environment variables and update your `.env.example` file.

### 4. Stage All Files

```bash
git add .
```

### 5. Create Initial Commit

```bash
git commit -m "Initial commit: SN-Insight AI Research Assistant"
```

### 6. Create GitHub Repository

Option A: Via GitHub Web Interface
- Go to https://github.com/new
- Repository name: `SN-Insight` (or your preferred name)
- Description: "AI-powered research assistant for analyzing papers, extracting insights, and generating reports"
- Choose Public or Private
- **Do NOT** initialize with README, .gitignore, or license (we already have these)
- Click "Create repository"

Option B: Via GitHub CLI (if installed)
```bash
gh repo create SN-Insight --public --description "AI-powered research assistant for analyzing papers, extracting insights, and generating reports" --source=. --remote=origin
```

### 7. Add Remote Origin (if created via web interface)

```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/SN-Insight.git
```

### 8. Verify Remote

```bash
git remote -v
```

### 9. Push to GitHub

```bash
# Push to main branch
git branch -M main
git push -u origin main
```

### 10. Verify Upload

Visit your repository on GitHub to confirm all files were uploaded correctly.

## Post-Publication Steps

### Add Repository Badges (Optional)

Add badges to your README.md for better visibility:

```markdown
![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/SN-Insight)
![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/SN-Insight)
![GitHub issues](https://img.shields.io/github/issues/YOUR_USERNAME/SN-Insight)
![License](https://img.shields.io/github/license/YOUR_USERNAME/SN-Insight)
```

### Set Up GitHub Actions (Optional)

Create `.github/workflows/ci.yml` for automated testing and deployment.

### Configure Repository Settings

- Add topics/tags for discoverability
- Set up branch protection rules
- Configure GitHub Pages (if applicable)
- Add collaborators (if needed)

## Updating the Repository

After making changes:

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Description of changes"

# Push to GitHub
git push origin main
```

## Troubleshooting

### Authentication Issues

If you encounter authentication errors:

1. **Use Personal Access Token (PAT)**:
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate new token with `repo` scope
   - Use token as password when pushing

2. **Set up SSH keys**:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   cat ~/.ssh/id_ed25519.pub
   # Add the public key to GitHub Settings → SSH and GPG keys
   
   # Change remote to SSH
   git remote set-url origin git@github.com:YOUR_USERNAME/SN-Insight.git
   ```

### Large Files

If you have files larger than 100MB, use Git LFS:

```bash
git lfs install
git lfs track "*.pdf"
git lfs track "*.model"
git add .gitattributes
git commit -m "Configure Git LFS"
```

### Accidentally Committed Secrets

If you accidentally committed sensitive data:

```bash
# Remove file from Git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/sensitive/file" \
  --prune-empty --tag-name-filter cat -- --all

# Force push
git push origin --force --all
```

**Important**: Rotate any exposed credentials immediately!

## Resources

- [GitHub Documentation](https://docs.github.com)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub CLI](https://cli.github.com/)
- [Git LFS](https://git-lfs.github.com/)
