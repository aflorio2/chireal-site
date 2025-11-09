# Greene Lab Website Setup Implementation Plan

## Overview

This plan guides the setup of a theoretical physics group website using the Greene Lab template, deployed to GitLab Pages. The website will feature automated citation management via Manubot (manual local approach), a clean minimalist design optimized for academic research groups, and straightforward YAML-based content management.

**Technology Stack:**
- **Static Site Generator**: Jekyll 4.3+
- **Template**: Greene Lab Website Template (BSD-3-Clause license)
- **Citation Management**: Manubot (manual local processing)
- **Hosting**: GitLab Pages (free .gitlab.io subdomain)
- **CI/CD**: GitLab CI/CD (simple Jekyll build)

**Timeline**: 4-6 weeks (16-24 total hours)

## Current State Analysis

**Starting Point:**
- Empty project directory at `/Users/aflorio/Documents/GroupWebsite/`
- Existing GitLab account available
- No existing content to migrate
- Fresh start - all content will be created during setup
- Using default GitLab Pages domain (username.gitlab.io)

**Research Completed:**
- Comprehensive research document at `thoughts/shared/research/2025-11-07-physics-group-website-design-static-site-generators.md`
- Decision made: Greene Lab template with Manual Local Manubot approach
- Platform decision: GitLab Pages hosting

## Desired End State

A fully functional theoretical physics group website with:
- Clean, professional design optimized for academic research
- Automated citation management via Manubot (DOI-based)
- Team member profiles with photos and links
- Publication list with thumbnails and arXiv links
- Project pages describing research areas
- Blog section for news and updates
- Mobile-responsive design
- Deployed to GitLab Pages with SSL/HTTPS
- Simple maintenance workflow (~2 minutes to add a publication)

### Verification of End State:
- Website is live at `https://[username].gitlab.io/[project-name]/`
- All team members added with photos and bios
- At least 3-5 publications displayed with auto-fetched metadata
- At least 2-3 project pages with descriptions
- About page with research focus description
- Blog with at least one sample post
- Site loads on mobile and desktop
- GitLab CI/CD pipeline successfully builds and deploys on push to main branch

## What We're NOT Doing

- **No custom domain setup** (using default GitLab Pages subdomain)
- **No migration from existing site** (fresh content only)
- **No advanced features** (comments, search, analytics) in initial setup
- **No automated CI/CD Manubot** (using manual local approach)
- **No custom Jekyll plugins** beyond what Greene Lab includes
- **No multi-language support** (English only initially)
- **No extensive customization** of template structure (keeping Greene Lab architecture)
- **No integration with external services** (newsletter, CRM, etc.) in initial setup

## Implementation Approach

The implementation follows a 6-phase approach:

1. **Phase 1**: Fork and clone the Greene Lab template, verify GitHub source
2. **Phase 2**: Set up local development environment (Ruby, Jekyll, Manubot)
3. **Phase 3**: Configure GitLab CI/CD for automatic deployment
4. **Phase 4**: Basic customization (branding, colors, site info)
5. **Phase 5**: Populate content (team, publications, projects, pages)
6. **Phase 6**: Polish design, test thoroughly, and launch

Each phase includes specific file changes, automated tests, and manual verification steps. Phases build incrementally - each phase produces a working state before proceeding.

---

## Phase 1: Fork Greene Lab Template and Initial GitLab Setup

### Overview
Fork the Greene Lab template from GitHub to GitLab, verify the template structure, and prepare the GitLab repository for development.

### Changes Required:

#### 1. Fork Template from GitHub
**Source Repository**: https://github.com/greenelab/lab-website-template
**Target**: New GitLab repository

**Process**:
1. Create new GitLab project (empty repository)
2. Clone GitHub template locally
3. Update Git remote to point to GitLab
4. Push to GitLab repository

**Commands**:
```bash
# Create a new directory for the project
cd /Users/aflorio/Documents/GroupWebsite/

# Clone the Greene Lab template from GitHub
git clone https://github.com/greenelab/lab-website-template.git site
cd site

# Remove GitHub origin and add GitLab origin
git remote remove origin
git remote add origin https://gitlab.com/[YOUR-USERNAME]/[PROJECT-NAME].git

# Push to GitLab
git push -u origin main
```

**Note**: Replace `[YOUR-USERNAME]` with your GitLab username and `[PROJECT-NAME]` with your desired project name (e.g., `physics-group-website`).

#### 2. Verify Template Structure
**Directory Structure Expected**:
```
site/
├── _data/                 # YAML data files (citations, members, projects)
│   ├── citations.yaml
│   ├── members.yaml
│   └── projects.yaml
├── _includes/             # Reusable components
├── _layouts/              # Page layouts
├── _posts/                # Blog posts
├── _styles/               # SCSS styles
│   └── variables.scss     # Color/font variables
├── images/                # Image assets
├── _config.yml            # Jekyll configuration
├── Gemfile                # Ruby dependencies
├── index.md               # Homepage
├── about.md               # About page
├── research.md            # Research page
├── team.md                # Team page
└── README.md              # Template documentation
```

**Files to Inspect**:
- `_config.yml` - Jekyll site configuration
- `Gemfile` - Ruby gem dependencies
- `_data/*.yaml` - Data file structure
- `README.md` - Template usage instructions

#### 3. Enable GitLab Pages
**GitLab Project Settings**:
1. Navigate to Settings > Pages in GitLab project
2. Note the default URL: `https://[username].gitlab.io/[project-name]/`
3. Ensure Pages is enabled (default on GitLab.com)

### Success Criteria:

#### Automated Verification:
- [x] GitLab repository created and accessible
- [x] Template successfully cloned: `ls -la site/` shows expected files
- [x] Git remote points to GitLab: `cd site && git remote -v`
- [x] All template files present: `test -f _config.yml && test -f Gemfile && test -d _data`

#### Manual Verification:
- [x] GitLab repository page loads in browser
- [x] Repository shows full Greene Lab template file structure
- [x] GitLab Pages setting is enabled (check Settings > Pages)
- [x] No errors or missing files in repository view

**Implementation Note**: After completing automated verification, manually confirm the GitLab repository is properly set up with all files visible before proceeding to Phase 2.

---

## Phase 2: Local Development Environment Setup

### Overview
Install all required dependencies (Ruby, Jekyll, Bundler, Manubot) and verify the site builds and runs locally.

### Changes Required:

#### 1. Install Ruby and Bundler
**Required Version**: Ruby 3.0+ (check with `ruby --version`)

**macOS Installation** (if Ruby not installed or outdated):
```bash
# Using Homebrew (recommended)
brew install ruby

# Add to PATH (add to ~/.zshrc or ~/.bash_profile)
export PATH="/opt/homebrew/opt/ruby/bin:$PATH"

# Verify Ruby version
ruby --version  # Should be 3.0+
```

**Install Bundler**:
```bash
gem install bundler
```

#### 2. Install Jekyll Dependencies
**Directory**: `site/`

**Commands**:
```bash
cd site/

# Install all Jekyll gems from Gemfile
bundle install

# This installs:
# - Jekyll (~> 4.3)
# - GitHub Pages gem (for compatibility)
# - jekyll-feed (RSS feeds)
# - jekyll-sitemap (SEO)
# - Other dependencies
```

**Expected Output**:
- "Bundle complete!" message
- All gems installed to `vendor/bundle/` (or system location)

#### 3. Install Manubot
**Required for Citation Management**

**Using npm** (recommended):
```bash
# Install Node.js/npm if not present (check with: node --version)
brew install node  # macOS with Homebrew

# Install Manubot globally
npm install --global manubot

# Verify installation
manubot --version
```

