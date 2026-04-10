---
name: Adrien Florio
image: images/team/adrien-florio.jpg
role: group-leader
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

Adrien Florio is the Group Leader of the $\left\lvert\chi\right\rangle$real **Emmy Noether** research group at **Bielefeld University** and **Project Leader** in the Collaborative Research Center-Transregio **CRC-TR 211** (Project A02).

<details class="cv-section" open>
<summary><h2>Positions</h2></summary>

{% for pos in site.data.cv.positions %}
<div class="cv-entry">
<span class="cv-date">{{ pos.date }}</span>
<strong class="cv-title">{{ pos.title }}</strong>
<span class="cv-institution">{{ pos.institution }}, {{ pos.location }}{% if pos.details %} · {{ pos.details }}{% endif %}</span>
</div>
{% endfor %}

</details>

<details class="cv-section" open>
<summary><h2>Funding</h2></summary>

{% for f in site.data.cv.funding %}
<div class="cv-entry">
<span class="cv-date">{{ f.date }}</span>
<strong class="cv-title">{{ f.title }}</strong>
<span class="cv-institution">{{ f.funder }}</span>
{% if f.details %}<p>{{ f.details }}</p>{% endif %}
</div>
{% endfor %}

</details>

<details class="cv-section" open>
<summary><h2>Awards &amp; Highlights</h2></summary>

{% for a in site.data.cv.awards %}
<div class="cv-award">
<span class="cv-date">{{ a.date }}</span>
<strong class="cv-title">{{ a.title }}{% if a.institution %}, {{ a.institution }}{% endif %}</strong>
{% if a.description %}<p>{{ a.description }}</p>{% endif %}
</div>
{% endfor %}

</details>

<details class="cv-section" open>
<summary><h2>Selected Talks</h2></summary>

<h3 class="cv-subsection">Plenary Talks</h3>

{% for talk in site.data.cv.selected_talks %}{% if talk.type == "Plenary talk" %}
<div class="cv-entry">
<span class="cv-date">{{ talk.date }}</span>
<strong class="cv-title">{% if talk.url %}<a href="{{ talk.url }}">{{ talk.event }}</a>{% else %}{{ talk.event }}{% endif %}{% if talk.event_detail %} — {{ talk.event_detail }}{% endif %}</strong>
{% if talk.location %}<span class="cv-institution">{{ talk.location }}</span>{% endif %}
</div>
{% endif %}{% endfor %}

<h3 class="cv-subsection">Invited Talks</h3>

{% for talk in site.data.cv.selected_talks %}{% if talk.type == "Invited talk" %}
<div class="cv-entry">
<span class="cv-date">{{ talk.date }}</span>
<strong class="cv-title">{% if talk.url %}<a href="{{ talk.url }}">{{ talk.event }}</a>{% else %}{{ talk.event }}{% endif %}{% if talk.event_detail %} — {{ talk.event_detail }}{% endif %}</strong>
{% if talk.location %}<span class="cv-institution">{{ talk.location }}</span>{% endif %}
</div>
{% endif %}{% endfor %}

</details>

<details class="cv-section">
<summary><h2>Education</h2></summary>

<div class="cv-multicol">
{% for edu in site.data.cv.education %}
<div class="cv-entry">
<span class="cv-date">{{ edu.date }}</span>
<strong class="cv-title">{{ edu.degree }}</strong>
<span class="cv-institution">{{ edu.institution }}, {{ edu.location }}{% if edu.details %} · {{ edu.details }}{% endif %}</span>
</div>
{% endfor %}
</div>

</details>

<details class="cv-section">
<summary><h2>Professional Services</h2></summary>

<h3 class="cv-subsection">Advisory Committees</h3>

{% for item in site.data.cv.professional_services.advisory_committees %}
<div class="cv-entry">
<span class="cv-date">{{ item.date }}</span>
<strong class="cv-title">{{ item.title }}</strong>
<span class="cv-institution">{{ item.institution }}, {{ item.location }}</span>
</div>
{% endfor %}

<div class="cv-multicol">

<h3 class="cv-subsection">Organizing Committees</h3>

