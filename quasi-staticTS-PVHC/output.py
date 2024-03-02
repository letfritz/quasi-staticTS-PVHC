# ---------- BIBLIOTECAS ----------
import os
import sys
import matplotlib

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from output_freq import Outputfreq
from output_time import Outputtime
from output_vmax import Outputmax

dist = []
for n in range(1000000):
    dist.append(np.random.normal(1.015, 0.005))
for n in range(1000000):
    dist.append(np.random.normal(1.04, 0.007))
dist_dict = {"dist": dist}
ev_arrival = pd.DataFrame.from_dict(dist_dict)

sns.displot(ev_arrival, x="dist", kind="kde")
plt.show()

input("teste")

sns.set_theme(style="whitegrid")
sns.set(font_scale=1.0)
sns.set_style("whitegrid")

BUS_NODE_LIST = ["802", "806", "808", "810", "812", "814", "850", "818", "824", "820", "822", "826", "828", "830",
                 "854", "858", "860", "842", "840", "862", "844", "846", "848", "816", "832", "856", "852", "864",
                 "834", "836", "838", "890"]

BUS_NODE_V1 = 28
BUS_NODE_V2 = 28
BUS_NODE_V3 = 24

print("ANALISANDO DADOS GERADOS DO TRABALHO DO ISGT")
print("-----")
simulation_number = int(input("NÚMERO DE SIMULAÇÕES DE MONTE CARLO: "))
print("-----")
print("MODOS DE ANÁLISE:")
print("[0] GRÁFICO HOSTING CAPACITY DE TENSÃO MÁXIMA")
print("[1] GRÁFICO HOSTING CAPACITY DE VIOLAÇÃO DE 1.05 [PU] ACIMA DE 15 [MIN]")
print("[2] GRÁFICO DE PENETRAÇÃO POR BARRA VIOLADA")
print("[3] GRÁFICO DO RISCO DE VIOLAR TENSÃO (PERCENTIL 90% e 95%)")
print("[4] GRÁFICO AO LONGO DO TEMPO DA BARRA 844")
print("[5] GRÁFICO DE PDF DA TENSÃO DE SAÍDA")
print("[6] GRÁFICO DE BOXPLOT DA MUDANÇA DE TAP")

output_choice = int(input("Qual output deseja?"))

print("... importando dados para output", output_choice, "...")

if output_choice == 0:
    max_violation = Outputmax(simulation_number)
    max_violation.get_vmax()

elif output_choice == 1:
    # Dados de penetração vs tempo de violação
    time_violation = Outputtime(simulation_number)
    time_violation.get_time_violation()
    hosting_capacity_violation = pd.read_csv(os.path.dirname(sys.argv[0]) + "/voltage_violation.csv", header=0,
                                             sep=',')
    # Plot único
    sns.scatterplot(data=hosting_capacity_violation,
                    x="penetration",
                    y="freq",
                    style="phase",
                    hue="type",
                    s=80)
    plt.xlabel('PV penetration [%]')
    plt.ylabel('Violation frequency per day')
    plt.show()
    # Plot triplo
    penetration_v1 = []
    penetration_v2 = []
    penetration_v3 = []
    type_v1 = []
    type_v2 = []
    type_v3 = []
    freq_v1 = []
    freq_v2 = []
    freq_v3 = []
    for n in range(len(hosting_capacity_violation)):
        if hosting_capacity_violation.iloc[n, 2] == 'V1':
            penetration_v1.append(hosting_capacity_violation.iloc[n, 0])
            freq_v1.append(hosting_capacity_violation.iloc[n, 1])
            type_v1.append(hosting_capacity_violation.iloc[n, 3])
        elif hosting_capacity_violation.iloc[n, 2] == 'V2':
            penetration_v2.append(hosting_capacity_violation.iloc[n, 0])
            freq_v2.append(hosting_capacity_violation.iloc[n, 1])
            type_v2.append(hosting_capacity_violation.iloc[n, 3])
        elif hosting_capacity_violation.iloc[n, 2] == 'V3':
            penetration_v3.append(hosting_capacity_violation.iloc[n, 0])
            freq_v3.append(hosting_capacity_violation.iloc[n, 1])
            type_v3.append(hosting_capacity_violation.iloc[n, 3])

    v1_dict = {"penetration": penetration_v1, "freq": freq_v1, "type": type_v1}
    v2_dict = {"penetration": penetration_v2, "freq": freq_v2, "type": type_v2}
    v3_dict = {"penetration": penetration_v3, "freq": freq_v3, "type": type_v3}
    hosting_capacity_violation_v1 = pd.DataFrame.from_dict(v1_dict)
    hosting_capacity_violation_v2 = pd.DataFrame.from_dict(v2_dict)
    hosting_capacity_violation_v3 = pd.DataFrame.from_dict(v3_dict)
    fig, axes = plt.subplots(1, 3)
    axes[0].set_title('V1')
    axes[1].set_title('V2')
    axes[2].set_title('V3')
    sns.scatterplot(data=hosting_capacity_violation_v1, x="penetration", y="freq", hue="type", ax=axes[0])
    sns.scatterplot(data=hosting_capacity_violation_v2, x="penetration", y="freq", hue="type", ax=axes[1])
    sns.scatterplot(data=hosting_capacity_violation_v3, x="penetration", y="freq", hue="type", ax=axes[2])
    axes[0].set_xlabel('PV penetration [%]')
    axes[0].set_ylabel('Violation frequency per day')
    axes[1].set_xlabel('PV penetration [%]')
    axes[1].set_ylabel('Violation frequency per day')
    axes[2].set_xlabel('PV penetration [%]')
    axes[2].set_ylabel('Violation frequency per day')
    plt.show()


