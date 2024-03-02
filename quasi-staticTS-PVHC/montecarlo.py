# ---------- BIBLIOTECAS ----------
import os
import sys

import pandas as pd
import py_dss_interface
import numpy as np
import matplotlib.pyplot as plt

from sample import Sample

# ---------- OBJETOS ----------
dss = py_dss_interface.DSSDLL()

# ---------- VARIAVEIS GLOBAIS ----------
PV_BUS_PHASE_LIST = [3, 3, 3, 3, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1]
PV_BUS_NODE_LIST = ["860", "840", "844", "848", "830.1.2", "830.2.3", "830.3.1", "890", "802.2", "806.2", "802.3",
                    "806.3", "808.2", "810.2", "818.1", "820.1", "820.1", "822.1", "816.2", "824.2", "824.2",
                    "826.2", "824.3", "828.3", "828.1", "830.1", "854.2", "856.2", "832.1", "858.1", "832.2",
                    "858.2", "832.3", "858.3", "858.1", "864.1", "858.1.2", "834.1.2", "858.2.3", "834.2.3",
                    "858.3.1", "834.3.1", "834.1.2", "860.1.2", "834.2.3", "860.2.3", "834.3.1", "860.3.1",
                    "860.1.2", "836.1.2", "860.2.3", "836.2.3", "860.3.1", "836.3.1", "836.1.2", "840.1.2",
                    "836.2.3", "840.2.3", "862.2", "838.2", "842.1", "844.1", "844.2", "846.2", "844.3",
                    "846.3", "846.2", "848.2"]
PV_BUS_KV_LIST = [24.900, 24.900, 24.900, 24.900, 24.900, 24.900, 24.900, 4.160, 14.376, 14.376, 14.376, 14.376,
                  14.376, 14.376, 14.376, 14.376, 14.376, 14.376, 24.900, 24.900, 14.376, 14.376, 14.376, 14.376,
                  14.376, 14.376, 14.376, 14.376, 24.900, 24.900, 24.900, 24.900, 24.900, 24.900, 14.376, 14.376,
                  24.900, 24.900, 24.900, 24.900, 24.900, 24.900, 24.900, 24.900, 24.900, 24.900, 24.900, 24.900,
                  24.900, 24.900, 24.900, 24.900, 24.900, 24.900, 24.900, 24.900, 24.900, 24.900, 14.376, 14.376,
                  14.376, 14.376, 14.376, 14.376, 14.376, 14.376, 14.376, 14.376]
LINE_BUS_KV_LIST = [24.9, 24.9, 24.9, 24.9, 24.9, 24.9, 14.376 * np.sqrt(3), 14.376 * np.sqrt(3),
                    14.376 * np.sqrt(3), 14.376 * np.sqrt(3), 14.376 * np.sqrt(3), 14.376 * np.sqrt(3),
                    14.376 * np.sqrt(3), 14.376 * np.sqrt(3), 14.376 * np.sqrt(3), 14.376 * np.sqrt(3),
                    14.376 * np.sqrt(3), 14.376 * np.sqrt(3), 14.376 * np.sqrt(3), 14.376 * np.sqrt(3),
                    14.376 * np.sqrt(3), 14.376 * np.sqrt(3), 14.376 * np.sqrt(3), 14.376 * np.sqrt(3),
                    14.376 * np.sqrt(3), 14.376 * np.sqrt(3), 14.376 * np.sqrt(3), 14.376 * np.sqrt(3),
                    14.376 * np.sqrt(3), 14.376 * np.sqrt(3), 14.376 * np.sqrt(3), 4.16]
EV_MAX_CONNECTION = [6, 3, 40, 6, 1, 1, 3, 45, 2, 2, 2, 2, 1, 1, 2, 2, 7, 7, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 6, 2, 2, 1, 1, 3, 3, 1, 1, 2, 2, 2, 2, 1, 1, 2,
                     2, 1, 1, 2, 2]


def get_daily_load(load):
    df = pd.DataFrame.from_dict(load)
    # Criar LoadShapes
    load_name = dss.loads_all_names()
    for i in range(len(load_name)):
        load = df.iloc[:, i]
        new_load = [float(item) for item in load]
        dss.text("New loadshape.loadshape_" + load_name[i] + " npts=1440 minterval=1")
        dss.text("~ mult=" + '[{:s}]'.format(', '.join(['{:.2f}'.format(x) for x in new_load])))
        dss.text("~ Action=Normalize")

    # Acrescentar loadshape nas cargas
    load_name = dss.loads_all_names()
    for i in range(dss.loads_count()):
        dss.loads_write_name(load_name[i])
        dss.loads_write_daily("LoadShape_" + load_name[i])


