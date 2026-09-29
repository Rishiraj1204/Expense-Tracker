from expense_tracker.dsa.queue import Queue


def test_queue():
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)

    assert queue.peek() == 1
    assert queue.dequeue() == 1
    assert queue.dequeue() == 2
    assert queue.is_empty() is True
