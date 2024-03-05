# Impacts of EV residential charging and charging stations on quasi-static time-series PV hosting capacity <img src="https://skillicons.dev/icons?i=python" /><img src="https://github.com/letfritz/DER-SmartCampus/assets/161434060/4696e7f4-d998-4032-8fb5-ad344b01b02e" style="max-width: 50%; height: 50px;">

<div align="center"><br/>
  <div style="display: inline-block;">
    <img align="center" alt="stars" src="https://img.shields.io/github/stars/letfritz/quasi-staticTS-PVHC">
    <img align="center" alt="watchers" src="https://img.shields.io/github/watchers/letfritz/quasi-staticTS-PVHC">
    <img align="center" alt="forks" src="https://img.shields.io/github/forks/letfritz/quasi-staticTS-PVHC">
  </div>
  <div style="display: inline-block;">
    <img align="center" alt="downloads" src="https://img.shields.io/github/downloads/letfritz/quasi-staticTS-PVHC/total.svg">
    <img align="center" alt="issues" src="https://img.shields.io/github/issues/letfritz/quasi-staticTS-PVHC/total.svg">
    <img align="center" alt="issues-closed" src="https://img.shields.io/github/issues-closed/letfritz/quasi-staticTS-PVHC/total.svg">
    <img align="center" alt="issues-pr" src="https://img.shields.io/github/issues-pr/letfritz/quasi-staticTS-PVHC/total.svg">
    <img align="center" alt="issues-pr-closed" src="https://img.shields.io/github/issues-pr-closed/letfritz/quasi-staticTS-PVHC/total.svg">
    <img align="center" alt="issues-pr-closed" src="https://img.shields.io/github/license/letfritz/quasi-staticTS-PVHC.svg">
  </div>
</div><br/>

Python code for investigating the quasi-static time-series photovoltaic (PV) hosting capacity from the integration of EVs residential charging and in a public charging station (PCS) considering an unbalanced medium voltage (MV) network.

