def calculate_moving_average(expenses, window_size=3):
    if not expenses:
        return []

    moving_average = []
    for index in range(len(expenses)):
        start = max(0, index - window_size + 1)
        window = expenses[start:index + 1]
        average = sum(item.amount for item in window) / len(window)
        moving_average.append({"date": expenses[index].expense_date, "value": average})

    return moving_average
