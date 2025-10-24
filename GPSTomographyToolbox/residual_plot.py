import numpy as np
import matplotlib.pyplot as plt


fid = open("figures/profiles/profile_residuals.csv")

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
        print(data[0])
        c = "black"
    colors = np.append(colors, c)

print(residuals)



residuals_sorted = residuals[np.argsort(residuals[:,1])]
#residuals_sorted = residuals_sorted[::-1]
print(residuals_sorted)
#print(np.shape())

fig, ax = plt.subplots()

# Example data
y = residuals_sorted[:,1]
x = residuals_sorted[:,2]



#ax.hlines(y=y_pos[np.where(residuals_sorted[:,0] == 11747)], xmin=0, xmax=x[np.where(residuals_sorted[:,0] == 11747)], color='blue', label='11747')
#ax.hlines(y=y_pos[np.where(residuals_sorted[:,0] == 14240)], xmin=0, xmax=x[np.where(residuals_sorted[:,0] == 14240)], color='red', label='14240')
#ax.hlines(y=y_pos[np.where(residuals_sorted[:,0] == 12843)], xmin=0, xmax=x[np.where(residuals_sorted[:,0] == 12843)], color='green', label='12843')
#ax.hlines(y=y_pos[np.where(residuals_sorted[:,0] == 12982)], xmin=0, xmax=x[np.where(residuals_sorted[:,0] == 12982)], color='pink', label='12982')
#ax.hlines(y=y_pos[np.where(residuals_sorted[:,0] == 11952)], xmin=0, xmax=x[np.where(residuals_sorted[:,0] == 11952)], color='cyan', label='11952')

print(np.max(y[np.where(residuals_sorted[:,0] == 11747)]))
#ax.plot(x[np.where(residuals_sorted[:,0] == 11747)], y[np.where(residuals_sorted[:,0] == 11747)], 'x', color='blue', label='11747')
#ax.plot(x[np.where(residuals_sorted[:,0] == 14240)], y[np.where(residuals_sorted[:,0] == 14240)], 'x', color='red', label='14240')
#ax.plot(x[np.where(residuals_sorted[:,0] == 12843)], y[np.where(residuals_sorted[:,0] == 12843)], 'x', color='green', label='12843')
#ax.plot(x[np.where(residuals_sorted[:,0] == 12982)], y[np.where(residuals_sorted[:,0] == 12982)], 'x', color='pink', label='12982')
ax.plot(x[np.where(residuals_sorted[:,0] == 11952)], y[np.where(residuals_sorted[:,0] == 11952)], 'x', color='cyan', label='11952')

print(np.shape(y[np.where(residuals_sorted[:,0] == 11747)]))
print(np.shape(y[np.where(residuals_sorted[:,0] == 14240)]))
print(np.shape(y[np.where(residuals_sorted[:,0] == 12843)]))
print(np.shape(y[np.where(residuals_sorted[:,0] == 12982)]))
print(np.shape(y[np.where(residuals_sorted[:,0] == 11952)]))

heights = (0,1000,2000,3000,5500,8000,12000)

ax.set_xlabel('Residuals [-]')
ax.set_ylabel('Height [m]')
ax.set_title('Residuals of Wet Refractivity values measured to RS profile 11952')
plt.xlim(-50,50)
plt.ylim(0,10000)
plt.legend()
#plt.show()
#exit()
fname="residuals_11952.png"
plt.savefig(fname, dpi=600, pad=0.3, bbox_inches='tight')
plt.close()