def obj(x):
    if x < 0:
        return 0
    if x < 10000:
        return 50 * x
    if x < 20000:
        return 49 * x
    return 47 * x

