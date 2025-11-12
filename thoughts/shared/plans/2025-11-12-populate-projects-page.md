---
date: 2025-11-12
author: Claude (Sonnet 4.5)
git_commit: 14d296ab18a65e275968c3a335bca5e8f2c2cb4b
branch: main
status: complete
last_updated: 2025-11-12
last_updated_by: Claude (Sonnet 4.5)
---

# Populate Projects Page with QuIReal Research Projects

## Overview

This plan outlines the steps to populate the QuIReal group website's Projects page with four featured research projects: ALPS (Advanced Lectures in Physics in Switzerland), CosmoLattice (lattice simulation software), Emmy Noether Grant (research group funding), and CRC-TR 211 (collaborative research centre). The implementation will replace placeholder content with real project information, create project images, and customize the page for QuIReal's research focus.

## Current State Analysis

**Existing Structure** (as of commit 14d296a):
- Projects page exists at `site/projects/index.md:1-28` with placeholder Lorem ipsum text
- Projects data file at `site/_data/projects.yaml:1-48` contains 5 sample Greene Lab entries with dummy data
- No `site/images/projects/` directory exists yet
- Projects page uses tags: "publication, resource, website" (line 13) - not suited for QuIReal projects
- All sample projects use placeholder image `images/photo.jpg` (lines 4, 14, 23, 33, 42)

**Available Information Sources**:
- Team member page at `site/_members/adrien-florio.md:1-111` contains detailed information about:
  - ALPS summer school series (lines 84-86)
  - CosmoLattice and related summer schools (lines 13, 90-92)
  - Emmy Noether Grant with DFG link (lines 58-60)
- Research document at `site/thoughts/shared/research/2025-11-12-projects-page-population.md` provides:
  - Greene Lab template architecture and best practices
  - YAML schema and image specifications (800x400px, < 500KB)
  - Example project structures for physics groups

**Project Information Gathered**:
1. **ALPS**: SwissMAP-funded PhD summer school series on quantum information (2024-2026)
2. **CosmoLattice**: Software package for lattice simulations in expanding universe (authors: Figueroa, Florio, Torrenti, Valkenburg)
3. **Emmy Noether Grant**: DFG project #545261797 on "chiral anomaly dynamics" (started 2024)
4. **CRC-TR 211**: Collaborative research centre "Strong-Interaction Matter under Extreme Conditions" (Bielefeld/Darmstadt/Frankfurt)

## Desired End State

After implementation completion:
- Four featured research projects displayed on Projects page with accurate descriptions
- Project images directory created at `site/images/projects/` with 4 images (800x400px, < 500KB each)
- Updated `_data/projects.yaml` with real QuIReal project entries replacing sample data
- Customized projects page intro text reflecting QuIReal research focus
- Updated tag filtering system using relevant categories: software, education, research-program, collaboration
- All projects marked as `group: featured` for prominent display
- CosmoLattice linked to both GitHub repository (cosmolattice/CosmoLattice) and website (cosmolattice.net)
- All other projects linked to their primary websites/resources

### Verification:
- Visit `/projects` page locally and verify all 4 projects display with images
- Click all project links to ensure they point to correct destinations
- Test tag filtering functionality
- Verify responsive layout on different screen sizes
- Check that project descriptions are clear and concise (2-4 sentences each)

## What We're NOT Doing

To prevent scope creep, explicitly out of scope:
- Creating detailed project landing pages on the QuIReal site (projects link externally)
- Adding publication lists to individual projects (handled via Research page)
- Implementing "Legacy" or "More" project sections (only Featured section used)
- Creating animated or interactive project visualizations
- Adding team member attribution to each project (this info is on Team page)
- Setting up automated project updates or CI/CD for project content
- Creating project-specific documentation beyond 2-4 sentence descriptions
- Implementing project filtering by year or custom categories beyond tags

## Implementation Approach

**Strategy**: Incremental, testable phases moving from infrastructure setup to content population to customization.

**Rationale**:
1. Create directory structure first to enable image preparation
2. Prepare images as separate phase to allow for iteration and optimization
3. Update YAML data file with complete project information
4. Customize page text and tags to match QuIReal branding
5. Test thoroughly before finalizing

