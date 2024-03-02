#################################################################
# NOME: LETÍCIA FRITZ HENRIQUE
# E-MAIL: LETICIA.HENRIQUE@ENGENHARIA.UFJF.BR
# PROJETO: DYNAMIC HOSTING CAPACITY FOR GRID WITH DER
# VERSÃO: 1.0
#################################################################

# BIBLIOTECAS
import sys
import os

import pandas as pd
import seaborn as sns
import py_dss_interface

from montecarlo import Montecarlo
from sample import Sample

# ---------- OBJETOS ----------
dss = py_dss_interface.DSSDLL()

# VARIAVÉIS GLOBAIS
EV_MAX_CONNECTION = [6, 3, 40, 6, 1, 1, 3, 45, 2, 2, 2, 2, 1, 1, 2, 2, 7, 7, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 6, 2, 2, 1, 1, 3, 3, 1, 1, 2, 2, 2, 2, 1, 1, 2,
                     2, 1, 1, 2, 2]

print("Essa rede tem", sum(EV_MAX_CONNECTION), "clientes")


# FUNÇÃO PRINCIPAL
def main():
    # Dados de Entrada
    print("FLUXO DE CARGA PROBABILISTICO PARA REDES COM RECURSOS ENERGÉTICOS DISTRIBUÍDOS")
    print("-----")
    simulation_number = input("NÚMERO DE SIMULAÇÕES DE MONTE CARLO: ")

    '''
    # Curvas de entrada
    load_det = pd.read_csv(os.path.dirname(sys.argv[0]) + "/curve_load.csv", header=0, sep=';')
    pv_det = pd.read_csv(os.path.dirname(sys.argv[0]) + "/curve_pv.csv", header=0, sep=';')

    # Gerando amostras
    sample = Sample(load_det, pv_det, EV_MAX_CONNECTION)
    dss.text("compile {}".format(os.path.dirname(sys.argv[0]) + "/ieee34.dss"))
    for n in range(int(simulation_number)):
        # Load
        load = sample.get_load_sample(dss.loads_count())
        output_load_file = 'uncertainty\load_' + str(n) + '.csv'
        output_load = pd.DataFrame(load)
        output_load.to_csv(output_load_file, index=False)
        pv = sample.get_pv_sample(dss.loads_count())
        # PV
        output_pv = pd.DataFrame(pv)
        output_pv_file = 'uncertainty\pv_' + str(n) + '.csv'
        output_pv.to_csv(output_pv_file, index=False)
        # EV
        ev_curve_hc, ev_curve_cs, ev_soc_init = sample.get_ev_sample(dss.loads_count())
        output_ev_curve_hc = pd.DataFrame(ev_curve_hc)
        output_ev_curve_cs = pd.DataFrame(ev_curve_cs)
        output_ev_curve_hc_file = 'uncertainty\ev_curve_hc_' + str(n) + '.csv'
        output_ev_curve_cs_file = 'uncertainty\ev_curve_cs_' + str(n) + '.csv'
        output_ev_curve_hc.to_csv(output_ev_curve_hc_file, index=False)
        output_ev_curve_cs.to_csv(output_ev_curve_cs_file, index=False)
        # CS
        cs_curve_a = sample.get_cs_sample(ev_soc_init, 'a')
        output_cs_curve = pd.DataFrame(cs_curve_a)
        output_cs_curve_file = 'uncertainty\cs_curve_a_' + str(n) + '.csv'
        output_cs_curve.to_csv(output_cs_curve_file, index=False)
        cs_curve_b = sample.get_cs_sample(ev_soc_init, 'b')
        output_cs_curve = pd.DataFrame(cs_curve_b)
        output_cs_curve_file = 'uncertainty\cs_curve_b_' + str(n) + '.csv'
        output_cs_curve.to_csv(output_cs_curve_file, index=False)
        cs_curve_c = sample.get_cs_sample(ev_soc_init, 'c')
        output_cs_curve = pd.DataFrame(cs_curve_c)
        output_cs_curve_file = 'uncertainty\cs_curve_c_' + str(n) + '.csv'
        output_cs_curve.to_csv(output_cs_curve_file, index=False)
    '''
    # Simulação de Monte Carlo
    penetration = 60
    for hosting in range(1):
        simulation = Montecarlo(simulation_number, penetration)
        simulation.set_simulation()
        penetration += 5


# RUN
if __name__ == '__main__':
    main()
