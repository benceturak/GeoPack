def normalFormToFloat(str):

    num = str.replace('D', 'e').replace('E', 'e').split('e')

    num_s = num[0].split('.')

    if num_s[0] == '':
        return (0 + float("0."+num_s[1]))*10**int(num[1])
    elif num_s[0] == "-":
        return (0 - float("0."+num_s[1]))*10**int(num[1])
    else:
        return float(num[0])*10**int(num[1])
