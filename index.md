---
---

{% capture col1 %}
Welcome! We are a theoretical physics research group exploring the dynamics of quantum fields beyond equilibrium. Our work bridges quantum field theory, quantum information, and computational physics to understand how complex quantum systems evolve and behave in real time.

Our research spans:
- Non-equilibrium phase transitions and critical phenomena
- Entanglement dynamics and quantum information measures in field theory
- Novel numerical methods for real-time quantum and classical field simulations
- Applications to early universe cosmology and high-energy physics

{%
  include button.html
  link="research"
  text="Learn More About Our Research"
  icon="fa-solid fa-arrow-right"
  flip=true
%}
{% endcapture %}

{% capture col2 %}
{%
  include figure.html
  image="images/photo.jpg"
  width="100%"
%}
{% endcapture %}

{% include cols.html col1=col1 col2=col2 %}

{% include section.html %}

<!-- News Carousel -->
{% include news-carousel.html limit=3 %}