elif output_choice == 2:
    hosting_capacity_bus = pd.read_csv(os.path.dirname(sys.argv[0]) + "/voltage_violation.csv", header=0,
                                       sep=',')
    bus_type = []
    bus_name = []
    bus_value = []
    bus_penetration = []

    penetration = 0
    count = 0
    for n in range(21):
        none_v1_value = 0
        none_v2_value = 0
        none_v3_value = 0
        hc_v1_value = 0
        hc_v2_value = 0
        hc_v3_value = 0
        cs_v1_value = 0
        cs_v2_value = 0
        cs_v3_value = 0
        none_v1_name = 0
        none_v2_name = 0
        none_v3_name = 0
        hc_v1_name = 0
        hc_v2_name = 0
        hc_v3_name = 0
        cs_v1_name = 0
        cs_v2_name = 0
        cs_v3_name = 0

        while hosting_capacity_bus.iloc[count, 0] == penetration:
            if hosting_capacity_bus.iloc[count, 1] > 0:
                if hosting_capacity_bus.iloc[count, 3] == 'none':
                    if hosting_capacity_bus.iloc[count, 2] == 'V1' and \
                            none_v1_name != hosting_capacity_bus.iloc[count, 4]:
                        none_v1_name = hosting_capacity_bus.iloc[count, 4]
                        none_v1_value += 1
                    elif hosting_capacity_bus.iloc[count, 2] == 'V2' and \
                            none_v2_name != hosting_capacity_bus.iloc[count, 4]:
                        none_v2_name = hosting_capacity_bus.iloc[count, 4]
                        none_v2_value += 1
                    elif hosting_capacity_bus.iloc[count, 2] == 'V3' and \
                            none_v3_name != hosting_capacity_bus.iloc[count, 4]:
                        none_v3_name = hosting_capacity_bus.iloc[count, 4]
                        none_v3_value += 1
                elif hosting_capacity_bus.iloc[count, 3] == 'home charging':
                    if hosting_capacity_bus.iloc[count, 2] == 'V1' and \
                            hc_v1_name != hosting_capacity_bus.iloc[count, 4]:
                        hc_v1_name = hosting_capacity_bus.iloc[count, 4]
                        hc_v1_value += 1
                    elif hosting_capacity_bus.iloc[count, 2] == 'V2' and \
                            hc_v2_name != hosting_capacity_bus.iloc[count, 4]:
                        hc_v2_name = hosting_capacity_bus.iloc[count, 4]
                        hc_v2_value += 1
                    elif hosting_capacity_bus.iloc[count, 2] == 'V3' and \
                            hc_v3_name != hosting_capacity_bus.iloc[count, 4]:
                        hc_v3_name = hosting_capacity_bus.iloc[count, 4]
                        hc_v3_value += 1
                elif hosting_capacity_bus.iloc[count, 3] == 'charging station':
                    if hosting_capacity_bus.iloc[count, 2] == 'V1' and \
                            cs_v1_name != hosting_capacity_bus.iloc[count, 4]:
                        cs_v1_name = hosting_capacity_bus.iloc[count, 4]
                        cs_v1_value += 1
                    elif hosting_capacity_bus.iloc[count, 2] == 'V2' and \
                            cs_v2_name != hosting_capacity_bus.iloc[count, 4]:
                        cs_v2_name = hosting_capacity_bus.iloc[count, 4]
                        cs_v2_value += 1
                    elif hosting_capacity_bus.iloc[count, 2] == 'V3' and \
                            cs_v3_name != hosting_capacity_bus.iloc[count, 4]:
                        cs_v3_name = hosting_capacity_bus.iloc[count, 4]
                        cs_v3_value += 1
            count += 1
            if count >= len(hosting_capacity_bus):
                count = 0
        bus_penetration.append(penetration)
        bus_name.append('Scenario A')
        bus_value.append(none_v1_value * 100 / BUS_NODE_V1)
        bus_type.append('V1')
        bus_penetration.append(penetration)
        bus_name.append('Scenario A')
        bus_value.append(none_v2_value * 100 / BUS_NODE_V2)
        bus_type.append('V2')
        bus_penetration.append(penetration)
        bus_name.append('Scenario A')
        bus_value.append(none_v3_value * 100 / BUS_NODE_V3)
        bus_type.append('V3')
        bus_penetration.append(penetration)
        bus_name.append('Scenario B')
        bus_value.append(hc_v1_value * 100 / BUS_NODE_V1)
        bus_type.append('V1')
        bus_penetration.append(penetration)
        bus_name.append('Scenario B')
        bus_value.append(hc_v2_value * 100 / BUS_NODE_V2)
        bus_type.append('V2')
        bus_penetration.append(penetration)
        bus_name.append('Scenario B')
        bus_value.append(hc_v3_value * 100 / BUS_NODE_V3)
        bus_type.append('V3')
        bus_penetration.append(penetration)
        bus_name.append('Scenario C')
        bus_value.append(cs_v1_value * 100 / BUS_NODE_V1)
        bus_type.append('V1')
        bus_penetration.append(penetration)
        bus_name.append('Scenario C')
        bus_value.append(cs_v2_value * 100 / BUS_NODE_V2)
        bus_type.append('V2')
        bus_penetration.append(penetration)
        bus_name.append('Scenario C')
        bus_value.append(cs_v3_value * 100 / BUS_NODE_V3)
        bus_type.append('V3')

        penetration += 5

    data_dict = {"penetration": bus_penetration, "case": bus_name, "phase": bus_type, "value": bus_value}
    data = pd.DataFrame.from_dict(data_dict)

    ax = sns.lineplot(data=data, x="penetration", y="value", hue="case", style="phase", linewidth=2)
    plt.xlabel("PV penetration [%]")
    plt.ylabel("Violated bus [%]")
    plt.xlim([40, 100])
    plt.ylim([-1, 100])
    plt.show()
    # Plot triplo por fase
    penetration_v1 = []
    penetration_v2 = []
    penetration_v3 = []
    type_v1 = []
    type_v2 = []
    type_v3 = []
    bus_v1 = []
    bus_v2 = []
    bus_v3 = []
    for n in range(len(data)):
        if data.iloc[n, 2] == 'V1':
            penetration_v1.append(data.iloc[n, 0])
            bus_v1.append(data.iloc[n, 3])
            type_v1.append(data.iloc[n, 1])
        elif data.iloc[n, 2] == 'V2':
            penetration_v2.append(data.iloc[n, 0])
            bus_v2.append(data.iloc[n, 3])
            type_v2.append(data.iloc[n, 1])
        elif data.iloc[n, 2] == 'V3':
            penetration_v3.append(data.iloc[n, 0])
            bus_v3.append(data.iloc[n, 3])
            type_v3.append(data.iloc[n, 1])
    v1_dict = {"penetration": penetration_v1, "bus": bus_v1, "phase": type_v1}
    v2_dict = {"penetration": penetration_v2, "bus": bus_v2, "phase": type_v2}
    v3_dict = {"penetration": penetration_v3, "bus": bus_v3, "phase": type_v3}
    hosting_capacity_violation_v1 = pd.DataFrame.from_dict(v1_dict)
    hosting_capacity_violation_v2 = pd.DataFrame.from_dict(v2_dict)
    hosting_capacity_violation_v3 = pd.DataFrame.from_dict(v3_dict)
    fig, axes = plt.subplots(3, 1)
    axes[0].set_title('V1')
    axes[1].set_title('V2')
    axes[2].set_title('V3')
    g1 = sns.lineplot(data=hosting_capacity_violation_v1,
                      x="penetration", y="bus", hue="phase", ax=axes[0], linewidth=2)
    g1.legend_.set_title(None)
    g2 = sns.lineplot(data=hosting_capacity_violation_v2,
                      x="penetration", y="bus", hue="phase", ax=axes[1], linewidth=2)
    g2.legend_.set_title(None)
    g2.legend_.remove()
    g3 = sns.lineplot(data=hosting_capacity_violation_v3,
                      x="penetration", y="bus", hue="phase", ax=axes[2], linewidth=2)
    g3.legend_.set_title(None)
    g3.legend_.remove()
    axes[0].set_ylabel('Violated bus [%]')
    axes[0].set_xlabel('')
    axes[0].set_xlim([50, 100])
    axes[0].set_ylim([-3, 90])
    axes[0].xaxis.set_ticklabels([])
    axes[1].set_ylabel('Violated bus [%]')
    axes[1].set_xlabel('')
    axes[1].set_xlim([50, 100])
    axes[1].set_ylim([-3, 90])
    axes[1].xaxis.set_ticklabels([])
    axes[2].set_ylabel('Violated bus [%]')
    axes[2].set_xlabel('PV penetration [%]')
    axes[2].set_xlim([50, 100])
    axes[2].set_ylim([-3, 90])
    plt.show()

    # Plot triplo
    penetration_none = []
    penetration_hc = []
    penetration_cs = []
    type_none = []
    type_hc = []
    type_cs = []
    bus_none = []
    bus_hc = []
    bus_cs = []
    for n in range(len(data)):
        if data.iloc[n, 1] == 'Scenario A':
            penetration_none.append(data.iloc[n, 0])
            bus_none.append(data.iloc[n, 3])
            type_none.append(data.iloc[n, 2])
        elif data.iloc[n, 1] == 'Scenario B':
            penetration_hc.append(data.iloc[n, 0])
            bus_hc.append(data.iloc[n, 3])
            type_hc.append(data.iloc[n, 2])
        elif data.iloc[n, 1] == 'Scenario C':
            penetration_cs.append(data.iloc[n, 0])
            bus_cs.append(data.iloc[n, 3])
            type_cs.append(data.iloc[n, 2])

    none_dict = {"penetration": penetration_none, "bus": bus_none, "phase": type_none}
    hc_dict = {"penetration": penetration_hc, "bus": bus_hc, "phase": type_hc}
    cs_dict = {"penetration": penetration_cs, "bus": bus_cs, "phase": type_cs}
    hosting_capacity_violation_none = pd.DataFrame.from_dict(none_dict)
    hosting_capacity_violation_hc = pd.DataFrame.from_dict(hc_dict)
    hosting_capacity_violation_cs = pd.DataFrame.from_dict(cs_dict)
    fig, axes = plt.subplots(1, 3)
    axes[0].set_title('Scenario A')
    axes[1].set_title('Scenario B')
    axes[2].set_title('Scenario C')
    sns.lineplot(data=hosting_capacity_violation_none,
                 x="penetration", y="bus", hue="phase", ax=axes[0], linewidth=2)
    sns.lineplot(data=hosting_capacity_violation_hc,
                 x="penetration", y="bus", hue="phase", ax=axes[1], linewidth=2)
    sns.lineplot(data=hosting_capacity_violation_cs,
                 x="penetration", y="bus", hue="phase", ax=axes[2], linewidth=2)
    axes[0].set_xlabel('PV penetration [%]')
    axes[0].set_ylabel('Violated bus [%]')
    axes[1].set_xlabel('PV penetration [%]')
    axes[2].set_xlabel('PV penetration [%]')
    plt.show()
    # Plot de V1
    penetration_list = []
    bus_list = []
    type_list = []
    for n in range(len(data)):
        if data.iloc[n, 2] == 'V1':
            penetration_list.append(data.iloc[n, 0])
            bus_list.append(data.iloc[n, 3])
            type_list.append(data.iloc[n, 1])

    data_dict = {"penetration": penetration_list, "bus": bus_list, "case": type_list}
    hosting_capacity_violation = pd.DataFrame.from_dict(data_dict)
    sns.lineplot(data=hosting_capacity_violation,
                 x="penetration", y="bus", hue="case", linewidth=2)
    plt.xlabel("PV penetration [%]")
    plt.ylabel("Violated bus [%]")
    plt.ylim(0, 100)
    plt.show()
