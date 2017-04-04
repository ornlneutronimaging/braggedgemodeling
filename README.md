# Bragg Edge Modeling

* Cross section calculation from crystal structure specification
  * Calculation of diffraction peaks data (d-spacing, form factors, etc.) according to sample crystal structure
  * Estimate of inelastic scattering using incoherent approximation
* Support of texture model: March Dollase
* Peak profile modeling: Jorgensen model
* Flexible design to allow future extension to the texture and peak profile models
* Allow easy fitting to measured Bragg Edge data


Known problems:
* Debye temperature is a table. It is missing data for some elements.