Each phase has clear success criteria with automated verification where possible and manual verification for content quality and visual appearance.

---

## Phase 1: Directory Structure and Image Preparation

### Overview
Create the projects images directory and prepare 4 project images optimized for web display.

### Changes Required:

#### 1. Create Projects Images Directory
**Location**: `site/images/`
**Action**: Create new directory `projects/`

```bash
mkdir -p site/images/projects/
```

#### 2. Prepare Project Images

Create or source 4 images (one per project) with specifications:
- **Size**: 800x400px (2:1 aspect ratio)
- **Format**: JPG or PNG
- **File size**: < 500KB each
- **Color scheme**: Match QuIReal purple/cyan theme where appropriate

**Image naming convention**:
- `alps-summer-school.jpg` - ALPS project
- `cosmolattice-simulation.jpg` - CosmoLattice project
- `emmy-noether-grant.jpg` - Emmy Noether grant
- `crc-tr211-collaboration.jpg` - CRC-TR 211 project

**Image content suggestions**:

1. **ALPS**:
   - Swiss Alps mountain scenery with overlay of quantum equations or diagrams
   - Collage of lecture scenes or whiteboard quantum information formulas
   - Swiss mountain lodge setting combined with physics notation

2. **CosmoLattice**:
   - Visualization of lattice field configuration or simulation output
   - Screenshot of field evolution plot or phase diagram
   - Cosmological visualization (early universe, field dynamics)

3. **Emmy Noether Grant**:
   - Abstract representation of quantum-to-classical transition
   - Chiral anomaly diagram or topological field visualization
   - Combined imagery: quantum circuits and lattice configurations

4. **CRC-TR 211**:
   - Lattice QCD visualization or quark-gluon plasma representation
   - Map showing Bielefeld-Darmstadt-Frankfurt collaboration
   - Strong interaction physics diagram (phase diagram, confinement)

**Image optimization**:
```bash
# After creating images, optimize file sizes if needed
# (Manual step using image editing software or online tools)
# Target: < 500KB each while maintaining quality
```

### Success Criteria:

#### Automated Verification:
- [x] Projects directory exists: `test -d site/images/projects && echo "Success" || echo "Failed"`
- [x] Exactly 4 image files present: `test $(ls site/images/projects/ | wc -l) -eq 4 && echo "Success" || echo "Failed"`
- [x] All images are appropriately sized: `cd site/images/projects && for f in *.{jpg,png}; do [ -f "$f" ] && ls -lh "$f"; done`

#### Manual Verification:
- [x] Each image is 800x400px (verify dimensions in image editor or browser)
- [x] Each image file is < 500KB (check file sizes)
- [x] Images are visually appealing and relevant to their projects
- [x] Images maintain QuIReal color scheme consistency where applicable
- [x] Images are clear and professional quality

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation that the images look appropriate and are properly sized before proceeding to Phase 2.

---

## Phase 2: Update Projects Data File

### Overview
Replace sample projects in `_data/projects.yaml` with the 4 QuIReal research projects, including complete metadata, descriptions, and links.

### Changes Required:

#### 1. Replace projects.yaml Content
**File**: `site/_data/projects.yaml`
**Changes**: Complete file replacement with new project data