{% for item in site.data.cv.professional_services.organizing_committees %}
<div class="cv-entry">
<span class="cv-date">{{ item.date }}</span>
<strong class="cv-title">{{ item.title }}</strong>
{% if item.description %}<p>{{ item.description }}</p>{% endif %}
</div>
{% endfor %}

<h3 class="cv-subsection">Referee</h3>

{% for item in site.data.cv.professional_services.referee %}
<div class="cv-entry">
<span class="cv-date">{{ item.date }}</span>
{% if item.journals %}
<strong class="cv-title">{{ item.journals }}</strong>
{% else %}
<strong class="cv-title">{{ item.title }}</strong>
{% endif %}
</div>
{% endfor %}

<h3 class="cv-subsection">Seminar Organization</h3>

{% for item in site.data.cv.professional_services.seminar_organization %}
<div class="cv-entry">
<span class="cv-date">{{ item.date }}</span>
<strong class="cv-title">{{ item.title }}</strong>
</div>
{% endfor %}

</div>

</details>

<details class="cv-section">
<summary><h2>Supervision</h2></summary>

<p class="cv-summary">{{ site.data.cv.supervision.summary }}</p>

<div class="cv-multicol">

<h3 class="cv-subsection">PhD Students</h3>

{% for s in site.data.cv.supervision.phd_students %}
<div class="cv-entry">
<span class="cv-date">{{ s.date }}</span>
<strong class="cv-title">{{ s.name }}</strong>
{% if s.description %}<span class="cv-institution">{{ s.description }}</span>{% endif %}
</div>
{% endfor %}

</div>

<h3 class="cv-subsection">Postdocs</h3>

{% for s in site.data.cv.supervision.postdocs %}
<div class="cv-entry">
<span class="cv-date">{{ s.date }}</span>
<strong class="cv-title">{{ s.name }}</strong>
{% if s.description %}<span class="cv-institution">{{ s.description }}</span>{% endif %}
</div>
{% endfor %}

<div class="cv-multicol">

<h3 class="cv-subsection">Master Students</h3>

{% for s in site.data.cv.supervision.master_students %}
<div class="cv-entry">
<span class="cv-date">{{ s.date }}</span>
<strong class="cv-title">{{ s.name }}</strong>
{% if s.description %}<span class="cv-institution">{{ s.description }}</span>{% endif %}
</div>
{% endfor %}

</div>

<h3 class="cv-subsection">Bachelor Students</h3>

{% for s in site.data.cv.supervision.bachelor_students %}
<div class="cv-entry">
<span class="cv-date">{{ s.date }}</span>
<strong class="cv-title">{{ s.name }}</strong>
{% if s.description %}<span class="cv-institution">{{ s.description }}</span>{% endif %}
</div>
{% endfor %}

<div class="cv-multicol">

<h3 class="cv-subsection">Mentorship</h3>

{% for s in site.data.cv.supervision.mentorship %}
<div class="cv-entry">
<span class="cv-date">{{ s.date }}</span>
<strong class="cv-title">{{ s.name }}</strong>
{% if s.description %}<span class="cv-institution">{{ s.description }}</span>{% endif %}
</div>
{% endfor %}

</div>

</details>

<details class="cv-section">
<summary><h2>Teaching</h2></summary>

<div class="cv-multicol">

<h3 class="cv-subsection">Courses</h3>

{% for t in site.data.cv.teaching.courses %}
<div class="cv-entry">
<span class="cv-date">{{ t.date }}</span>
<strong class="cv-title">{{ t.title }}</strong>
{% if t.description %}<span class="cv-institution">{{ t.description }}</span>{% endif %}
</div>
{% endfor %}

<h3 class="cv-subsection">PhD Schools &amp; Lectures</h3>

{% for t in site.data.cv.teaching.phd_schools %}
<div class="cv-entry">
<span class="cv-date">{{ t.date }}</span>
<strong class="cv-title">{% if t.url %}<a href="{{ t.url }}">{{ t.title }}</a>{% else %}{{ t.title }}{% endif %}</strong>
{% if t.topic %}<span class="cv-institution">{{ t.topic }}</span>{% endif %}
</div>
{% endfor %}

<h3 class="cv-subsection">Teaching Assistant</h3>

