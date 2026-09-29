from .min_heap import MinHeap


def top_k_expenses(expenses, k):
    heap = MinHeap()
    for expense in expenses:
        value = expense.amount if hasattr(expense, 'amount') else expense
        heap.insert(value)
        if len(heap.heap) > k:
            heap.extract_min()
    return heap.heap
