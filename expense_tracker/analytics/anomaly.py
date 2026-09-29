import math


def detect_anomalies(expenses):
    if len(expenses) < 2:
        return []

    amounts = [expense.amount for expense in expenses]
    mean = sum(amounts) / len(amounts)
    variance = sum((amount - mean) ** 2 for amount in amounts) / len(amounts)
    std_dev = math.sqrt(variance)

    anomalies = []
    threshold = mean + std_dev

    for expense in expenses:
        if expense.amount > threshold:
            anomalies.append({
                "expense": expense,
                "mean": mean,
                "std_dev": std_dev,
                "threshold": threshold,
            })

    return anomalies
