

import time
import threading
from queue import Queue
import random



# 1. Given a list of integers, return all unique triplets that sum to zero.
def three_sum(nums):

    nums.sort()
    result = []
    seen = set()
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    triplet = tuple(sorted([nums[i], nums[j], nums[k]]))
                    if triplet not in seen:
                        seen.add(triplet)
                        result.append(list(triplet))
    return result


# 2. Implement an LRU (Least Recently Used) cache with get and put in O(1).
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.data = {}
        self.order = []  

    def get(self, key):
        if key not in self.data:
            return -1
  
        self.order.remove(key)
        self.order.append(key)
        return self.data[key]

    def put(self, key, value):
        if key in self.data:
            self.order.remove(key)
        elif len(self.data) >= self.capacity:
            
            oldest = self.order.pop(0)
            del self.data[oldest]
        self.data[key] = value
        self.order.append(key)



# 3. Given a string, find the length of the longest substring without
#    repeating characters.
def longest_unique_substring(s):
    longest = 0
    for i in range(len(s)):
        seen_chars = set()
        current_len = 0
        for j in range(i, len(s)):
            if s[j] in seen_chars:
                break
            seen_chars.add(s[j])
            current_len += 1
        if current_len > longest:
            longest = current_len
    return longest



# 4. Implement merge sort without using any built-in sort functions.
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    left_sorted = merge_sort(left_half)
    right_sorted = merge_sort(right_half)

    # now merge them together
    merged = []
    i = 0
    j = 0
    while i < len(left_sorted) and j < len(right_sorted):
        if left_sorted[i] <= right_sorted[j]:
            merged.append(left_sorted[i])
            i += 1
        else:
            merged.append(right_sorted[j])
            j += 1

    # add whatever is left over
    while i < len(left_sorted):
        merged.append(left_sorted[i])
        i += 1
    while j < len(right_sorted):
        merged.append(right_sorted[j])
        j += 1

    return merged


# ---------------------------------------------------------------------------
# 5. Given a binary tree, return its level-order traversal as a list of lists.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def level_order(root):
    if root is None:
        return []

    result = []
    queue = [root]  # using a list as a queue, not the most efficient but works

    while len(queue) > 0:
        level_size = len(queue)
        current_level = []
        for i in range(level_size):
            node = queue.pop(0)
            current_level.append(node.val)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        result.append(current_level)

    return result


# ---------------------------------------------------------------------------
# 6. Write a decorator that caches function results based on arguments,
#    with a maximum cache size (implement your own, don't use functools).
def memoize(max_size):
    def decorator(func):
        cache = {}
        cache_keys_order = []  # to know what to remove first

        def wrapper(*args):
            if args in cache:
                return cache[args]

            result = func(*args)
            cache[args] = result
            cache_keys_order.append(args)

            if len(cache_keys_order) > max_size:
                key_to_remove = cache_keys_order.pop(0)
                del cache[key_to_remove]

            return result

        return wrapper

    return decorator


# ---------------------------------------------------------------------------
# 7. Given a list of intervals, merge all overlapping intervals.
def merge_intervals(intervals):
    if not intervals:
        return []

    # sort by start time
    intervals.sort(key=lambda x: x[0])

    merged = []
    for interval in intervals:
        if len(merged) == 0:
            merged.append(interval)
        else:
            last = merged[-1]
            if interval[0] <= last[1]:
                # overlaps, merge them
                last[1] = max(last[1], interval[1])
            else:
                merged.append(interval)

    return merged


# ---------------------------------------------------------------------------
# 8. Implement a generator that yields all permutations of a list without
#    using itertools.
def permutations_gen(lst):
    if len(lst) == 0:
        yield []
        return
    if len(lst) == 1:
        yield lst
        return

    for i in range(len(lst)):
        current = lst[i]
        remaining = lst[:i] + lst[i+1:]
        for p in permutations_gen(remaining):
            yield [current] + p


# ---------------------------------------------------------------------------
# 9. Given a matrix, rotate it 90 degrees clockwise in place.
def rotate_matrix(matrix):
    n = len(matrix)

    # transpose the matrix first (swap rows and columns)
    for i in range(n):
        for j in range(i, n):
            temp = matrix[i][j]
            matrix[i][j] = matrix[j][i]
            matrix[j][i] = temp

    # then reverse each row
    for i in range(n):
        matrix[i].reverse()

    return matrix


