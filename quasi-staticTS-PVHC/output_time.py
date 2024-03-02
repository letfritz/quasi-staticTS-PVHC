# ---------- BIBLIOTECAS ----------
import os
import sys

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

BUS_NODE_LIST = ["802", "806", "808", "810", "812", "814", "850", "818", "824", "820", "822", "826", "828", "830",
                 "854", "858", "860", "842", "840", "862", "844", "846", "848", "816", "832", "856", "852", "864",
                 "834", "836", "838", "890"]
BUS_LIST = ["802.1.2.3", "806.1.2.3", "808.1.2.3", "810.2", "812.1.2.3", "814.1.2.3", "850.1.2.3", "818.1",
            "824.1.2.3", "820.1", "822.1", "826.2", "828.1.2.3", "830.1.2.3", "854.1.2.3", "858.1.2.3", "860.1.2.3",
            "842.1.2.3", "840.1.2.3", "862.1.2.3", "844.1.2.3", "846.1.2.3", "848.1.2.3", "816.1.2.3", "832.1.2.3",
            "856.2", "852.1.2.3", "864.1", "834.1.2.3", "836.1.2.3", "838.2", "890.1.2.3"]


class Outputtime:
    def __init__(self, simulation_number):
        self.simulation_number = simulation_number

    def get_more_than_15(self, df, line, freq):
        df = pd.DataFrame(df.iloc[freq * 1440:(freq * 1440 + 1440), :])
        violation = np.zeros(len(df))
        for n in range(len(violation)):
            if df.iloc[n, line] > 1.05:
                if n == 0:
                    violation[n] = 1
                else:
                    violation[n] = violation[n - 1] + 1
            else:
                violation[n] = 0

        count_violation = 0
        for time in range(len(violation)):
            if violation[time] == 15:
                count_violation += 1

        return count_violation

    def get_time_violation(self):
        # Dados de entrada para penetração vs tempo de violação
        penetration_time_list = []
        bus_time_list = []
        type_time_list = []
        name_time_list = []
        freq_time_list = []

        penetration = 0

        for file in range(21):
            print("Penetração", penetration, "em andamento")
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

            # df2_pv.drop(['3', '7', '9', '10', '11', '25', '27', '30'], axis=1, inplace=True)
            # df2_hc.drop(['3', '7', '9', '10', '11', '25', '27', '30'], axis=1, inplace=True)
            # df2_cs.drop(['3', '7', '9', '10', '11', '25', '27', '30'], axis=1, inplace=True)
            # df3_pv.drop(['3', '4', '7', '9', '10', '11', '25', '27', '30'], axis=1, inplace=True)
            # df3_hc.drop(['3', '4', '7', '9', '10', '11', '25', '27', '30'], axis=1, inplace=True)
            # df3_cs.drop(['3', '4', '7', '9', '10', '11', '25', '27', '30'], axis=1, inplace=True)

            for line in range(df1_pv.shape[1]):
                if ".1" in BUS_LIST[line]:
                    # ----- V1 -----
                    for freq in range(self.simulation_number):
                        # none
                        count = self.get_more_than_15(df1_pv, line, freq)
                        penetration_time_list.append(penetration)
                        bus_time_list.append(BUS_NODE_LIST[line])
                        freq_time_list.append(count)
                        type_time_list.append('none')
                        name_time_list.append('V1')
                        # home charging
                        count = self.get_more_than_15(df1_hc, line, freq)
                        penetration_time_list.append(penetration)
                        bus_time_list.append(BUS_NODE_LIST[line])
                        freq_time_list.append(count)
                        type_time_list.append('home charging')
                        name_time_list.append('V1')
                        # charging station
                        count = self.get_more_than_15(df1_cs, line, freq)
                        penetration_time_list.append(penetration)
                        bus_time_list.append(BUS_NODE_LIST[line])
                        freq_time_list.append(count)
                        type_time_list.append('charging station')
                        name_time_list.append('V1')
            for line in range(df2_pv.shape[1]):
                if ".1.2" in BUS_LIST[line]:
                    # ----- V2 -----
                    for freq in range(self.simulation_number):
                        # none
                        count = self.get_more_than_15(df2_pv, line, freq)
                        penetration_time_list.append(penetration)
                        bus_time_list.append(BUS_NODE_LIST[line])
                        freq_time_list.append(count)
                        type_time_list.append('none')
                        name_time_list.append('V2')
                        # home charging
                        count = self.get_more_than_15(df2_hc, line, freq)
                        penetration_time_list.append(penetration)
                        bus_time_list.append(BUS_NODE_LIST[line])
                        freq_time_list.append(count)
                        type_time_list.append('home charging')
                        name_time_list.append('V2')
                        # charging station
                        count = self.get_more_than_15(df2_cs, line, freq)
                        penetration_time_list.append(penetration)
                        bus_time_list.append(BUS_NODE_LIST[line])
                        freq_time_list.append(count)
                        type_time_list.append('charging station')
                        name_time_list.append('V2')
                elif ".2" in BUS_LIST[line]:
                    # ----- V2 -----
                    for freq in range(self.simulation_number):
                        # none
                        count = self.get_more_than_15(df1_pv, line, freq)
                        penetration_time_list.append(penetration)
                        bus_time_list.append(BUS_NODE_LIST[line])
                        freq_time_list.append(count)
                        type_time_list.append('none')
                        name_time_list.append('V2')
                        # home charging
                        count = self.get_more_than_15(df1_hc, line, freq)
                        penetration_time_list.append(penetration)
                        bus_time_list.append(BUS_NODE_LIST[line])
                        freq_time_list.append(count)
                        type_time_list.append('home charging')
                        name_time_list.append('V2')
                        # charging station
                        count = self.get_more_than_15(df1_cs, line, freq)
                        penetration_time_list.append(penetration)
                        bus_time_list.append(BUS_NODE_LIST[line])
                        freq_time_list.append(count)
                        type_time_list.append('charging station')
                        name_time_list.append('V2')

            for line in range(df3_pv.shape[1]):
                if ".1.2.3" in BUS_LIST[line]:
                    # ----- V3 -----
                    for freq in range(self.simulation_number):
                        # none
                        count = self.get_more_than_15(df3_pv, line, freq)
                        penetration_time_list.append(penetration)
                        bus_time_list.append(BUS_NODE_LIST[line])
                        freq_time_list.append(count)
                        type_time_list.append('none')
                        name_time_list.append('V3')
                        # home charging
                        count = self.get_more_than_15(df3_hc, line, freq)
                        penetration_time_list.append(penetration)
                        bus_time_list.append(BUS_NODE_LIST[line])
                        freq_time_list.append(count)
                        type_time_list.append('home charging')
                        name_time_list.append('V3')
                        # charging station
                        count = self.get_more_than_15(df3_cs, line, freq)
                        penetration_time_list.append(penetration)
                        bus_time_list.append(BUS_NODE_LIST[line])
                        freq_time_list.append(count)
                        type_time_list.append('charging station')
                        name_time_list.append('V3')
                elif ".2.3" in BUS_LIST[line] or ".1.3" in BUS_LIST[line]:
                    # ----- V3 -----
                    for freq in range(self.simulation_number):
                        # none
                        count = self.get_more_than_15(df2_pv, line, freq)
                        penetration_time_list.append(penetration)
                        bus_time_list.append(BUS_NODE_LIST[line])
                        freq_time_list.append(count)
                        type_time_list.append('none')
                        name_time_list.append('V3')
                        # home charging
                        count = self.get_more_than_15(df2_hc, line, freq)
                        penetration_time_list.append(penetration)
                        bus_time_list.append(BUS_NODE_LIST[line])
                        freq_time_list.append(count)
                        type_time_list.append('home charging')
                        name_time_list.append('V3')
                        # charging station
                        count = self.get_more_than_15(df2_cs, line, freq)
                        penetration_time_list.append(penetration)
                        bus_time_list.append(BUS_NODE_LIST[line])
                        freq_time_list.append(count)
                        type_time_list.append('charging station')
                        name_time_list.append('V3')
                elif ".3" in BUS_LIST[line]:
                    # ----- V3 -----
                    for freq in range(self.simulation_number):
                        # none
                        count = self.get_more_than_15(df1_pv, line, freq)
                        penetration_time_list.append(penetration)
                        bus_time_list.append(BUS_NODE_LIST[line])
                        freq_time_list.append(count)
                        type_time_list.append('none')
                        name_time_list.append('V3')
                        # home charging
                        count = self.get_more_than_15(df1_hc, line, freq)
                        penetration_time_list.append(penetration)
                        bus_time_list.append(BUS_NODE_LIST[line])
                        freq_time_list.append(count)
                        type_time_list.append('home charging')
                        name_time_list.append('V3')
                        # charging station
                        count = self.get_more_than_15(df1_cs, line, freq)
                        penetration_time_list.append(penetration)
                        bus_time_list.append(BUS_NODE_LIST[line])
                        freq_time_list.append(count)
                        type_time_list.append('charging station')
                        name_time_list.append('V3')

            penetration += 5

        data_time_penetration_dict = {"penetration": penetration_time_list,
                                      "freq": freq_time_list,
                                      "phase": name_time_list,
                                      "type": type_time_list,
                                      "bus": bus_time_list}
        hosting_capacity_violation = pd.DataFrame.from_dict(data_time_penetration_dict)
        hosting_capacity_violation.to_csv('voltage_violation.csv', index=False)

    def get_vmax_violation(self, penetration):
        # Dados de entrada para penetração vs tempo de violação
        penetration_time_v1_list = []
        type_time_v1_list = []
        name_time_v1_list = []
        vmax_time_v1_list = []
        penetration_time_v2_list = []
        type_time_v2_list = []
        name_time_v2_list = []
        vmax_time_v2_list = []
        penetration_time_v3_list = []
        type_time_v3_list = []
        name_time_v3_list = []
        vmax_time_v3_list = []

        print("Penetração", penetration, "em andamento")
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

        for line in range(df1_pv.shape[1]):
            if ".1" in BUS_LIST[line]:
                # ----- V1 -----
                # none
                penetration_time_v1_list.extend([penetration] * 1440 * self.simulation_number)
                vmax_time_v1_list.extend(df1_pv.iloc[0:1440 * self.simulation_number, line])
                type_time_v1_list.extend(['none'] * 1440 * self.simulation_number)
                name_time_v1_list.extend(['V1'] * 1440 * self.simulation_number)
                # home charging
                penetration_time_v1_list.extend([penetration] * 1440 * self.simulation_number)
                vmax_time_v1_list.extend(df1_hc.iloc[0:1440 * self.simulation_number, line])
                type_time_v1_list.extend(['home charging'] * 1440 * self.simulation_number)
                name_time_v1_list.extend(['V1'] * 1440 * self.simulation_number)
                # charging station
                penetration_time_v1_list.extend([penetration] * 1440 * self.simulation_number)
                vmax_time_v1_list.extend(df1_cs.iloc[0:1440 * self.simulation_number, line])
                type_time_v1_list.extend(['charging station'] * 1440 * self.simulation_number)
                name_time_v1_list.extend(['V1'] * 1440 * self.simulation_number)
        for line in range(df2_pv.shape[1]):
            if ".1.2" in BUS_LIST[line]:
                # ----- V2 -----
                # none
                penetration_time_v2_list.extend([penetration] * 1440 * self.simulation_number)
                vmax_time_v2_list.extend(df2_pv.iloc[0:1440 * self.simulation_number, line])
                type_time_v2_list.extend(['none'] * 1440 * self.simulation_number)
                name_time_v2_list.extend(['V2'] * 1440 * self.simulation_number)
                # home charging
                penetration_time_v2_list.extend([penetration] * 1440 * self.simulation_number)
                vmax_time_v2_list.extend(df2_hc.iloc[0:1440 * self.simulation_number, line])
                type_time_v2_list.extend(['home charging'] * 1440 * self.simulation_number)
                name_time_v2_list.extend(['V2'] * 1440 * self.simulation_number)
                # charging station
                penetration_time_v2_list.extend([penetration] * 1440 * self.simulation_number)
                vmax_time_v2_list.extend(df2_cs.iloc[0:1440 * self.simulation_number, line])
                type_time_v2_list.extend(['charging station'] * 1440 * self.simulation_number)
                name_time_v2_list.extend(['V2'] * 1440 * self.simulation_number)
            elif ".2" in BUS_LIST[line]:
                # ----- V2 -----
                # none
                penetration_time_v2_list.extend([penetration] * 1440 * self.simulation_number)
                vmax_time_v2_list.extend(df1_pv.iloc[0:1440 * self.simulation_number, line])
                type_time_v2_list.extend(['none'] * 1440 * self.simulation_number)
                name_time_v2_list.extend(['V2'] * 1440 * self.simulation_number)
                # home charging
                penetration_time_v2_list.extend([penetration] * 1440 * self.simulation_number)
                vmax_time_v2_list.extend(df1_hc.iloc[0:1440 * self.simulation_number, line])
                type_time_v2_list.extend(['home charging'] * 1440 * self.simulation_number)
                name_time_v2_list.extend(['V2'] * 1440 * self.simulation_number)
                # charging station
                penetration_time_v2_list.extend([penetration] * 1440 * self.simulation_number)
                vmax_time_v2_list.extend(df1_cs.iloc[0:1440 * self.simulation_number, line])
                type_time_v2_list.extend(['charging station'] * 1440 * self.simulation_number)
                name_time_v2_list.extend(['V2'] * 1440 * self.simulation_number)
        for line in range(df3_pv.shape[1]):
            if ".1.2.3" in BUS_LIST[line]:
                # ----- V3 -----
                # none
                penetration_time_v3_list.extend([penetration] * 1440 * self.simulation_number)
                vmax_time_v3_list.extend(df3_pv.iloc[0:1440 * self.simulation_number, line])
                type_time_v3_list.extend(['none'] * 1440 * self.simulation_number)
                name_time_v3_list.extend(['V3'] * 1440 * self.simulation_number)
                # home charging
                penetration_time_v3_list.extend([penetration] * 1440 * self.simulation_number)
                vmax_time_v3_list.extend(df3_hc.iloc[0:1440 * self.simulation_number, line])
                type_time_v3_list.extend(['home charging'] * 1440 * self.simulation_number)
                name_time_v3_list.extend(['V3'] * 1440 * self.simulation_number)
                # charging station
                penetration_time_v3_list.extend([penetration] * 1440 * self.simulation_number)
                vmax_time_v3_list.extend(df3_cs.iloc[0:1440 * self.simulation_number, line])
                type_time_v3_list.extend(['charging station'] * 1440 * self.simulation_number)
                name_time_v3_list.extend(['V3'] * 1440 * self.simulation_number)
            elif ".2.3" in BUS_LIST[line] or ".1.3" in BUS_LIST[line]:
                # ----- V3 -----
                # none
                penetration_time_v3_list.extend([penetration] * 1440 * self.simulation_number)
                vmax_time_v3_list.extend(df2_pv.iloc[0:1440 * self.simulation_number, line])
                type_time_v3_list.extend(['none'] * 1440 * self.simulation_number)
                name_time_v3_list.extend(['V3'] * 1440 * self.simulation_number)
                # home charging
                penetration_time_v3_list.extend([penetration] * 1440 * self.simulation_number)
                vmax_time_v3_list.extend(df2_hc.iloc[0:1440 * self.simulation_number, line])
                type_time_v3_list.extend(['home charging'] * 1440 * self.simulation_number)
                name_time_v3_list.extend(['V3'] * 1440 * self.simulation_number)
                # charging station
                penetration_time_v3_list.extend([penetration] * 1440 * self.simulation_number)
                vmax_time_v3_list.extend(df2_cs.iloc[0:1440 * self.simulation_number, line])
                type_time_v3_list.extend(['charging station'] * 1440 * self.simulation_number)
                name_time_v3_list.extend(['V3'] * 1440 * self.simulation_number)
            elif ".3" in BUS_LIST[line]:
                # ----- V3 -----
                # none
                penetration_time_v3_list.extend([penetration] * 1440 * self.simulation_number)
                vmax_time_v3_list.extend(df1_pv.iloc[0:1440 * self.simulation_number, line])
                type_time_v3_list.extend(['none'] * 1440 * self.simulation_number)
                name_time_v3_list.extend(['V3'] * 1440 * self.simulation_number)
                # home charging
                penetration_time_v3_list.extend([penetration] * 1440 * self.simulation_number)
                vmax_time_v3_list.extend(df1_hc.iloc[0:1440 * self.simulation_number, line])
                type_time_v3_list.extend(['home charging'] * 1440 * self.simulation_number)
                name_time_v3_list.extend(['V3'] * 1440 * self.simulation_number)
                # charging station
                penetration_time_v3_list.extend([penetration] * 1440 * self.simulation_number)
                vmax_time_v3_list.extend(df1_cs.iloc[0:1440 * self.simulation_number, line])
                type_time_v3_list.extend(['charging station'] * 1440 * self.simulation_number)
                name_time_v3_list.extend(['V3'] * 1440 * self.simulation_number)

        data_vmax_penetration_v1_dict = {"penetration": penetration_time_v1_list,
                                         "vmax": vmax_time_v1_list,
                                         "phase": name_time_v1_list,
                                         "type": type_time_v1_list}
        data_vmax_penetration_v2_dict = {"penetration": penetration_time_v2_list,
                                         "vmax": vmax_time_v2_list,
                                         "phase": name_time_v2_list,
                                         "type": type_time_v2_list}
        data_vmax_penetration_v3_dict = {"penetration": penetration_time_v3_list,
                                         "vmax": vmax_time_v3_list,
                                         "phase": name_time_v3_list,
                                         "type": type_time_v3_list}
        hosting_capacity_max_v1_violation = pd.DataFrame.from_dict(data_vmax_penetration_v1_dict)
        hosting_capacity_max_v2_violation = pd.DataFrame.from_dict(data_vmax_penetration_v2_dict)
        hosting_capacity_max_v3_violation = pd.DataFrame.from_dict(data_vmax_penetration_v3_dict)
        hosting_capacity_max_v1_violation.to_csv('voltage_max_v1_violation.csv', index=False)
        hosting_capacity_max_v2_violation.to_csv('voltage_max_v2_violation.csv', index=False)
        hosting_capacity_max_v3_violation.to_csv('voltage_max_v3_violation.csv', index=False)

        return hosting_capacity_max_v1_violation, hosting_capacity_max_v2_violation, \
               hosting_capacity_max_v3_violation