elif output_choice == 3:
    pass
elif output_choice == 4:
    none_v1_100 = pd.read_csv(os.path.dirname(sys.argv[0]) + "/hc_pv/output_v1_penetration_100.csv",
                              header=0,
                              sep=',')
    hc_v1_100 = pd.read_csv(os.path.dirname(sys.argv[0]) + "/hc_hc/output_v1_penetration_100.csv",
                            header=0,
                            sep=',')
    cs_v1_100 = pd.read_csv(os.path.dirname(sys.argv[0]) + "/hc_cs/output_v1_penetration_100.csv",
                            header=0,
                            sep=',')
    none_v2_100 = pd.read_csv(os.path.dirname(sys.argv[0]) + "/hc_pv/output_v2_penetration_100.csv",
                              header=0,
                              sep=',')
    hc_v2_100 = pd.read_csv(os.path.dirname(sys.argv[0]) + "/hc_hc/output_v2_penetration_100.csv",
                            header=0,
                            sep=',')
    cs_v2_100 = pd.read_csv(os.path.dirname(sys.argv[0]) + "/hc_cs/output_v2_penetration_100.csv",
                            header=0,
                            sep=',')
    none_v3_100 = pd.read_csv(os.path.dirname(sys.argv[0]) + "/hc_pv/output_v3_penetration_100.csv",
                              header=0,
                              sep=',')
    hc_v3_100 = pd.read_csv(os.path.dirname(sys.argv[0]) + "/hc_hc/output_v3_penetration_100.csv",
                            header=0,
                            sep=',')
    cs_v3_100 = pd.read_csv(os.path.dirname(sys.argv[0]) + "/hc_cs/output_v3_penetration_100.csv",
                            header=0,
                            sep=',')
    none_v1 = none_v1_100.iloc[:, 20]
    cs_v1 = cs_v1_100.iloc[:, 20]
    hc_v1 = hc_v1_100.iloc[:, 20]
    none_v2 = none_v2_100.iloc[:, 20]
    cs_v2 = cs_v2_100.iloc[:, 20]
    hc_v2 = hc_v2_100.iloc[:, 20]
    none_v3 = none_v3_100.iloc[:, 20]
    cs_v3 = cs_v3_100.iloc[:, 20]
    hc_v3 = hc_v3_100.iloc[:, 20]
    value = np.concatenate((none_v1, hc_v1, cs_v1, none_v2, hc_v2, cs_v2, none_v3, hc_v3, cs_v3), axis=0)
    phase_v1 = ['V1'] * simulation_number * 3 * 1440
    phase_v2 = ['V2'] * simulation_number * 3 * 1440
    phase_v3 = ['V3'] * simulation_number * 3 * 1440
    phase = phase_v1 + phase_v2 + phase_v3
    case_none = ['none'] * simulation_number * 1440
    case_hc = ['home charging'] * simulation_number * 1440
    case_cs = ['charging station'] * simulation_number * 1440
    case = case_none + case_hc + case_cs + case_none + case_hc + case_cs + case_none + case_hc + case_cs
    time = [i for _ in range(3 * 3 * simulation_number) for i in range(1440)]

    data_dict = {"timepoint": time, "voltage": value, "case": case, "phase": phase}
    data = pd.DataFrame.from_dict(data_dict)
    print(data)

    data.to_csv("teste.csv")
    sns.lineplot(data=data, x="timepoint", y="voltage", hue="case", style="phase")
    plt.axhline(y=1.05, color='r', linestyle='-')
    plt.ylabel("Voltage magnitude [pu]")
    plt.xlabel("Time [min]")
    plt.xlim(0, 1440)
    plt.show()
    '''
    # Ampliando no tempo de 400 a 600
    count = 0
    for n in range(len(data)):
        if 400 <= data.iloc[count, 0] <= 600:
            data = data.drop(index=n)
            count -= 1
        count += 1
    print(data)
    #none_v1 = none_v1_100.iloc[400:600, 20]
    #cs_v1 = cs_v1_100.iloc[400:600, 20]
    #hc_v1 = hc_v1_100.iloc[400:600, 20]
    #none_v2 = none_v2_100.iloc[400:600, 20]
    #cs_v2 = cs_v2_100.iloc[400:600, 20]
    #hc_v2 = hc_v2_100.iloc[400:600, 20]
    #none_v3 = none_v3_100.iloc[400:600, 20]
    #cs_v3 = cs_v3_100.iloc[400:600, 20]
    #hc_v3 = hc_v3_100.iloc[400:600, 20]
    #value = np.concatenate((none_v1, hc_v1, cs_v1, none_v2, hc_v2, cs_v2, none_v3, hc_v3, cs_v3), axis=0)
    #print("value", len(value))
    #phase_v1 = ['V1'] * simulation_number * 3 * 200
    #phase_v2 = ['V2'] * simulation_number * 3 * 200
    #phase_v3 = ['V3'] * simulation_number * 3 * 200
    #phase = phase_v1 + phase_v2 + phase_v3
    #print("phase", len(phase))
    #case_none = ['none'] * simulation_number * 200
    #case_hc = ['home charging'] * simulation_number * 200
    #case_cs = ['charging station'] * simulation_number * 200
    #case = case_none + case_hc + case_cs + case_none + case_hc + case_cs + case_none + case_hc + case_cs
    #print("case", len(case))
    #time = [i for _ in range(3 * 3 * simulation_number) for i in range(400, 600)]
    #print("time", len(time))

    #data_dict = {"timepoint": time, "voltage": value, "case": case, "phase": phase}
    #data = pd.DataFrame.from_dict(data_dict)
    #data.to_csv("teste.csv")
    sns.lineplot(data=data, x="timepoint", y="voltage", hue="case", style="phase")
    plt.axhline(y=1.05, color='r', linestyle='-')
    plt.ylabel("Voltage magnitude [pu]")
    plt.xlabel("Time [min]")
    plt.xlim(0, 200)
    plt.show()
    '''