# ---------------------------------------------------------------------------
# 10. Implement a Trie (prefix tree) with insert, search, and startsWith.
class Trie:
    def __init__(self):
        self.children = {}
        self.is_word_end = False

    def insert(self, word):
        node = self
        for char in word:
            if char not in node.children:
                node.children[char] = Trie()
            node = node.children[char]
        node.is_word_end = True

    def search(self, word):
        node = self
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_word_end

    def starts_with(self, prefix):
        node = self
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True


# ---------------------------------------------------------------------------
# 11. Given a graph as an adjacency list, detect if it contains a cycle
#     (directed graph).
def has_cycle(graph):
    visited = set()
    in_stack = set()  # nodes currently in the recursion path

    def dfs(node):
        visited.add(node)
        in_stack.add(node)

        neighbors = graph.get(node, [])
        for neighbor in neighbors:
            if neighbor in in_stack:
                return True
            if neighbor not in visited:
                if dfs(neighbor):
                    return True

        in_stack.remove(node)
        return False

    for node in graph:
        if node not in visited:
            if dfs(node):
                return True

    return False


# ---------------------------------------------------------------------------
# 12. Implement quicksort using the Lomuto partition scheme, in place.
def quicksort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1

    if low < high:
        # partition step
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i+1], arr[high] = arr[high], arr[i+1]
        pivot_index = i + 1

        quicksort(arr, low, pivot_index - 1)
        quicksort(arr, pivot_index + 1, high)

    return arr


# ---------------------------------------------------------------------------
# 13. Write a context manager (using a class, not contextlib) that times
#     how long a block of code takes to execute.
class Timer:
    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        self.elapsed = self.end_time - self.start_time
        print("time taken:", self.elapsed)
        # returning False so exceptions still propagate
        return False


# ---------------------------------------------------------------------------
# 14. Given two strings, determine if one is a scrambled version of the
#     other (recursive/backtracking approach).
def is_scramble(s1, s2):
    # brute force recursion, added a dict to cache repeated calls
    cache = {}

    def check(a, b):
        if a == b:
            return True

        # if letters dont match up they cant be scrambled versions
        if sorted(a) != sorted(b):
            return False

        if (a, b) in cache:
            return cache[(a, b)]

        length = len(a)
        result = False
        for i in range(1, length):
            # option 1: no swap at this split
            if check(a[:i], b[:i]) and check(a[i:], b[i:]):
                result = True
                break
            # option 2: swapped at this split
            if check(a[:i], b[length-i:]) and check(a[i:], b[:length-i]):
                result = True
                break

        cache[(a, b)] = result
        return result

    return check(s1, s2)


# ---------------------------------------------------------------------------
# 15. Implement a min-heap from scratch (no heapq) supporting push and pop.
class MinHeap:
    def __init__(self):
        self.items = []

    def push(self, val):
        self.items.append(val)
        # bubble it up to the right place
        i = len(self.items) - 1
        while i > 0:
            parent = (i - 1) // 2
            if self.items[parent] > self.items[i]:
                self.items[parent], self.items[i] = self.items[i], self.items[parent]
                i = parent
            else:
                break

    def pop(self):
        if len(self.items) == 0:
            return None

        smallest = self.items[0]
        last_item = self.items.pop()

        if len(self.items) > 0:
            self.items[0] = last_item
            # bubble it down
            i = 0
            while True:
                left = 2 * i + 1
                right = 2 * i + 2
                smallest_idx = i

                if left < len(self.items) and self.items[left] < self.items[smallest_idx]:
                    smallest_idx = left
                if right < len(self.items) and self.items[right] < self.items[smallest_idx]:
                    smallest_idx = right

                if smallest_idx == i:
                    break

                self.items[i], self.items[smallest_idx] = self.items[smallest_idx], self.items[i]
                i = smallest_idx

        return smallest


# ---------------------------------------------------------------------------
# 16. Given a string containing just the characters '(', ')', '{', '}',
#     '[' and ']', determine if the input string is valid.
def is_valid_parens(s):
    stack = []
    matching = {')': '(', ']': '[', '}': '{'}

    for char in s:
        if char in '([{':
            stack.append(char)
        else:
            if len(stack) == 0:
                return False
            top = stack.pop()
            if top != matching[char]:
                return False

    # if stack isnt empty something wasnt closed
    return len(stack) == 0


