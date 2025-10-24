import numpy as np
import matplotlib.pyplot as plt


fid = open("results/figures/profiles/profile_residuals_integral_20242.csv")
#fid = open("results/figures/profiles/profile_residuals.csv")
residuals = np.empty((0,3))
colors = np.empty((0,))
for line in fid.readlines():
    data = line.split(",")

    residuals = np.append(residuals, [[int(data[0]), float(data[2]), float(data[3])]], axis=0)

    if data[0] == "11747":
        c = "blue"
    elif data[0] == "14240":
        c = "red"
    elif data[0] == "12843":
        c = "green"
    elif data[0] == "12982":
        c = "purple"
    elif data[0] == "11952":
        c = "cyan"
    else:
        c = "black"
    colors = np.append(colors, c)

#print(residuals)



residuals_sorted = residuals[np.argsort(residuals[:,1])]
#residuals_sorted = residuals_sorted[::-1]
#print(residuals_sorted)
#print(np.shape())

#fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(3.31,3))

# Example data
y = residuals_sorted[:,1]
x = residuals_sorted[:,2]

stations = ("11747", "14240", "12843", "12982", "11952")
#stations = ("12843", "12982", "11952")
barColors = ("blue", "red", "green", "orange", "purple")
#barColors = ("green", "pink", "cyan")

heights = (0,1000,2000,3000,5500,8000,12000)


#ax.hlines(y=y_pos[np.where(residuals_sorted[:,0] == 11747)], xmin=0, xmax=x[np.where(residuals_sorted[:,0] == 11747)], color='blue', label='11747')
#ax.hlines(y=y_pos[np.where(residuals_sorted[:,0] == 14240)], xmin=0, xmax=x[np.where(residuals_sorted[:,0] == 14240)], color='red', label='14240')
#ax.hlines(y=y_pos[np.where(residuals_sorted[:,0] == 12843)], xmin=0, xmax=x[np.where(residuals_sorted[:,0] == 12843)], color='green', label='12843')
#ax.hlines(y=y_pos[np.where(residuals_sorted[:,0] == 12982)], xmin=0, xmax=x[np.where(residuals_sorted[:,0] == 12982)], color='pink', label='12982')
#ax.hlines(y=y_pos[np.where(residuals_sorted[:,0] == 11952)], xmin=0, xmax=x[np.where(residuals_sorted[:,0] == 11952)], color='cyan', label='11952')

#print(np.max(y[np.where(residuals_sorted[:,0] == 11747)]))
#ax.plot(x[np.where(residuals_sorted[:,0] == 11747)], y[np.where(residuals_sorted[:,0] == 11747)], 'x', color='blue', label='11747')
#ax.plot(x[np.where(residuals_sorted[:,0] == 14240)], y[np.where(residuals_sorted[:,0] == 14240)], 'x', color='red', label='14240')
#ax.plot(x[np.where(residuals_sorted[:,0] == 12843)], y[np.where(residuals_sorted[:,0] == 12843)], 'x', color='green', label='12843')
#ax.plot(x[np.where(residuals_sorted[:,0] == 12982)], y[np.where(residuals_sorted[:,0] == 12982)], 'x', color='pink', label='12982')
#ax.plot(x[np.where(residuals_sorted[:,0] == 11952)], y[np.where(residuals_sorted[:,0] == 11952)], 'x', color='cyan', label='11952')
width = 0.35
k = 0


for s in stations:
    y_fr = np.empty((0,))
    x_fr = np.empty((0,))
    h_m = np.empty((0,))
    x_mean = np.empty((0,))
    x_min = np.empty((0,))
    x_max = np.empty((0,))
    x_std = np.empty((0,))

    y_labels = np.empty((0,))

    y_bar = residuals_sorted[np.where(residuals_sorted[:,0] == int(s)),1]
    x_bar = residuals_sorted[np.where(residuals_sorted[:,0] == int(s)),2]
    for i in range(0,len(heights)-1):
        y_labels = np.append(y_labels, 1+i*2)
        y_fr = np.append(y_fr, (heights[i] + heights[i+1])/2)

        #x_bar[np.all((y_bar > heights[i], y_bar <= heights[i+1]), axis=0)]
        h_m = np.append(h_m, 1+i*2-2*width + k*width)

        #x_fr[i] = x_bar[np.all((y_bar > heights[i], y_bar <= heights[i+1]), axis=0)]
        x_fr =x_bar[np.all((y_bar > heights[i], y_bar <= heights[i+1]), axis=0)]
        print("#########################x")
        print(heights[i])
        try:
            while(True):
                mean = np.mean(x_fr)
                std = np.std(x_fr)
                print(x_fr)
                print("_____________________________________________________________________________")
                print(mean)
                print(std)
                max_i = np.argmax(x_fr - mean)
                min_i = np.argmin(x_fr - mean)

                min = mean - 3*std
                max = mean + 3*std

                before = np.shape(x_fr)

                x_fr = x_fr[np.all((x_fr >= min, x_fr <= max), axis=0)]
                after = np.shape(x_fr)
                
                if before == after:
                    break
            x_min = np.append(x_min, x_fr[min_i])
            x_max = np.append(x_max, x_fr[max_i])
            x_mean = np.append(x_mean, mean)
            x_std = np.append(x_std, std)
        except:
            x_min = np.append(x_min, 0)
            x_max = np.append(x_max, 0)
            x_mean = np.append(x_mean, 0)
            x_std = np.append(x_std, 0)

        



    print(before[0])
    print(x_min)
    stats = np.append([y_fr], [x_min], axis=0)
    stats = np.append(stats, [x_max], axis=0)
    stats = np.append(stats, [x_mean], axis=0)
    stats = np.append(stats, [x_std], axis=0).T
    p = ax.barh(h_m, x_mean, width ,label=s, align='center', color=barColors[k])
    ax.hlines(h_m, -x_std, x_std, color=barColors[k], linewidth=1)
    np.savetxt("stats2_"+s+".csv", stats, delimiter=",")
    k = k + 1
ax.vlines(0, 0, 12, color="black")
ax.hlines((0,2,4,6,8,10,12), -20, 20, color="grey")



print(np.shape(y[np.where(residuals_sorted[:,0] == 11747)]))
print(np.shape(y[np.where(residuals_sorted[:,0] == 14240)]))
print(np.shape(y[np.where(residuals_sorted[:,0] == 12843)]))
print(np.shape(y[np.where(residuals_sorted[:,0] == 12982)]))
print(np.shape(y[np.where(residuals_sorted[:,0] == 11952)]))

heights = (0.0,1.0,2.0,3.0,5.5,8.0,12.0) 

ax.set_xlabel('Mean value and std of residuals [-]')
ax.set_ylabel('Height [km]')
ax.set_yticks(np.arange(7)*2)
ax.set_yticklabels(heights)

#ax.set_title('Mean value and std of residuals for each atmospheric layers')
plt.legend(prop = { "size": 8 })
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.rc('legend',fontsize=8)
plt.legend(fontsize=8)

plt.xlim(-15,15)
plt.ylim(0,12)

#ax.set_yticks((0,1,2,3,4,6), )
#plt.show()
#exit()
fname = "residuals_mean_std.tif"
plt.savefig(fname, dpi=900, bbox_inches='tight')
plt.close()