elif output_choice == 5:
    # PDF das tensões
    vmax_violation = Outputtime(simulation_number)
    fig, axes = plt.subplots(3, 3)

    penetration = 0
    p = 0
    for file in range(3):
        hosting_capacity_max_v1_violation, hosting_capacity_max_v2_violation, \
        hosting_capacity_max_v3_violation = vmax_violation.get_vmax_violation(penetration)
        print("Penetração de ", str(penetration))
        print("Fase A - Média: ", str(np.mean(hosting_capacity_max_v1_violation)), " ; Desvio padrão: ",
              str(np.std(hosting_capacity_max_v1_violation)))
        print("Fase B - Média: ", str(np.mean(hosting_capacity_max_v2_violation)), " ; Desvio padrão: ",
              str(np.std(hosting_capacity_max_v2_violation)))
        print("Fase C - Média: ", str(np.mean(hosting_capacity_max_v3_violation)), " ; Desvio padrão: ",
              str(np.std(hosting_capacity_max_v3_violation)))

        sns.displot(hosting_capacity_max_v1_violation, x="vmax", kind="kde", hue="type")
        ax = plt.gca()
        none = ax.lines[2]
        hc = ax.lines[1]
        cs = ax.lines[0]
        none_result = {'x': none.get_xdata(), 'y': none.get_ydata()}
        hc_result = {'x': hc.get_xdata(), 'y': hc.get_ydata()}
        cs_result = {'x': cs.get_xdata(), 'y': cs.get_ydata()}
        none_result = pd.DataFrame.from_dict(none_result)
        hc_result = pd.DataFrame.from_dict(hc_result)
        cs_result = pd.DataFrame.from_dict(cs_result)
        axes[p, 0].plot(none_result['x'], none_result['y'], label="Scenario A")
        axes[p, 0].plot(hc_result['x'], hc_result['y'], label="Scenario B")
        axes[p, 0].plot(cs_result['x'], cs_result['y'], label="Scenario C")
        sns.displot(hosting_capacity_max_v2_violation, x="vmax", kind="kde", hue="type")
        ax = plt.gca()
        none = ax.lines[2]
        hc = ax.lines[1]
        cs = ax.lines[0]
        none_result = {'x': none.get_xdata(), 'y': none.get_ydata()}
        hc_result = {'x': hc.get_xdata(), 'y': hc.get_ydata()}
        cs_result = {'x': cs.get_xdata(), 'y': cs.get_ydata()}
        none_result = pd.DataFrame.from_dict(none_result)
        hc_result = pd.DataFrame.from_dict(hc_result)
        cs_result = pd.DataFrame.from_dict(cs_result)
        axes[p, 1].plot(none_result['x'], none_result['y'], label="Scenario A")
        axes[p, 1].plot(hc_result['x'], hc_result['y'], label="Scenario B")
        axes[p, 1].plot(cs_result['x'], cs_result['y'], label="Scenario C")
        sns.displot(hosting_capacity_max_v3_violation, x="vmax", kind="kde", hue="type")
        ax = plt.gca()
        none = ax.lines[2]
        hc = ax.lines[1]
        cs = ax.lines[0]
        none_result = {'x': none.get_xdata(), 'y': none.get_ydata()}
        hc_result = {'x': hc.get_xdata(), 'y': hc.get_ydata()}
        cs_result = {'x': cs.get_xdata(), 'y': cs.get_ydata()}
        none_result = pd.DataFrame.from_dict(none_result)
        hc_result = pd.DataFrame.from_dict(hc_result)
        cs_result = pd.DataFrame.from_dict(cs_result)
        axes[p, 2].plot(none_result['x'], none_result['y'], label="Scenario A")
        axes[p, 2].plot(hc_result['x'], hc_result['y'], label="Scenario B")
        axes[p, 2].plot(cs_result['x'], cs_result['y'], label="Scenario C")
        penetration += 50
        p += 1
    axes[0, 0].set(ylabel='PDF for 0% PV [%]')
    axes[1, 0].set(ylabel='PDF for 50% PV [%]')
    axes[2, 0].set(xlabel='Phase 1 voltage magnitude [pu]', ylabel='PDF for 100% PV [%]')
    axes[2, 1].set(xlabel='Phase 2 voltage magnitude [pu]')
    axes[2, 2].set(xlabel='Phase 3 voltage magnitude [pu]')
    axes[2, 2].legend()
    axes[0, 0].set_xlim([0.83, 1.11])
    axes[0, 0].axvline(x=1.05, color='r', linestyle='--')
    axes[0, 1].set_xlim([0.83, 1.11])
    axes[0, 1].axvline(x=1.05, color='r', linestyle='--')
    axes[0, 2].set_xlim([0.83, 1.11])
    axes[0, 2].axvline(x=1.05, color='r', linestyle='--')
    axes[1, 0].set_xlim([0.83, 1.11])
    axes[1, 0].axvline(x=1.05, color='r', linestyle='--')
    axes[1, 1].set_xlim([0.83, 1.11])
    axes[1, 1].axvline(x=1.05, color='r', linestyle='--')
    axes[1, 2].set_xlim([0.83, 1.11])
    axes[1, 2].axvline(x=1.05, color='r', linestyle='--')
    axes[2, 0].set_xlim([0.83, 1.11])
    axes[2, 0].axvline(x=1.05, color='r', linestyle='--')
    axes[2, 1].set_xlim([0.83, 1.11])
    axes[2, 1].axvline(x=1.05, color='r', linestyle='--')
    axes[2, 2].set_xlim([0.83, 1.11])
    axes[2, 2].axvline(x=1.05, color='r', linestyle='--')
    axes[0, 0].set_ylim([0.0, 17])
    axes[0, 1].set_ylim([0.0, 17])
    axes[0, 2].set_ylim([0.0, 17])
    axes[1, 0].set_ylim([0.0, 17])
    axes[1, 1].set_ylim([0.0, 17])
    axes[1, 2].set_ylim([0.0, 17])
    axes[2, 0].set_ylim([0.0, 17])
    axes[2, 1].set_ylim([0.0, 17])
    axes[2, 2].set_ylim([0.0, 17])
    plt.show()
