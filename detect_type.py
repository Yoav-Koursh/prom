def detect(speeds, locations):
    max_alt =   max([locations[i][2] for i in range(len(locations))])
    max_speed = max(speeds)
    if max_alt < 200:
        return 'quadcopter'
    elif max_speed < 10:
        return 'baloon'
    elif max_speed < 60:
        return 'drone'
    elif max_speed > 680 or max_alt > 20000:
        return 'rocket'
    else:
        return 'plane'