# ---------- BIBLIOTECAS ----------
import os
import sys

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

BUS_NODE_LIST = ["802", "806", "808", "810", "812", "814", "850", "818", "824", "820", "822", "826", "828", "830",
                 "854", "858", "860", "842", "840", "862", "844", "846", "848", "816", "832", "856", "852", "864",
                 "834", "836", "838", "890"]


class Outputmax:
    def __init__(self, simulation_number):
        self.simulation_number = int(simulation_number)

    def get_vmax(self):
        # Vetor para armazenar os dados
        vmax_list = []
        name_list = []
        type_list = []
        penetration_list = []
        bus_list = []

        penetration = 0
        for file in range(21):
            df1_pv = pd.read_csv(
                os.path.dirname(sys.argv[0]) + "/hc_pv/output_v1_penetration_" + str(penetration) + ".csv",
                header=0, sep=',')
            df2_pv = pd.read_csv(
                os.path.dirname(sys.argv[0]) + "/hc_pv/output_v2_penetration_" + str(penetration) + ".csv",
                header=0, sep=',')
            df3_pv = pd.read_csv(
                os.path.dirname(sys.argv[0]) + "/hc_pv/output_v3_penetration_" + str(penetration) + ".csv",
                header=0, sep=',')
            df1_hc = pd.read_csv(
                os.path.dirname(sys.argv[0]) + "/hc_hc/output_v1_penetration_" + str(penetration) + ".csv",
                header=0, sep=',')
            df2_hc = pd.read_csv(
                os.path.dirname(sys.argv[0]) + "/hc_hc/output_v2_penetration_" + str(penetration) + ".csv",
                header=0, sep=',')
            df3_hc = pd.read_csv(
                os.path.dirname(sys.argv[0]) + "/hc_hc/output_v3_penetration_" + str(penetration) + ".csv",
                header=0, sep=',')
            df1_cs = pd.read_csv(
                os.path.dirname(sys.argv[0]) + "/hc_cs/output_v1_penetration_" + str(penetration) + ".csv",
                header=0, sep=',')
            df2_cs = pd.read_csv(
                os.path.dirname(sys.argv[0]) + "/hc_cs/output_v2_penetration_" + str(penetration) + ".csv",
                header=0, sep=',')
            df3_cs = pd.read_csv(
                os.path.dirname(sys.argv[0]) + "/hc_cs/output_v3_penetration_" + str(penetration) + ".csv",
                header=0, sep=',')

            df1_pv.drop(['0', '1'], axis=1, inplace=True)
            df1_hc.drop(['0', '1'], axis=1, inplace=True)
            df1_cs.drop(['0', '1'], axis=1, inplace=True)
            df2_pv.drop(['0', '1', '3', '7', '9', '10', '11', '25', '27', '30'], axis=1, inplace=True)
            df2_hc.drop(['0', '1', '3', '7', '9', '10', '11', '25', '27', '30'], axis=1, inplace=True)
            df2_cs.drop(['0', '1', '3', '7', '9', '10', '11', '25', '27', '30'], axis=1, inplace=True)
            df3_pv.drop(['0', '1', '3', '4', '7', '9', '10', '11', '25', '27', '30'], axis=1, inplace=True)
            df3_hc.drop(['0', '1', '3', '4', '7', '9', '10', '11', '25', '27', '30'], axis=1, inplace=True)
            df3_cs.drop(['0', '1', '3', '4', '7', '9', '10', '11', '25', '27', '30'], axis=1, inplace=True)

            # Construindo listas para formar o dicionário
            # ----- V1 -----
            for line in range(df1_pv.shape[1]):
                # base case
                for n in range(self.simulation_number):
                    vmax = max(df1_pv.iloc[n * 1440:(n * 1440 + 1440), line])
                    penetration_list.append(penetration)
                    vmax_list.append(vmax)
                    type_list.append('Scenario A')
                    name_list.append('V1')
                    bus_list.append(BUS_NODE_LIST[line])
                # home charging
                for n in range(self.simulation_number):
                    vmax = max(df1_hc.iloc[n * 1440:(n * 1440 + 1440), line])
                    penetration_list.append(penetration)
                    vmax_list.append(vmax)
                    type_list.append('Scenario B')
                    name_list.append('V1')
                    bus_list.append(BUS_NODE_LIST[line])
                # charging station
                for n in range(self.simulation_number):
                    vmax = max(df1_cs.iloc[n * 1440:(n * 1440 + 1440), line])
                    penetration_list.append(penetration)
                    vmax_list.append(vmax)
                    type_list.append('Scenario C')
                    name_list.append('V1')
                    bus_list.append(BUS_NODE_LIST[line])

            # ----- V2 -----
            for line in range(df2_pv.shape[1]):
                # base case
                for n in range(self.simulation_number):
                    vmax = max(df2_pv.iloc[n * 1440:(n * 1440 + 1440), line])
                    penetration_list.append(penetration)
                    vmax_list.append(vmax)
                    type_list.append('Scenario A')
                    name_list.append('V2')
                    bus_list.append(BUS_NODE_LIST[line])
                # home charging
                for n in range(self.simulation_number):
                    vmax = max(df2_hc.iloc[n * 1440:(n * 1440 + 1440), line])
                    penetration_list.append(penetration)
                    vmax_list.append(vmax)
                    type_list.append('Scenario B')
                    name_list.append('V2')
                    bus_list.append(BUS_NODE_LIST[line])
                # charging station
                for n in range(self.simulation_number):
                    vmax = max(df2_cs.iloc[n * 1440:(n * 1440 + 1440), line])
                    penetration_list.append(penetration)
                    vmax_list.append(vmax)
                    type_list.append('Scenario C')
                    name_list.append('V2')
                    bus_list.append(BUS_NODE_LIST[line])

            # ----- V3 -----
            for line in range(df3_pv.shape[1]):
                # base case
                for n in range(self.simulation_number):
                    vmax = max(df3_pv.iloc[n * 1440:(n * 1440 + 1440), line])
                    penetration_list.append(penetration)
                    vmax_list.append(vmax)
                    type_list.append('Scenario A')
                    name_list.append('V3')
                    bus_list.append(BUS_NODE_LIST[line])
                # home charging
                for n in range(self.simulation_number):
                    vmax = max(df3_hc.iloc[n * 1440:(n * 1440 + 1440), line])
                    penetration_list.append(penetration)
                    vmax_list.append(vmax)
                    type_list.append('Scenario B')
                    name_list.append('V3')
                    bus_list.append(BUS_NODE_LIST[line])
                # charging station
                for n in range(self.simulation_number):
                    vmax = max(df3_cs.iloc[n * 1440:(n * 1440 + 1440), line])
                    penetration_list.append(penetration)
                    vmax_list.append(vmax)
                    type_list.append('Scenario C')
                    name_list.append('V3')
                    bus_list.append(BUS_NODE_LIST[line])

            penetration += 5

        # Formando dicionário
        data_max_dict = {"penetration": penetration_list, "vmax": vmax_list, "phase": name_list,
                         "scenarios": type_list, "bus": bus_list}
        # Formando dataframe
        hosting_capacity_max = pd.DataFrame.from_dict(data_max_dict)

        sns.scatterplot(data=hosting_capacity_max, x="penetration", y="vmax", style="phase", hue="scenarios", s=80)
        plt.xlabel('PV penetration [%]')
        plt.ylabel('Maximum voltage [pu]')
        plt.ylim([0.94, 1.15])
        plt.xlim([0, 100])
        plt.axhline(y=1.05, color='r', linestyle='-')
        plt.show()

        # Plot triplo
        penetration_v1 = []
        penetration_v2 = []
        penetration_v3 = []
        type_v1 = []
        type_v2 = []
        type_v3 = []
        vmax_v1 = []
        vmax_v2 = []
        vmax_v3 = []

        for n in range(len(hosting_capacity_max)):
            if hosting_capacity_max.iloc[n, 2] == 'V1':
                penetration_v1.append(hosting_capacity_max.iloc[n, 0])
                vmax_v1.append(hosting_capacity_max.iloc[n, 1])
                type_v1.append(hosting_capacity_max.iloc[n, 3])
            elif hosting_capacity_max.iloc[n, 2] == 'V2':
                penetration_v2.append(hosting_capacity_max.iloc[n, 0])
                vmax_v2.append(hosting_capacity_max.iloc[n, 1])
                type_v2.append(hosting_capacity_max.iloc[n, 3])
            elif hosting_capacity_max.iloc[n, 2] == 'V3':
                penetration_v3.append(hosting_capacity_max.iloc[n, 0])
                vmax_v3.append(hosting_capacity_max.iloc[n, 1])
                type_v3.append(hosting_capacity_max.iloc[n, 3])
        v1_dict = {"penetration": penetration_v1, "vmax": vmax_v1, "scenarios": type_v1}
        v2_dict = {"penetration": penetration_v2, "vmax": vmax_v2, "scenarios": type_v2}
        v3_dict = {"penetration": penetration_v3, "vmax": vmax_v3, "scenarios": type_v3}
        hosting_capacity_violation_v1 = pd.DataFrame.from_dict(v1_dict)
        hosting_capacity_violation_v2 = pd.DataFrame.from_dict(v2_dict)
        hosting_capacity_violation_v3 = pd.DataFrame.from_dict(v3_dict)
        fig, axes = plt.subplots(1, 3)
        axes[0].set_title('V1')
        axes[1].set_title('V2')
        axes[2].set_title('V3')
        g1 = sns.scatterplot(data=hosting_capacity_violation_v1, x="penetration", y="vmax", hue="scenarios", ax=axes[0])
        g1.legend_.set_title(None)
        g2 = sns.scatterplot(data=hosting_capacity_violation_v2, x="penetration", y="vmax", hue="scenarios", ax=axes[1])
        g2.legend_.set_title(None)
        g3 = sns.scatterplot(data=hosting_capacity_violation_v3, x="penetration", y="vmax", hue="scenarios", ax=axes[2])
        g3.legend_.set_title(None)
        axes[0].set_xlabel('PV penetration [%]')
        axes[0].set_ylabel('Maximum voltage magnitude [pu]')
        axes[0].axhline(y=1.05, color='r', linestyle='-')
        axes[0].set_ylim([0.94, 1.15])
        axes[0].set_xlim([0, 100])
        axes[1].set_xlabel('PV penetration [%]')
        axes[1].set_ylabel(' ')
        axes[1].axhline(y=1.05, color='r', linestyle='-')
        axes[1].set_ylim([0.94, 1.15])
        axes[1].yaxis.set_ticklabels([])
        axes[1].set_xlim([0, 100])
        axes[2].set_xlabel('PV penetration [%]')
        axes[2].set_ylabel(' ')
        axes[2].yaxis.set_ticklabels([])
        axes[2].axhline(y=1.05, color='r', linestyle='-')
        axes[2].set_ylim([0.94, 1.15])
        axes[2].set_xlim([0, 100])
        plt.show()

        # Boxplot
        hosting_capacity_violation_v1 = \
            hosting_capacity_violation_v1[~hosting_capacity_violation_v1['penetration'].
                isin(['5', '10', '15', '25', '30', '35', '45', '50', '55', '65', '70', '75', '85', '90', '95'])]
        hosting_capacity_violation_v2 = \
            hosting_capacity_violation_v2[~hosting_capacity_violation_v2['penetration'].
                isin(['5', '10', '15', '25', '30', '35', '45', '50', '55', '65', '70', '75', '85', '90', '95'])]
        hosting_capacity_violation_v3 = \
            hosting_capacity_violation_v3[~hosting_capacity_violation_v3['penetration'].
                isin(['5', '10', '15', '25', '30', '35', '45', '50', '55', '65', '70', '75', '85', '90', '95'])]

        fig, axes = plt.subplots(1, 3)
        axes[0].set_title('V1')
        axes[1].set_title('V2')
        axes[2].set_title('V3')
        g1 = sns.boxplot(data=hosting_capacity_violation_v1, x="penetration", y="vmax", hue="scenarios",
                         ax=axes[0], palette="Set2")
        g1.legend_.set_title(None)
        g2 = sns.boxplot(data=hosting_capacity_violation_v2, x="penetration", y="vmax", hue="scenarios",
                         ax=axes[1], palette="Set2")
        g2.legend_.set_title(None)
        g2.legend_.remove()
        g3 = sns.boxplot(data=hosting_capacity_violation_v3, x="penetration", y="vmax", hue="scenarios",
                         ax=axes[2], palette="Set2")
        g3.legend_.set_title(None)
        g3.legend_.remove()
        axes[0].set_xlabel('PV penetration [%]')
        axes[0].set_ylabel('Maximum voltage magnitude [pu]')
        axes[0].axhline(y=1.05, color='r', linestyle='-')
        axes[0].set_ylim([0.94, 1.15])
        axes[1].set_xlabel('PV penetration [%]')
        axes[1].set_ylabel(' ')
        axes[1].axhline(y=1.05, color='r', linestyle='-')
        axes[1].set_ylim([0.94, 1.15])
        axes[1].yaxis.set_ticklabels([])
        axes[2].set_xlabel('PV penetration [%]')
        axes[2].set_ylabel(' ')
        axes[2].yaxis.set_ticklabels([])
        axes[2].axhline(y=1.05, color='r', linestyle='-')
        axes[2].set_ylim([0.94, 1.15])
        plt.show()

        '''
        # Plot 3D
        print(hosting_capacity_max)
        sns.set(style='darkgrid')
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        y = hosting_capacity_max.iloc[:, 0]
        z = hosting_capacity_max.iloc[:, 1]
        x_aux = np.zeros(len(hosting_capacity_max))
        for n in range(len(hosting_capacity_max)):
            if hosting_capacity_max.iloc[n, 4] == "802":
                x_aux[n] = 1
            elif hosting_capacity_max.iloc[n, 4] == "806":
                x_aux[n] = 2
            elif hosting_capacity_max.iloc[n, 4] == "808":
                x_aux[n] = 3
            elif hosting_capacity_max.iloc[n, 4] == "810":
                x_aux[n] = 4
            elif hosting_capacity_max.iloc[n, 4] == "812":
                x_aux[n] = 5
            elif hosting_capacity_max.iloc[n, 4] == "814":
                x_aux[n] = 6
            elif hosting_capacity_max.iloc[n, 4] == "850":
                x_aux[n] = 7
            elif hosting_capacity_max.iloc[n, 4] == "818":
                x_aux[n] = 8
            elif hosting_capacity_max.iloc[n, 4] == "824":
                x_aux[n] = 9
            elif hosting_capacity_max.iloc[n, 4] == "820":
                x_aux[n] = 10
            elif hosting_capacity_max.iloc[n, 4] == "822":
                x_aux[n] = 11
            elif hosting_capacity_max.iloc[n, 4] == "826":
                x_aux[n] = 12
            elif hosting_capacity_max.iloc[n, 4] == "828":
                x_aux[n] = 13
            elif hosting_capacity_max.iloc[n, 4] == "830":
                x_aux[n] = 14
            elif hosting_capacity_max.iloc[n, 4] == "854":
                x_aux[n] = 15
            elif hosting_capacity_max.iloc[n, 4] == "858":
                x_aux[n] = 16
            elif hosting_capacity_max.iloc[n, 4] == "860":
                x_aux[n] = 17
            elif hosting_capacity_max.iloc[n, 4] == "842":
                x_aux[n] = 18
            elif hosting_capacity_max.iloc[n, 4] == "840":
                x_aux[n] = 19
            elif hosting_capacity_max.iloc[n, 4] == "862":
                x_aux[n] = 20
            elif hosting_capacity_max.iloc[n, 4] == "844":
                x_aux[n] = 21
            elif hosting_capacity_max.iloc[n, 4] == "846":
                x_aux[n] = 22
            elif hosting_capacity_max.iloc[n, 4] == "848":
                x_aux[n] = 23
            elif hosting_capacity_max.iloc[n, 4] == "816":
                x_aux[n] = 24
            elif hosting_capacity_max.iloc[n, 4] == "832":
                x_aux[n] = 25
            elif hosting_capacity_max.iloc[n, 4] == "856":
                x_aux[n] = 26
            elif hosting_capacity_max.iloc[n, 4] == "852":
                x_aux[n] = 27
            elif hosting_capacity_max.iloc[n, 4] == "864":
                x_aux[n] = 28
            elif hosting_capacity_max.iloc[n, 4] == "834":
                x_aux[n] = 29
            elif hosting_capacity_max.iloc[n, 4] == "836":
                x_aux[n] = 30
            elif hosting_capacity_max.iloc[n, 4] == "838":
                x_aux[n] = 31
            elif hosting_capacity_max.iloc[n, 4] == "890":
                x_aux[n] = 32
        x = x_aux
        print(x)
        print(y)
        print(z)
        ax.set_xlabel("bus")
        ax.set_ylabel("penetration")
        ax.set_zlabel("vmax")
        ax.scatter(x, y, z)
        plt.show()
        '''
