def analyse_trends(series):
    if len(series) < 2:
        return []

    results = []
    keys = list(series.keys())
    values = list(series.values())

    for index in range(1, len(values)):
        current = values[index]
        previous = values[index - 1]
        change = 0 if previous == 0 else ((current - previous) / previous) * 100

        if abs(change) < 1:
            trend = "Stable"
        elif change > 0:
            trend = "Increasing"
        else:
            trend = "Decreasing"

        results.append({"period": keys[index], "current": current, "previous": previous, "change": change, "trend": trend})

    return results