def get_daily_pv(pv, penetration):
    df = pd.DataFrame.from_dict(pv)

    # Cria loadshape com as curvas de geração PV
    pv_bus_list = dss.loads_all_names()
    for i in range(len(pv_bus_list)):
        pv = df.iloc[:, i]
        new_pv = [float(item) for item in pv]
        dss.text("New loadshape.loadshape_pv_" + pv_bus_list[i] + " npts=1440 minterval=1")
        dss.text("~ mult=" + '[{:s}]'.format(', '.join(['{:.2f}'.format(x) for x in new_pv])))
        dss.text("~ Action=Normalize")

    # Criando geradores PV
    for i in range(len(pv_bus_list)):
        dss.loads_write_name(pv_bus_list[i])
        pv_bus_kw_list = dss.loads_read_kw() * (penetration / 100)
        dss.text("New Generator.PV_" + pv_bus_list[i] + " phases=" + str(PV_BUS_PHASE_LIST[i]))
        dss.text("~ bus1=" + PV_BUS_NODE_LIST[i] + " kv=" + str(PV_BUS_KV_LIST[i]))
        dss.text("~ kW=" + str(pv_bus_kw_list) + " pf=1 model=1 conn=wye")
        dss.text("~ daily=LoadShape_pv_" + pv_bus_list[i])


def get_daily_ev(ev_curve):
    df_curve = pd.DataFrame.from_dict(ev_curve)

    # Cria loadshape com carregamento de EV
    ev_bus_list = dss.loads_all_names()
    for i in range(len(ev_bus_list)):
        ev = df_curve.iloc[:, i]
        new_ev = [float(item) for item in ev]
        dss.text("New loadshape.loadshape_hc_" + ev_bus_list[i] + " npts=1440 minterval=1")
        dss.text("~ mult=" + '[{:s}]'.format(', '.join(['{:.2f}'.format(x) for x in new_ev])))
        dss.text("~ UseActual=yes")

    # Criando carga PEV
    for i in range(len(ev_bus_list)):
        dss.text("New Load.HC_" + ev_bus_list[i] + " bus1=" + PV_BUS_NODE_LIST[i])
        dss.text("~ phases=" + str(PV_BUS_PHASE_LIST[i]) + " conn=wye Model=1 kV=" + str(PV_BUS_KV_LIST[i]))
        dss.text("~ Status=variable daily=LoadShape_hc_" + ev_bus_list[i])


def get_daily_cs(cs_curve_a, cs_curve_b, cs_curve_c):
    # Criando barra do eletroposto
    # dss.text("New line.lcs phase=3 Bus1=844.1.2.3  Bus2=cs.1.2.3  LineCode=301  Length=0.5   units=kft")

    # Cria loadshape com carregamento de EV para agrupamento A
    df_curve = pd.DataFrame.from_dict(cs_curve_a)
    cs = df_curve.iloc[:, 0]
    new_cs = [float(item) for item in cs]
    dss.text("New loadshape.loadshape_cs_814 npts=1440 minterval=1")
    dss.text("~ mult=" + '[{:s}]'.format(', '.join(['{:.2f}'.format(x) for x in new_cs])))
    dss.text("~ UseActual=yes")

    # Cria loadshape com carregamento de EV para agrupamento B
    df_curve = pd.DataFrame.from_dict(cs_curve_b)
    cs = df_curve.iloc[:, 0]
    new_cs = [float(item) for item in cs]
    dss.text("New loadshape.loadshape_cs_844 npts=1440 minterval=1")
    dss.text("~ mult=" + '[{:s}]'.format(', '.join(['{:.2f}'.format(x) for x in new_cs])))
    dss.text("~ UseActual=yes")

    # Cria loadshape com carregamento de EV para agrupamento C
    df_curve = pd.DataFrame.from_dict(cs_curve_c)
    cs = df_curve.iloc[:, 0]
    new_cs = [float(item) for item in cs]
    dss.text("New loadshape.loadshape_cs_860 npts=1440 minterval=1")
    dss.text("~ mult=" + '[{:s}]'.format(', '.join(['{:.2f}'.format(x) for x in new_cs])))
    dss.text("~ UseActual=yes")

    # Criando carga PEV
    dss.text("New Load.CS_814 bus1=814.1.2.3 phases=3 conn=delta Model=1 kV=14.376 status=variable ")
    dss.text("~ daily=LoadShape_cs_814")
    dss.text("New Load.CS_844 bus1=844.1.2.3 phases=3 conn=delta Model=1 kV=14.376 status=variable ")
    dss.text("~ daily=LoadShape_cs_844")
    dss.text("New Load.CS_860 bus1=860.1.2.3 phases=3 conn=delta Model=1 kV=24.900 status=variable ")
    dss.text("~ daily=LoadShape_cs_860")


