# CV-Style Personal Page Content Implementation Plan

## Overview

This plan guides the implementation of concise, CV-style content for Adrien Florio's member page, inspired by academic CV layouts like https://www.repond.ch/#resume and https://aleksas.eu/cv/. The implementation emphasizes **conciseness and scannability** while adding custom CSS for a timeline-style professional layout.

**Scope**: Adrien Florio's member page only (Franz Sattler and Vasundhara Krishnan can be updated later using the same pattern)

**Key Principles**:
- **Conciseness**: Max 2-3 bullets per position, outcome-focused
- **Visual hierarchy**: Clear sections with timeline-style date formatting
- **Scannability**: Someone should grasp the profile in 30 seconds
- **Essential highlights only**: Not comprehensive - curated and impactful

**Timeline**: 4-6 hours total

## Current State Analysis

**Starting Point**:
- Basic member page at `_members/adrien-florio.md` with placeholder content
- Existing Jekyll member layout with floating portrait sidebar
- Standard markdown styling (headings, lists, paragraphs)
- No timeline/CV-specific CSS components
- Front matter has placeholder ORCID and links

**Existing Architecture** (from research):
- Member layout (`_layouts/member.html`) creates two-column layout: portrait sidebar + main content
- Float component (`_includes/float.html`) positions portrait at max 50% width, left-aligned
- Heading styles with H2 bottom borders, H3 for subsections
- List styles with square bullets and proper spacing
- Responsive at 600px breakpoint (portrait stacks on top)

**CV Content Available** (from `~/ProtonDrive/Documents/cv/cv.pdf`):
- 3 positions (Emmy Noether, Goldhaber Fellow, Postdoc)
- 4 major awards with detailed descriptions
- 5 education entries (PhD, MS, Minor, BS, Maturité)
- 20+ invited talks across multiple years
- Extensive professional service (organizing, advisory, referee)
- Current supervision (2 people) + past mentorship
- Teaching experience and outreach programs
- Software development (CosmoLattice)

## Desired End State

A concise, CV-style personal page that:
- **Presents essential professional information** in scannable format
- **Uses timeline-style visual elements** for positions and education
- **Emphasizes impact and outcomes** over duties
- **Maintains mobile responsiveness** with Jekyll's existing architecture
- **Loads quickly** and is easy to update

### Key Features:
1. **Updated front matter** with correct ORCID, homepage, INSPIRE-HEP, Google Scholar
2. **Custom CSS components** for CV timeline styling (optional timeline bars, date badges)
3. **Concise content sections**:
   - Education (5 entries, year-only dates)
   - Professional Experience (3 positions, 2-3 bullets each)
   - Awards & Highlights (4 items, one-sentence descriptions)
   - Selected Invited Talks (5 most prestigious)
   - Professional Service (3-4 key roles)
   - Current Supervision (2 people)
   - Research Interests (refined, 4-5 bullets)
   - Software (CosmoLattice, 1-2 sentences)
   - Outreach (2-3 programs, one line each)

### Verification:
- Page builds successfully with Jekyll
- All sections display correctly on desktop (1920px) and mobile (375px)
- Content is scannable (30-second test: can someone grasp your profile?)
- All external links work (ORCID, INSPIRE-HEP, Google Scholar, award links)
- Timeline styling looks professional and doesn't break layout
- No sections exceed 10 lines of content

## What We're NOT Doing

- **Not comprehensive**: This is curated highlights, not a full CV
- **Not including all talks**: Just 5 most prestigious (not 20+)
- **Not listing all service**: 3-4 key roles only (not every referee assignment)
- **Not adding computing skills section**: Too technical/detailed for web bio
- **Not including full languages section**: Can mention if needed, but not priority
- **Not updating other team members**: Franz and Vasundhara can be done later using same pattern
- **Not creating new layouts**: Extending existing member layout with CSS
- **Not using JavaScript**: Pure CSS solution for timeline styling
- **Not adding progress bars/skill indicators**: Academic CV style, not resume style

## Implementation Approach

The implementation follows a 7-phase approach:

1. **Phase 1**: Create custom CSS for CV timeline styling
2. **Phase 2**: Update front matter with correct links and metadata
3. **Phase 3**: Add Education and Professional Experience sections (concise)
4. **Phase 4**: Add Awards & Highlights section
5. **Phase 5**: Add Professional Activities (talks, service, supervision)
6. **Phase 6**: Add Research Identity sections (interests, software, outreach)
7. **Phase 7**: Test, polish, and verify responsiveness

Each phase builds incrementally and is testable before proceeding.

---

## Phase 1: Create Custom CSS for CV Timeline Styling

**Status**: Completed with styling adjustments in progress

### Overview
Add custom CSS styling for timeline-style CV entries with date badges, position titles, and clean visual hierarchy. This creates a professional, scannable layout similar to aleksas.eu/cv/ with a two-column grid layout (dates left, content right) while maintaining Jekyll's existing architecture.

**Note**: Initial implementation used fancy styling (colored dates, background boxes). Simplified to match reference site with clean two-column grid layout. Portrait column width set to 250px to align with CV date column.

### Changes Required:

#### 1. Create CV Styles File
**File**: `_styles/cv.scss` (new file)