```yaml
# ALPS - Advanced Lectures in Physics in Switzerland
- title: Advanced Lectures in Physics in Switzerland (ALPS)
  subtitle: SwissMAP-funded PhD summer school series
  group: featured
  image: images/projects/alps-summer-school.jpg
  link: https://indico.global/event/9618/
  description: >
    A junior school in theoretical physics held annually in the Swiss Alps,
    designed to foster collaboration among young researchers through lectures
    bridging different areas of modern theoretical physics. The series focuses
    on quantum information theory, quantum computing, entanglement in QFT, and
    holography. Fully funded by SwissMAP with accommodation and meals covered.
  tags:
    - education
    - collaboration

# CosmoLattice Software
- title: CosmoLattice
  subtitle: Lattice simulations of field dynamics in expanding universe
  group: featured
  image: images/projects/cosmolattice-simulation.jpg
  link: https://cosmolattice.net
  description: >
    Modern software package for lattice simulations of field dynamics in an
    expanding universe. Supports interacting scalar field theories, Abelian U(1)
    and non-Abelian SU(2) gauge theories in flat or FLRW backgrounds. Features
    gravitational wave computation modules and customizable field description
    language. Actively developed and freely available for research use.
  repo: cosmolattice/CosmoLattice
  tags:
    - software

# Emmy Noether Grant
- title: Emmy Noether Research Group
  subtitle: "From classical to quantum simulations of chiral anomaly dynamics"
  group: featured
  image: images/projects/emmy-noether-grant.jpg
  link: https://gepris.dfg.de/gepris/projekt/545261797?language=en
  description: >
    DFG-funded junior research group (Project #545261797) investigating anomalous
    transport effects on topology-changing processes in the Standard Model.
    Combines classical numerical simulations with quantum computing techniques to
    study real-time field-theoretic dynamics in 1D and 2D systems. Aims to achieve
    quantum advantage in simulating early universe evolution and quark-gluon plasma.
  tags:
    - research-program

# CRC-TR 211 Project A02
- title: "CRC-TR 211: Strong-Interaction Matter"
  subtitle: "Project A02 [To be filled in]"
  group: featured
  image: images/projects/crc-tr211-collaboration.jpg
  link: https://crc-tr211.org/
  description: >
    Collaborative Research Centre (TransRegio) examining strong-interaction matter
    under extreme conditions from a theoretical perspective. Partners: Bielefeld,
    Darmstadt, and Frankfurt universities. Combines complex numerical simulations
    on supercomputers (lattice QCD) with analytical methods to study matter at
    temperatures and densities present in the early Universe and heavy-ion collisions.
    [Project A02 specific details to be added by PI]
  tags:
    - research-program
    - collaboration
```

**Key Changes**:
- Line 1-48: Complete replacement of all 5 sample entries
- All projects use `group: featured` for prominent display
- CosmoLattice includes `repo: cosmolattice/CosmoLattice` field for GitHub badge
- Image paths point to `images/projects/[filename].jpg`
- Tags use new categories: education, collaboration, software, research-program
- CRC-TR 211 description includes placeholder for Project A02 details

### Success Criteria:

#### Automated Verification:
- [x] YAML file is valid syntax: `cd site && bundle exec jekyll build --dry-run 2>&1 | grep -i "error" && echo "Failed" || echo "Success"`
- [x] Exactly 4 projects defined: `grep -c "^- title:" site/_data/projects.yaml` should output 4
- [x] All 4 projects have `group: featured`: `grep -c "group: featured" site/_data/projects.yaml` should output 4
- [x] All image paths are correct: `grep "image:" site/_data/projects.yaml | sed 's/.*image: //' | while read img; do test -f "site/$img" && echo "OK: $img" || echo "MISSING: $img"; done`

#### Manual Verification:
- [x] All project titles are accurate and properly formatted
- [x] Descriptions are 2-4 sentences and clearly explain each project
- [x] All external links are correct and functional
- [x] CosmoLattice has both `link` and `repo` fields
- [x] Tags are appropriate for each project
- [x] YAML indentation and syntax is correct

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation that the project descriptions are accurate and links are correct before proceeding to Phase 3.

---

## Phase 3: Customize Projects Page Content

### Overview
Update the projects page intro text and tag filtering to reflect QuIReal research focus, replacing placeholder Lorem ipsum text.

### Changes Required:

#### 1. Update Page Introduction Text
**File**: `site/projects/index.md`
**Lines**: 10-11
**Changes**: Replace Lorem ipsum with QuIReal-specific intro

```markdown
Our group develops computational tools, educational programs, and collaborative
research initiatives to advance quantum information theory and real-time quantum
field evolution. All projects support open science and reproducible research in
theoretical physics and quantum computing.
```

#### 2. Update Tag Filtering Categories
**File**: `site/projects/index.md`
**Line**: 13
**Changes**: Update tags to match new project categories

```markdown
{% include tags.html tags="software, education, research-program, collaboration" %}
```

**Key Changes**:
- Removed: "publication, resource, website" (not relevant to these projects)
- Added: "software, education, research-program, collaboration" (match project tags)

### Success Criteria:

