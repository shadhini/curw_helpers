
def append_value_for_timestamp(existing_ts, new_ts):

    """
    Appending timeseries assuming start and end of both timeseries are same
    :param existing_ts: list of [timestamp, value1, value2, .., valuen] lists (note: this might include several values)
    :param new_ts: list of [timestamp, VALUE] list (note: this include single value)
    :return: list of [timestamp, value1, value2, .., valuen, VALUE]
    """

    appended_ts =[]

    if len(existing_ts) == len(new_ts) and existing_ts[0][0] == new_ts[0][0]:
        for i in range(len(existing_ts)):
            appended_ts.append(existing_ts[i])
            appended_ts[i].append(new_ts[i][1])
    else:
        return existing_ts

    return appended_ts


def average_timeseries(timeseries):
    """
    Give the timeseries with avg value for given timeseries containing several values per one timestamp
    :param timeseries:
    :return:
    """
    avg_timeseries = []

    if len(timeseries[0]) <= 2:
        return timeseries
    else:
        for i in range(len(timeseries)):
            count = len(timeseries[i])-1
            avg_timeseries.append([timeseries[i][0], '%.3f' % (sum(timeseries[i][1:])/count)])

    return avg_timeseries


