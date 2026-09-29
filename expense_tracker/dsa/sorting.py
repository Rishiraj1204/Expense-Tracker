def merge_sort(items, key=None):
    if len(items) <= 1:
        return items

    midpoint = len(items) // 2
    left = merge_sort(items[:midpoint], key)
    right = merge_sort(items[midpoint:], key)
    return merge(left, right, key)


def merge(left, right, key=None):
    merged = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        left_value = left[left_index]
        right_value = right[right_index]
        if key:
            left_value = key(left_value)
            right_value = key(right_value)

        if left_value <= right_value:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    merged.extend(left[left_index:])
    merged.extend(right[right_index:])
    return merged
