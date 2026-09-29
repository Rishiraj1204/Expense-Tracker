from expense_tracker.dsa.searching import binary_search, linear_search


def test_linear_search():
    assert linear_search([1, 2, 3, 4], 3) == 2
    assert linear_search([1, 2, 3, 4], 9) == -1


def test_binary_search():
    assert binary_search([1, 2, 3, 4, 5], 4) == 3
    assert binary_search([1, 2, 3, 4, 5], 9) == -1
