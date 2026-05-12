---
lang: de
permalink: /de/
alt_lang_url: /
---

{% capture col1 %}
Willkommen! Wir sind eine theoretische Physikgruppe an der Universität Bielefeld. Wir erforschen die fundamentalen Wechselwirkungen unseres Universums und ihren Einfluss auf seine Entwicklung seit dem Urknall. Dabei verbinden wir Methoden und Konzepte aus **Quantenfeldtheorie**, **Quanteninformation** und **Computerphysik**. Unsere Arbeit umfasst:
- Verschränkungsdynamik und Quanteninformationsmaße in der Feldtheorie
- Nichtgleichgewichts-Phasenübergänge und kritische Phänomene
- Anwendungen in der Frühzeitkosmologie und Hochenergiephysik
{% endcapture %}

{% capture col2 %}
{%
  include figure.html
  image="images/team/group-photo-optimized.jpg"
  caption="Die $\\left\\lvert\\chi\\right\\rangle$real Gruppe"
  link="/de/team/"
  width="100%"
%}
{% endcapture %}

{% include cols.html col1=col1 col2=col2 ratio="3fr 2fr" %}

<!-- Call to Action Buttons -->
<div class="homepage-cta-buttons">
  {%
    include button.html
    link="/de/research/"
    text="Mehr zu unserer Forschung"
    icon="fa-solid fa-atom"
    flip=true
    style="button"
  %}
  {%
    include button.html
    link="/de/projects/"
    text="Unsere Projekte entdecken"
    icon="fa-solid fa-diagram-project"
    flip=true
    style="button"
  %}
  {%
    include button.html
    link="/de/team/"
    text="Unser Team kennenlernen"
    icon="fa-solid fa-users"
    flip=true
    style="button"
  %}
</div>

{% include section.html %}

<!-- News Carousel -->
{% include news-carousel.html limit=3 %}
