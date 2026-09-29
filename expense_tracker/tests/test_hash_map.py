from expense_tracker.dsa.hash_map import HashMap, build_category_map


def test_hash_map():
    hashmap = HashMap()
    hashmap.add('Food', 300)
    hashmap.add('Food', 200)

    assert hashmap.get('Food') == 500


def test_build_category_map():
    class Expense:
        def __init__(self, category_name, amount):
            self.category = type('Category', (), {'name': category_name})()
            self.amount = amount

    expenses = [Expense('Food', 100), Expense('Travel', 50), Expense('Food', 150)]
    category_map = build_category_map(expenses)

    assert category_map.get('Food') == 250
