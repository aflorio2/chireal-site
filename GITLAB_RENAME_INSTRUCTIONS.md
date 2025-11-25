# GitLab Repository Rename Instructions

## Overview

This document provides instructions for renaming your GitLab repository from `QCReaTE-website` to `quireal` to match the new branding.

**Current Repository URL:** `https://gitlab.ub.uni-bielefeld.de/qcreate/QCReaTE-website`
**Current Pages URL:** `https://qcreate-website-fa4cbb.pages.ub.uni-bielefeld.de/`

**Target Repository Name:** `quireal`
**Expected New Pages URL:** `https://quireal-[hash].pages.ub.uni-bielefeld.de/`

---

## Step-by-Step Instructions

### Step 1: Rename the GitLab Repository

1. Go to your GitLab repository: https://gitlab.ub.uni-bielefeld.de/qcreate/QCReaTE-website

2. Navigate to **Settings** → **General** → **Advanced**

3. Scroll down to the **"Change path"** section

4. In the **"Path"** field, change from `QCReaTE-website` to `quireal`

5. Click **"Change path"** and confirm the change

6. GitLab will automatically redirect from the old URL to the new URL

**New Repository URL will be:** `https://gitlab.ub.uni-bielefeld.de/qcreate/quireal`

---

### Step 2: Update Local Git Remote

After renaming the repository on GitLab, update your local Git configuration:

```bash
cd /Users/aflorio/Documents/GroupWebsite/site

# Update the remote URL
git remote set-url origin https://gitlab.ub.uni-bielefeld.de/qcreate/quireal.git

# Verify the change
git remote -v
```

Expected output:
```
origin  https://gitlab.ub.uni-bielefeld.de/qcreate/quireal.git (fetch)
origin  https://gitlab.ub.uni-bielefeld.de/qcreate/quireal.git (push)
```

---

### Step 3: Check New GitLab Pages URL

After the repository is renamed, GitLab Pages will rebuild with a new URL:

1. Go to **Settings** → **Pages** in your GitLab project

2. Note the new GitLab Pages URL (it will have changed to include "quireal")

3. The new URL will be something like: `https://quireal-[hash].pages.ub.uni-bielefeld.de/`

---

### Step 4: Update _config.yaml with New URL

Once you know the new GitLab Pages URL, update the site configuration:

```bash
cd /Users/aflorio/Documents/GroupWebsite/site

# Edit _config.yaml
```

Update these lines in `_config.yaml`:

```yaml
# GitLab Pages configuration
baseurl: ""
url: "https://quireal-[new-hash].pages.ub.uni-bielefeld.de"
```

Replace `[new-hash]` with the actual hash from your GitLab Pages URL.

---

### Step 5: Commit and Push the Configuration Update

```bash
cd /Users/aflorio/Documents/GroupWebsite/site

# Stage the config file
git add _config.yaml

# Commit the change
git commit -m "Update GitLab Pages URL after repository rename"

# Push to GitLab
git push origin main
```

---

### Step 6: Verify Deployment

1. Wait 1-3 minutes for the GitLab CI/CD pipeline to complete

2. Check the pipeline status: **CI/CD** → **Pipelines**

3. Once the pipeline passes, visit the new GitLab Pages URL

4. Verify the site loads correctly with all styling and images

---

## Important Notes

- **Old URL Redirect:** GitLab will automatically redirect from the old repository URL to the new one for a period of time, but it's best to update any bookmarks or external links.

- **Pages URL Change:** The GitLab Pages URL will change after the repository rename. Make sure to update `_config.yaml` with the new URL.

- **No Downtime:** The old Pages URL should continue to work temporarily while GitLab rebuilds at the new URL.

- **Update External Links:** If you've shared the website URL anywhere (email signatures, social media, department websites), update those links to the new URL.

---

## Rollback (If Needed)

If you need to revert the rename:

1. Go back to **Settings** → **General** → **Advanced**
2. Change the path back to `QCReaTE-website`
3. Update local remote: `git remote set-url origin https://gitlab.ub.uni-bielefeld.de/qcreate/QCReaTE-website.git`
4. Revert `_config.yaml` to the original URL

---

## Troubleshooting

### Issue: Can't push after renaming
**Solution:** Make sure you updated the remote URL (Step 2): `git remote set-url origin https://gitlab.ub.uni-bielefeld.de/qcreate/quireal.git`

### Issue: Pages not loading at new URL
**Solution:**
- Check the pipeline passed successfully
- Wait a few minutes for DNS propagation
- Clear your browser cache and try again

### Issue: Styling broken on new URL
**Solution:**
- Verify `baseurl` and `url` in `_config.yaml` match the new Pages URL exactly
- Make sure the baseurl is set to `""` (empty string) for the subdomain-based Pages URL

---

## Questions?

If you encounter any issues, check:
- GitLab CI/CD pipeline logs for build errors
- GitLab Pages settings to confirm the new URL
- Browser console for any 404 errors on resources

---

**Document Created:** 2025-11-09
**Related Commit:** a5d921b - "Rebrand to $\left\lvert\chi\right\rangle$real - Quantum Information and Real-time evolution in QFT"