**Content**:
```scss
// CV Timeline Styling
// Compact, professional layout for CV entries

// CV Entry Container
.cv-entry {
  position: relative;
  margin: 20px 0 30px 0;
  padding-left: 0;
  border-left: none;
}

// Date Badge (Year range on left)
.cv-date {
  display: inline-block;
  font-family: var(--heading);
  font-weight: var(--semi-bold);
  font-size: 0.9rem;
  color: var(--primary);
  margin-bottom: 5px;
}

// Position/Degree Title (Bold, prominent)
.cv-title {
  display: block;
  font-family: var(--heading);
  font-weight: var(--semi-bold);
  font-size: 1.1rem;
  color: var(--text);
  margin-bottom: 5px;
  line-height: 1.3;
}

// Institution/Company (Lighter weight)
.cv-institution {
  display: block;
  font-weight: var(--regular);
  font-size: 0.95rem;
  color: var(--text);
  opacity: 0.8;
  margin-bottom: 10px;
}

// Details list (bullets for accomplishments)
.cv-details {
  margin: 10px 0 0 20px;
  padding: 0;
  list-style-type: disc;
}

.cv-details li {
  margin: 5px 0;
  padding-left: 5px;
  font-size: 0.95rem;
  line-height: 1.5;
}

// Award/Highlight Entry (slightly different styling)
.cv-award {
  margin: 15px 0;
  padding: 15px;
  background: var(--background-alt);
  border-left: 3px solid var(--primary);
  border-radius: var(--rounded);
}

.cv-award .cv-title {
  font-size: 1rem;
  margin-bottom: 8px;
}

.cv-award .cv-date {
  font-size: 0.85rem;
  margin-right: 10px;
}

.cv-award p {
  margin: 5px 0;
  font-size: 0.9rem;
  line-height: 1.6;
}

// Compact list for talks/service (no bullets, just entries)
.cv-list {
  margin: 15px 0;
  padding: 0;
  list-style: none;
}

.cv-list li {
  margin: 8px 0;
  padding-left: 0;
  font-size: 0.95rem;
  line-height: 1.5;
}

.cv-list .cv-date {
  display: inline;
  margin-right: 10px;
  font-size: 0.9rem;
}

// Section with reduced vertical spacing
.cv-section {
  margin-bottom: 30px;
}

.cv-section h2 {
  margin-top: 40px;
  margin-bottom: 20px;
}

.cv-section h3 {
  margin-top: 25px;
  margin-bottom: 15px;
}

// Responsive adjustments
@media (max-width: 600px) {
  .cv-entry {
    padding-left: 0;
  }

  .cv-title {
    font-size: 1rem;
  }

  .cv-date {
    font-size: 0.85rem;
  }

  .cv-award {
    padding: 10px;
  }
}
```

**Why this CSS**:
- Creates visual hierarchy with date badges and title prominence
- Maintains existing Jekyll color variables (--primary, --text, etc.)
- Uses existing font families and weights from theme
- Adds subtle background for awards (scannable highlights)
- Responsive design for mobile (reduces font sizes)
- No timeline bars (simpler, more academic style)

#### 2. Import CV Styles in Main Stylesheet
**File**: `_styles/main.scss`

**Find the imports section** (around line 10-20) and add:
```scss
@import "cv";
```

**Example location** (`_styles/main.scss`):
```scss
@import "theme";
@import "variables";
@import "cv";  // <-- Add this line
@import "layout";
@import "section";
// ... other imports
```

### Success Criteria:

#### Automated Verification:
- [x] CV styles file exists: `test -f _styles/cv.scss`
- [x] CV styles imported in main.scss: Jekyll auto-includes all _styles/*.scss files
- [x] Site builds without SCSS errors: `cd /Users/aflorio/Documents/GroupWebsite/site && bundle exec jekyll build`
- [x] No broken CSS: Check build output for SCSS compilation errors

#### Manual Verification:
- [x] Local build completes successfully
- [x] No console errors when viewing site in browser
- [x] CSS file is generated in `_site/_styles/cv.css`
- [x] Two-column grid layout working (250px date column, content in right column)
- [x] Dates right-aligned within their column
- [x] Portrait column (250px) extends with dates below links

**Styling Notes**:
- Grid layout: `grid-template-columns: 250px 1fr; gap: 40px`
- Portrait float width matched to date column: 250px
- Dates right-aligned for clean visual separation
- All content uses `grid-column: 2` to stay in right column

**Implementation Note**: After automated checks pass, verify that the site still builds and displays correctly. The CSS won't be visible yet since we haven't applied the classes, but this ensures no syntax errors. Only proceed to Phase 2 after confirming the build succeeds.

---

## Phase 2: Update Front Matter with Correct Links

### Overview
Update Adrien Florio's member file front matter with accurate ORCID, homepage, and academic profile links from the CV. This ensures contact buttons display correct information.

### Changes Required:

#### 1. Update Member Front Matter
**File**: `_members/adrien-florio.md`

**Change front matter** (lines 1-13):

**Before**:
```yaml
---
name: Adrien Florio
image: images/team/adrien-florio.jpg
role: pi
affiliation: Bielefeld University
aliases:
  - A. Florio
  - A Florio
links:
  email: adrien.florio@uni-bielefeld.de
  orcid: 0000-0002-1234-5678
  home-page: https://qcreate-website-fa4cbb.pages.ub.uni-bielefeld.de/
---
```

**After**:
```yaml
---
name: Adrien Florio
image: images/team/adrien-florio.jpg
role: pi
affiliation: Bielefeld University
aliases:
  - A. Florio
  - A Florio
  - Adrien Florio
links:
  email: adrien.florio@uni-bielefeld.de
  orcid: 0000-0002-7276-4515
  home-page: https://cosmolattice.net
  inspirehep: https://inspirehep.net/authors/1844184
  google-scholar: AvWN0nIAAAAJ
---
```

**Changes**:
- ORCID updated to correct value: `0000-0002-7276-4515`
- Homepage changed to CosmoLattice site: `https://cosmolattice.net`
- Added INSPIRE-HEP link (full URL)
- Added Google Scholar ID (just the ID, button component will construct URL)
- Added "Adrien Florio" to aliases for publication searching

**Why these links**:
- ORCID and Google Scholar provide academic identity verification
- INSPIRE-HEP is the main physics publication database
- CosmoLattice homepage showcases software contributions
- Additional alias helps catch more publication variations

### Success Criteria:

#### Automated Verification:
- [x] ORCID updated: `grep "0000-0002-7276-4515" _members/adrien-florio.md`
- [x] Homepage updated: `grep "cosmolattice.net" _members/adrien-florio.md`
- [x] INSPIRE-HEP added: `grep "inspirehep" _members/adrien-florio.md`
- [x] Google Scholar added: `grep "google-scholar" _members/adrien-florio.md`
- [x] Site builds: `cd /Users/aflorio/Documents/GroupWebsite/site && bundle exec jekyll build`
- [x] No YAML errors: Check build output for parsing errors

#### Manual Verification:
- [ ] Local site builds without errors
- [ ] Navigate to http://localhost:4000/team/adrien-florio/
- [ ] Portrait sidebar shows all 5 contact buttons (email, ORCID, home-page, INSPIRE-HEP, Google Scholar)
- [ ] Clicking ORCID link opens https://orcid.org/0000-0002-7276-4515
- [ ] Clicking Google Scholar opens correct profile page
- [ ] Clicking INSPIRE-HEP opens https://inspirehep.net/authors/1844184
- [ ] Clicking homepage opens https://cosmolattice.net
- [ ] Email link opens mailto: with correct address

**Implementation Note**: Test all links thoroughly. Google Scholar button uses type system to construct URL (https://scholar.google.com/citations?user=AvWN0nIAAAAJ), while INSPIRE-HEP uses full URL directly. Both should work correctly based on existing button component logic. Only proceed after confirming all 5 buttons appear and link correctly.

---

## Phase 3: Add Education and Professional Experience Sections

### Overview
Add concise Education and Professional Experience sections using custom CV styling. Focus on **outcomes and impact** with 2-3 bullets per position, year-only dates, and clean visual hierarchy.

### Changes Required:

#### 1. Update Member Content - Education Section
**File**: `_members/adrien-florio.md`

**Replace the Background section** (around line 27-29) with:

```markdown
## Education

<div class="cv-entry">
<span class="cv-date">2016-2020</span>
<strong class="cv-title">PhD in Physics</strong>
<span class="cv-institution">EPFL, Lausanne, Switzerland</span>
<p style="margin: 5px 0; font-size: 0.95rem;">Supervisor: Prof. Mikhail Shaposhnikov</p>
</div>

<div class="cv-entry">
<span class="cv-date">2014-2016</span>
<strong class="cv-title">MSc in Physics</strong>
<span class="cv-institution">EPFL, Lausanne, Switzerland</span>
</div>

<div class="cv-entry">
<span class="cv-date">2014-2016</span>
<strong class="cv-title">Minor in Mathematics</strong>
<span class="cv-institution">EPFL, Lausanne, Switzerland</span>
</div>

<div class="cv-entry">
<span class="cv-date">2011-2014</span>
<strong class="cv-title">BSc in Physics</strong>
<span class="cv-institution">EPFL, Lausanne, Switzerland</span>
</div>

<div class="cv-entry">
<span class="cv-date">2008-2011</span>
<strong class="cv-title">Maturité Suisse</strong>
<span class="cv-institution">Gymnase d'Yverdon, Cheseaux-Noréaz, Switzerland</span>
</div>
```

**Why this format**:
- Year-only dates (concise, no months)
- Degree prominence with bold title
- Institution as secondary information
- PhD supervisor mentioned (academic credential)
- No bullet points needed for education (degrees are self-explanatory)

#### 2. Add Professional Experience Section
**File**: `_members/adrien-florio.md`

**Add after Education section**:

```markdown
## Professional Experience

<div class="cv-entry">
<span class="cv-date">2025-present</span>
<strong class="cv-title">Emmy Noether Junior Group Leader</strong>
<span class="cv-institution">Bielefeld University, Germany</span>
<ul class="cv-details">
  <li>Secured ~1.5M€ Emmy Noether Grant from German Research Foundation (DfG)</li>
  <li>Leading QuIReal research group on quantum information and real-time evolution in QFT</li>
  <li>Supervising 1 postdoc and 1 PhD student</li>
</ul>
</div>

<div class="cv-entry">
<span class="cv-date">2022-2025</span>
<strong class="cv-title">Goldhaber Distinguished Fellow</strong>
<span class="cv-institution">Brookhaven National Laboratory, Nuclear Theory Group, US</span>
<ul class="cv-details">
  <li>Co-design Center for Quantum Advantage (C2QA) researcher</li>
  <li>$34K yearly additional funding (salary bonus + travel/materials)</li>
  <li>Research highlighted in <a href="https://www.bnl.gov/newsroom/news.php?a=220996">BNL news</a></li>
</ul>
</div>

<div class="cv-entry">
<span class="cv-date">2020-2022</span>
<strong class="cv-title">Postdoctoral Researcher</strong>
<span class="cv-institution">Center for Nuclear Theory, Stony Brook University, US</span>
<ul class="cv-details">
  <li>Research on quantum field theory and quantum information</li>
  <li>Collaboration with Brookhaven National Laboratory</li>
</ul>
</div>
```

**Why this format**:
- **Impact-focused bullets**: Grant amounts, funding, team size, recognition
- **Concise**: 2-3 bullets per position (not 5-6)
- **Outcome over duty**: "Secured 1.5M€ grant" not "Responsible for grant writing"
- **Quantifiable**: Numbers (€, people supervised, years) provide concrete achievements
- **Link included**: BNL news article for credibility

### Success Criteria:

#### Automated Verification:
- [x] Education section exists: `grep -q "## Education" _members/adrien-florio.md`
- [x] Professional Experience section exists: `grep -q "## Professional Experience" _members/adrien-florio.md`
- [x] CV styling classes used: `grep -q "cv-entry" _members/adrien-florio.md`
- [x] All 5 degrees listed: `grep -c "cv-title" _members/adrien-florio.md` returns at least 8 (5 education + 3 positions)
- [x] Site builds successfully: `cd /Users/aflorio/Documents/GroupWebsite/site && bundle exec jekyll build`

#### Manual Verification:
- [ ] Navigate to http://localhost:4000/team/adrien-florio/
- [ ] Education section displays 5 entries in reverse chronological order (PhD first, Maturité last)
- [ ] Each education entry shows: date badge, degree title (bold), institution
- [ ] Professional Experience shows 3 positions in reverse chronological order
- [ ] Each position has 2-3 concise bullet points
- [ ] Date badges are styled in primary color
- [ ] Titles are bold and prominent
- [ ] Institutions are lighter weight (readable but secondary)
- [ ] Bullets are indented and use disc style
- [ ] BNL news link works and opens in new tab
- [ ] Layout looks clean on desktop (1920px) and mobile (375px)
- [ ] No text overflow or layout breaks

**Implementation Note**: After automated checks, visually inspect both sections. The timeline styling should create clear visual hierarchy with dates drawing the eye, titles being most prominent, and institutions/bullets providing supporting detail. If bullets seem too long, edit to be more concise (aim for one line per bullet). Only proceed after confirming the layout looks professional and scannable.

---

## Phase 4: Add Awards & Highlights Section

### Overview
Add a concise Awards & Highlights section showcasing the 4 major awards from the CV. Use award card styling for visual prominence and scannability.

### Changes Required:

#### 1. Add Awards Section
**File**: `_members/adrien-florio.md`

**Add after Professional Experience section**:

```markdown
## Awards & Highlights

<div class="cv-award">
<span class="cv-date">2025-present</span>
<strong class="cv-title">Emmy Noether Grant</strong>
<p>German Research Foundation (DfG). ~1,500,000€ funding to establish a junior research group on quantum information and real-time QFT evolution.</p>
</div>

<div class="cv-award">
<span class="cv-date">2022-2025</span>
<strong class="cv-title">Goldhaber Distinguished Fellowship</strong>
<p>Brookhaven National Laboratory. Prestigious fellowship with $22K yearly salary bonus and $12K travel/material fund. <a href="https://www.bnl.gov/newsroom/news.php?a=220996">Featured in BNL news</a>.</p>
</div>

<div class="cv-award">
<span class="cv-date">2023</span>
<strong class="cv-title">Buchalter Cosmology Prize</strong>
<p>Third place prize ($2,500) for "'Stairway to Heaven' – Spectroscopy of Particle Couplings with Gravitational Waves." <a href="http://www.buchaltercosmologyprize.org/">Prize announcement</a>.</p>
</div>

<div class="cv-award">
<span class="cv-date">2024</span>
<strong class="cv-title">DOE Highlight and Public Coverage</strong>
<p>Research on quantum real-time dynamics of string breaking (PRL 131, 021902) highlighted by <a href="https://science.osti.gov/np/Highlights/2023/NP-2023-11-g">US Department of Energy</a>, <a href="https://www.bnl.gov/newsroom/news.php?a=221731">BNL</a>, and featured on popular science podcast.</p>
</div>
```

**Why this format**:
- **Award card styling**: Light background, left border for visual distinction
- **One paragraph per award**: Concise, no bullet points needed
- **Key information**: Amount/recognition level, brief impact statement, link
- **Scannable**: Date + title immediately visible, details in paragraph
- **Links for credibility**: External validation from official sources

### Success Criteria:

#### Automated Verification:
- [ ] Awards section exists: `grep -q "## Awards & Highlights" _members/adrien-florio.md`
- [ ] 4 award cards present: `grep -c "cv-award" _members/adrien-florio.md` returns 4
- [ ] All awards have dates: `grep -c "cv-date" _members/adrien-florio.md` (within awards section)
- [ ] External links included: `grep -c "https://" _members/adrien-florio.md` returns at least 5
- [ ] Site builds: `cd /Users/aflorio/Documents/GroupWebsite/site && bundle exec jekyll build`

#### Manual Verification:
- [ ] Navigate to http://localhost:4000/team/adrien-florio/
- [ ] Awards section displays 4 award cards
- [ ] Each card has light background and primary-colored left border
- [ ] Date and title are prominent at top of each card
- [ ] Paragraphs are concise (1-2 sentences max)
- [ ] All 5 external links work:
  - [ ] BNL news (Goldhaber)
  - [ ] Buchalter prize announcement
  - [ ] DOE highlight
  - [ ] BNL research highlight
- [ ] Cards are visually distinct from regular content
- [ ] Mobile layout (375px) shows cards stacked properly without overflow
- [ ] Award amounts are clearly visible (€1.5M, $2.5K, etc.)

**Implementation Note**: Awards should stand out visually from other sections due to background styling. If paragraphs seem long, trim to essential facts only (award name, amount, one-sentence impact). The goal is someone scanning the page should immediately see "Emmy Noether Grant - €1.5M" and understand the significance. Only proceed after confirming awards are visually prominent and scannable.

---

## Phase 5: Add Professional Activities (Talks, Service, Supervision)

### Overview
Add curated professional activities showcasing the most impactful talks, service roles, and current supervision. Maximum 5 talks, 3-4 service items, keep it brief.

### Changes Required:

#### 1. Add Selected Invited Talks
**File**: `_members/adrien-florio.md`

**Add after Awards section**:

```markdown
## Selected Invited Talks

<ul class="cv-list">
<li><span class="cv-date">2026</span> <strong>APS March/April Meeting</strong>, Denver – Symposium "Advances in Quantum Simulation for Nuclear Physics"</li>
<li><span class="cv-date">2025</span> <strong>DPG Quantum 2025</strong>, Göttingen – Symposium "Quantum Thermalization"</li>
<li><span class="cv-date">2024</span> <strong>Plenary Talk:</strong> Conference "Strong and Electroweak Matter", Frankfurt</li>
<li><span class="cv-date">2024</span> <strong>CERN Workshop</strong> – "Non-perturbative and Topological Aspects of QCD"</li>
<li><span class="cv-date">2023</span> <strong>Workshop "Quantum Entanglement in HEP"</strong>, Cracow</li>
</ul>
```

**Why this selection**:
- **5 talks maximum**: Most prestigious only (plenary, major conferences)
- **Prominent venues**: APS, DPG, CERN, Frankfurt plenary
- **No details needed**: Venue and topic are sufficient
- **Compact list format**: One line per talk, date badge for quick scanning

#### 2. Add Professional Service
**File**: `_members/adrien-florio.md`

**Add after Selected Talks**:

```markdown
## Professional Service

**Organizing Committees**
- Advanced Lectures in Physics in Switzerland (ALPS) summer school series (2024-2026) – Secured CHF 30K+ funding, organized 3 editions
- CosmoLattice School 2022 – PhD summer school organizer

**Advisory & Editorial Roles**
- Advisory Committee, Graduate and Academic Career Development Centre, Bielefeld University
- Referee for Physical Review Letters (PRL), JHEP, JCAP, Nature Communications
- Seminar organizer: BNL Nuclear Theory Seminars (2022-2025)
```

**Why this format**:
- **Grouped by category**: Organizing, Advisory/Editorial
- **One line per role**: No lengthy descriptions
- **Key details only**: Funding amounts (CHF 30K), journal names, years
- **Impact highlighted**: "Secured funding", "3 editions" shows sustained contribution

#### 3. Add Teaching & Supervision
**File**: `_members/adrien-florio.md`

**Add after Professional Service**:

```markdown
## Teaching & Supervision

**Current Supervision**
- Vasundhara Krishnan (PhD student, 2025-present)
- Franz Sattler (Postdoctoral researcher, 2025-present)

**Teaching Highlights**
- PhD Summer School Lectures: CosmoLattice software (2022, 2023), YETI 2022 "Phenomenology in the sky"
- Teaching Assistant, EPFL (2016-2019): General Relativity and Cosmology, Quantum Mechanics III

**Past Mentorship**
- Supervised 3 Master students (EPFL, 2019-2021)
- Mentored 2 PhD students (Valencia, Stony Brook, 2020-2024)
```

**Why this format**:
- **Current supervision first**: Most relevant, shows active research group
- **Teaching summarized**: No need to list every course, highlights suffice
- **Numbers provided**: 3 master students, 2 PhD mentorships (quantifiable impact)
- **Concise**: Each category is 2-3 lines max

### Success Criteria:

#### Automated Verification:
- [ ] Selected Talks section exists: `grep -q "## Selected Invited Talks" _members/adrien-florio.md`
- [ ] 5 talks listed: `grep -c "<li>" _members/adrien-florio.md` (within talks section) returns 5
- [ ] Professional Service section exists: `grep -q "## Professional Service" _members/adrien-florio.md`
- [ ] Teaching & Supervision section exists: `grep -q "## Teaching & Supervision" _members/adrien-florio.md`
- [ ] Current supervision mentions both: `grep "Vasundhara Krishnan" _members/adrien-florio.md` and `grep "Franz Sattler" _members/adrien-florio.md`
- [ ] Site builds: `cd /Users/aflorio/Documents/GroupWebsite/site && bundle exec jekyll build`

#### Manual Verification:
- [ ] Navigate to http://localhost:4000/team/adrien-florio/
- [ ] Selected Talks section shows 5 entries in reverse chronological order (2026 first)
- [ ] Each talk entry is one line with date badge
- [ ] Talk venues are recognizable (APS, DPG, CERN clearly visible)
- [ ] Professional Service section has 2 subsections (Organizing, Advisory/Editorial)
- [ ] Service items are concise (no entry exceeds 2 lines)
- [ ] Teaching & Supervision shows:
  - [ ] Current Supervision with 2 people (Vasundhara, Franz)
  - [ ] Teaching Highlights with PhD schools and EPFL TA work
  - [ ] Past Mentorship with counts (3 master, 2 PhD)
- [ ] All sections are scannable (no dense paragraphs)
- [ ] Mobile layout displays properly (no text overflow)

**Implementation Note**: These sections demonstrate ongoing professional engagement. If any entry seems too long, trim to essentials. For example, "Secured CHF 30K+ funding, organized 3 editions" could be shortened to just "Organizer, 2024-2026" if space is tight. The goal is showing breadth of professional activity without overwhelming detail. Only proceed after confirming all three sections are present and concise.

---

## Phase 6: Add Research Identity Sections (Interests, Software, Outreach)

### Overview
Finalize the member page with refined Research Interests, Software contributions, and Outreach activities. Keep each section brief and focused.

### Changes Required:

#### 1. Refine Research Interests Section
**File**: `_members/adrien-florio.md`

**Update the existing Research Interests section** (currently at line 19-25) to be more concise:

**Replace with**:
```markdown
## Research Interests

- Quantum information in high-energy physics and cosmology
- Real-time dynamics in quantum field theory
- Quantum entanglement and thermalization in gauge theories
- Early universe dynamics and gravitational wave signatures
- Lattice field theory simulations and quantum computing applications
```

**Why this version**:
- **5 bullet points**: Covers key areas without redundancy
- **Concise phrasing**: Each bullet is one line
- **Keyword-rich**: Good for search and quick scanning
- **Balanced**: Theory, methods, and applications represented

#### 2. Add Software Section
**File**: `_members/adrien-florio.md`

**Add after Research Interests**:

```markdown
## Software

**CosmoLattice** – Creator and Lead Developer
Open-source modern C++ Expression Template library for lattice field theory simulations. Used by research groups worldwide for real-time QFT dynamics and cosmology. [cosmolattice.net](https://cosmolattice.net)
```

**Why this format**:
- **Single software highlight**: CosmoLattice is the main contribution
- **Two sentences**: What it is + impact
- **Link included**: Direct to project website
- **Concise**: No need to list every feature or technical detail

#### 3. Add Outreach Section
**File**: `_members/adrien-florio.md`

**Add after Software section**:

```markdown
## Outreach & Public Engagement

- **REYES** (2024) – Online tutor at Lawrence Berkeley National Lab for high school STEM education
- **QISE High School Summer School** (2022-2024) – Tutor teaching quantum computing to high school students, Virginia Tech (3 sessions)
- **C2QA Quantum Thursdays** (2023) – Invited speaker for undergraduate outreach talk on quantum information
```

**Why this format**:
- **3 programs**: Most significant outreach activities
- **One line each**: Program name, year, brief description
- **Audience clear**: High school students, undergraduates
- **Bold program names**: Easy to scan

### Success Criteria:

#### Automated Verification:
- [ ] Research Interests section exists: `grep -q "## Research Interests" _members/adrien-florio.md`
- [ ] 5 research bullets: Count bullets in Research Interests section equals 5
- [ ] Software section exists: `grep -q "## Software" _members/adrien-florio.md`
- [ ] CosmoLattice mentioned: `grep "CosmoLattice" _members/adrien-florio.md`
- [ ] Outreach section exists: `grep -q "## Outreach" _members/adrien-florio.md`
- [ ] 3 outreach programs listed: `grep -c "^\- \*\*" _members/adrien-florio.md` (within outreach section) returns 3
- [ ] Site builds: `cd /Users/aflorio/Documents/GroupWebsite/site && bundle exec jekyll build`

#### Manual Verification:
- [ ] Navigate to http://localhost:4000/team/adrien-florio/
- [ ] Research Interests section shows 5 concise bullet points
- [ ] Each research interest is one line (no wrapping on desktop 1920px)
- [ ] Software section displays:
  - [ ] "CosmoLattice" in bold
  - [ ] "Creator and Lead Developer" as subtitle
  - [ ] Two-sentence description
  - [ ] Link to cosmolattice.net works
- [ ] Outreach section shows 3 programs
- [ ] Each outreach entry is one line
- [ ] Program names are bold for scanning
- [ ] Years and institutions are clearly visible
- [ ] All sections together fit in ~2 scroll-lengths on desktop
- [ ] Mobile view (375px) displays all sections properly stacked

**Implementation Note**: After adding these sections, review the entire page from top to bottom. The complete profile should be scannable in 30-60 seconds. If any section seems too long, trim further. Research Interests should be quick bullet points, Software should be 2-3 sentences max, Outreach should be a simple list. Only proceed to Phase 7 after confirming the complete page reads well and nothing feels excessive.

---

## Phase 7: Testing, Polish, and Verification

### Overview
Final testing phase to ensure the complete CV-style member page is professional, responsive, and error-free. Test on multiple devices and verify all links.

### Changes Required:

#### 1. Final Content Review
**File**: `_members/adrien-florio.md`

**Review checklist** (make edits if needed):
- [ ] No section exceeds 10 lines of content
- [ ] All bullets are outcome-focused (no "responsible for" language)
- [ ] Dates are year-only (no months)
- [ ] All external links are working and open in new tabs
- [ ] No placeholder text remains (e.g., "[Add content here]")
- [ ] Introduction paragraph at top is concise (2-3 sentences)
- [ ] Section order makes sense: Intro → Interests → Education → Experience → Awards → Talks → Service → Teaching → Software → Outreach → Publications (auto-generated)

#### 2. Build and Serve Test
**Commands**:
```bash
cd /Users/aflorio/Documents/GroupWebsite/site

# Clean build
bundle exec jekyll clean
bundle exec jekyll build

# Serve locally
bundle exec jekyll serve --port 4000
```

**Verify in browser**: http://localhost:4000/team/adrien-florio/

#### 3. Responsive Testing
**Test on multiple viewport sizes**:
- **Desktop (1920x1080)**: Portrait sidebar floats left, content flows right, all sections visible
- **Laptop (1366x768)**: Similar to desktop, verify no horizontal scroll
- **Tablet (768x1024)**: Portrait should still float or stack depending on breakpoint
- **Mobile (375x667)**: Portrait stacks on top, all sections stack vertically, no text overflow

**Browser DevTools**: Use responsive design mode to test breakpoints

#### 4. Link Verification
**Test all external links**:
- [ ] ORCID link (https://orcid.org/0000-0002-7276-4515)
- [ ] Homepage (https://cosmolattice.net)
- [ ] INSPIRE-HEP (https://inspirehep.net/authors/1844184)
- [ ] Google Scholar (constructs URL from ID)
- [ ] BNL news (Goldhaber Fellowship)
- [ ] Buchalter Prize announcement
- [ ] DOE highlight
- [ ] BNL research highlight
- [ ] CosmoLattice website
- [ ] Email (mailto: link)

**Verify**:
- All links open correctly
- External links open in new tab
- No broken links (404 errors)

#### 5. Visual Polish Check
**Inspect visually**:
- [ ] CV timeline styling applies correctly (date badges, title prominence)
- [ ] Award cards have light background and left border
- [ ] Proper spacing between sections (not too cramped, not too much whitespace)
- [ ] Font sizes are readable (minimum 14px on mobile)
- [ ] Colors match theme (primary color for dates, text color for content)
- [ ] Portrait sidebar displays properly with all 5 buttons
- [ ] No layout breaks or overlapping text
- [ ] Lists are properly indented
- [ ] Bold and emphasis used appropriately

#### 6. Performance Check
**Test page load**:
- [ ] Page loads in < 2 seconds on good connection
- [ ] No console errors in browser DevTools
- [ ] No missing images (portrait, any linked images)
- [ ] CSS loads completely (check Network tab)
- [ ] No JavaScript errors (check Console tab)

#### 7. Content Scannability Test
**30-second scan test** (have someone else try this):
- Can someone understand your:
  - [ ] Current position (Emmy Noether Group Leader)
  - [ ] Main research areas (quantum info + real-time QFT)
  - [ ] Key achievements (Emmy Noether grant, Goldhaber fellowship)
  - [ ] Academic background (PhD from EPFL)
  - [ ] Software contribution (CosmoLattice)

If they can't grasp these in 30 seconds, content is too dense – trim further.

### Success Criteria:

#### Automated Verification:
- [ ] Site builds without errors: `cd /Users/aflorio/Documents/GroupWebsite/site && bundle exec jekyll build`
- [ ] No broken internal links: `htmlproofer ./_site --disable-external` (if htmlproofer installed)
- [ ] CV styles present in output CSS: `grep -q "cv-entry" _site/main.css`
- [ ] Member page generated: `test -f _site/team/adrien-florio/index.html`
- [ ] All sections present in HTML: `grep -c "<h2>" _site/team/adrien-florio/index.html` returns at least 9

#### Manual Verification:
- [ ] **Desktop (1920x1080)**:
  - [ ] Portrait floats left at ~175px width
  - [ ] Main content flows right of portrait
  - [ ] All sections display without horizontal scroll
  - [ ] CV timeline styling visible (date badges in primary color)
  - [ ] Award cards have light background
  - [ ] Section headings have bottom border (H2 style)

- [ ] **Tablet (768x1024)**:
  - [ ] Portrait either floats or stacks (depending on breakpoint)
  - [ ] Content is readable and properly spaced
  - [ ] No layout breaks or overlapping text

- [ ] **Mobile (375x667)**:
  - [ ] Portrait stacks on top (full width)
  - [ ] Contact buttons stack vertically
  - [ ] All content sections stack properly
  - [ ] No text overflow (all text wraps correctly)
  - [ ] Font sizes are readable (min 14px)
  - [ ] Date badges don't cause horizontal scroll

- [ ] **All Links Work**:
  - [ ] 10 external links tested and functional
  - [ ] Email opens mail client
  - [ ] Academic profiles (ORCID, INSPIRE, Scholar) open correctly

- [ ] **Content Quality**:
  - [ ] No section exceeds 10 lines
  - [ ] All bullets are concise (one line each)
  - [ ] No placeholder text remains
  - [ ] Language is outcome-focused
  - [ ] Dates are consistent (year-only format)

- [ ] **Visual Quality**:
  - [ ] Clean, professional appearance
  - [ ] Consistent spacing between sections
  - [ ] Colors match theme
  - [ ] Typography is readable
  - [ ] Award cards stand out visually

- [ ] **Performance**:
  - [ ] Page loads quickly (< 2 seconds)
  - [ ] No console errors
  - [ ] All assets load completely

- [ ] **Scannability**:
  - [ ] 30-second scan test passes
  - [ ] Key information immediately visible
  - [ ] Clear visual hierarchy (dates → titles → details)

**Implementation Note**: This is the final validation phase. Test thoroughly on multiple devices and browsers (Chrome, Firefox, Safari). Ask a colleague to review the page and provide feedback on scannability and clarity. If anything feels off, go back and refine. The goal is a professional, concise, scannable CV-style page that loads fast and looks good everywhere. Only mark complete after all manual verifications pass.

---

## Testing Strategy

### Build Tests
- Jekyll build completes without errors
- SCSS compiles without syntax errors
- All YAML front matter parses correctly
- No liquid template errors
- Generated HTML is valid

### Visual Regression Tests
- Portrait sidebar doesn't break with new content
- Float layout still works on mobile
- Existing Greene Lab styling not affected
- Theme colors apply correctly to new CV styles
- Award cards render with proper background/border

### Responsive Design Tests
- Test 4 breakpoints: 1920px, 1366px, 768px, 375px
- Portrait sidebar behavior at 600px breakpoint
- CV entry layout on narrow screens
- Date badges don't cause horizontal scroll
- Lists wrap properly on mobile

### Link Validation
- All 10+ external links functional
- ORCID, INSPIRE, Google Scholar URLs correct
- Email mailto: link works
- Award announcement links valid
- Software homepage accessible

### Content Quality Tests
- Each section independently scannable
- No section exceeds 10 lines
- Bullets are outcome-focused
- Dates are consistent (year-only)
- No placeholder text remains

### Performance Tests
- Page load time < 2 seconds
- CSS file size reasonable (< 100KB)
- No render-blocking resources
- Images load efficiently (lazy loading)
- No JavaScript errors

---

## Performance Considerations

### CSS Impact
- **Added file size**: ~2-3KB for CV styles (minimal)
- **Render performance**: Pure CSS, no JavaScript needed
- **Caching**: CSS bundles with main.css, cached by browser
- **Mobile performance**: Responsive CSS, no separate mobile stylesheet

### Content Size
- **Essential highlights only**: Keeps page < 50KB total
- **No large images**: Portrait is only image on page
- **Concise text**: Faster to read and render
- **External links**: Don't slow page load

### Build Time
- **SCSS compilation**: Adds < 0.1s to build time
- **Jekyll generation**: No impact (same number of pages)
- **CI/CD**: No significant change to deployment time

---

## Migration Notes

This is not a migration – creating new content for existing page. However, for future reference:

**If migrating other team members to CV style**:
1. Copy custom CSS (already in `_styles/cv.scss`, no duplication needed)
2. Follow same content structure (Education → Experience → Awards → etc.)
3. Use same HTML classes (`cv-entry`, `cv-award`, `cv-list`)
4. Maintain conciseness rules (max 2-3 bullets per position)
5. Verify responsive layout for each new member

**If reverting to simple markdown**:
1. Remove HTML div wrappers and class attributes
2. Convert to standard markdown headings and lists
3. Custom CSS remains harmless (unused classes have no effect)

---

## Maintenance Workflow

### Adding a New Position
**Time**: ~5 minutes

**Steps**:
1. Edit `_members/adrien-florio.md`
2. Add new `<div class="cv-entry">` at top of Professional Experience
3. Include: date, title, institution, 2-3 bullets
4. Test locally: `bundle exec jekyll serve`
5. Commit and push

**Example**:
```markdown
<div class="cv-entry">
<span class="cv-date">2026-present</span>
<strong class="cv-title">Professor of Physics</strong>
<span class="cv-institution">New University, Germany</span>
<ul class="cv-details">
  <li>Leading research group of 10+ members</li>
  <li>Secured €3M collaborative research grant</li>
</ul>
</div>
```

### Adding a New Award
**Time**: ~3 minutes

**Steps**:
1. Edit `_members/adrien-florio.md`
2. Add new `<div class="cv-award">` at top of Awards section
3. Include: date, title, one-sentence description + link
4. Test and commit

### Updating Current Supervision
**Time**: ~2 minutes

**Steps**:
1. Edit Teaching & Supervision section
2. Update Current Supervision list (add new member or move to Past)
3. Update counts if needed (e.g., "Supervised 4 Master students")
4. Test and commit

### Adding a New Talk
**Time**: ~1 minute

**Steps**:
1. Edit Selected Invited Talks section
2. Add new `<li>` at top (reverse chronological)
3. Format: `<span class="cv-date">YEAR</span> <strong>Venue</strong>, Location – Details`
4. Keep total at 5 talks (remove oldest if adding new)
5. Test and commit

---

## Troubleshooting Guide

### Issue: CV Styling Not Applying

**Symptoms**: Content displays but no timeline styling, dates not colored, awards have no background

**Solutions**:
1. Check CV styles imported: `grep "cv" _styles/main.scss`
2. Verify SCSS compilation: `bundle exec jekyll build` shows no errors
3. Clear Jekyll cache: `bundle exec jekyll clean && bundle exec jekyll build`
4. Check browser cache: Hard reload (Cmd+Shift+R) or incognito mode
5. Inspect element in DevTools: Check if `.cv-entry`, `.cv-date`, etc. classes exist in HTML

### Issue: Layout Breaks on Mobile

**Symptoms**: Text overflow, horizontal scroll, overlapping elements

**Solutions**:
1. Check date badge length: Keep years only ("2020-2022" not "September 2020 - August 2022")
2. Verify viewport meta tag in `_layouts/default.html`: `<meta name="viewport" content="width=device-width, initial-scale=1">`
3. Test exact breakpoint: Use DevTools responsive mode at 600px, 375px
4. Reduce content: If bullets are too long, shorten to one line
5. Check CSS media queries: Ensure `@media (max-width: 600px)` rules in `cv.scss` are present

### Issue: Portrait Sidebar Overlaps Content

**Symptoms**: Portrait and main content overlap, text wraps around portrait awkwardly

**Solutions**:
1. Check float.scss: `max-width: 50%` should be set on `.float`
2. Verify content width: Main content should not exceed available space
3. Reduce portrait width: Try changing `_styles/portrait.scss` width from 175px to 150px
4. Test breakpoint behavior: Portrait should stack at 600px
5. Add clear fix: Ensure `{% include float.html %}` has proper parameters

### Issue: Links Not Working

**Symptoms**: ORCID, Google Scholar, or other links don't open correctly

**Solutions**:
1. **ORCID**: Verify format in front matter: `orcid: 0000-0002-7276-4515` (just the ID)
2. **Google Scholar**: Check ID format: `google-scholar: AvWN0nIAAAAJ` (alphanumeric ID only)
3. **INSPIRE-HEP**: Use full URL: `inspirehep: https://inspirehep.net/authors/1844184`
4. **Homepage**: Ensure URL is absolute: `home-page: https://cosmolattice.net` (include https://)
5. Check button component: `_includes/button.html` should process link types correctly
6. Verify types.yaml: Ensure link templates exist for each type

### Issue: Award Cards Not Displaying Background

**Symptoms**: Award entries look like regular text, no background color or left border

**Solutions**:
1. Check class name: Should be `<div class="cv-award">` (not `cv-entry`)
2. Verify CSS loaded: Inspect element, check if `.cv-award` styles present
3. Check theme variables: `--background-alt` and `--primary` should be defined in `_styles/-theme.scss`
4. Browser compatibility: Test in different browser (Safari, Firefox, Chrome)
5. Clear cache and rebuild: `bundle exec jekyll clean && bundle exec jekyll build`

### Issue: Page Too Long / Too Dense

**Symptoms**: Page scrolls for too long, information overload

**Solutions**:
1. **Trim bullets**: Each position should have max 2-3 bullets, one line each
2. **Reduce talks**: Keep only 5 most prestigious (remove others)
3. **Consolidate service**: Group similar roles ("Referee for 5+ journals" instead of listing each)
4. **Shorten descriptions**: Award descriptions should be one sentence
5. **Remove sections**: If needed, remove Outreach or Software sections temporarily
6. **Test scannability**: 30-second scan test – can someone grasp key points quickly?

### Issue: Dates Not Colored/Styled

**Symptoms**: Dates appear as regular text, not in primary color

**Solutions**:
1. Check class usage: Should be `<span class="cv-date">2020-2022</span>`
2. Verify CSS rule: `.cv-date { color: var(--primary); }` should exist in `cv.scss`
3. Check theme variable: `--primary` should be defined in `_styles/-theme.scss`
4. Inspect element: Use DevTools to check computed styles
5. Specificity issue: Ensure no other CSS rules override `.cv-date` color

### Issue: Build Fails After Changes

**Symptoms**: `bundle exec jekyll build` returns errors

**Solutions**:
1. **YAML error**: Check front matter syntax (proper indentation, no tabs)
2. **HTML error**: Verify all `<div>` tags are closed, quotes are matched
3. **Liquid error**: Check for unmatched `{% %}` or `{{ }}` tags
4. **SCSS error**: Look for syntax errors in `cv.scss` (missing semicolons, braces)
5. **Read error message**: Jekyll errors usually point to exact file and line number

---

## References

- **Original research document**: `thoughts/shared/research/2025-11-11-cv-style-personal-page-architecture.md`
- **CV source**: `~/ProtonDrive/Documents/cv/cv.pdf`
- **Reference CVs**:
  - https://aleksas.eu/cv/ (al-folio theme)
  - https://www.repond.ch/#resume (concise, visual)
- **Jekyll Documentation**: https://jekyllrb.com/docs/
- **SCSS Documentation**: https://sass-lang.com/documentation/
- **Greene Lab Website Plan**: `thoughts/shared/plans/2025-11-07-greene-lab-website-setup.md`

---

## Appendix A: Complete File Structure

```
site/
├── _styles/
│   ├── cv.scss                 # NEW: Custom CV timeline styles
│   ├── main.scss               # MODIFIED: Import cv.scss
│   └── [other styles]
├── _members/
│   └── adrien-florio.md        # MODIFIED: CV content with HTML classes
├── _layouts/
│   └── member.html             # UNCHANGED: Existing layout works
├── _includes/
│   ├── portrait.html           # UNCHANGED: Portrait component
│   ├── button.html             # UNCHANGED: Contact buttons
│   └── float.html              # UNCHANGED: Sidebar float
└── _data/
    └── types.yaml              # UNCHANGED: Link type definitions
```

---

## Appendix B: CSS Class Reference

| Class | Purpose | Parent Element |
|-------|---------|----------------|
| `.cv-entry` | Container for position/degree entry | `<div>` |
| `.cv-date` | Year range badge (colored) | `<span>` |
| `.cv-title` | Position/degree title (bold) | `<strong>` |
| `.cv-institution` | Institution/company name | `<span>` |
| `.cv-details` | Bullet list for accomplishments | `<ul>` |
| `.cv-award` | Award card container (background) | `<div>` |
| `.cv-list` | Compact list for talks/service | `<ul>` |
| `.cv-section` | Reduced spacing section wrapper | `<div>` (optional) |

---

## Appendix C: Content Guidelines Summary

### Conciseness Rules:
- **Positions**: Max 3 bullets, outcome-focused ("Published X", "Led Y", "Secured Z€")
- **Awards**: One sentence + link
- **Talks**: Just title, venue, year (one line)
- **Service**: One line per role
- **Education**: Degree, institution, year (no bullets needed)

### Formatting Rules:
- **Dates**: Year-only ("2020-2022" not "Sep 2020 - Aug 2022")
- **Bullets**: One line each, start with verb ("Secured", "Led", "Published")
- **Links**: Include for credibility (award announcements, news coverage)
- **Bold**: Use sparingly (position titles, award names, program names)

### Length Targets:
- **Education**: 5 entries, no bullets = ~10 lines total
- **Experience**: 3 positions × 3 bullets = ~15 lines total
- **Awards**: 4 cards × 2 lines each = ~10 lines total
- **Talks**: 5 entries = ~5 lines total
- **Service**: 6-8 items = ~8 lines total
- **Total page**: ~60-80 lines of content (excluding headings/spacing)

---

## Appendix D: Example Full Member Page Structure

**Complete section order**:
1. Introduction (2-3 sentences)
2. Research Interests (5 bullets)
3. Education (5 entries)
4. Professional Experience (3 positions)
5. Awards & Highlights (4 cards)
6. Selected Invited Talks (5 entries)
7. Professional Service (6-8 items)
8. Teaching & Supervision (3 subsections)
9. Software (1 entry)
10. Outreach (3 programs)
11. Selected Publications (auto-generated by Jekyll)

**Estimated total length**: 2-3 screen heights on desktop, ~5-6 swipes on mobile

**Reading time**: 2-3 minutes full read, 30 seconds for scanning

---

## Conclusion

This implementation plan provides a step-by-step approach to creating a concise, CV-style member page with custom timeline CSS. The plan emphasizes **scannability, conciseness, and visual hierarchy** while maintaining Jekyll's existing architecture and mobile responsiveness.

**Key Success Factors**:
1. Follow phases sequentially – test at each step
2. Maintain conciseness – trim ruthlessly
3. Verify responsiveness – test on mobile
4. Focus on outcomes – not duties
5. Keep it scannable – 30-second test

**After Completion**:
- Page loads quickly and looks professional
- All sections are scannable and concise
- Responsive layout works on all devices
- Easy to maintain (add positions, awards, talks)
- Can be used as template for other team members

**Questions or Issues**:
- Consult Troubleshooting Guide (Appendix)
- Review research document for architecture details
- Test locally before pushing to production
- Ask for feedback from colleagues on scannability