## 📷 Screenshot
IEEE 34-bus distribution system with PV systems and charging station regions:<br></br>
![ieee34bus](https://github.com/letfritz/quasi-staticTS-PVHC/assets/161434060/ef6a1440-8883-4594-a36f-959d179eb6ab)

Simulation process to evaluate the scenarios proposed:<br></br>
![flowchart](https://github.com/letfritz/quasi-staticTS-PVHC/assets/161434060/b2b01f6f-018a-446f-b832-154b2e4b5fa0)

Maximum voltage magnitude without regulator:<br></br>
![Figure5](https://github.com/letfritz/quasi-staticTS-PVHC/assets/161434060/84db63b4-45a0-4ebb-999c-7b9c559e4d5d)

## Installation
1. Install the `py_dss_interface`:
   ```
   pip install py-dss-interface
   ```
2. Download the package to a local folder (e.g. ~/quasi-staticTS-PVHC/) by running:
    ```
    git clone https://github.com/letfritz/quasi-staticTS-PVHC.git
    ```
3. Run Python IDE and navigate to the folder (~/quasi-staticTS-PVHC/), then run the main.py script.

## Usage
  - Running the main.py to compile the code.
  - People can change the excel file with the load and generation curves.
  - People can change the OpenDSS file with the IEEE 34-bus grid.

## License
Released under MIT license.

## DER-SmartCampus Folder Contents
1. Files
    - main.py: main code.
    - montecarlo.py: File with code for Monte Carlo simulation.
    - output.py: File with code for organizing the results.
    - output_freq.py: File with code for organizing the results of the grid frequency.
    - output_time.py: File with code for organizing the results of the voltage over time.
    - output_vmax.py: File with code for organizing the results of the maximum voltage.
    - pdfcurve.py: File with code for creating the probability distribution function.
    - sample.py: File with code for creating the sample of some customers.
    - stoprofile.py: File with code for creating the stochastic curve profiles.
    - ieee34.dss: OpenDSS file with the IEEE 34-bus model.
    - IEEELineCodes.dss: OpenDSS file with the node specification.
    - IEEELoads.dss: OpenDSS file with the load specification.
    - curve_load.xlsx: File with load curves.
    - curve_load_simulador.xlsx: File with buses load curves
    - curve_pv.xlsx: File with photovoltaic generation curves.

## 📝 About this Project
The increasing adoption of distributed energy resources, such as rooftop photovoltaic (PV) systems and electric vehicles (EVs), can cause adverse impacts on distribution systems, including the growth in PV hosting capacity (PVHC) and the depreciation of on-load tap changers (OLTC) lifetime. To analyze the impacts of these technologies in the network over the day, the quasi-static time series (QSTS) can be used with a resolution capable of performing the start and end times of the EVs charging and PV generation process to observe the role of the OLTC in the grid. This work investigates the QSTS PVHC from the integration of EVs residential charging and in a public charging station (PCS) considering an unbalanced medium voltage (MV) network with and without OLCT. For this, a set of random variables for EV behavior are used, such as home and PCS arrival and departure times. The model is developed in Python and OpenDSS in a Monte Carlo simulation. In addition, the results show that the PCSs along the grid can increase the QSTS PVHC in MV networks that do not have OLTC. However, when the distribution system presents OLTC, the number of tap changes increases significantly if many EVs use the PCS. This result can drive actions by the distribution network operator to consider the distance between PCSs and OLTCs.

See more in [![Blog](https://img.shields.io/website?label=myquasi-staticTS-PVHC-paper.com&url=https://link.springer.com/article/10.1007/s00202-022-01513-8)](https://link.springer.com/article/10.1007/s00202-022-01513-8)

## 💡 Tool Innovation
Given the wide insertion of DERs in electrical distribution networks and the beneﬁts and concerns provoked by the on-load tap changer presence in the medium voltage (MV) network, this study aims to investigate the impacts that EVs cause on the QSTS PVHC in grids with and without OLTCs. Thus, the paper [![Blog](https://img.shields.io/website?label=myquasi-staticTS-PVHC-paper.com&url=https://link.springer.com/article/10.1007/s00202-022-01513-8)](https://link.springer.com/article/10.1007/s00202-022-01513-8) seeks to contribute to the literature as follows.
  - Direct discussion of the impacts on photovoltaic hosting capacity caused by the integration of on-load tap changers in unbalanced networks that have electric vehicles with residential charging (RC) and public charging stations;
  - Quasi-static time-series analysis in a medium voltage network to assess the impacts of electric vehicles on on-load tap changer devices facing photovoltaic hosting capacity;
  - Driving discussions on public charging station allocations, taking  into  account  the presence  of  on-load  tap  changers;
  - Simulations are designed and implemented under uncertainties of electric vehicle charging proﬁles, residential demand, and photovoltaic generation curves.
Furthermore, the paper [![Blog](https://img.shields.io/website?label=myquasi-staticTS-PVHC-paper.com&url=https://link.springer.com/article/10.1007/s00202-022-01513-8)](https://link.springer.com/article/10.1007/s00202-022-01513-8) provides a comparison between how different types of EV charging can contribute to PVHC, aiming to assist the distribution network operator (DNO) in the decision of reinforcements in the advent of the increasing penetration of DERs. Moreover, this study carried out Monte Carlo simulations to generate several uncertainty scenarios with 1 min curves for different types of EV charging using real load and PV generation proﬁles in an IEEE 34-bus distribution system.

## Citation
```
@article{HENRIQUE2022,
title = {Impacts of EV residential charging and charging stations on quasi-static time-series PV hosting capacity},
journal = {Electrical Engineering},
volume = {104},
pages = {2717–2728},
year = {2022},
doi = {https://doi.org/10.1007/s00202-022-01513-8},
url = {https://link.springer.com/article/10.1007/s00202-022-01513-8#citeas},
author = {Henrique, Letícia F. and Bitencourt, Leonardo A. and Borba, Bruno S. M. C. and Dias, Bruno H.}
}
```