#### Automated Verification:
- [x] Site builds without errors: `cd site && bundle exec jekyll build 2>&1 | grep -i "error" && echo "Failed" || echo "Success"`
- [x] Projects page exists in built site: `test -f site/_site/projects/index.html && echo "Success" || echo "Failed"`
- [x] No Lorem ipsum text remains: `grep -i "lorem ipsum" site/projects/index.md && echo "Failed" || echo "Success"`

#### Manual Verification:
- [x] Intro text accurately describes QuIReal projects focus
- [x] Intro text is grammatically correct and professional
- [x] Tag filtering includes all 4 categories used in projects.yaml
- [x] Page title and icon remain unchanged (wrench icon)
- [x] Section structure (Featured/More) remains intact

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation that the intro text reads well and tags are appropriate before proceeding to Phase 4.

---

## Phase 4: Local Testing and Final Verification

### Overview
Build and test the site locally to ensure all projects display correctly with images, links work, and the page renders properly.

### Changes Required:

#### 1. Build Site Locally
**Action**: Run Jekyll server to preview changes

```bash
cd site/
bundle exec jekyll serve
```

#### 2. Manual Testing Steps

**Navigation**: Visit `http://localhost:4000/projects` in browser

**Visual Verification**:
1. Verify all 4 projects appear in "Featured" section
2. Check that all 4 project images load and display correctly
3. Verify "More" section is empty (all projects are featured)
4. Check responsive layout by resizing browser window

**Interaction Testing**:
1. Click each project title link - verify it opens correct external page
2. Click each project image - verify it links to correct destination
3. Test tag filtering - click each of 4 tags and verify projects filter correctly
4. Test search functionality with project keywords

**Content Review**:
1. Read all 4 project descriptions for accuracy and clarity
2. Verify GitHub badge appears for CosmoLattice project
3. Check that all text is properly formatted (no Markdown errors)
4. Verify page intro text displays correctly

#### 3. Cross-browser Testing

Test in multiple browsers if available:
- Chrome/Chromium
- Firefox
- Safari
- Mobile browser (iOS Safari or Android Chrome)

### Success Criteria:

#### Automated Verification:
- [x] Site builds successfully: `make -C site build`
- [x] No broken links in projects: `cd site && bundle exec jekyll build && grep -r "href.*projects" _site/projects/index.html`
- [x] All 4 projects render: `grep -c "data-style" site/_site/projects/index.html` (should be ≥ 4)

#### Manual Verification:
- [x] All 4 project cards display in Featured section
- [x] All 4 project images load correctly (no broken images)
- [x] All project titles are clickable and link correctly
- [x] CosmoLattice shows GitHub repository badge
- [x] Tag filtering works (clicking tags filters projects)
- [x] Search functionality works with project keywords
- [x] Page intro text displays without Lorem ipsum
- [x] Responsive layout works on mobile/tablet/desktop
- [x] No console errors in browser developer tools
- [x] No visual layout issues or text overflow
- [x] "More" section is empty (expected, since all are featured)

**Implementation Note**: This is the final phase. Once all automated and manual verification passes, the projects page population is complete and ready for deployment.

---

## Testing Strategy

### Unit Tests
Not applicable - this is content population rather than code changes. Jekyll template rendering is already tested by Greene Lab template.

### Integration Tests
- **Jekyll Build**: Verify site builds without errors
- **Link Validation**: Check all external project links are accessible
- **Image Loading**: Verify all images load in built site
- **YAML Syntax**: Validate projects.yaml parses correctly

### Manual Testing Steps

1. **Initial Build Test**:
   ```bash
   cd site/
   bundle exec jekyll build
   # Should complete without errors
   ```

2. **Local Preview**:
   ```bash
   cd site/
   bundle exec jekyll serve
   # Visit http://localhost:4000/projects
   ```

3. **Visual Inspection Checklist**:
   - [ ] 4 projects visible in Featured section
   - [ ] All images load and are properly sized
   - [ ] No broken image placeholders
   - [ ] Text is readable and properly formatted
   - [ ] Links are styled correctly (underlined/colored)

