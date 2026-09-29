from expense_tracker.dsa.max_heap import MaxHeap
from expense_tracker.dsa.min_heap import MinHeap
from expense_tracker.dsa.top_k import top_k_expenses


def test_max_heap():
    heap = MaxHeap()
    for value in [3, 5, 1, 7, 9]:
        heap.insert(value)

    assert heap.peek() == 9
    assert heap.extract_max() == 9


def test_min_heap():
    heap = MinHeap()
    for value in [3, 5, 1, 7, 9]:
        heap.insert(value)

    assert heap.peek() == 1
    assert heap.extract_min() == 1


def test_top_k_expenses():
    result = top_k_expenses([10, 8, 5, 12, 15], 3)
    assert sorted(result) == [10, 12, 15]