**Alternative using Python** (if npm not preferred):
```bash
pip3 install manubot

# Verify installation
manubot --version
```

#### 4. Test Local Build
**Directory**: `site/`

**Build the site**:
```bash
cd site/

# Build static site to _site/ directory
bundle exec jekyll build

# Expected output:
# Configuration file: _config.yml
# Source: [...]
# Destination: _site
# Generating... done in X seconds.
```

**Serve locally**:
```bash
# Run local development server
bundle exec jekyll serve

# Expected output:
# Server address: http://127.0.0.1:4000
# Server running... press ctrl-c to stop.
```

**Access in browser**: http://localhost:4000

#### 5. Verify Site Functions
**Checks to perform** in browser (http://localhost:4000):
- Homepage loads with Greene Lab default content
- Navigation menu works (About, Research, Team, etc.)
- Team page shows sample members
- Publications page shows sample citations
- No broken images or 404 errors

### Success Criteria:

#### Automated Verification:
- [x] Ruby installed: `ruby --version` shows 3.0 or higher (Ruby 3.3.10 installed)
- [x] Bundler installed: `bundle --version` works
- [x] Jekyll dependencies installed: `bundle exec jekyll --version` works
- [x] Manubot installed: `manubot --version` shows version number (v0.6.1)
- [x] Site builds successfully: `cd site && bundle exec jekyll build` completes without errors
- [x] Build output directory created: `test -d site/_site`

#### Manual Verification:
- [x] Local server starts without errors
- [x] Website loads at http://localhost:4000
- [x] All navigation links work
- [x] Sample content displays correctly (team, publications)
- [x] No console errors in browser developer tools
- [x] Images load properly
- [x] Mobile responsive view works (test with browser dev tools)

**Implementation Note**: After automated verification passes, manually browse the local site to confirm all features work correctly. Test navigation, verify sample content displays, and check browser console for errors. Only proceed to Phase 3 after confirming the local site is fully functional.

---

## Phase 3: GitLab CI/CD Configuration

### Overview
Configure GitLab CI/CD to automatically build and deploy the Jekyll site to GitLab Pages on every push to the main branch.

### Changes Required:

#### 1. Create GitLab CI/CD Configuration
**File**: `site/.gitlab-ci.yml` (create new file)

**Content**:
```yaml
# GitLab CI/CD configuration for Greene Lab Jekyll site
# Manual Local Manubot approach - Manubot runs locally, not in CI

image: ruby:3.2

# Cache gems to speed up builds
cache:
  paths:
    - vendor/bundle

# Install Jekyll dependencies before building
before_script:
  - gem install bundler
  - bundle install --path vendor/bundle --jobs $(nproc)

# Pages job - builds and deploys the site
pages:
  stage: deploy
  script:
    # Build Jekyll site to public/ directory
    - bundle exec jekyll build -d public

    # Show build info
    - echo "Site built successfully to public/"
    - ls -lh public/ | head -20

  artifacts:
    paths:
      - public

  rules:
    # Only deploy on main branch
    - if: $CI_COMMIT_BRANCH == "main"

  environment: production
```

**Why This Configuration**:
- Uses Ruby 3.2 Docker image (stable, maintained)
- Caches gems to speed up builds (saves ~30-60 seconds per build)
- Builds to `public/` directory (GitLab Pages requirement)
- Only deploys on `main` branch (protects production)
- No Manubot in CI - citations processed locally before push

#### 2. Update Jekyll Configuration for GitLab Pages
**File**: `site/_config.yml`

**Changes**:
```yaml
# Update baseurl for GitLab Pages
baseurl: "/[PROJECT-NAME]"  # Replace with your project name

# Update url
url: "https://[USERNAME].gitlab.io"  # Replace with your GitLab username

# Ensure correct permalink structure
permalink: /:year/:month/:day/:title/

# Exclude files from build
exclude:
  - Gemfile
  - Gemfile.lock
  - node_modules
  - vendor/bundle/
  - .sass-cache/
  - .jekyll-cache/
  - gemfiles/
  - README.md
  - LICENSE.md
```

**Note**: Replace placeholders:
- `[PROJECT-NAME]` with your GitLab project name
- `[USERNAME]` with your GitLab username

#### 3. Test CI/CD Pipeline
**Commands**:
```bash
cd site/

# Add the new CI/CD configuration
git add .gitlab-ci.yml _config.yml

# Commit the changes
git commit -m "Add GitLab CI/CD configuration for Pages deployment"

# Push to GitLab
git push origin main
```

**Pipeline Monitoring**:
1. Go to GitLab project > CI/CD > Pipelines
2. Watch the pipeline run (should take 1-3 minutes)
3. Check for "passed" status
4. Navigate to Settings > Pages to see deployed URL

#### 4. Verify Deployment
**URL**: `https://[username].gitlab.io/[project-name]/`

**Checks**:
- Pages URL is active (may take 1-2 minutes after pipeline completes)
- Site loads correctly
- All assets (CSS, images) load properly
- Navigation works
- HTTPS works (GitLab provides automatic SSL)

### Success Criteria:

#### Automated Verification:
- [x] CI/CD configuration file exists: `test -f site/.gitlab-ci.yml`
- [x] Jekyll config updated: `grep "baseurl:" site/_config.yml`
- [x] Git status clean: `cd site && git status` shows no uncommitted CI/CD changes
- [x] Pipeline triggered: Check GitLab project > CI/CD > Pipelines
- [x] Pipeline passed: Latest pipeline shows green checkmark
- [x] Pages deployed: GitLab Settings > Pages shows "Deployed" status

#### Manual Verification:
- [x] GitLab Pages URL loads in browser
- [x] Homepage displays correctly with all styling
- [x] All pages accessible via navigation
- [x] Images and assets load (no broken resources)
- [x] HTTPS works (lock icon in browser)
- [x] No 404 errors when clicking internal links
- [x] CSS styling matches local development version
- [x] Mobile responsive view works on deployed site

**Notes on Completion**:
- Actual GitLab Pages URL: `https://qcreate-website-fa4cbb.pages.ub.uni-bielefeld.de/`
- Fixed Ruby 3.3 compatibility issues (sass-embedded, posix-spawn)
- Fixed baseurl configuration for subdomain-based Pages URL
- Pages access control: Can be set to Public or Private in Settings → Pages (independent of repository visibility)

**Implementation Note**: After the pipeline passes automated checks, manually visit the GitLab Pages URL and thoroughly test the site. Verify all pages load, navigation works, and styling is correct. The baseurl setting is critical - if pages load but styling is broken, double-check the baseurl matches your project name. Only proceed to Phase 4 after confirming the deployed site works correctly.

---

## Phase 4: Basic Customization (Branding & Site Info)

### Overview
Customize the Greene Lab template with your theoretical physics group's branding, colors, and basic information. This phase transforms the template from "Greene Lab" to your group's identity.

### Changes Required:

#### 1. Update Site Configuration
**File**: `site/_config.yml`

**Changes**:
```yaml
# Site settings
title: "[Your Lab Name]"
tagline: "Theoretical Physics Research Group"
description: "Quantum field theory, gravitational physics, and cosmology"

# Contact information
email: "contact@[yourdomain].edu"
phone: "+1-XXX-XXX-XXXX"
address: |
  Department of Physics
  [Your University]
  [City, State ZIP]

# Social media (update with your handles, or remove lines)
github: [your-github-username]
twitter: [your-twitter-handle]
youtube: [your-youtube-channel]

# Research interests (for SEO and display)
keywords:
  - quantum field theory
  - general relativity
  - black holes
  - cosmology
  - theoretical physics

# Logo/favicon (update in Phase 5 with actual image)
logo: images/logo.png
favicon: images/favicon.ico

# Footer information
footer: |
  © 2025 [Your Lab Name]. All rights reserved.
  Built with [Greene Lab Website Template](https://github.com/greenelab/lab-website-template).
```

**Note**: Replace all `[placeholders]` with actual values.

#### 2. Customize Color Scheme
**File**: `site/_styles/variables.scss`

**Changes for Theoretical Physics Theme**:
```scss
// Color palette - Dark red and gold for theoretical physics
$primary: #8B0000;        // Dark red (deep crimson)
$accent: #DAA520;         // Gold
$secondary: #2F4F4F;      // Dark slate gray
$background: #FFFFFF;     // White
$text: #333333;           // Dark gray text
$light-gray: #F5F5F5;     // Light background
$medium-gray: #CCCCCC;    // Borders

// Typography
$font-heading: "Computer Modern Serif", "Georgia", serif;  // LaTeX-like
$font-body: "Source Sans Pro", "Helvetica Neue", sans-serif;
$font-mono: "Fira Code", "Monaco", monospace;

// Sizes
$text-size: 16px;
$heading-size: 2.5rem;
$spacing: 1.5rem;

// Effects
$border-radius: 8px;
$box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
$transition: 0.3s ease;
```

**Alternative Color Schemes** (choose one):

**Option A: Classic Academic Blue**
```scss
$primary: #003366;        // Navy blue
$accent: #0066CC;         // Bright blue
$secondary: #666666;      // Medium gray
```

**Option B: Modern Minimalist**
```scss
$primary: #000000;        // Black
$accent: #4A90E2;         // Sky blue
$secondary: #7F7F7F;      // Gray
```

**Option C: Physics Purple/Blue**
```scss
$primary: #5B2C6F;        // Deep purple
$accent: #00CED1;         // Turquoise
$secondary: #2F4F4F;      // Dark slate
```

#### 3. Update Homepage Content
**File**: `site/index.md`

**Changes**:
```markdown
---
title: Home
layout: default
---

# Welcome to [Your Lab Name]

## Theoretical Physics Research Group

We are a research group in the Department of Physics at [Your University],
specializing in quantum field theory, gravitational physics, and cosmology.

Our research focuses on:
- Quantum field theory in curved spacetime
- Black hole thermodynamics and information paradox
- Early universe cosmology and inflation
- Quantum gravity and string theory

{:.center}
[Learn More About Our Research](/research) | [Meet the Team](/team)

---

## Latest Publications

{% include list.html data="citations" component="citation" %}

---

## Featured Projects

{% include list.html data="projects" component="project" %}

---

## News & Updates

{% include list.html data="posts" component="post" limit=3 %}
```

**Note**:
- Replace `[Your Lab Name]` and `[Your University]` with actual names
- Customize research focus areas to match your group's work
- Keep Jekyll Liquid syntax (`{% %}`) intact

#### 4. Update About Page
**File**: `site/about.md`

**Changes**:
```markdown
---
title: About
layout: default
---

# About Our Research Group

[Your Lab Name] is a theoretical physics research group at [Your University].
We investigate fundamental questions in quantum field theory, gravitational
physics, and cosmology.

## Our Mission

Our research aims to advance the understanding of [describe your research goals].
We combine analytical methods, numerical simulations, and collaboration with
experimental groups to tackle the most challenging problems in modern physics.

## Research Areas

### Quantum Field Theory
[Brief description of QFT research]

### Gravitational Physics
[Brief description of gravity research]

### Cosmology
[Brief description of cosmology research]

## Facilities

We have access to:
- High-performance computing clusters
- [Other facilities or resources]

## Collaborations

We collaborate with research groups at:
- [Institution 1]
- [Institution 2]
- [Institution 3]

## Funding

Our research is supported by:
- [Funding Agency 1]
- [Funding Agency 2]
- [Grant numbers if applicable]
```

#### 5. Test Customization Locally
**Commands**:
```bash
cd site/

# Build site with new customization
bundle exec jekyll build

# Serve locally to preview
bundle exec jekyll serve

# Open http://localhost:4000 in browser to review changes
```

**Visual Checks**:
- Colors applied correctly (headers, links, buttons)
- Typography looks appropriate
- Homepage shows updated content
- About page shows group information
- Site title in browser tab matches your lab name

#### 6. Commit and Deploy
**Commands**:
```bash
cd site/

# Add all customized files
git add _config.yml _styles/variables.scss index.md about.md

# Commit with descriptive message
git commit -m "Customize site branding, colors, and basic content"

# Push to GitLab (triggers deployment)
git push origin main
```

### Success Criteria:

#### Automated Verification:
- [x] Config file updated: `grep "title:" site/_config.yaml` shows group name
- [x] Colors customized: Custom purple/cyan theme in `site/_styles/-theme.scss`
- [x] Homepage updated: Homepage shows new content with group branding
- [x] About page created: `site/about/index.md` exists with group content
- [x] Local build succeeds: `cd site && bundle exec jekyll build` completes
- [x] **REBRAND TO QuIReal**: Updated all references from QCReaTE to QuIReal (Quantum Information and Real-time evolution in QFT) throughout site
- [x] Git changes committed: `cd site && git status` shows clean state
- [x] GitLab pipeline passes: Latest pipeline shows green checkmark
- [ ] **Update GitLab repository name**: Rename GitLab project from "qcreate-website-fa4cbb" to "quireal" (see GITLAB_RENAME_INSTRUCTIONS.md)
- [ ] **Update _config.yaml URLs**: Update baseurl and url to reflect new GitLab Pages URL after repository rename

#### Manual Verification:
- [x] Local site (http://localhost:4000) shows new branding
- [x] Colors match chosen scheme throughout site (custom purple/cyan)
- [x] Typography is readable and appropriate
- [x] Lab name "QuIReal" appears in header and browser tab
- [x] Homepage content reflects QuIReal focus on quantum information and real-time evolution
- [x] About page describes QuIReal research areas accurately
- [x] Custom quantum dynamics background image added
- [x] Custom logo created with quantum ket notation |χ⟩ and orbiting particles
- [x] Deployed site shows updated QuIReal branding
- [x] No styling regressions (all pages still look good)

**Implementation Note**: After automated verification passes, review both local and deployed versions of the site. Pay attention to color contrast (ensure text is readable), typography consistency, and overall aesthetic. The branding should feel cohesive across all pages. If colors don't look right, adjust `_styles/variables.scss` and rebuild. Only proceed to Phase 5 after confirming the customized design meets your vision.

**QuIReal Rebranding (Completed 2025-11-09)**:
- [x] Updated site content files (_config.yaml, index.md, about/index.md) with QuIReal branding
- [x] Changed title to "QuIReal - Quantum Information and Real-time evolution in QFT"
- [x] Changed subtitle to "Adrien Florio's Emmy Noether group"
- [x] Created logo_with_name.svg variant (saved for future use)
- [x] Committed and pushed changes to GitLab
- [x] Created GITLAB_RENAME_INSTRUCTIONS.md for repository rename steps
- [ ] Rename GitLab repository to "quireal" (see GITLAB_RENAME_INSTRUCTIONS.md)
- [ ] Update git remote URL locally after rename
- [ ] Update _config.yaml with new GitLab Pages URL after rename

**Note**: Repository rename steps documented in GITLAB_RENAME_INSTRUCTIONS.md for execution when convenient.

---

## Phase 5: Content Population (Team, Publications, Projects)

### Overview
Add real content to the website: team members, publications, research projects, and initial blog posts. This phase brings the site to life with your group's actual information.

### Changes Required:

#### 1. Add Team Member Photos
**Directory**: `site/images/team/`

**Process**:
```bash
cd site/

# Create team images directory if it doesn't exist
mkdir -p images/team/

# Add team member photos (300x300px recommended)
# Copy photos to images/team/
# Example: images/team/jane-doe.jpg, images/team/john-smith.jpg
```

**Image Guidelines**:
- Format: JPG or PNG
- Size: 300x300px (square, will be displayed in circles)
- File size: < 200KB per image (optimize with ImageOptim or similar)
- Naming: Use lowercase with hyphens (e.g., `jane-doe.jpg`)

#### 2. Configure Team Members
**File**: `site/_data/members.yaml`

**Changes** (replace all sample data):
```yaml
# Principal Investigator
- name: Prof. [PI Name]
  image: images/team/[pi-photo].jpg
  role: pi
  affiliation: [Your University]
  description: >
    [Brief research description - 2-3 sentences about PI's research interests
    and background]
  links:
    home-page: https://[personal-website]
    email: [email]@[domain].edu
    orcid: 0000-0002-XXXX-XXXX
    google-scholar: [scholar-id]
    github: [github-username]

# Postdocs
- name: Dr. [Postdoc Name]
  image: images/team/[postdoc-photo].jpg
  role: postdoc
  affiliation: [Your University]
  description: >
    [Research focus - 1-2 sentences]
  links:
    email: [email]@[domain].edu
    orcid: 0000-0002-XXXX-XXXX

# Graduate Students
- name: [Student Name]
  image: images/team/[student-photo].jpg
  role: phd
  affiliation: [Your University]
  description: >
    [Research topic and year]
  links:
    email: [email]@[domain].edu
    github: [github-username]

# Undergraduate Students (optional)
- name: [Undergrad Name]
  image: images/team/[undergrad-photo].jpg
  role: undergrad
  affiliation: [Your University]
  description: >
    [Project description]
  links:
    email: [email]@[domain].edu

# Alumni (optional)
- name: [Alumni Name]
  image: images/team/[alumni-photo].jpg
  role: alumni
  affiliation: [Current Position, Institution]
  description: >
    [What they did in the group, where they are now]
  links:
    home-page: https://[current-website]
```

**Note**:
- Replace all `[placeholders]` with actual information
- Add as many members as needed
- Keep `role` values: `pi`, `postdoc`, `phd`, `undergrad`, `alumni`

#### 3. Add Publications with Manubot
**File**: `site/_data/citations.yaml`

**Step 1: Clear sample data**
```yaml
# Remove all existing sample citations from Greene Lab template
```

**Step 2: Add your publications (using DOIs)**
```yaml
# Example publications - replace with your actual DOIs
- id: doi:10.1103/PhysRevD.109.064023
  # Manubot will auto-fetch: title, authors, journal, date, abstract

  # Optional: Add custom buttons/links
  buttons:
    - type: preprint
      text: arXiv
      link: https://arxiv.org/abs/2403.12345
    - type: source
      text: Code
      link: https://github.com/yourlab/project-code

- id: doi:10.1103/PhysRevLett.130.101801
  buttons:
    - type: preprint
      text: arXiv
      link: https://arxiv.org/abs/2301.54321

- id: doi:10.1088/1475-7516/2024/03/042
  buttons:
    - type: preprint
      text: arXiv
      link: https://arxiv.org/abs/2312.98765
    - type: data
      text: Data
      link: https://zenodo.org/record/1234567
```

**Step 3: Run Manubot locally to fetch metadata**
```bash
cd site/

# Process citations with Manubot
manubot process --content-directory=.

# This creates/updates _data/citations-output.yaml with full metadata
# Check the output:
cat _data/citations-output.yaml
```

**Expected Output**:
- `_data/citations-output.yaml` created
- File contains full citation metadata (title, authors, journal, date, etc.)
- No errors from Manubot

**Troubleshooting**:
- If DOI not found: Double-check DOI format (must be valid and public)
- If Manubot fails: Check internet connection, try again
- For non-DOI publications: See manual citation format in Greene Lab docs

#### 4. Configure Research Projects
**File**: `site/_data/projects.yaml`

**Changes** (replace sample data):
```yaml
# Project 1
- title: Quantum Field Theory in Curved Spacetime
  subtitle: Black Hole Thermodynamics
  image: images/projects/qft-curved.jpg
  description: >
    We investigate quantum field theory in curved spacetime backgrounds,
    focusing on black hole thermodynamics and the information paradox.
    Our approach combines analytical methods with numerical simulations
    to understand quantum effects near event horizons.
  tags:
    - quantum field theory
    - general relativity
    - black holes
  links:
    website: https://project-site.org
    github: https://github.com/yourlab/qft-project

# Project 2
- title: Early Universe Cosmology
  subtitle: Inflation and Primordial Fluctuations
  image: images/projects/cosmology.jpg
  description: >
    Our cosmology research explores inflationary models and the generation
    of primordial density fluctuations. We develop theoretical frameworks
    to connect early universe physics with observable signatures in the
    cosmic microwave background.
  tags:
    - cosmology
    - inflation
    - CMB
  links:
    paper: https://arxiv.org/abs/XXXX.XXXXX

# Project 3
- title: Quantum Gravity Phenomenology
  subtitle: String Theory and Loop Quantum Gravity
  image: images/projects/quantum-gravity.jpg
  description: >
    We investigate phenomenological signatures of quantum gravity theories,
    including string theory and loop quantum gravity. Our work bridges
    fundamental theory with potential observational tests.
  tags:
    - quantum gravity
    - string theory
    - phenomenology
```

**Project Images**:
- Add images to `site/images/projects/`
- Size: 800x400px (2:1 aspect ratio recommended)
- File size: < 500KB each
- Use descriptive filenames

#### 5. Create Initial Blog Post
**File**: `site/_posts/2025-11-07-welcome.md` (adjust date to today)

**Content**:
```markdown
---
title: "Welcome to Our New Website"
author: [Your Name]
tags:
  - news
  - website
---

We're excited to launch our new research group website! Built with the
[Greene Lab Website Template](https://github.com/greenelab/lab-website-template),
our site now features:

- Automated publication listings
- Team member profiles
- Research project descriptions
- Regular news updates

Stay tuned for updates on our latest research, publications, and group activities.

<!-- more -->

## What's Next

Over the coming weeks, we'll be adding:
- More detailed project pages
- Research blog posts
- Tutorials and resources
- Links to talks and presentations

Check back regularly for updates, or subscribe to our [RSS feed](/feed.xml).
```

**Note**:
- Filename format: `YYYY-MM-DD-title-slug.md`
- Date in filename determines post order
- `<!-- more -->` tag creates excerpt break

#### 6. Test Content Locally
**Commands**:
```bash
cd site/

# Build site with new content
bundle exec jekyll build

# Serve locally
bundle exec jekyll serve

# Visit http://localhost:4000 and verify:
# - Team page shows all members with photos
# - Publications page displays fetched citations
# - Projects page shows research areas
# - Blog shows welcome post
```

**Visual Checks**:
- All team photos display correctly (no broken images)
- Team member bios are readable and well-formatted
- Publications show titles, authors, journals (auto-fetched by Manubot)
- Publication buttons (arXiv links) work
- Project descriptions display properly
- Blog post renders correctly with proper date

#### 7. Commit and Deploy
**Commands**:
```bash
cd site/

# Add all new content files
git add images/ _data/ _posts/

# Commit with descriptive message
git commit -m "Add team members, publications, projects, and initial blog post"

# Push to GitLab (triggers deployment)
git push origin main

# Wait for pipeline to complete (check GitLab CI/CD > Pipelines)
```

### Success Criteria:

#### Automated Verification:
- [ ] Team photos added: `ls site/images/team/*.jpg | wc -l` shows correct count
- [ ] Team YAML updated: `grep "name:" site/_data/members.yaml | wc -l` shows all members
- [ ] Citations YAML has DOIs: `grep "doi:" site/_data/citations.yaml | wc -l` ≥ 3
- [ ] Manubot processed: `test -f site/_data/citations-output.yaml` exists
- [ ] Projects YAML updated: `grep "title:" site/_data/projects.yaml | wc -l` ≥ 2
- [ ] Blog post created: `ls site/_posts/*.md | wc -l` ≥ 1
- [ ] Local build succeeds: `cd site && bundle exec jekyll build` completes
- [ ] Git changes committed: `cd site && git log -1 --oneline` shows content commit
- [ ] GitLab pipeline passes: Latest pipeline shows green checkmark

#### Manual Verification:
- [ ] Local team page shows all members with correct photos
- [ ] All team member links work (email, ORCID, Google Scholar)
- [ ] Publications page displays 3+ papers with complete metadata
- [ ] Publication metadata looks correct (titles, authors, journals, dates)
- [ ] arXiv/PDF buttons work on publications
- [ ] Projects page shows research descriptions with images
- [ ] Project images load properly
- [ ] Blog page shows welcome post
- [ ] Blog post displays with correct date and formatting
- [ ] Deployed site (GitLab Pages) shows all new content
- [ ] No broken images or 404 errors on deployed site
- [ ] Mobile view displays content correctly

**Implementation Note**: This is the most content-heavy phase. After automated verification, thoroughly review the local site to ensure all content displays correctly. Test all links (ORCID, Google Scholar, arXiv, email) to verify they work. Check that Manubot correctly fetched publication metadata - if any citations look wrong, verify the DOI and re-run Manubot. Only proceed to Phase 6 after confirming all content is accurate and displays properly on both local and deployed sites.

---

## Phase 6: Design Polish and Launch

### Overview
Final polish, testing, optimization, and official launch. This phase ensures the site is production-ready with proper SEO, performance optimization, and thorough cross-browser/device testing.

### Changes Required:

#### 1. Add Logo and Favicon
**Files**:
- `site/images/logo.png` (site logo)
- `site/images/favicon.ico` (browser tab icon)

**Logo Specifications**:
- Size: 200x200px (PNG, transparent background)
- File size: < 50KB
- Contains lab name or initials

**Favicon Specifications**:
- Size: 32x32px or 64x64px
- Format: ICO or PNG
- File size: < 10KB

**Generate Favicon** (from logo):
```bash
# Online tools:
# - https://favicon.io/ (free favicon generator)
# - https://realfavicongenerator.net/ (comprehensive)

# Or use ImageMagick locally:
convert images/logo.png -resize 32x32 images/favicon.ico
```

**Update Config**:
```yaml
# In _config.yml
logo: /images/logo.png
favicon: /images/favicon.ico
```

#### 2. Optimize Images
**Directory**: `site/images/`

**Process**:
```bash
cd site/

# Check image sizes
du -sh images/*/*

# Recommended tools for optimization:
# - ImageOptim (macOS GUI): https://imageoptim.com/mac
# - TinyPNG (online): https://tinypng.com/
# - Or command-line tools like imagemagick, pngquant

# Target sizes:
# - Team photos: < 200KB each
# - Project images: < 500KB each
# - Logo: < 50KB
```

**Optimization Goals**:
- Reduce total image payload by 30-50%
- Maintain visual quality
- Faster page load times

#### 3. Add SEO Metadata
**File**: `site/_includes/head.html` (if customizing, otherwise already in template)

**Verify/Add Meta Tags**:
```html
<!-- Open Graph (Facebook, LinkedIn) -->
<meta property="og:title" content="{{ page.title }} - {{ site.title }}" />
<meta property="og:description" content="{{ page.description | default: site.description }}" />
<meta property="og:image" content="{{ site.url }}{{ site.baseurl }}/images/logo.png" />
<meta property="og:url" content="{{ page.url | absolute_url }}" />
<meta property="og:type" content="website" />

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{{ page.title }} - {{ site.title }}" />
<meta name="twitter:description" content="{{ page.description | default: site.description }}" />
<meta name="twitter:image" content="{{ site.url }}{{ site.baseurl }}/images/logo.png" />

<!-- Canonical URL -->
<link rel="canonical" href="{{ page.url | absolute_url }}" />
```

**Note**: Greene Lab template likely includes most of these. Verify presence in `_includes/head.html`.

#### 4. Create Additional Pages

**Research Page**: `site/research.md`
```markdown
---
title: Research
layout: default
---

# Research

## Overview
[High-level description of research program]

## Research Areas

{% include list.html data="projects" component="project" %}

## Publications

{% include list.html data="citations" component="citation" %}

## Collaborations

We collaborate with research groups at:
- [Institution 1] - [PI Name]
- [Institution 2] - [PI Name]
- [Institution 3] - [PI Name]
```

**Contact Page**: `site/contact.md`
```markdown
---
title: Contact
layout: default
---

# Contact Us

## Address

{{ site.address }}

## Email

General inquiries: [{{ site.email }}](mailto:{{ site.email }})

## Join Our Group

We are always interested in motivated students and postdocs. If you're
interested in joining our research group, please send an email with:
- Your CV
- Research statement (1-2 pages)
- Names of 2-3 references

## Visitor Information

[Add information about visiting the university/department]
```

#### 5. Test Across Browsers and Devices
**Manual Testing Checklist**:

**Browsers** (test on each):
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

**Devices** (use browser dev tools or physical devices):
- [ ] Desktop (1920x1080)
- [ ] Laptop (1366x768)
- [ ] Tablet (768x1024)
- [ ] Mobile (375x667 - iPhone SE size)

**Tests on Each Browser/Device**:
- [ ] Homepage loads correctly
- [ ] Navigation menu works
- [ ] All pages accessible
- [ ] Images load and display properly
- [ ] Text is readable (check font sizes)
- [ ] Links work
- [ ] Mobile menu (hamburger) works on small screens
- [ ] Forms work (if any)
- [ ] No JavaScript errors in console

#### 6. Performance Optimization
**Test Page Speed**:
- Visit: https://pagespeed.web.dev/
- Enter your GitLab Pages URL
- Aim for scores:
  - Performance: > 90
  - Accessibility: > 90
  - Best Practices: > 90
  - SEO: > 90

**Common Optimizations** (if scores are low):
```yaml
# In _config.yml, enable compression
plugins:
  - jekyll-compress-images

# Add Brotli/gzip compression in GitLab Pages (already enabled by default)
```

**Image Lazy Loading** (if needed):
```html
<!-- In image tags, add loading attribute -->
<img src="..." loading="lazy" alt="..." />
```

#### 7. Create Launch Checklist
**Pre-Launch Checks**:
- [ ] All placeholder text replaced with real content
- [ ] All team member information accurate
- [ ] All publication links work
- [ ] All images optimized and loading
- [ ] Logo and favicon display correctly
- [ ] Footer copyright year is correct
- [ ] Contact information is correct
- [ ] Social media links work (if added)
- [ ] No "TODO" or "FIXME" comments in content
- [ ] Site tested on multiple browsers and devices
- [ ] Page speed scores acceptable
- [ ] No console errors
- [ ] GitLab CI/CD pipeline passing

#### 8. Final Deployment and Announcement
**Commands**:
```bash
cd site/

# Add all final changes
git add .

# Final commit
git commit -m "Final polish: Add logo, optimize images, complete SEO setup"

# Push to production
git push origin main

# Wait for pipeline to complete
# Verify deployment at https://[username].gitlab.io/[project-name]/
```

**Announcement**:
- Share URL with research group
- Add URL to email signatures
- Update department website with link
- Share on social media (Twitter, LinkedIn)
- Add to Google Scholar profiles

#### 9. Setup Ongoing Maintenance
**Create Shell Alias for Publication Workflow** (optional):
```bash
# Add to ~/.zshrc or ~/.bash_profile
alias add-pub='cd ~/Documents/GroupWebsite/site && manubot process --content-directory=. && git add _data/'

# Usage:
# 1. Edit _data/citations.yaml (add DOI)
# 2. Run: add-pub
# 3. git commit -m "Add publication" && git push
```

**Document Workflow**:
Create `site/MAINTENANCE.md`:
```markdown
# Website Maintenance Guide

## Adding Publications

1. Edit `_data/citations.yaml`
2. Add new entry with DOI:
   ```yaml
   - id: doi:10.1103/PhysRevD.XXX.XXXXXX
   ```
3. Run Manubot: `manubot process --content-directory=.`
4. Commit and push:
   ```bash
   git add _data/
   git commit -m "Add publication"
   git push origin main
   ```

## Adding Team Members

1. Add photo to `images/team/`
2. Edit `_data/members.yaml`
3. Add new member entry
4. Commit and push

## Adding Blog Posts

1. Create file: `_posts/YYYY-MM-DD-title.md`
2. Add front matter and content
3. Commit and push

## Updating Content

- Edit Markdown files in root directory
- Commit and push
- GitLab CI/CD automatically deploys
```

### Success Criteria:

#### Automated Verification:
- [ ] Logo exists: `test -f site/images/logo.png`
- [ ] Favicon exists: `test -f site/images/favicon.ico`
- [ ] Research page exists: `test -f site/research.md`
- [ ] Contact page exists: `test -f site/contact.md`
- [ ] Maintenance doc created: `test -f site/MAINTENANCE.md`
- [ ] Local build succeeds: `cd site && bundle exec jekyll build`
- [ ] No broken links: Use tool like `htmlproofer` or manual check
- [ ] Git status clean: `cd site && git status`
- [ ] GitLab pipeline passes: Final pipeline shows green checkmark

#### Manual Verification:
- [ ] Logo displays in header
- [ ] Favicon shows in browser tab
- [ ] All pages load on deployed site
- [ ] Navigation works on all pages
- [ ] Research page displays projects and publications
- [ ] Contact page shows correct information
- [ ] Site works on Chrome, Firefox, Safari, Edge
- [ ] Mobile responsive design works (test on phone or dev tools)
- [ ] Tablet view works correctly
- [ ] All images load and are properly sized
- [ ] Text is readable on all devices
- [ ] No JavaScript errors in browser console
- [ ] Page speed scores > 85 (check pagespeed.web.dev)
- [ ] Social media cards work (test with Twitter Card Validator or similar)
- [ ] SSL/HTTPS works (lock icon in browser)
- [ ] Site loads in < 3 seconds on good connection
- [ ] All links work (no 404 errors)
- [ ] Email links open mail client correctly

**Implementation Note**: This is the final validation phase. After automated verification, perform comprehensive manual testing. Test the site on multiple browsers and devices - pay special attention to mobile experience as many visitors will use phones. Use Google PageSpeed Insights to verify performance is acceptable. Test all functionality: navigation, links, images, forms (if any). Have a colleague or group member review the site and provide feedback. Only mark this phase complete after the site is fully functional, well-tested, and ready for public announcement.

---

## Testing Strategy

### Unit Tests
Not applicable for static Jekyll site. Content validation occurs during build process.

### Build Tests
- Jekyll build completes without errors: `bundle exec jekyll build`
- No liquid syntax errors
- All data files (YAML) parse correctly
- All images referenced in content exist
- No broken internal links

### Integration Tests
- GitLab CI/CD pipeline passes
- Site deploys successfully to GitLab Pages
- Pages URL accessible
- All assets (CSS, JS, images) load via CDN

### Manual Testing Steps

#### Content Accuracy Testing
1. Verify all team member names, photos, and links are correct
2. Confirm publication metadata matches original sources
3. Check that project descriptions accurately represent research
4. Ensure contact information is current

#### Cross-Browser Testing
1. Test on Chrome, Firefox, Safari, Edge (latest versions)
2. Verify layout doesn't break in any browser
3. Check that all interactive elements work
4. Confirm styling is consistent

#### Responsive Design Testing
1. Test on desktop (1920x1080, 1366x768)
2. Test on tablet (768x1024 portrait and landscape)
3. Test on mobile (375x667, 414x896)
4. Verify navigation menu transforms to hamburger on mobile
5. Check that images scale properly
6. Ensure text remains readable at all sizes

#### Performance Testing
1. Run Google PageSpeed Insights on all main pages
2. Check Time to First Byte (TTFB) < 600ms
3. Verify Largest Contentful Paint (LCP) < 2.5s
4. Ensure images are optimized (< 500KB for large images)
5. Check total page size < 3MB

#### Accessibility Testing
1. Test with keyboard navigation (Tab, Enter, Arrow keys)
2. Verify all images have alt text
3. Check color contrast ratios meet WCAG AA standards
4. Test with screen reader (VoiceOver on Mac or NVDA on Windows)
5. Ensure all links are descriptive

#### Link Validation
1. Test all internal navigation links
2. Verify all external links work (publications, social media, etc.)
3. Check email links open mail client
4. Confirm DOI links resolve to correct papers
5. Test arXiv links go to correct preprints

---

## Performance Considerations

### Build Performance
- **Jekyll Build Time**: Expected 3-10 seconds locally, 30-60 seconds in CI/CD
- **Optimization**: Cache gems in GitLab CI (`vendor/bundle/`)
- **Impact**: Faster deployments, reduced CI minutes usage

### Page Load Performance
- **Target Metrics**:
  - First Contentful Paint (FCP): < 1.8s
  - Largest Contentful Paint (LCP): < 2.5s
  - Time to Interactive (TTI): < 3.8s
  - Cumulative Layout Shift (CLS): < 0.1

- **Optimization Strategies**:
  - Image optimization (compression, proper sizing)
  - CSS minification (Jekyll handles automatically)
  - Lazy loading for images below fold
  - Efficient use of webfonts (consider font-display: swap)

### Image Optimization
- **Team Photos**: 300x300px, < 200KB each (optimized JPEG)
- **Project Images**: 800x400px, < 500KB each (optimized JPEG/PNG)
- **Logo**: 200x200px, < 50KB (PNG with transparency)
- **Favicon**: 32x32px, < 10KB (ICO or PNG)

**Tools**:
- ImageOptim (macOS)
- TinyPNG (online)
- Squoosh (online)
- `imagemagick` (CLI)

### Bandwidth Considerations
- **Total Page Size**: Target < 2MB per page
- **Homepage**: Likely 500KB-1MB (includes team photos)
- **Publications Page**: 300KB-600KB (text-heavy, few images)
- **Projects Page**: 1-2MB (multiple project images)

### CDN and Caching
- GitLab Pages uses CloudFlare CDN (automatic)
- Static assets cached by browser (CSS, JS, images)
- HTML pages cached for short duration (5 minutes default)

---

## Migration Notes

Not applicable - this is a fresh website setup with no existing site to migrate from.

**For Future Reference**:
If migrating from an existing site in the future:
1. Export existing content to Markdown
2. Convert BibTeX to Manubot DOI format
3. Map old URL structure to new structure (create redirects if needed)
4. Test all old URLs to ensure no broken links

---

## Maintenance Workflow

### Adding a Publication (Most Common Task)

**Time**: ~2 minutes

**Steps**:
```bash
cd site/

# 1. Edit citations file
vim _data/citations.yaml

# Add new entry with DOI
- id: doi:10.1103/PhysRevD.XXX.XXXXXX
  buttons:
    - type: preprint
      text: arXiv
      link: https://arxiv.org/abs/XXXX.XXXXX

# 2. Run Manubot to fetch metadata
manubot process --content-directory=.

# 3. Preview locally (optional)
bundle exec jekyll serve
# Check http://localhost:4000/publications

# 4. Commit and push
git add _data/
git commit -m "Add publication: [Short Title]"
git push origin main

# 5. Wait for GitLab CI/CD to deploy (1-3 minutes)
```

### Adding a Team Member

**Time**: ~5 minutes

**Steps**:
```bash
cd site/

# 1. Add photo to images/team/
cp ~/Downloads/new-member-photo.jpg images/team/new-member.jpg

# 2. Optimize photo
# Use ImageOptim or similar tool
# Target: 300x300px, < 200KB

# 3. Edit members file
vim _data/members.yaml

# Add new member entry (see Phase 5 for format)

# 4. Test locally
bundle exec jekyll serve

# 5. Commit and push
git add images/team/ _data/members.yaml
git commit -m "Add team member: [Name]"
git push origin main
```

### Adding a Blog Post

**Time**: ~10-30 minutes (depending on content)

**Steps**:
```bash
cd site/

# 1. Create new post file (use today's date)
vim _posts/2025-11-15-new-research-result.md

# Add front matter and content:
---
title: "New Research Result on Black Hole Thermodynamics"
author: Prof. Jane Doe
tags:
  - research
  - black holes
  - publications
---

We're excited to announce our latest research result...

<!-- more -->

[Full content here]

# 2. Test locally
bundle exec jekyll serve

# 3. Commit and push
git add _posts/
git commit -m "New blog post: [Title]"
git push origin main
```

### Updating Team Member Info

**Time**: ~2 minutes

**Steps**:
```bash
cd site/

# 1. Edit members file
vim _data/members.yaml

# Update relevant fields (email, affiliation, description, links)

# 2. Test locally
bundle exec jekyll serve

# 3. Commit and push
git add _data/members.yaml
git commit -m "Update team member info: [Name]"
git push origin main
```

### Quarterly Maintenance

**Time**: ~15 minutes every 3 months

**Steps**:
```bash
cd site/

# 1. Update Ruby gems
bundle update

# 2. Update Manubot
npm update -g manubot

# 3. Test local build
bundle exec jekyll build
bundle exec jekyll serve

# 4. Check for template updates
cd /tmp
git clone https://github.com/greenelab/lab-website-template.git
cd lab-website-template
git log --since="3 months ago" --oneline

# If relevant updates exist, consider merging:
# git remote add upstream https://github.com/greenelab/lab-website-template.git
# git fetch upstream
# git merge upstream/main
# (Resolve conflicts, test thoroughly)

# 5. Commit updates
git add Gemfile.lock
git commit -m "Update dependencies"
git push origin main
```

---

## References

- **Greene Lab Template**: https://github.com/greenelab/lab-website-template
- **Greene Lab Documentation**: https://greene-lab.gitbook.io/lab-website-template-docs
- **Manubot Documentation**: https://manubot.org/docs/
- **Jekyll Documentation**: https://jekyllrb.com/docs/
- **GitLab Pages Documentation**: https://docs.gitlab.com/user/project/pages/
- **GitLab CI/CD Documentation**: https://docs.gitlab.com/ci/
- **Research Document**: `thoughts/shared/research/2025-11-07-physics-group-website-design-static-site-generators.md`

---

## Troubleshooting Guide

### Issue: Jekyll Build Fails Locally

**Symptoms**: `bundle exec jekyll build` fails with errors

**Solutions**:
1. Check Ruby version: `ruby --version` (need 3.0+)
2. Reinstall dependencies: `bundle install`
3. Clear cache: `bundle exec jekyll clean`
4. Check for YAML syntax errors in `_data/*.yaml` files
5. Review error message for specific file causing issue

### Issue: Manubot Cannot Fetch Citation

**Symptoms**: `manubot process` fails or citation missing metadata

**Solutions**:
1. Verify DOI is correct and public
2. Check internet connection
3. Try alternative identifier (PubMed ID, arXiv)
4. If DOI not working, use manual citation format:
```yaml
- id: custom-2024-paper
  title: "Paper Title"
  authors:
    - Author Name
  publisher: Journal Name
  date: 2024-01-15
  link: https://doi.org/...
```

### Issue: GitLab CI/CD Pipeline Fails

**Symptoms**: Pipeline shows red X, site not deploying

**Solutions**:
1. Check pipeline logs in GitLab (CI/CD > Pipelines > click failed job)
2. Common issues:
   - YAML syntax error in `.gitlab-ci.yml`
   - Jekyll build error (same as local build issues)
   - Missing files referenced in content
3. Test build locally first: `bundle exec jekyll build`
4. If local build works but CI fails, check Ruby versions match

### Issue: Images Not Loading on Deployed Site

**Symptoms**: Images show broken on GitLab Pages but work locally

**Solutions**:
1. Check `baseurl` in `_config.yml` matches project name
2. Verify image paths use relative URLs: `{{ site.baseurl }}/images/...`
3. Ensure images committed to Git: `git status` shows no untracked images
4. Check file names are lowercase (case-sensitive on server)
5. Verify images aren't too large (< 5MB per file)

### Issue: Styling Broken on Deployed Site

**Symptoms**: Site looks unstyled, CSS not loading

**Solutions**:
1. Most likely `baseurl` misconfiguration in `_config.yml`
2. Check browser console for 404 errors on CSS files
3. Verify `baseurl` matches project name exactly
4. Test with `bundle exec jekyll serve --baseurl /[project-name]` locally

### Issue: Team Photos Not Displaying

**Symptoms**: Team page shows broken image icons

**Solutions**:
1. Verify image filenames in `_data/members.yaml` match actual files
2. Check file paths: `images/team/filename.jpg` (not `/images/...`)
3. Ensure images are committed: `git ls-files images/team/`
4. Check image file sizes aren't too large (< 5MB each)
5. Verify file extensions are correct (`.jpg` not `.jpeg` in YAML)

### Issue: Publications Not Showing

**Symptoms**: Publications page is empty

**Solutions**:
1. Check `_data/citations-output.yaml` exists and has content
2. Re-run Manubot: `manubot process --content-directory=.`
3. Verify DOIs in `_data/citations.yaml` are correct
4. Check for YAML syntax errors
5. Ensure both `citations.yaml` and `citations-output.yaml` are committed

### Issue: Site Slow to Load

**Symptoms**: Pages take > 5 seconds to load

**Solutions**:
1. Optimize images (reduce file sizes)
2. Check total page size: use browser dev tools Network tab
3. Run PageSpeed Insights: https://pagespeed.web.dev/
4. Reduce number of team photos on homepage if many members
5. Consider lazy loading for images below fold

---

## Appendix A: Command Reference

### Common Jekyll Commands
```bash
# Build site
bundle exec jekyll build

# Serve locally
bundle exec jekyll serve

# Serve with baseurl (test production config)
bundle exec jekyll serve --baseurl /project-name

# Clean build artifacts
bundle exec jekyll clean

# Build in production mode
JEKYLL_ENV=production bundle exec jekyll build
```

### Common Manubot Commands
```bash
# Process citations
manubot process --content-directory=.

# Process with verbose output
manubot process --content-directory=. --log-level=INFO

# Check Manubot version
manubot --version

# Update Manubot
npm update -g manubot
```

### Common Git Commands
```bash
# Check status
git status

# Add files
git add .
git add _data/citations.yaml

# Commit
git commit -m "Message"

# Push to GitLab
git push origin main

# View recent commits
git log --oneline -5

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard local changes
git checkout -- filename
```

### Common Bundle Commands
```bash
# Install dependencies
bundle install

# Update dependencies
bundle update

# Show installed gems
bundle list

# Check for outdated gems
bundle outdated

# Check Bundler version
bundle --version
```

---

## Appendix B: File Structure Reference

```
site/
├── .gitlab-ci.yml              # GitLab CI/CD configuration
├── _config.yml                 # Jekyll site configuration
├── Gemfile                     # Ruby dependencies
├── Gemfile.lock               # Locked dependency versions
├── README.md                  # Template documentation
├── MAINTENANCE.md             # Maintenance guide (create in Phase 6)
│
├── _data/                     # YAML data files
│   ├── citations.yaml         # Publication DOIs (input)
│   ├── citations-output.yaml  # Full citation metadata (Manubot output)
│   ├── members.yaml           # Team member info
│   ├── projects.yaml          # Research projects
│   └── sources.yaml           # Other data sources
│
├── _includes/                 # Reusable components
│   ├── head.html              # HTML head (meta tags)
│   ├── header.html            # Site header/navigation
│   ├── footer.html            # Site footer
│   ├── citation.html          # Publication display component
│   ├── member.html            # Team member display component
│   └── project.html           # Project display component
│
├── _layouts/                  # Page layouts
│   ├── default.html           # Base layout
│   ├── post.html              # Blog post layout
│   └── page.html              # Standard page layout
│
├── _posts/                    # Blog posts
│   └── YYYY-MM-DD-title.md    # Post files (date-based naming)
│
├── _styles/                   # SCSS styles
│   ├── variables.scss         # Color/font variables
│   ├── mixins.scss            # SCSS mixins
│   └── main.scss              # Main stylesheet
│
├── images/                    # Image assets
│   ├── team/                  # Team member photos
│   ├── projects/              # Project images
│   ├── logo.png               # Site logo
│   └── favicon.ico            # Browser favicon
│
├── index.md                   # Homepage
├── about.md                   # About page
├── research.md                # Research page
├── team.md                    # Team page
├── contact.md                 # Contact page
└── blog.md                    # Blog index page
```

---

## Appendix C: YAML Data File Schemas

### members.yaml Schema
```yaml
- name: String (required)           # Full name
  image: String (required)          # Path to photo (images/team/filename.jpg)
  role: String (required)           # One of: pi, postdoc, phd, undergrad, alumni
  affiliation: String (required)    # Institution name
  description: String (required)    # Research focus (1-3 sentences)
  links:                            # Optional links
    home-page: URL
    email: Email address
    orcid: ORCID ID (0000-0002-XXXX-XXXX)
    google-scholar: Scholar ID
    github: GitHub username
    twitter: Twitter handle
```

### citations.yaml Schema
```yaml
- id: String (required)             # DOI, PubMed ID, or ORCID
                                    # Format: doi:10.1234/example
                                    #         pmid:12345678
                                    #         orcid:0000-0002-1234-5678
  buttons:                          # Optional custom buttons
    - type: String                  # Button type: preprint, source, data, website
      text: String                  # Button label
      link: URL                     # Button URL
```

### projects.yaml Schema
```yaml
- title: String (required)          # Project title
  subtitle: String (optional)       # Subtitle/tagline
  image: String (optional)          # Path to image (images/projects/filename.jpg)
  description: String (required)    # Project description (2-4 sentences)
  tags:                             # Optional tags (list)
    - String
    - String
  links:                            # Optional links
    website: URL
    github: URL
    paper: URL
    data: URL
```

---

## Appendix D: Sample Content Templates

### Sample Blog Post Template
```markdown
---
title: "Your Post Title"
author: Author Name
tags:
  - tag1
  - tag2
  - tag3
---

Opening paragraph with key point or hook.

<!-- more -->

## Section 1

Content for section 1.

## Section 2

Content for section 2.

### Subsection

More detailed content.

## Conclusion

Wrap-up and call to action.
```

### Sample Project Entry
```yaml
- title: Example Research Project
  subtitle: A Brief Description
  image: images/projects/example.jpg
  description: >
    A comprehensive description of the research project spanning multiple lines.
    This should explain the motivation, approach, and significance of the work
    in 2-4 sentences.
  tags:
    - quantum field theory
    - numerical methods
    - high energy physics
  links:
    website: https://project-site.org
    github: https://github.com/yourlab/project-repo
    paper: https://arxiv.org/abs/XXXX.XXXXX
```

### Sample Team Member Entry
```yaml
- name: Dr. Example Researcher
  image: images/team/example-researcher.jpg
  role: postdoc
  affiliation: Your University
  description: >
    Dr. Researcher specializes in quantum field theory and gravitational physics.
    Their current work focuses on black hole thermodynamics and the information paradox.
  links:
    home-page: https://example-researcher.com
    email: researcher@university.edu
    orcid: 0000-0002-1234-5678
    google-scholar: ABC123XYZ
    github: example-researcher
```

---

## Appendix E: Timeline Summary

| Phase | Duration | Key Deliverable |
|-------|----------|-----------------|
| Phase 1 | 30 min | Template forked, GitLab repo created |
| Phase 2 | 1-2 hours | Local environment working |
| Phase 3 | 1 hour | CI/CD configured, site deployed |
| Phase 4 | 2-3 hours | Site branded, colors customized |
| Phase 5 | 6-8 hours | Content populated (team, pubs, projects) |
| Phase 6 | 4-6 hours | Final polish, testing, launch |
| **Total** | **16-24 hours** | **Live, functional website** |

**Recommended Schedule**:
- Week 1: Phases 1-3 (infrastructure setup)
- Week 2: Phase 4 (customization)
- Week 3: Phase 5 (content creation)
- Week 4: Phase 6 (polish and launch)

---

## Conclusion

This implementation plan provides a comprehensive, step-by-step approach to setting up a theoretical physics group website using the Greene Lab template on GitLab Pages. Each phase is designed to be incremental and testable, ensuring a working site at every stage. The manual local Manubot approach balances automation with simplicity, making the site easy to maintain long-term.

**Key Success Factors**:
1. Follow phases sequentially - don't skip ahead
2. Test thoroughly at each phase before proceeding
3. Commit changes frequently with descriptive messages
4. Use local development server to preview before deploying
5. Document any customizations for future reference

**After Launch**:
- Add publications as papers are published (~2 min each)
- Update team member info as needed (~2 min each)
- Post regular blog updates about research activities
- Keep dependencies updated quarterly
- Monitor GitLab Pages analytics (if enabled)

**Questions or Issues**:
- Consult Greene Lab documentation: https://greene-lab.gitbook.io/lab-website-template-docs
- Check troubleshooting guide in this plan
- Review research document for alternative approaches
- GitLab Pages support: https://docs.gitlab.com/user/project/pages/

Good luck with your new research group website!