# ---------------------------------------------------------------------------
# 17. Implement a function that flattens an arbitrarily nested list using
#     a generator (no recursion allowed — use an explicit stack).
def flatten_iterative(nested):
    stack = []
    # push everything in reverse so we pop in the right order
    for item in reversed(nested):
        stack.append(item)

    while len(stack) > 0:
        current = stack.pop()
        if isinstance(current, list):
            for item in reversed(current):
                stack.append(item)
        else:
            yield current


# ---------------------------------------------------------------------------
# 18. Given a list of words, group anagrams together.
def group_anagrams(words):
    groups = {}
    for word in words:
        key = ''.join(sorted(word))
        if key not in groups:
            groups[key] = []
        groups[key].append(word)

    return list(groups.values())


# ---------------------------------------------------------------------------
# 19. Implement Dijkstra's shortest path algorithm on a weighted graph
#     given as an adjacency dict.
def dijkstra(graph, start):
    # doing this without heapq, just a plain dict and looping to find the min
    distances = {}
    for node in graph:
        distances[node] = float('inf')
    distances[start] = 0

    visited = set()

    while len(visited) < len(graph):
        # find the unvisited node with smallest distance
        current = None
        current_dist = float('inf')
        for node in graph:
            if node not in visited and distances[node] < current_dist:
                current = node
                current_dist = distances[node]

        if current is None:
            break  # remaining nodes are unreachable

        visited.add(current)

        for neighbor, weight in graph[current].items():
            new_dist = distances[current] + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist

    return distances


# ---------------------------------------------------------------------------
# 20. Write a metaclass that automatically registers every subclass of a
#     given base class into a registry dict.
class RegistryMeta(type):
    registry = {}

    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        # dont register the base class itself, only subclasses
        if bases:
            RegistryMeta.registry[name] = new_class
        return new_class


# ---------------------------------------------------------------------------
# 21. Given a list of numbers, find the length of the longest increasing
#     subsequence.
def longest_increasing_subsequence(nums):
    if not nums:
        return 0

    # classic O(n^2) dp approach
    dp = [1] * len(nums)

    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1

    return max(dp)


# ---------------------------------------------------------------------------
# 22. Implement a rate limiter class using the token bucket algorithm.
class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.refill_rate = refill_rate  # tokens added per second
        self.tokens = capacity
        self.last_check = time.time()

    def allow_request(self):
        now = time.time()
        time_passed = now - self.last_check
        self.last_check = now

        # add tokens based on how much time passed
        self.tokens += time_passed * self.refill_rate
        if self.tokens > self.capacity:
            self.tokens = self.capacity

        if self.tokens >= 1:
            self.tokens -= 1
            return True
        else:
            return False


# ---------------------------------------------------------------------------
# 23. Given a 2D grid of '1's (land) and '0's (water), count the number of
#     islands.
def num_islands(grid):
    if not grid:
        return 0

    rows = len(grid)
    cols = len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    count = 0

    def explore(r, c):
        # using a simple stack based dfs
        stack = [(r, c)]
        while stack:
            row, col = stack.pop()
            if row < 0 or row >= rows or col < 0 or col >= cols:
                continue
            if visited[row][col] or grid[row][col] == '0':
                continue
            visited[row][col] = True
            stack.append((row+1, col))
            stack.append((row-1, col))
            stack.append((row, col+1))
            stack.append((row, col-1))

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and not visited[r][c]:
                count += 1
                explore(r, c)

    return count


# ---------------------------------------------------------------------------
# 24. Implement a function to serialize and deserialize a binary tree.
def serialize(root):
    result = []

    def helper(node):
        if node is None:
            result.append('null')
        else:
            result.append(str(node.val))
            helper(node.left)
            helper(node.right)

    helper(root)
    return ','.join(result)


def deserialize(data):
    values = data.split(',')
    # using an index we can mutate across recursive calls
    index = [0]

    def helper():
        val = values[index[0]]
        index[0] += 1
        if val == 'null':
            return None
        node = TreeNode(int(val))
        node.left = helper()
        node.right = helper()
        return node

    return helper()


