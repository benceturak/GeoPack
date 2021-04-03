import numpy as np


def normalizeTime1Row(time):
    months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if time.ndim == 1:
        row = time
        #seconds
        while row[5] > 60:
            row[5] -= 60
            row[4] += 1
        while row[5] < 0:
            row[5] += 60
            row[4] -= 1
        #minutes
        while row[4] > 60:
            row[4] -= 60
            row[3] += 1
        while row[4] < 0:
            row[4] += 60
            row[3] -= 1

        #hour
        while row[3] > 23:
            row[3] -= 24
            row[2] += 1
        while row[3] < 0:
            row[3] += 24
            row[2] -= 1

        #day
        m = int(row[1])
        while m > 12:
            m -= 12
        while m < 0:
            m += 12


        daysOfMonth = months[m-1]

        if row[0] % 4 == 0 and m == 1:
            daysOfMonth += 1

        while row[2] > daysOfMonth:
            row[2] -= daysOfMonth
            row[1] += 1
        while row[2] < 0:
            row[2] += daysOfMonth
            row[1] -= 1

        #months

        while row[1] > 12:
            row[1] -= 12
            row[0] += 1
        while row[1] < 0:
            row[1] += 12
            row[0] -= 1

        return row


def normalizeTime(time):

    if time.ndim == 1:
        return normalizeTime1Row(time)
    elif time.ndim == 2:
        re = np.empty((0,6))
        for row in time:
            re = np.append(re, [normalizeTime1Row(row)], axis=0)
        return re



time = np.array([[2021, 5, 15, 14, 47, 35], [1998, 10, 23, 5, 8, 35]])
print(time)
print(normalizeTime(time))
