from expense_tracker.dsa.sorting import merge_sort


def test_merge_sort():
    values = [5, 1, 4, 2, 3]
    result = merge_sort(values)
    assert result == [1, 2, 3, 4, 5]
