---
---

{% capture col1 %}
Welcome! We are a theoretical physics group at Bielefeld University. We work on understanding the fundamental forces at play in our universe, and their impact on its evolution since the big-bang. To do so, we use methods and ideas bridging **quantum field theory**, **quantum information**, and **computational physics**. Our work spans
- Entanglement dynamics and quantum information measures in field theory
- Non-equilibrium phase transitions and critical phenomena
- Applications to early universe cosmology and high-energy physics
{% endcapture %}

{% capture col2 %}
{%
  include figure.html
  image="images/team/group-photo-optimized.jpg"
  caption="The $\\left\\lvert\\chi\\right\\rangle$real group"
  link="team"
  width="100%"
%}
{% endcapture %}

{% include cols.html col1=col1 col2=col2 ratio="3fr 2fr" %}

<!-- Call to Action Buttons -->
<div class="homepage-cta-buttons">
  {%
    include button.html
    link="research"
    text="Learn About Our Research"
    icon="fa-solid fa-atom"
    flip=true
    style="button"
  %}
  {%
    include button.html
    link="projects"
    text="Discover Our Projects"
    icon="fa-solid fa-diagram-project"
    flip=true
    style="button"
  %}
  {%
    include button.html
    link="team"
    text="Meet Our Team"
    icon="fa-solid fa-users"
    flip=true
    style="button"
  %}
</div>

{% include section.html %}

<!-- News Carousel -->
{% include news-carousel.html limit=3 %}
