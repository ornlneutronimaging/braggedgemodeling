---
title: 'bem: modeling for neutron Bragg-edge imaging'
tags:
  - neutron
  - neutron imaging
  - Bragg-edge
authors:
  - name: "Jiao Y. Y. Lin^[Corresponding author: linjiao@ornl.gov]"
    orcid: 0000-0001-9233-0100
    affiliation: 1
  - name: Gian Song
    orcid: 0000-0001-7462-384X
    affiliation: 1
affiliations:
  - name: Oak Ridge National Laboratory
    index: 1
date: August 24, 2018
bibliography: paper.bib
---

# Summary
Due to its zero net charge, neutron is a unique probe of materials.
Low neutron absorption and scattering cross sections by most nuclei make it
suitable for studying bulk samples.
Unlike X-ray scattering, neutron form factors are not monotonically dependent on atomic numbers;
the fact that the neutron scattering cross section of hydrogen is large makes neutron
a useful tool in biology.
In the past half century, neutron imaging has seen growing applications
in various scientific fields
including physics, engineering sciences, biology, and archaeology
[@strobl2009].

With energy-resolved neutron imaging techniques,
neutron Bragg-edge imaging has recently found applications for materials science in phase mapping,
stress/strain mapping, and texture analysis
[@lehmann2010, @sato2017].
To model Bragg-edge neutron imaging data, it is necessary to calculate
the total neutron cross section of a sample.
This open-source python package
provides easy-to-use functions to calculate coherent elastic (diffraction),
incoherent elastic, coherent inelastic, and incoherent inelastic scattering
cross sections, as well as absorption cross sections
based on approximations and formulas in [@vogel2000thesis].
Also implemented are algorithms that take into account 
the March-Dollase texture model, and the Jorgensen peak profile
[@vogel2000thesis].


# Notice of Copyright
This manuscript has been authored by UT-Battelle, LLC under Contract
No. DE-AC05-00OR22725 with the U.S. Department of Energy. The United
States Government retains and the publisher, by accepting the article
for publication, acknowledges that the United States Government retains
a non-exclusive, paid-up, irrevocable, worldwide license to publish
or reproduce the published form of this manuscript, or allow others
to do so, for United States Government purposes. The Department of Energy
will provide public access to these results of federally sponsored
research in accordance with the DOE Public Access Plan
(http://energy.gov/downloads/doe-public-access-plan).

# Acknowledgements

This work is sponsored by the Laboratory Directed Research and
Development Program of Oak Ridge National Laboratory, managed by
UT-Battelle LLC, for DOE. Part of this research is supported by the U.S.
Department of Energy, Office of Science, Office of Basic Energy
Sciences, User Facilities under contract number DE-AC05-00OR22725.

# References
