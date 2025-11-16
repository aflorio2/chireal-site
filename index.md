---
---

{% capture col1 %}
We are a theoretical physics research group specializing in the out-of-equilibrium dynamics of quantum fields, quantum information aspects of field theory, and real-time simulations of quantum and classical fields.

Our research focuses on:
- Out-of-equilibrium dynamics of quantum fields
- Quantum information aspects of field theory
- Real-time simulations of quantum and classical fields
- Quantum field theory methods and applications

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
