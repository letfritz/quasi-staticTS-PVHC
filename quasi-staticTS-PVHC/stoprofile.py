import sys
import os

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")
sns.set(font_scale=2)
sns.set_style("whitegrid")

bus_list = ['860', '840', '844', '848', '830', '830', '830', '890', '802', '806', '802', '806', '808', '810', '818',
            '820', '820', '822', '816', '824', '824', '826', '824', '828', '828', '830', '854', '856', '832', '858',
            '832', '858', '832', '858', '858', '864', '858', '834', '858', '834', '858', '834', '834', '860', '834',
            '860', '834', '860', '860', '836', '860', '836', '860', '836', '836', '840', '836', '840', '862', '838',
            '842', '844', '844', '846', '844', '846', '846', '848']

load_dict = {}
pv_dict = {}
time_load = []
time_pv = []
time_ev = []
time_cs = []
vals_load = []
vals_pv = []
vals_ev = []
vals_cs = []
ev_type = []
buses = []
for n in range(1):
    load_case = pd.read_csv(os.path.dirname(sys.argv[0]) + "/uncertainty/load_" + str(n) + ".csv", header=0, sep=',')

    for bus in range(len(load_case.columns)):
        vals_load.extend(load_case.iloc[:, bus] / max(load_case.iloc[:, bus]))
        time_load.extend(range(1440))
        #bus_actual = bus_list[bus]
        #buses.extend([bus_actual]*1440)

    pv_case = pd.read_csv(os.path.dirname(sys.argv[0]) + "/uncertainty/pv_" + str(n) + ".csv", header=0, sep=',')
    for bus in range(len(pv_case.columns)):
        vals_pv.extend(pv_case.iloc[:, bus] / max(pv_case.iloc[:, bus]))
        time_pv.extend(range(1440))
        #bus_actual = bus_list[bus]
        #buses.extend([bus_actual]*1440)

    ev_case = pd.read_csv(os.path.dirname(sys.argv[0]) + "/uncertainty/ev_curve_hc_" + str(n) + ".csv",
                          header=0, sep=',')
    for bus in range(len(ev_case.columns)):
        vals_ev.extend(ev_case.iloc[:, bus] / max(ev_case.iloc[:, bus]))
        time_ev.extend(range(1440))

    cs_case = pd.read_csv(os.path.dirname(sys.argv[0]) + "/uncertainty/cs_curve_a_" + str(n) + ".csv",
                          header=0, sep=',')
    for bus in range(len(cs_case.columns)):
        vals_cs.extend(cs_case.iloc[:, bus] / max(cs_case.iloc[:, bus]))
        time_cs.extend(range(1440))
        ev_type.extend(['PCS']*1440)

    cs_case = pd.read_csv(os.path.dirname(sys.argv[0]) + "/uncertainty/ev_curve_cs_" + str(n) + ".csv",
                          header=0, sep=',')
    for bus in range(len(cs_case.columns)):
        vals_cs.extend(cs_case.iloc[:, bus] / max(ev_case.iloc[:, bus]))
        time_cs.extend(range(1440))
        ev_type.extend(['RC'] * 1440)


print("aqui1")
#load_dict = {"time": time, "vals": vals, "buses": buses}
load_dict = {"time": time_load, "vals": vals_load}
pv_dict = {"time": time_pv, "vals": vals_pv}
ev_dict = {"time": time_ev, "vals": vals_ev}
cs_dict = {"time": time_cs, "vals": vals_cs, "type": ev_type}
print("aqui2")
load = pd.DataFrame.from_dict(load_dict)
pv = pd.DataFrame.from_dict(pv_dict)
ev = pd.DataFrame.from_dict(ev_dict)
cs = pd.DataFrame.from_dict(cs_dict)
print("aqui3")
#sns.lineplot(data=load, x="time", y="vals", hue="buses")
sns.lineplot(data=load, x="time", y="vals")
plt.xlabel('Time [min]')
plt.ylabel('Buses load profile [pu]')
plt.xlim([2, 1440])
plt.show()
sns.lineplot(data=pv, x="time", y="vals", color='orange')
plt.xlabel('Time [min]')
plt.ylabel('PV profile [pu]')
plt.xlim([0, 1440])
plt.show()
print("aqui4")
sns.lineplot(data=ev, x="time", y="vals", color='green')
plt.xlabel('Time [min]')
plt.ylabel('EVs charging in RC [pu]')
plt.xlim([0, 1440])
plt.show()
sns.lineplot(data=cs, x="time", y="vals", hue="type", color="red")
plt.xlabel('Time [min]')
plt.ylabel('EVs charging in RC and PCS [pu]')
plt.xlim([0, 1440])
plt.show()