---
title: Team
lang: en
alt_lang_url: /de/team/
nav:
  order: 3
  tooltip: About our team
---

# {% include icon.html icon="fa-solid fa-users" %}Team
{% include section.html %}

## Current

{% include list.html data="members" component="portrait" filter="role == 'group-leader' && !hidden" %}
{% include list.html data="members" component="portrait" filter="role == 'postdoc' && !hidden" %}
{% include list.html data="members" component="portrait" filter="role == 'phd' && !hidden" %}
{% include list.html data="members" component="portrait" filter="role == 'bachelor' && !hidden" %}

{% include section.html %}

## {% include icon.html icon="fa-solid fa-user-plus" %}Join us!

We are always interested in motivated researchers who want to explore quantum
field theory and quantum information. In particular, if you are interested in
applying with us to some external funding opportunities such as
[DFG Walter Benjamin Programme](https://www.dfg.de/en/research-funding/funding-opportunities/programmes/individual/walter-benjamin),
[Humboldt Research Fellowship](https://www.humboldt-foundation.de/en/apply/sponsorship-programmes/humboldt-research-fellowship),
or [Marie Skłodowska-Curie Postdoctoral Fellowships](https://marie-sklodowska-curie-actions.ec.europa.eu/actions/postdoctoral-fellowships),
do not hesitate to reach out. [DAAD](https://www2.daad.de/deutschland/stipendium/datenbank/en/21148-scholarship-database/) also offers many opportunities to fund month-long visits.

{%
  include button.html
  type="email"
  text="adrien.florio@uni-bielefeld.de"
  link="adrien.florio@uni-bielefeld.de"
%}