{% for t in site.data.cv.teaching.teaching_assistant %}
<div class="cv-entry">
<span class="cv-date">{{ t.date }}</span>
<strong class="cv-title">{{ t.title }}</strong>
</div>
{% endfor %}

<h3 class="cv-subsection">Workshops</h3>

{% for t in site.data.cv.teaching.workshops %}
<div class="cv-entry">
<span class="cv-date">{{ t.date }}</span>
<strong class="cv-title">{{ t.title }}</strong>
</div>
{% endfor %}

</div>

</details>

<details class="cv-section">
<summary><h2>Outreach</h2></summary>

<div class="cv-multicol">
{% for o in site.data.cv.outreach %}
<div class="cv-entry">
<span class="cv-date">{{ o.date }}</span>
<strong class="cv-title">{{ o.title }}</strong>
{% if o.description %}<p>{{ o.description }}</p>{% endif %}
</div>
{% endfor %}
</div>

</details>

<details class="cv-section">
<summary><h2>Full List of Talks</h2></summary>

<div class="cv-talks-legend">
<span class="cv-talk-type cv-talk-type-P">P</span>Plenary
<span class="cv-talk-type cv-talk-type-I">I</span>Invited
<span class="cv-talk-type cv-talk-type-Co">Co</span>Colloquium
<span class="cv-talk-type cv-talk-type-S">S</span>Seminar
<span class="cv-talk-type cv-talk-type-Cf">Cf</span>Conference
<span class="cv-talk-type cv-talk-type-J">J</span>Journal club
</div>

<div class="cv-talks-list">
{% for year_group in site.data.cv.talks %}
<details class="cv-talks-year-group"{% if forloop.first %} open{% endif %}>
<summary class="cv-talks-year">{{ year_group.year }}</summary>
{% for talk in year_group.entries %}
<div class="cv-talk-entry">
{% case talk.type %}
{% when 'Plenary' %}<span class="cv-talk-type cv-talk-type-P">P</span>
{% when 'Invited' %}<span class="cv-talk-type cv-talk-type-I">I</span>
{% when 'Colloquium' %}<span class="cv-talk-type cv-talk-type-Co">Co</span>
{% when 'Seminar' or 'HET Seminar' or 'Lattice Seminar' %}<span class="cv-talk-type cv-talk-type-S">S</span>
{% when 'Conference' %}<span class="cv-talk-type cv-talk-type-Cf">Cf</span>
{% when 'Journal club' %}<span class="cv-talk-type cv-talk-type-J">J</span>
{% else %}<span class="cv-talk-type cv-talk-type-S">S</span>
{% endcase %}
"{{ talk.title }}"{% if talk.event %}, {{ talk.event }}{% endif %}{% if talk.location %}, {{ talk.location }}{% endif %}{% if talk.url %} · <a href="{{ talk.url }}">↗</a>{% endif %}
</div>
{% endfor %}
</details>
{% endfor %}
</div>

</details>

<details class="cv-section">
<summary><h2>Computing Skills</h2></summary>

<div class="cv-multicol">
{% for skill in site.data.cv.computing_skills %}
<div class="cv-entry">
<span class="cv-date">
<span class="cv-grade">
{% assign full = skill.grade | floor %}
{% assign has_half = skill.grade | modulo: 1 %}
{% assign half_pos = full | plus: 1 %}
{% for i in (1..5) %}
{% if i <= full %}
<span class="cv-grade-circle filled"></span>
{% elsif has_half != 0 and i == half_pos %}
<span class="cv-grade-circle half"></span>
{% else %}
<span class="cv-grade-circle"></span>
{% endif %}
{% endfor %}
</span>
</span>
<strong class="cv-title">{{ skill.name }}</strong>
{% if skill.description %}<p>{{ skill.description }}</p>{% endif %}
</div>
{% endfor %}
</div>

</details>

<details class="cv-section">
<summary><h2>Languages</h2></summary>

<div class="cv-multicol">
{% for lang in site.data.cv.languages %}
<div class="cv-entry">
<span class="cv-date"></span>
<strong class="cv-title">{{ lang.name }}</strong>
<span class="cv-institution">{{ lang.level }}{% if lang.note %} ({{ lang.note }}){% endif %}</span>
</div>
{% endfor %}
</div>

</details>

