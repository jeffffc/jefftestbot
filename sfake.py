def calc(num):
    numint = int(num)
    numstr = str(num)
    firstnum = int(numstr[:1])
    firststr = numstr[:1]
    afternum = int(numstr[1:])
    afterstr = numstr[1:]
    numlength = len(numstr)

    rows_count = numlength
    cols_count = 2
    history = [[0 for j in range(cols_count)] for i in range(rows_count)]

    history[0][0] = firstnum
    history[0][1] = 1
    index = 0
    for i in afterstr:
        if history[index][0] == int(i):
            history[index][1] = history[index][1] + 1
            continue
        else:
            index = index + 1
            history[index][0] = int(i)
            history[index][1] = 1
            continue

    final = ""
    for x in history:
        if x[0] == 0 or x[1] == 0:
            continue
        final += str(x[1]) + str(x[0])
    return(final)

#calc(11132122233113)
