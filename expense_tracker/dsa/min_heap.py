class MinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, value):
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)

    def peek(self):
        if not self.heap:
            return None
        return self.heap[0]

    def extract_min(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def _heapify_up(self, index):
        parent_index = (index - 1) // 2
        while index > 0 and self.heap[parent_index] > self.heap[index]:
            self.heap[parent_index], self.heap[index] = self.heap[index], self.heap[parent_index]
            index = parent_index
            parent_index = (index - 1) // 2

    def _heapify_down(self, index):
        last_index = len(self.heap) - 1
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if left <= last_index and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right <= last_index and self.heap[right] < self.heap[smallest]:
                smallest = right
            if smallest == index:
                break

            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            index = smallest
