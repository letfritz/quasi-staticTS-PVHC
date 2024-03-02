import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
#plt.rcParams['axes.facecolor'] = 'white'
sns.set_theme(style="whitegrid")
sns.set(font_scale=1.5)
sns.set_style("whitegrid")
#plt.rcParams['axes.facecolor'] = 'white'
#font = {'weight': 'normal',
#        'size': 18}

#matplotlib.rc('font', **font)
'''
# log normal
dist = []
case = []
for n in range(1000000):
    dist.append(np.random.lognormal(0, 0.25))
    case.append('m=0, sd=0.25')
for n in range(1000000):
    dist.append(np.random.lognormal(0, 0.50))
    case.append('m=0, sd=0.5')
for n in range(1000000):
    dist.append(np.random.lognormal(0, 1))
    case.append('m=0, sd=1.0')
dist_dict = {"dist": dist, "case": case}
ev_arrival = pd.DataFrame.from_dict(dist_dict)

sns.displot(ev_arrival, x="dist", kind="kde", linewidth=2, hue="case")
plt.xlim(-1, 5)
plt.xlabel("x")
plt.ylabel("PDF")
plt.show()

# gaussiana
dist = []
case = []
for n in range(1000000):
    dist.append(np.random.normal(0, 0.25))
    case.append('m=0, sd=0.25')
for n in range(1000000):
    dist.append(np.random.normal(0, 0.50))
    case.append('m=0, sd=0.5')
for n in range(1000000):
    dist.append(np.random.normal(0, 1))
    case.append('m=0, sd=1.0')
dist_dict = {"dist": dist, "case": case}
ev_arrival = pd.DataFrame.from_dict(dist_dict)

sns.displot(ev_arrival, x="dist", kind="kde", linewidth=2, hue="case")
plt.xlim(-3, 3)
plt.xlabel("x")
plt.ylabel("PDF")
plt.show()

# beta
dist = []
case = []
for n in range(1000000):
    dist.append(np.random.beta(2, 8))
    case.append('a=2.0, b=8.0')
for n in range(1000000):
    dist.append(np.random.beta(5, 5))
    case.append('a=5.0, b=5.0')
for n in range(1000000):
    dist.append(np.random.beta(8, 2))
    case.append('a=8.0, b=2.0')
dist_dict = {"dist": dist, "case": case}
ev_arrival = pd.DataFrame.from_dict(dist_dict)

sns.displot(ev_arrival, x="dist", kind="kde", linewidth=2, hue="case")
plt.xlim(0, 1)
plt.xlabel("x")
plt.ylabel("PDF")
plt.show()

'''

t_ev_arrive = []
t_type = []
for n in range(100000):
    # CS
    ev_mu_choice = np.random.randint(0, 3)
    if ev_mu_choice == 0:
        ev_mu = 8 * 60
    elif ev_mu_choice == 1:
        ev_mu = 12 * 60
    elif ev_mu_choice == 2:
        ev_mu = 18 * 60
    sorteio = np.random.normal(ev_mu, 30)
    t_ev_arrive.append(sorteio)
    t_type.append('CS')

    # Arrival
    t_start_charge = int(np.random.normal(17.01 * 60, 3.2 * 60))
    t_ev_arrive.append(t_start_charge)
    t_type.append('Arrival')
    # Departure
    t_stop_charge = int(np.random.normal(9.97 * 60, 2.2 * 60))
    t_ev_arrive.append(t_stop_charge)
    t_type.append('Departure')

ev_arrival_dict = {"time [min]": t_ev_arrive, "type": t_type}
ev_arrival = pd.DataFrame.from_dict(ev_arrival_dict)

sns.displot(ev_arrival, x="time [min]", kind="kde", hue="type")
ax = plt.gca()
cs = ax.lines[2]
ev = ax.lines[1]
ev_0 = ax.lines[0]

cs_result = {'time_x': cs.get_xdata(), 'cs_y': cs.get_ydata()}
cs_result = pd.DataFrame.from_dict(cs_result)

num = 0
status = 0
for n in range(len(cs_result)):
    if cs_result.iloc[num, 0] < 7 * 59 or cs_result.iloc[num, 0] > (20 * 60 - 30):
        if status == 0:
            cs_result.iloc[num, 0] = 0
            status = 1
        cs_result.iloc[num, 1] = 0
    num += 1
df = pd.DataFrame([[1440, 0]], columns=['time_x', 'cs_y'])
cs_result = cs_result.append(df, ignore_index=True)

ev_result = {'time_x': ev.get_xdata(), 'ev_y': ev.get_ydata()}
ev_result = pd.DataFrame.from_dict(ev_result)
ev_result.iloc[0, 0] = 0
ev_result.iloc[0, 1] = 0

ev_0_result = {'time_x': ev_0.get_xdata(), 'ev_y': ev_0.get_ydata()}
ev_0_result = pd.DataFrame.from_dict(ev_0_result)
ev_0_result.iloc[199, 0] = 1440
ev_0_result.iloc[199, 1] = 0
plt.show()

fig, ax = plt.subplots()
fig.canvas.draw()

ax.plot(cs_result['time_x'], cs_result['cs_y'], label="Arrival in Charging Station", linewidth=2)
ax.plot(ev_result['time_x'], ev_result['ev_y'], label="Arrival at Home", linewidth=2)
ax.plot(ev_0_result['time_x'], ev_0_result['ev_y'], label="Departure from Home", linewidth=2)
ax.grid(b=True, axis='both')
ax.legend()
plt.xlabel("Time [h]")
plt.ylabel("PDF")
plt.xlim([0, 1440])
plt.axvline(x=413, color='r', linestyle='--')
plt.axvline(x=1170, color='r', linestyle='--')

labels = [item.get_text() for item in ax.get_xticklabels()]
print(labels)
labels[0] = '00:00'
labels[1] = '03:20'
labels[2] = '06:40'
labels[3] = '10:00'
labels[4] = '13:20'
labels[5] = '16:40'
labels[6] = '20:00'
#labels[7] = '23:20'
ax.set_xticklabels(labels)
plt.show()

#x_axis = np.concatenate((cs_result['time_x'], ev_result['time_x'], ev_0_result['time_x']), axis=0)
#y_axis = np.concatenate((cs_result['cs_y'], ev_result['ev_y'], ev_0_result['ev_y']), axis=0)
#label_axis1 = ["Arrival in Charging Station"] * len(cs_result['time_x'])
#label_axis2 = ["Arrival at Home"] * len(ev_result['time_x'])
#label_axis3 = ["Departure from Home"] * len(ev_0_result['time_x'])
#label_axis = np.concatenate((label_axis1, label_axis2, label_axis3), axis=0)
#data_dict = {"time": x_axis, "result": y_axis, "legend":label_axis}
#data = pd.DataFrame.from_dict(data_dict)

#plt.figure()
#sns.lineplot(data=data, x="time", y="result", hue="legend")
#plt.xlabel("Time [min]")
#plt.ylabel("PDF")

#plt.xlim([0, 1440])
#plt.show()