def get_all_monitors(mode):
    lines_name = dss.lines_all_names()
    for item in lines_name:
        dss.text("New Monitor.M" + item + "_voltage element=line." + item + " terminal=2 mode=0")

    dss.text("New Monitor.Mreg1a element=transformer.reg1a terminal=2 mode=2 ppolar=no")
    dss.text("New Monitor.Mreg1b element=Transformer.reg1b terminal=2 mode=2 ppolar=no")
    dss.text("New Monitor.Mreg1c element=Transformer.reg1c terminal=2 mode=2 ppolar=no")
    dss.text("New Monitor.Mreg2a element=transformer.reg2a terminal=2 mode=2")
    dss.text("New Monitor.Mreg2b element=Transformer.reg2b terminal=2 mode=2 ppolar=no")
    dss.text("New Monitor.Mreg2c element=Transformer.reg2c terminal=2 mode=2 ppolar=no")
    dss.text("New Monitor.M844_power element=Line.L21 terminal=2 mode=1 ppolar=no")
    dss.text("New Monitor.M848_power element=Line.L23 terminal=2 mode=1 ppolar=no")
    # if mode == 2:
    #    dss.text("New Monitor.Mcs_power element=Line.lcs terminal=2 mode=1 ppolar=no")


class Montecarlo:
    def __init__(self, number, penetration):
        self.number = int(number)
        self.penetration = penetration

    def set_simulation(self):

        # Criando matriz para os medidores
        dss.text("compile {}".format(os.path.dirname(sys.argv[0]) + "/ieee34.dss"))
        somakva = 0
        for item in dss.loads_all_names():
            dss.loads_write_name(item)
            kw = dss.loads_read_kw() ** 2
            dss.loads_write_name(item)
            kvar = dss.loads_read_kvar() ** 2
            somakva += np.sqrt(kw + kvar)
        print("Nível de carregamento é:", (somakva / 25000) * 100, "%")

        step = int(1440 / 1)

        monitors_total_vmag1_modepv = np.zeros((step * self.number, len(dss.lines_all_names())))
        monitors_total_vmag2_modepv = np.zeros((step * self.number, len(dss.lines_all_names())))
        monitors_total_vmag3_modepv = np.zeros((step * self.number, len(dss.lines_all_names())))
        monitors_total_tap_modepv = np.zeros((step * self.number, 6))
        monitors_max_vmag1_modepv = np.zeros((self.number, len(dss.lines_all_names())))
        monitors_max_vmag2_modepv = np.zeros((self.number, len(dss.lines_all_names())))
        monitors_max_vmag3_modepv = np.zeros((self.number, len(dss.lines_all_names())))
        monitors_total_vmag1_modehc = np.zeros((step * self.number, len(dss.lines_all_names())))
        monitors_total_vmag2_modehc = np.zeros((step * self.number, len(dss.lines_all_names())))
        monitors_total_vmag3_modehc = np.zeros((step * self.number, len(dss.lines_all_names())))
        monitors_total_tap_modehc = np.zeros((step * self.number, 6))
        monitors_max_vmag1_modehc = np.zeros((self.number, len(dss.lines_all_names())))
        monitors_max_vmag2_modehc = np.zeros((self.number, len(dss.lines_all_names())))
        monitors_max_vmag3_modehc = np.zeros((self.number, len(dss.lines_all_names())))
        monitors_total_vmag1_modecs = np.zeros((step * self.number, len(dss.lines_all_names())))
        monitors_total_vmag2_modecs = np.zeros((step * self.number, len(dss.lines_all_names())))
        monitors_total_vmag3_modecs = np.zeros((step * self.number, len(dss.lines_all_names())))
        monitors_total_tap_modecs = np.zeros((step * self.number, 6))
        monitors_max_vmag1_modecs = np.zeros((self.number, len(dss.lines_all_names())))
        monitors_max_vmag2_modecs = np.zeros((self.number, len(dss.lines_all_names())))
        monitors_max_vmag3_modecs = np.zeros((self.number, len(dss.lines_all_names())))
        monitors_total_power1_modepv = np.zeros((step * self.number, 2))
        monitors_total_power2_modepv = np.zeros((step * self.number, 2))
        monitors_total_power3_modepv = np.zeros((step * self.number, 2))
        monitors_total_power1_modehc = np.zeros((step * self.number, 2))
        monitors_total_power2_modehc = np.zeros((step * self.number, 2))
        monitors_total_power3_modehc = np.zeros((step * self.number, 2))
        monitors_total_power1_modecs = np.zeros((step * self.number, 3))
        monitors_total_power2_modecs = np.zeros((step * self.number, 3))
        monitors_total_power3_modecs = np.zeros((step * self.number, 3))
        monitors_cs_vmag_modecs = np.zeros((step * self.number, 3))

        for n in range(self.number):

            load = pd.read_csv(os.path.dirname(sys.argv[0]) + "/uncertainty/load_" + str(n) +
                               ".csv", header=0, sep=',')
            pv = pd.read_csv(os.path.dirname(sys.argv[0]) + "/uncertainty/pv_" + str(n) +
                             ".csv", header=0, sep=',')
            ev_curve_hc = pd.read_csv(os.path.dirname(sys.argv[0]) + "/uncertainty/ev_curve_hc_" + str(n) +
                                      ".csv", header=0, sep=',')
            ev_curve_cs = pd.read_csv(os.path.dirname(sys.argv[0]) + "/uncertainty/ev_curve_cs_" + str(n) +
                                      ".csv", header=0, sep=',')
            cs_curve_a = pd.read_csv(os.path.dirname(sys.argv[0]) + "/uncertainty/cs_curve_a_" + str(n) +
                                     ".csv", header=0, sep=',')
            cs_curve_b = pd.read_csv(os.path.dirname(sys.argv[0]) + "/uncertainty/cs_curve_b_" + str(n) +
                                     ".csv", header=0, sep=',')
            cs_curve_c = pd.read_csv(os.path.dirname(sys.argv[0]) + "/uncertainty/cs_curve_c_" + str(n) +
                                     ".csv", header=0, sep=',')

            for mode in range(3):
                # Compilando a rede
                dss.text("compile {}".format(os.path.dirname(sys.argv[0]) + "/ieee34.dss"))
                dss.text("New Energymeter.Feeder Line.L1 1")

                # Colocando curva de PV
                get_daily_load(load)
                get_daily_pv(pv, self.penetration)
                if mode == 1:
                    get_daily_ev(ev_curve_hc)
                if mode == 2:
                    get_daily_ev(ev_curve_cs)
                    get_daily_cs(cs_curve_a, cs_curve_b, cs_curve_c)

                # Criando monitores para todas as barras
                get_all_monitors(mode)

                # Solução
                dss.text("Set Mode=daily")
                dss.text("Set stepsize=5m")
                number_dss = "Set number=" + str(step)
                dss.text(number_dss)
                dss.text("Set controlmode=TIME")
                dss.solution_solve()

                # dss.text("plot profile")
                # dss.text("plot loadshape object=loadshape_D802_806sb")
                # dss.text("plot loadshape object=loadshape_cs_890")
                # dss.text("plot monitor object=ml1_voltage  channels = (1 3 5)")
                # dss.text("plot monitor object=Mreg2a channels=(1)")
                # dss.text("plot monitor object=M844_power channels=(1 3 5)")

                if mode == 0:
                    # Análise global da rede para tensão
                    monitors_name = dss.monitors_all_names()
                    num = 0
                    num_reg = 0
                    num_power = 0
                    for item in monitors_name:
                        if item == 'mreg2a' or item == 'mreg2b' or item == 'mreg2c' or item == 'mreg1a' or \
                                item == 'mreg1b' or item == 'mreg1c':
                            for hour in range(step):
                                dss.monitors_write_name(item)
                                monitors_total_tap_modepv[n * step + hour, num_reg] = dss.monitors_channel(1)[hour]
                            num_reg += 1
                        elif item == 'm844_power' or item == 'm848_power':
                            for hour in range(step):
                                dss.monitors_write_name(item)
                                monitors_total_power1_modepv[n * step + hour, num_power] = dss.monitors_channel(1)[hour]
                                dss.monitors_write_name(item)
                                monitors_total_power2_modepv[n * step + hour, num_power] = dss.monitors_channel(3)[hour]
                                dss.monitors_write_name(item)
                                monitors_total_power3_modepv[n * step + hour, num_power] = dss.monitors_channel(5)[hour]
                            num_power += 1
                        else:
                            if item == 'ml4_voltage' or item == 'ml8_voltage' or item == 'ml10_voltage' or \
                                    item == 'ml11_voltage' or item == 'ml12_voltage' or item == 'ml26_voltage' or \
                                    item == 'ml28_voltage' or item == 'ml31_voltage':
                                for hour in range(step):
                                    dss.monitors_write_name(item)
                                    monitors_total_vmag1_modepv[n * step + hour, num] = \
                                        dss.monitors_channel(1)[hour] / (LINE_BUS_KV_LIST[num] * 1000 / np.sqrt(3))
                            else:
                                for hour in range(step):
                                    dss.monitors_write_name(item)
                                    monitors_total_vmag1_modepv[n * step + hour, num] = \
                                        dss.monitors_channel(1)[hour] / (LINE_BUS_KV_LIST[num] * 1000 / np.sqrt(3))
                                    dss.monitors_write_name(item)
                                    monitors_total_vmag2_modepv[n * step + hour, num] = \
                                        dss.monitors_channel(3)[hour] / (LINE_BUS_KV_LIST[num] * 1000 / np.sqrt(3))
                                    dss.monitors_write_name(item)
                                    monitors_total_vmag3_modepv[n * step + hour, num] = \
                                        dss.monitors_channel(5)[hour] / (LINE_BUS_KV_LIST[num] * 1000 / np.sqrt(3))
                            num += 1
                    # Análise das médias da rede para tensão
                    for bus in range(len(monitors_name) - 6 - 2):
                        monitors_max_vmag1_modepv[n, bus] = \
                            np.max(monitors_total_vmag1_modepv[n * step:(n * step + step), bus])
                        monitors_max_vmag2_modepv[n, bus] = \
                            np.max(monitors_total_vmag2_modepv[n * step:(n * step + step), bus])
                        monitors_max_vmag3_modepv[n, bus] = \
                            np.max(monitors_total_vmag3_modepv[n * step:(n * step + step), bus])

                    # Aviso ao usuário
                    print("Simulação ", str(n), " do modo PV para penetração de ", str(self.penetration), " concluída!")
                elif mode == 1:
                    # Análise global da rede para tensão
                    monitors_name = dss.monitors_all_names()
                    num = 0
                    num_reg = 0
                    num_power = 0
                    for item in monitors_name:
                        if item == 'mreg2a' or item == 'mreg2b' or item == 'mreg2c' or item == 'mreg1a' or \
                                item == 'mreg1b' or item == 'mreg1c':
                            for hour in range(step):
                                dss.monitors_write_name(item)
                                monitors_total_tap_modehc[n * step + hour, num_reg] = dss.monitors_channel(1)[hour]
                            num_reg += 1
                        elif item == 'm844_power' or item == 'm848_power':
                            for hour in range(step):
                                dss.monitors_write_name(item)
                                monitors_total_power1_modehc[n * step + hour, num_power] = dss.monitors_channel(1)[hour]
                                dss.monitors_write_name(item)
                                monitors_total_power2_modehc[n * step + hour, num_power] = dss.monitors_channel(3)[hour]
                                dss.monitors_write_name(item)
                                monitors_total_power3_modehc[n * step + hour, num_power] = dss.monitors_channel(5)[hour]
                            num_power += 1
                        else:
                            if item == 'ml4_voltage' or item == 'ml8_voltage' or item == 'ml10_voltage' or \
                                    item == 'ml11_voltage' or item == 'ml12_voltage' or item == 'ml26_voltage' or \
                                    item == 'ml28_voltage' or item == 'ml31_voltage':
                                for hour in range(step):
                                    dss.monitors_write_name(item)
                                    monitors_total_vmag1_modehc[n * step + hour, num] = \
                                        dss.monitors_channel(1)[hour] / (LINE_BUS_KV_LIST[num] * 1000 / np.sqrt(3))
                            else:
                                for hour in range(step):
                                    dss.monitors_write_name(item)
                                    monitors_total_vmag1_modehc[n * step + hour, num] = \
                                        dss.monitors_channel(1)[hour] / (LINE_BUS_KV_LIST[num] * 1000 / np.sqrt(3))
                                    dss.monitors_write_name(item)
                                    monitors_total_vmag2_modehc[n * step + hour, num] = \
                                        dss.monitors_channel(3)[hour] / (LINE_BUS_KV_LIST[num] * 1000 / np.sqrt(3))
                                    dss.monitors_write_name(item)
                                    monitors_total_vmag3_modehc[n * step + hour, num] = \
                                        dss.monitors_channel(5)[hour] / (LINE_BUS_KV_LIST[num] * 1000 / np.sqrt(3))

                            num += 1
                    # Análise das médias da rede para tensão
                    for bus in range(len(monitors_name) - 6 - 2):
                        monitors_max_vmag1_modehc[n, bus] = \
                            np.max(monitors_total_vmag1_modehc[n * step:(n * step + step), bus])
                        monitors_max_vmag2_modehc[n, bus] = \
                            np.max(monitors_total_vmag2_modehc[n * step:(n * step + step), bus])
                        monitors_max_vmag3_modehc[n, bus] = \
                            np.max(monitors_total_vmag3_modehc[n * step:(n * step + step), bus])

                    # Aviso ao usuário
                    print("Simulação ", str(n), " do modo HC para penetração de ", str(self.penetration), " concluída!")
                elif mode == 2:
                    # Análise global da rede para tensão
                    monitors_name = dss.monitors_all_names()
                    num = 0
                    num_reg = 0
                    num_power = 0
                    for item in monitors_name:
                        if item == 'mreg2a' or item == 'mreg2b' or item == 'mreg2c' or item == 'mreg1a' or \
                                item == 'mreg1b' or item == 'mreg1c':
                            for hour in range(step):
                                dss.monitors_write_name(item)
                                monitors_total_tap_modecs[n * step + hour, num_reg] = dss.monitors_channel(1)[hour]
                            num_reg += 1
                        elif item == 'm844_power' or item == 'm848_power':
                            for hour in range(step):
                                dss.monitors_write_name(item)
                                monitors_total_power1_modecs[n * step + hour, num_power] = dss.monitors_channel(1)[hour]
                                dss.monitors_write_name(item)
                                monitors_total_power2_modecs[n * step + hour, num_power] = dss.monitors_channel(3)[hour]
                                dss.monitors_write_name(item)
                                monitors_total_power3_modecs[n * step + hour, num_power] = dss.monitors_channel(5)[hour]
                            num_power += 1
                        # elif item == 'mlcs_voltage':
                        #    for hour in range(step):
                        #        dss.monitors_write_name(item)
                        #        monitors_cs_vmag_modecs[n * step + hour, 0] = \
                        #            dss.monitors_channel(1)[hour] / (14.376 * 1000)
                        #        dss.monitors_write_name(item)
                        #        monitors_cs_vmag_modecs[n * step + hour, 1] = \
                        #            dss.monitors_channel(3)[hour] / (14.376 * 1000)
                        #        dss.monitors_write_name(item)
                        #        monitors_cs_vmag_modecs[n * step + hour, 2] = \
                        #            dss.monitors_channel(5)[hour] / (14.376 * 1000)
                        else:
                            if item == 'ml4_voltage' or item == 'ml8_voltage' or item == 'ml10_voltage' or \
                                    item == 'ml11_voltage' or item == 'ml12_voltage' or item == 'ml26_voltage' or \
                                    item == 'ml28_voltage' or item == 'ml31_voltage':
                                for hour in range(step):
                                    dss.monitors_write_name(item)
                                    monitors_total_vmag1_modecs[n * step + hour, num] = \
                                        dss.monitors_channel(1)[hour] / (LINE_BUS_KV_LIST[num] * 1000 / np.sqrt(3))
                            else:
                                for hour in range(step):
                                    dss.monitors_write_name(item)
                                    monitors_total_vmag1_modecs[n * step + hour, num] = \
                                        dss.monitors_channel(1)[hour] / (LINE_BUS_KV_LIST[num] * 1000 / np.sqrt(3))
                                    dss.monitors_write_name(item)
                                    monitors_total_vmag2_modecs[n * step + hour, num] = \
                                        dss.monitors_channel(3)[hour] / (LINE_BUS_KV_LIST[num] * 1000 / np.sqrt(3))
                                    dss.monitors_write_name(item)
                                    monitors_total_vmag3_modecs[n * step + hour, num] = \
                                        dss.monitors_channel(5)[hour] / (LINE_BUS_KV_LIST[num] * 1000 / np.sqrt(3))
                            num += 1
                    # Análise das médias da rede para tensão
                    for bus in range(len(monitors_name) - 6 - 2):
                        monitors_max_vmag1_modecs[n, bus] = \
                            np.max(monitors_total_vmag1_modecs[n * step:(n * step + step), bus])
                        monitors_max_vmag2_modecs[n, bus] = \
                            np.max(monitors_total_vmag2_modecs[n * step:(n * step + step), bus])
                        monitors_max_vmag3_modecs[n, bus] = \
                            np.max(monitors_total_vmag3_modecs[n * step:(n * step + step), bus])

                    # Aviso ao usuário
                    print("Simulação ", str(n), " do modo CS para penetração de ", str(self.penetration), " concluída!")

        # Dados de saída
        print("... preparando dados de saída ...")
        # Modo 0
        output_v1_modepv = pd.DataFrame(monitors_total_vmag1_modepv)
        output_v2_modepv = pd.DataFrame(monitors_total_vmag2_modepv)
        output_v3_modepv = pd.DataFrame(monitors_total_vmag3_modepv)
        output_v1_file_modepv = 'hc_pv/output_v1_penetration_' + str(self.penetration) + '.csv'
        output_v2_file_modepv = 'hc_pv/output_v2_penetration_' + str(self.penetration) + '.csv'
        output_v3_file_modepv = 'hc_pv/output_v3_penetration_' + str(self.penetration) + '.csv'
        output_v1_modepv.to_csv(output_v1_file_modepv, index=False)
        output_v2_modepv.to_csv(output_v2_file_modepv, index=False)
        output_v3_modepv.to_csv(output_v3_file_modepv, index=False)
        output_tap_modepv = pd.DataFrame(monitors_total_tap_modepv)
        output_tap_file_modepv = 'hc_pv/output_tap_penetration_' + str(self.penetration) + '.csv'
        output_tap_modepv.to_csv(output_tap_file_modepv, index=False)
        output_max_v1_modepv = pd.DataFrame(monitors_max_vmag1_modepv)
        output_max_v2_modepv = pd.DataFrame(monitors_max_vmag2_modepv)
        output_max_v3_modepv = pd.DataFrame(monitors_max_vmag3_modepv)
        output_max_v1_file_modepv = 'hc_pv/output_max_v1_penetration_' + str(self.penetration) + '.csv'
        output_max_v2_file_modepv = 'hc_pv/output_max_v2_penetration_' + str(self.penetration) + '.csv'
        output_max_v3_file_modepv = 'hc_pv/output_max_v3_penetration_' + str(self.penetration) + '.csv'
        output_max_v1_modepv.to_csv(output_max_v1_file_modepv, index=False)
        output_max_v2_modepv.to_csv(output_max_v2_file_modepv, index=False)
        output_max_v3_modepv.to_csv(output_max_v3_file_modepv, index=False)
        output_power1_modepv = pd.DataFrame(monitors_total_power1_modepv)
        output_power2_modepv = pd.DataFrame(monitors_total_power2_modepv)
        output_power3_modepv = pd.DataFrame(monitors_total_power3_modepv)
        output_power1_file_modepv = 'hc_pv/output_power1_penetration_' + str(self.penetration) + '.csv'
        output_power2_file_modepv = 'hc_pv/output_power2_penetration_' + str(self.penetration) + '.csv'
        output_power3_file_modepv = 'hc_pv/output_power3_penetration_' + str(self.penetration) + '.csv'
        output_power1_modepv.to_csv(output_power1_file_modepv, index=False)
        output_power2_modepv.to_csv(output_power2_file_modepv, index=False)
        output_power3_modepv.to_csv(output_power3_file_modepv, index=False)

        # Modo 1
        output_v1_modehc = pd.DataFrame(monitors_total_vmag1_modehc)
        output_v2_modehc = pd.DataFrame(monitors_total_vmag2_modehc)
        output_v3_modehc = pd.DataFrame(monitors_total_vmag3_modehc)
        output_v1_file_modehc = 'hc_hc/output_v1_penetration_' + str(self.penetration) + '.csv'
        output_v2_file_modehc = 'hc_hc/output_v2_penetration_' + str(self.penetration) + '.csv'
        output_v3_file_modehc = 'hc_hc/output_v3_penetration_' + str(self.penetration) + '.csv'
        output_v1_modehc.to_csv(output_v1_file_modehc, index=False)
        output_v2_modehc.to_csv(output_v2_file_modehc, index=False)
        output_v3_modehc.to_csv(output_v3_file_modehc, index=False)
        output_tap_modehc = pd.DataFrame(monitors_total_tap_modehc)
        output_tap_file_modehc = 'hc_hc/output_tap_penetration_' + str(self.penetration) + '.csv'
        output_tap_modehc.to_csv(output_tap_file_modehc, index=False)
        output_max_v1_modehc = pd.DataFrame(monitors_max_vmag1_modehc)
        output_max_v2_modehc = pd.DataFrame(monitors_max_vmag2_modehc)
        output_max_v3_modehc = pd.DataFrame(monitors_max_vmag3_modehc)
        output_max_v1_file_modehc = 'hc_hc/output_max_v1_penetration_' + str(self.penetration) + '.csv'
        output_max_v2_file_modehc = 'hc_hc/output_max_v2_penetration_' + str(self.penetration) + '.csv'
        output_max_v3_file_modehc = 'hc_hc/output_max_v3_penetration_' + str(self.penetration) + '.csv'
        output_max_v1_modehc.to_csv(output_max_v1_file_modehc, index=False)
        output_max_v2_modehc.to_csv(output_max_v2_file_modehc, index=False)
        output_max_v3_modehc.to_csv(output_max_v3_file_modehc, index=False)
        output_power1_modehc = pd.DataFrame(monitors_total_power1_modehc)
        output_power2_modehc = pd.DataFrame(monitors_total_power2_modehc)
        output_power3_modehc = pd.DataFrame(monitors_total_power3_modehc)
        output_power1_file_modehc = 'hc_hc/output_power1_penetration_' + str(self.penetration) + '.csv'
        output_power2_file_modehc = 'hc_hc/output_power2_penetration_' + str(self.penetration) + '.csv'
        output_power3_file_modehc = 'hc_hc/output_power3_penetration_' + str(self.penetration) + '.csv'
        output_power1_modehc.to_csv(output_power1_file_modehc, index=False)
        output_power2_modehc.to_csv(output_power2_file_modehc, index=False)
        output_power3_modehc.to_csv(output_power3_file_modehc, index=False)

        # Modo 2
        output_v1_modecs = pd.DataFrame(monitors_total_vmag1_modecs)
        output_v2_modecs = pd.DataFrame(monitors_total_vmag2_modecs)
        output_v3_modecs = pd.DataFrame(monitors_total_vmag3_modecs)
        output_v1_file_modecs = 'hc_cs/output_v1_penetration_' + str(self.penetration) + '.csv'
        output_v2_file_modecs = 'hc_cs/output_v2_penetration_' + str(self.penetration) + '.csv'
        output_v3_file_modecs = 'hc_cs/output_v3_penetration_' + str(self.penetration) + '.csv'
        output_v1_modecs.to_csv(output_v1_file_modecs, index=False)
        output_v2_modecs.to_csv(output_v2_file_modecs, index=False)
        output_v3_modecs.to_csv(output_v3_file_modecs, index=False)
        output_tap_modecs = pd.DataFrame(monitors_total_tap_modecs)
        output_tap_file_modecs = 'hc_cs/output_tap_penetration_' + str(self.penetration) + '.csv'
        output_tap_modecs.to_csv(output_tap_file_modecs, index=False)
        output_max_v1_modecs = pd.DataFrame(monitors_max_vmag1_modecs)
        output_max_v2_modecs = pd.DataFrame(monitors_max_vmag2_modecs)
        output_max_v3_modecs = pd.DataFrame(monitors_max_vmag3_modecs)
        output_max_v1_file_modecs = 'hc_cs/output_max_v1_penetration_' + str(self.penetration) + '.csv'
        output_max_v2_file_modecs = 'hc_cs/output_max_v2_penetration_' + str(self.penetration) + '.csv'
        output_max_v3_file_modecs = 'hc_cs/output_max_v3_penetration_' + str(self.penetration) + '.csv'
        output_max_v1_modecs.to_csv(output_max_v1_file_modecs, index=False)
        output_max_v2_modecs.to_csv(output_max_v2_file_modecs, index=False)
        output_max_v3_modecs.to_csv(output_max_v3_file_modecs, index=False)
        output_power1_modecs = pd.DataFrame(monitors_total_power1_modecs)
        output_power2_modecs = pd.DataFrame(monitors_total_power2_modecs)
        output_power3_modecs = pd.DataFrame(monitors_total_power3_modecs)
        output_power1_file_modecs = 'hc_cs/output_power1_penetration_' + str(self.penetration) + '.csv'
        output_power2_file_modecs = 'hc_cs/output_power2_penetration_' + str(self.penetration) + '.csv'
        output_power3_file_modecs = 'hc_cs/output_power3_penetration_' + str(self.penetration) + '.csv'
        output_power1_modecs.to_csv(output_power1_file_modecs, index=False)
        output_power2_modecs.to_csv(output_power2_file_modecs, index=False)
        output_power3_modecs.to_csv(output_power3_file_modecs, index=False)
        output_vcs_modecs = pd.DataFrame(monitors_cs_vmag_modecs)
        output_vcs_file_modecs = 'hc_cs/output_vcs_penetration_' + str(self.penetration) + '.csv'
        output_vcs_modecs.to_csv(output_vcs_file_modecs, index=False)
