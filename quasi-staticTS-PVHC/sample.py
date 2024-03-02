# ---------- BIBLIOTECAS ----------
import numpy as np
import pandas as pd
import matplotlib.pylab as plt

# ---------- VARIAVEIS GLOBAIS ----------
# VARIAVEIS GLOBAIS PARA FDP
SD_LOAD, SD_PV = .05, .05
MU_EV, SD_EV = 3.2, 0.88
MU_EV_HOUR_ARRIVE, SD_EV_HOUR_A = (17.01 * 60), (3.2 * 60)  # [Wu, 2013], carro estaciona para carregar às 17:36
MU_EV_HOUR_DEPARTURE, SD_EV_HOUR_D = (9.97 * 60), (2.2 * 60)

# VARIAVEIS GLOBAIS PARA EV
EV_BATTERY_CAPACITY = 62  # 62[kWh] Nissan Leaf
EV_CONSUMPTION_KM = 62 / 350  # 350[kWh] Nissan Leaf
EV_CONSUMPTION_V2G = 0.5
EV_VOLTAGE = 127  # [V]
EV_CURRENT_CHARGE = 16  # [A]
EV_POWER_CHARGE = 3.6  # [kW]

# VARIAVEIS GLOBAIS DO CS
CS_POWER_CHARGE = 50  # [kW]
CS_MAX_CHARGE = 20  # máximo de carros que irão carregar durante o dia
CS_NUMBER_CHARGE = 10  # vagas para carregar ao mesmo tempo no CS
CS_HOUR_IN, CS_HOUR_OUT = (7 * 59), (20 * 60)


# FUNÇÃO DE ESTADO DA CARGA DO EV
def get_ev_soc():
    # Distribuição de probabilidade acumulativa da distância percorrida pelo carro (sorteio de quanto vai andar no dia)
    dist = np.random.lognormal(MU_EV, SD_EV)

    # Estado da carga da bateria mínimo (o SOC não pode ter menos que 20% em momento algum)
    # O SOC não deve ser menor que o SOC_min, durante o período de descarga
    soc_min = 0.2

    # Energia necessária para usar o carro no dia
    soc_needed_dest = dist * EV_CONSUMPTION_KM / EV_BATTERY_CAPACITY

    # Estado de carga da bateria antes de descarregar (soc minímo e 1)
    soc_init_0 = np.random.uniform(soc_min, 1)

    return soc_min, soc_needed_dest, soc_init_0


