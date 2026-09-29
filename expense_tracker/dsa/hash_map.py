class HashMap:
    def __init__(self):
        self._data = {}

    def set(self, key, value):
        self._data[key] = value

    def get(self, key, default=None):
        return self._data.get(key, default)

    def add(self, key, amount):
        if key in self._data:
            self._data[key] += amount
        else:
            self._data[key] = amount

    def items(self):
        return self._data.items()

    def to_dict(self):
        return dict(self._data)


def build_category_map(expenses):
    category_map = HashMap()
    for expense in expenses:
        category_map.add(expense.category.name, expense.amount)
    return category_map
