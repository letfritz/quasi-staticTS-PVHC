# ---------- BIBLIOTECAS ----------
import os
import sys

import pandas as pd

BUS_NODE_LIST = ["802", "806", "808", "810", "812", "814", "850", "818", "824", "820", "822", "826", "828", "830",
                 "854", "858", "860", "842", "840", "862", "844", "846", "848", "816", "832", "856", "852", "864",
                 "834", "836", "838", "890"]

# Dados de entrada para penetração vs frequência de violação
penetration_freq_list = []
bus_freq_list = []
type_freq_list = []
name_freq_list = []
freq_freq_list = []


class Outputfreq:
    def __init__(self):
        pass

    def get_freq_violation(self):

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

            df2_pv.drop(['3', '7', '9', '10', '11', '25', '27', '30'], axis=1, inplace=True)
            df2_hc.drop(['3', '7', '9', '10', '11', '25', '27', '30'], axis=1, inplace=True)
            df2_cs.drop(['3', '7', '9', '10', '11', '25', '27', '30'], axis=1, inplace=True)
            df3_pv.drop(['3', '4', '7', '9', '10', '11', '25', '27', '30'], axis=1, inplace=True)
            df3_hc.drop(['3', '4', '7', '9', '10', '11', '25', '27', '30'], axis=1, inplace=True)
            df3_cs.drop(['3', '4', '7', '9', '10', '11', '25', '27', '30'], axis=1, inplace=True)

            for line in range(df1_pv.shape[1]):
                count = 0
                for time in range(len(df1_pv)):
                    if df1_pv.iloc[time, line] > 1.05:
                        count += 1
                penetration_freq_list.append(penetration)
                bus_freq_list.append(BUS_NODE_LIST[line])
                freq_freq_list.append((count / len(df1_pv)) * 100)
                type_freq_list.append('none')
                name_freq_list.append('V1')

                count = 0
                for time in range(len(df1_hc)):
                    if df1_hc.iloc[time, line] > 1.05:
                        count += 1
                penetration_freq_list.append(penetration)
                bus_freq_list.append(BUS_NODE_LIST[line])
                freq_freq_list.append((count / len(df1_hc)) * 100)
                type_freq_list.append('home charging')
                name_freq_list.append('V1')

                count = 0
                for time in range(len(df1_cs)):
                    if df1_cs.iloc[time, line] > 1.05:
                        count += 1
                penetration_freq_list.append(penetration)
                bus_freq_list.append(BUS_NODE_LIST[line])
                freq_freq_list.append((count / len(df1_cs)) * 100)
                type_freq_list.append('charging station')
                name_freq_list.append('V1')

            for line in range(df2_pv.shape[1]):
                count = 0
                for time in range(len(df2_pv)):
                    if df2_pv.iloc[time, line] > 1.05:
                        count += 1
                penetration_freq_list.append(penetration)
                bus_freq_list.append(BUS_NODE_LIST[line])
                freq_freq_list.append((count / len(df2_pv)) * 100)
                type_freq_list.append('none')
                name_freq_list.append('V2')

                count = 0
                for time in range(len(df2_hc)):
                    if df2_hc.iloc[time, line] > 1.05:
                        count += 1
                penetration_freq_list.append(penetration)
                bus_freq_list.append(BUS_NODE_LIST[line])
                freq_freq_list.append((count / len(df2_hc)) * 100)
                type_freq_list.append('home charging')
                name_freq_list.append('V2')

                count = 0
                for time in range(len(df2_cs)):
                    if df2_cs.iloc[time, line] > 1.05:
                        count += 1
                penetration_freq_list.append(penetration)
                bus_freq_list.append(BUS_NODE_LIST[line])
                freq_freq_list.append((count / len(df2_cs)) * 100)
                type_freq_list.append('charging station')
                name_freq_list.append('V2')

            for line in range(df3_pv.shape[1]):
                count = 0
                for time in range(len(df3_pv)):
                    if df3_pv.iloc[time, line] > 1.05:
                        count += 1
                penetration_freq_list.append(penetration)
                bus_freq_list.append(BUS_NODE_LIST[line])
                freq_freq_list.append((count / len(df3_pv)) * 100)
                type_freq_list.append('none')
                name_freq_list.append('V3')

                count = 0
                for time in range(len(df3_hc)):
                    if df3_hc.iloc[time, line] > 1.05:
                        count += 1
                penetration_freq_list.append(penetration)
                bus_freq_list.append(BUS_NODE_LIST[line])
                freq_freq_list.append((count / len(df3_hc)) * 100)
                type_freq_list.append('home charging')
                name_freq_list.append('V3')

                count = 0
                for time in range(len(df3_cs)):
                    if df3_cs.iloc[time, line] > 1.05:
                        count += 1
                penetration_freq_list.append(penetration)
                bus_freq_list.append(BUS_NODE_LIST[line])
                freq_freq_list.append((count / len(df3_cs)) * 100)
                type_freq_list.append('charging station')
                name_freq_list.append('V3')
            penetration += 5

        return penetration_freq_list, bus_freq_list, freq_freq_list, type_freq_list, name_freq_list