class Sample:
    def __init__(self, load, pv, ev_max_connection):
        self.load = pd.DataFrame(load)
        self.pv = pv
        self.ev_max_connection = ev_max_connection

    # AMOSTRA DE CURVA DE CARGA
    def get_load_sample(self, bus):
        load = {}
        for n in range(bus):
            load_sample_aux = np.zeros(1440)
            for hour in range(1440):
                # distribuição normal [Morshed, 2018]  [Unidade: kWh]
                load_sample_aux[hour] = np.random.normal(self.load.iloc[hour, n],
                                                         (self.load.iloc[hour, n] * SD_LOAD))
            load[n] = load_sample_aux

        return load

    # AMOSTRA DE CURVA PV
    def get_pv_sample(self, bus):
        pv_sample = {}
        for n in range(bus):
            pv_sample_aux = np.zeros(1440)
            for hour in range(1440):
                pv_sample_aux[hour] = np.random.normal(float(self.pv.iloc[hour, 0]),
                                                       (abs(float(self.pv.iloc[hour, 0])) * SD_PV))
            pv_sample[n] = pv_sample_aux

        return pv_sample

    # AMOSTRA DE CURVA EV RESIDENCIAL
    def get_ev_sample(self, bus):
        ev_curve = {}
        ev_curve_cs = {}
        ev_power = {}
        ev_power_aux = 0
        ev_incoming = [0] * bus
        ev_t_duration = []
        ev_t_time_total = [0] * (24 * 60)
        ev_soc_init = {}

        # Organizando vetor de escolha do carro nas barras do grupo A: 802, 806, 808, 810, 812, 814, 850, 816, 818,
        # 820, 822, 824, 828, 826
        ev_incoming_bus_a = [8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 17, 19, 20, 21, 22, 23, 24]
        # Organizando vetor de escolha do carro nas barras do grupo B: 848, 846, 844, 842, 864, 858, 834
        ev_incoming_bus_b = [2, 3, 29, 31, 33, 34, 36, 38, 40, 45, 47, 49, 51, 52, 54, 56, 60, 61, 62, 63, 64, 65, 66,
                           67]
        # Organizando vetor de escolha do carro nas barras do grupo C: 830, 854, 856, 852, 832, 858, 834, 860, 836,
        # 840, 862, 838, 888, 890
        ev_incoming_bus_c = [0, 1, 4, 5, 6, 7, 25, 26, 27, 28, 30, 32, 29, 31, 33, 34, 36, 38, 40, 37, 39, 41, 42, 43,
                             44, 45, 46, 47, 48, 49, 50, 52, 51, 53, 54, 55, 56, 57, 58, 59]

        count_cs_a = 0
        residual_cs_a = CS_MAX_CHARGE - len(ev_incoming_bus_a)
        count_cs_b = 0
        residual_cs_b = CS_MAX_CHARGE - len(ev_incoming_bus_b)
        count_cs_c = 0
        residual_cs_c = CS_MAX_CHARGE - len(ev_incoming_bus_c)

        for bus_i in range(bus):
            # Quantidade de EV
            ev_curve_aux = [0] * (24 * 60)
            ev_curve_aux_cs = [0] * (24 * 60)
            ev_incoming[bus_i] = self.ev_max_connection[bus_i]
            ev_hc_charge = np.ones(ev_incoming[bus_i])
            # Verificando grupo A
            if bus_i in ev_incoming_bus_a and count_cs_a < CS_MAX_CHARGE:
                ev_hc_charge[0] = 0
                count_cs_a += 1
                if residual_cs_a > 0:
                    ev_hc_charge[1] = 0
                    count_cs_a += 1
                    residual_cs_a -= 1

            # Verificando grupo B
            if bus_i in ev_incoming_bus_b and count_cs_b < CS_MAX_CHARGE:
                ev_hc_charge[0] = 0
                count_cs_b += 1
                if residual_cs_b > 0:
                    ev_hc_charge[1] = 0
                    count_cs_b += 1
                    residual_cs_b -= 1

            # Verificando grupo C
            if bus_i in ev_incoming_bus_c and count_cs_c < CS_MAX_CHARGE:
                ev_hc_charge[0] = 0
                count_cs_c += 1
                if residual_cs_c > 0:
                    ev_hc_charge[1] = 0
                    count_cs_c += 1
                    residual_cs_c -= 1

            # print("ev_incoming", ev_incoming[bus_i])
            ev_soc_bus = []
            for ev_i in range(ev_incoming[bus_i]):
                # SOC do veículo elétrico
                soc_min, soc_needed_dest, soc_init_0 = get_ev_soc()

                # Armazenando o soc inicial
                ev_soc_bus.append(soc_init_0)
                # print("soc", ev_soc_bus)

                # Estimando tempos de chegada e saída da residência
                t_start_charge = int(np.random.normal(MU_EV_HOUR_ARRIVE, SD_EV_HOUR_A))
                while t_start_charge > (24 * 60):
                    t_start_charge = int(np.random.normal(MU_EV_HOUR_ARRIVE, SD_EV_HOUR_A))
                t_stop_charge = int(np.random.normal(MU_EV_HOUR_DEPARTURE, SD_EV_HOUR_D))
                while t_stop_charge < 0 or t_stop_charge > t_start_charge:
                    t_stop_charge = int(np.random.normal(MU_EV_HOUR_DEPARTURE, SD_EV_HOUR_D))
                # print("t_start_charge", t_start_charge)
                # print("t_stop_charge", t_stop_charge)
                ev_t_time = [1] * t_stop_charge
                # print("ev_t_time1", len(ev_t_time))
                ev_t_time.extend([0] * (t_start_charge - t_stop_charge))
                # print("ev_t_time0", len(ev_t_time))
                ev_t_time.extend([1] * ((24 * 60) - len(ev_t_time)))
                # print(ev_t_time)
                # print("ev_t_time", len(ev_t_time))

                # Sorteio se carrega de manhã ou não
                ev_status = np.random.randint(0, 2)
                # print("ev_status", ev_status)

                # Estimando carregamento antes da saída
                t_duration_charge_0 = int(((1 - soc_init_0) * EV_BATTERY_CAPACITY / EV_POWER_CHARGE) * 60)
                t_duration_charge = 0
                ev_t_duration.append(t_duration_charge_0)
                soc_charge_0 = soc_init_0 + ((t_duration_charge_0 / 60) * EV_POWER_CHARGE / EV_BATTERY_CAPACITY)

                if soc_charge_0 < (soc_min + soc_needed_dest):
                    # Estado em que o carro não sai de casa e continua carregando
                    curve = [EV_POWER_CHARGE] * t_duration_charge_0
                    curve.extend([0] * ((24 * 60) - len(curve)))
                else:
                    # Estado em que o carro sai de casa
                    if t_duration_charge_0 > t_stop_charge:
                        t_duration_charge_0 = t_stop_charge
                    # print("t_duration_charge_0", t_duration_charge_0)
                    if ev_status == 0:
                        curve = [0] * t_duration_charge_0
                    else:
                        curve = [EV_POWER_CHARGE] * t_duration_charge_0
                    # print(curve)
                    # print(len(curve))
                    curve.extend([0] * (t_stop_charge - len(curve)))
                    # print(curve)
                    # print(len(curve))
                    # Estimando soc de chegada
                    # print("soc_init_0", soc_init_0)
                    # print("soc_charge_0", soc_charge_0)
                    # print("soc_needed_dest", soc_needed_dest)
                    soc_arrival = soc_charge_0 - soc_needed_dest
                    # print("soc_arrival", soc_arrival)

                    # Estimando tempo de recarga
                    t_duration_charge = int(((1 - soc_arrival) * EV_BATTERY_CAPACITY / EV_POWER_CHARGE) * 60)
                    ev_t_duration.append(t_duration_charge)
                    # print("t_duration_charge", t_duration_charge)
                    ev_t_duration.append(t_duration_charge)

                    # Período fora da residência
                    curve.extend([0] * (t_start_charge - t_stop_charge))
                    # print(curve)
                    # print(len(curve))

                    # Período carregando
                    curve.extend([EV_POWER_CHARGE] * t_duration_charge)
                    if len(curve) < (24 * 60):
                        curve.extend([0] * ((24 * 60) - len(curve)))
                    else:
                        curve = curve[0:(24 * 60)]

                    # print(curve)
                    # print(len(curve))
                # Energia do carro
                energy = sum(curve) / 60
                ev_power_aux = energy / (t_duration_charge + t_duration_charge_0)
                ev_curve_aux += np.asarray(curve)
                # Verificando se no modo CS o carro vai carregar em casa
                if ev_hc_charge[ev_i] == 1:
                    ev_curve_aux_cs += np.asarray(curve)
                ev_t_time_total += np.asarray(ev_t_time)
                # print("ev_t_time_total", len(ev_t_time_total))
                # print("ev_curve_aux", ev_curve_aux)
                ##plt.plot(range(1440), curve)
                ##plt.show()
            ev_soc_init[bus_i] = ev_soc_bus
            # plt.plot(range(len(ev_soc_bus)), ev_soc_bus)
            # plt.show()
            ev_curve[bus_i] = ev_curve_aux
            ev_curve_cs[bus_i] = ev_curve_aux_cs
            ev_power[bus_i] = ev_power_aux
            # plt.plot(range(1440), ev_curve_aux)
            # plt.plot(range(1440), ev_curve_aux_cs)
            # plt.show()

        return ev_curve, ev_curve_cs, ev_soc_init

    # AMOSTRA DE CURVA CS
    def get_cs_sample(self, ev_soc_init, case):
        ev_curve_aux = [0] * (24 * 60)
        ev_t_duration = []
        # Quantidade de EV
        ev_incoming = CS_MAX_CHARGE
        # Organizando vetor de escolha do carro nas barras do grupo A: 802, 806, 808, 810, 812, 814, 850, 816, 818,
        # 820, 822, 824, 828, 826
        ev_incoming_bus_a = [8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 17, 19, 20, 21, 22, 23, 24]
        # Organizando vetor de escolha do carro nas barras do grupo B: 848, 846, 844, 842, 864, 858, 834
        ev_incoming_bus_b = [2, 3, 29, 31, 33, 34, 36, 38, 40, 45, 47, 49, 51, 52, 54, 56, 60, 61, 62, 63, 64, 65, 66,
                             67]
        # Organizando vetor de escolha do carro nas barras do grupo C: 830, 854, 856, 852, 832, 858, 834, 860, 836,
        # 840, 862, 838, 888, 890
        ev_incoming_bus_c = [0, 1, 4, 5, 6, 7, 25, 26, 27, 28, 30, 32, 29, 31, 33, 34, 36, 38, 40, 37, 39, 41, 42, 43,
                             44, 45, 46, 47, 48, 49, 50, 52, 51, 53, 54, 55, 56, 57, 58, 59]
        if case == 'a':
            ev_incoming_bus = ev_incoming_bus_a
        elif case == 'b':
            ev_incoming_bus = ev_incoming_bus_b
        elif case == 'c':
            ev_incoming_bus = ev_incoming_bus_c
        ev_incoming_soc = []
        count = 0
        count_ev = 0
        for n in range(ev_incoming):
            car = ev_soc_init[ev_incoming_bus[count]][count_ev]
            ev_incoming_soc.append(car)
            count += 1
            if count >= len(ev_incoming_bus):
                count = 0
                count_ev += 1

        for ev_i in range(ev_incoming):
            ev_mu_choice = np.random.randint(0, 3)
            if ev_mu_choice == 0:
                ev_mu = 8 * 60
            elif ev_mu_choice == 1:
                ev_mu = 12 * 60
            elif ev_mu_choice == 2:
                ev_mu = 18 * 60
            t_ev_arrive = np.random.normal(ev_mu, 30)

            if t_ev_arrive < CS_HOUR_IN:
                t_ev_arrive = CS_HOUR_IN
            elif t_ev_arrive > (CS_HOUR_OUT - 30):
                t_ev_arrive = CS_HOUR_OUT - 30
            t_ev_arrive = int(t_ev_arrive)

            # Verificando limite de vagas
            if (ev_curve_aux[t_ev_arrive] / CS_POWER_CHARGE) > (CS_NUMBER_CHARGE - 1):
                t_wait = t_ev_arrive + 1
                while (ev_curve_aux[t_wait] / CS_POWER_CHARGE) > (CS_NUMBER_CHARGE - 1):
                    t_wait += 1
                t_ev_arrive = t_wait

            # Estado de carga da bateria chegando no posto (mesmo utilizado no HC)
            soc_init = ev_incoming_soc[ev_i]

            # Tempo de recarga
            t_duration_charge = int(((1 - soc_init) * EV_BATTERY_CAPACITY / CS_POWER_CHARGE) * 60)

            # Construindo curva
            curve = [0] * t_ev_arrive
            curve.extend([CS_POWER_CHARGE] * t_duration_charge)
            if len(curve) < (20 * 60):
                curve.extend([0] * ((24 * 60) - len(curve)))
            else:
                curve = curve[(20 * 60):]
                curve.extend([0] * ((24 * 60) - len(curve)))
            ev_curve_aux += np.asarray(curve[0:(24 * 60)])
            # plt.plot(range(1440), curve)
            # plt.show()

        ev_curve = ev_curve_aux
        # print(ev_curve)
        # plt.plot(range(1440), ev_curve)
        # plt.show()

        return ev_curve
