---
title: Team
nav:
  order: 3
  tooltip: About our team
---

# {% include icon.html icon="fa-solid fa-users" %}Team

The QuIReal group is an Emmy Noether research group at Bielefeld University
dedicated to exploring quantum information and real-time evolution in quantum
field theory. We combine analytical methods with numerical simulations to
tackle fundamental questions at the intersection of quantum mechanics and
high-energy physics.

{% include section.html %}

{% include list.html data="members" component="portrait" filter="role == 'pi'" %}
{% include list.html data="members" component="portrait" filter="role != 'pi'" %}

{% include section.html %}

## Join Our Team

We are always interested in motivated researchers who want to explore quantum
field theory and quantum information. If you're interested in joining our group
as a postdoc, PhD student, or visiting researcher, please get in touch!

{% include section.html %}

## {% include icon.html icon="fa-regular fa-envelope" %}Contact

For inquiries about research collaboration, joining the group, or general questions,
please contact:

{%
  include button.html
  type="email"
  text="aflorio@physik.uni-bielefeld.de"
  link="aflorio@physik.uni-bielefeld.de"
%}

**Address:**
Bielefeld University
Faculty of Physics
Universitätsstraße 25
33615 Bielefeld, Germany

{%
  include button.html
  type="address"
  tooltip="Bielefeld University on Google Maps"
  link="https://www.google.com/maps/place/Bielefeld+University"
%}