elif output_choice == 6:
    none_0 = pd.read_csv(os.path.dirname(sys.argv[0]) + "/hc_pv/output_tap_penetration_0.csv",
                         header=0,
                         sep=',')
    none_50 = pd.read_csv(os.path.dirname(sys.argv[0]) + "/hc_pv/output_tap_penetration_50.csv",
                          header=0,
                          sep=',')
    none_100 = pd.read_csv(os.path.dirname(sys.argv[0]) + "/hc_pv/output_tap_penetration_100.csv",
                           header=0,
                           sep=',')
    hc_0 = pd.read_csv(os.path.dirname(sys.argv[0]) + "/hc_hc/output_tap_penetration_0.csv",
                       header=0,
                       sep=',')
    hc_50 = pd.read_csv(os.path.dirname(sys.argv[0]) + "/hc_hc/output_tap_penetration_50.csv",
                        header=0,
                        sep=',')
    hc_100 = pd.read_csv(os.path.dirname(sys.argv[0]) + "/hc_hc/output_tap_penetration_100.csv",
                         header=0,
                         sep=',')
    cs_0 = pd.read_csv(os.path.dirname(sys.argv[0]) + "/hc_cs/output_tap_penetration_0.csv",
                       header=0,
                       sep=',')
    cs_50 = pd.read_csv(os.path.dirname(sys.argv[0]) + "/hc_cs/output_tap_penetration_50.csv",
                        header=0,
                        sep=',')
    cs_100 = pd.read_csv(os.path.dirname(sys.argv[0]) + "/hc_cs/output_tap_penetration_100.csv",
                         header=0,
                         sep=',')
    value = np.concatenate((none_0.iloc[:, 0], none_0.iloc[:, 1], none_0.iloc[:, 2], none_50.iloc[:, 0],
                            none_50.iloc[:, 1], none_50.iloc[:, 2], none_100.iloc[:, 0], none_100.iloc[:, 1],
                            none_100.iloc[:, 2], hc_0.iloc[:, 0], hc_0.iloc[:, 1], hc_0.iloc[:, 2],
                            hc_50.iloc[:, 0], hc_50.iloc[:, 1], hc_50.iloc[:, 2], hc_100.iloc[:, 0],
                            hc_100.iloc[:, 1], hc_100.iloc[:, 2], cs_0.iloc[:, 0], cs_0.iloc[:, 1],
                            cs_0.iloc[:, 2], cs_50.iloc[:, 0], cs_50.iloc[:, 1], cs_50.iloc[:, 2],
                            cs_100.iloc[:, 0], cs_100.iloc[:, 1], cs_100.iloc[:, 2]), axis=0)
    penetration_0 = ['0 % PV'] * len(none_0.iloc[:, 0]) * 3
    penetration_50 = ['50 % PV'] * len(none_0.iloc[:, 0]) * 3
    penetration_100 = ['100 % PV'] * len(none_0.iloc[:, 0]) * 3
    penetration = penetration_0 + penetration_50 + penetration_100 + penetration_0 + penetration_50 + \
                  penetration_100 + penetration_0 + penetration_50 + penetration_100
    case_none = ['Scenario A'] * len(none_0.iloc[:, 0]) * 3 * 3
    case_hc = ['Scenario B'] * len(none_0.iloc[:, 0]) * 3 * 3
    case_cs = ['Scenario C'] * len(none_0.iloc[:, 0]) * 3 * 3
    case = case_none + case_hc + case_cs
    phase_v1 = ['V1'] * len(none_0.iloc[:, 0])
    phase_v2 = ['V2'] * len(none_0.iloc[:, 0])
    phase_v3 = ['V3'] * len(none_0.iloc[:, 0])
    phase = phase_v1 + phase_v2 + phase_v3
    phase = phase + phase + phase + phase + phase + phase + phase + phase + phase

    data_dict = {"penetration": penetration, "voltage": value, "case": case, "phase": phase}
    data = pd.DataFrame.from_dict(data_dict)
    sns.catplot(x="penetration", y="voltage", hue="case", col="phase", data=data, kind="box", palette="Set3",
                height=4, aspect=.7)
    # plt.axhline(y=1.05, color='r', linestyle='-')
    plt.show()