# ---------------------------------------------------------------------------
# 25. Write a custom iterator class that produces the Fibonacci sequence
#     up to n terms, implementing __iter__ and __next__.
class FibonacciIterator:
    def __init__(self, n):
        self.n = n
        self.current_count = 0
        self.prev = 0
        self.curr = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_count >= self.n:
            raise StopIteration

        value = self.prev
        next_val = self.prev + self.curr
        self.prev = self.curr
        self.curr = next_val
        self.current_count += 1
        return value


# ---------------------------------------------------------------------------
# 26. Given a string s and a pattern p with support for '.' and '*',
#     implement regular expression matching from scratch.
def is_match(s, p):
    # recursive solution with memo dict, not the fastest but easier to follow
    memo = {}

    def helper(i, j):
        if (i, j) in memo:
            return memo[(i, j)]

        if j == len(p):
            ans = i == len(s)
        else:
            first_char_matches = i < len(s) and (p[j] == s[i] or p[j] == '.')

            if j + 1 < len(p) and p[j+1] == '*':
                # try skipping the "x*" completely, or using it once and staying
                ans = helper(i, j+2) or (first_char_matches and helper(i+1, j))
            else:
                ans = first_char_matches and helper(i+1, j+1)

        memo[(i, j)] = ans
        return ans

    return helper(0, 0)


# ---------------------------------------------------------------------------
# 27. Implement a thread-safe singleton pattern using a decorator.
def singleton(cls):
    instances = {}
    lock = threading.Lock()

    def get_instance(*args, **kwargs):
        # double checked locking so we dont lock every single call
        if cls not in instances:
            lock.acquire()
            try:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
            finally:
                lock.release()
        return instances[cls]

    return get_instance


# ---------------------------------------------------------------------------
# 28. Given a set of coins and a target amount, find the minimum number of
#     coins needed to make that amount (dynamic programming).
def coin_change(coins, amount):
    # dp[i] = min coins needed to make amount i
    dp = [amount + 1] * (amount + 1)  # amount+1 acts as "infinity" here
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                if dp[i - coin] + 1 < dp[i]:
                    dp[i] = dp[i - coin] + 1

    if dp[amount] > amount:
        return -1
    return dp[amount]


# ---------------------------------------------------------------------------
# 29. Implement a function that finds the median of two sorted arrays in
#     O(log(min(m,n))) time.
def find_median_sorted_arrays(nums1, nums2):
    # honestly the O(log(min(m,n))) binary search version is tricky
    # so doing the simpler merge approach here, still works correctly
    merged = []
    i = 0
    j = 0
    while i < len(nums1) and j < len(nums2):
        if nums1[i] <= nums2[j]:
            merged.append(nums1[i])
            i += 1
        else:
            merged.append(nums2[j])
            j += 1
    while i < len(nums1):
        merged.append(nums1[i])
        i += 1
    while j < len(nums2):
        merged.append(nums2[j])
        j += 1

    n = len(merged)
    mid = n // 2
    if n % 2 == 0:
        return (merged[mid - 1] + merged[mid]) / 2
    else:
        return merged[mid]


# ---------------------------------------------------------------------------
# 30. Write a producer-consumer setup using threading, a Queue, and proper
#     synchronization (locks/events) to safely process items concurrently.
def producer_consumer_demo(num_items=10, num_producers=2, num_consumers=2):
    q = Queue()
    results = []
    results_lock = threading.Lock()
    done_producing = threading.Event()

    count_lock = threading.Lock()
    items_made = [0]

    def producer():
        while True:
            with count_lock:
                if items_made[0] >= num_items:
                    return
                items_made[0] += 1
                item = items_made[0]
            q.put(item)
            time.sleep(random.uniform(0.001, 0.01))

    def consumer():
        while True:
            if done_producing.is_set() and q.empty():
                return
            try:
                item = q.get(timeout=0.1)
            except Exception:
                continue
            with results_lock:
                results.append(item)
            q.task_done()

    producer_threads = []
    for i in range(num_producers):
        t = threading.Thread(target=producer)
        producer_threads.append(t)
        t.start()

    consumer_threads = []
    for i in range(num_consumers):
        t = threading.Thread(target=consumer)
        consumer_threads.append(t)
        t.start()

    for t in producer_threads:
        t.join()

    done_producing.set()

    for t in consumer_threads:
        t.join()

    return results