4. **Interaction Testing**:
   - [ ] Click ALPS title → opens https://indico.global/event/9618/
   - [ ] Click CosmoLattice title → opens https://cosmolattice.net
   - [ ] Click Emmy Noether title → opens DFG gepris page
   - [ ] Click CRC-TR 211 title → opens https://crc-tr211.org/
   - [ ] Click "software" tag → filters to show only CosmoLattice
   - [ ] Click "education" tag → filters to show only ALPS
   - [ ] Click "research-program" tag → shows Emmy Noether and CRC-TR 211
   - [ ] Click "collaboration" tag → shows ALPS and CRC-TR 211

5. **Responsive Testing**:
   - Desktop (≥1200px): Cards should be in grid layout
   - Tablet (768-1199px): Cards should adjust to 2 columns
   - Mobile (<768px): Cards should stack vertically

6. **Cross-browser Testing**:
   - Test in at least 2 different browsers
   - Verify consistent rendering
   - Check for browser-specific layout issues

7. **Link Accessibility**:
   - Right-click each link → "Open in new tab"
   - Verify external sites load correctly
   - Check for 404 errors or redirects

## Performance Considerations

### Image Optimization
- All images must be < 500KB to ensure fast page load
- Use lazy loading (already implemented in card.html:12)
- Consider WebP format for better compression (future enhancement)

### Build Time
- Adding 4 projects with images adds minimal build time (< 1 second)
- Jekyll build should remain under 10 seconds for entire site

### Page Load Speed
- Target: Projects page loads in < 2 seconds on 3G connection
- Monitor image sizes if page feels slow
- Greene Lab template uses responsive images by default

## Migration Notes

### Existing Content
- **Before**: 5 sample projects with Lorem ipsum text
- **After**: 4 real QuIReal projects with accurate descriptions
- **Impact**: No migration needed, complete replacement

### Image Assets
- **New**: 4 images added to `site/images/projects/`
- **Removed**: None (placeholder images remain unused)
- **Total size**: ~1-2MB for 4 optimized images

### Data Structure
- YAML schema unchanged (uses same fields as Greene Lab template)
- All projects use `group: featured` (no "More" section projects)
- CosmoLattice uses optional `repo` field for GitHub integration

### Rollback Plan
If issues arise:
1. Revert `_data/projects.yaml` to previous version
2. Remove `images/projects/` directory if needed
3. Revert `projects/index.md` intro text changes
4. Run `bundle exec jekyll serve` to verify rollback

```bash
# Quick rollback commands
cd site/
git checkout HEAD~1 -- _data/projects.yaml projects/index.md
rm -rf images/projects/
bundle exec jekyll serve
```

## References

### Original Context
- **Personal page**: `site/_members/adrien-florio.md:1-111` - Source of project information
- **Research document**: `site/thoughts/shared/research/2025-11-12-projects-page-population.md` - Greene Lab template analysis
- **Implementation plan**: `site/thoughts/shared/plans/2025-11-07-greene-lab-website-setup.md` - Phase 5 context

### External Resources
- **ALPS I**: https://indico.global/event/9618/
- **ALPS II**: https://indico.global/event/9641/
- **ALPS III**: https://swissmaprs.ch/wp-content/uploads/2025/03/2026-SRS-Programme.pdf
- **CosmoLattice**: https://cosmolattice.net
- **CosmoLattice GitHub**: https://github.com/cosmolattice/CosmoLattice
- **CosmoLattice 2022 School**: https://indico.ific.uv.es/event/6631/
- **CosmoLattice 2023 School**: https://indico.ific.uv.es/event/7055/
- **Emmy Noether Grant**: https://gepris.dfg.de/gepris/projekt/545261797?language=en
- **CRC-TR 211**: https://crc-tr211.org/

### Template Documentation
- **Greene Lab Docs**: https://greene-lab.gitbook.io/lab-website-template-docs
- **Projects Page Guide**: https://greene-lab.gitbook.io/lab-website-template-docs/basics/edit-pages
- **Card Component**: `site/_includes/card.html:1-48`
- **List Component**: `site/_includes/list.html:1-60`

### Code References
- Projects page structure: `site/projects/index.md:1-28`
- Projects data file: `site/_data/projects.yaml:1-48`
- Featured filter: `site/projects/index.md:21` - `filter="group == 'featured'"`
- More filter: `site/projects/index.md:27` - `filter="!group"`
- Image specifications: 800x400px, < 500KB per research doc recommendations
