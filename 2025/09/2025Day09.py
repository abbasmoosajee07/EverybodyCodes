"""Everybody Codes - Quest 9, Year 2025
Solution Started: November 14, 2025
Puzzle Link: https://everybody.codes/event/2025/quests/9
Solution by: Abbas Moosajee
Brief: [Encoded in the Scales]"""

#!/usr/bin/env python3
from collections import defaultdict, deque
from itertools import combinations
from pathlib import Path
from operator import eq
import time
start_time = time.time()
input_files = ["Day09_input_p1.txt", "Day09_input_p2.txt", "Day09_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

def basic_family(family_data):
    parent_1, parent_2 = family_data[0].split(":")[1], family_data[1].split(":")[1]
    child = family_data[2].split(":")[1]
    sim_1, sim_2 = 0, 0
    for child_idx, child_sym in enumerate(child):
        if parent_1[child_idx] == child_sym:
            sim_1 += 1
        if parent_2[child_idx] == child_sym:
            sim_2 += 1
    return sim_1 * sim_2

def build_family_tree(family_data):
    # Parse "id:GENES"
    family_dict = {
        int(person.split(":")[0]): person.split(":")[1]
        for person in family_data
    }

    ids = list(family_dict.keys())
    parent_pairs = list(combinations(ids, 2))
    similarity_sum = 0
    for child in ids:
        child_genes = family_dict[child]
        best_score = 0
        best_parents = None

        for p1, p2 in parent_pairs:
            if child in (p1, p2):
                continue

            a, b = family_dict[p1], family_dict[p2]

            # Only accept genetically valid triples
            if not all(ci == ai or ci == bi for ai, bi, ci in zip(a, b, child_genes)):
                continue

            score = sum(map(eq, child_genes, a)) * sum(map(eq, child_genes, b))

            if score > best_score:
                best_score = score
                best_parents = (p1, p2)

                # print(f"Child {child}: best score = {best_score}, parents = {best_parents}\n")
        similarity_sum  += best_score
    return similarity_sum

def find_largest_family(family_data):

    def child_of(a, b, c):
        # True if c[i] is exactly a[i] or b[i] at each locus
        return all(c[i] == a[i] or c[i] == b[i] for i in range(len(c)))

    # Parse IDs and genomes
    family_dict = {
        int(person.split(":")[0]): person.split(":")[1]
        for person in family_data
    }
    ids = list(family_dict.keys())

    # Build graph
    graph = defaultdict(set)

    # For every pair of parents, find valid children
    for p1, p2 in combinations(ids, 2):
        g1 = family_dict[p1]
        g2 = family_dict[p2]

        for c in ids:
            if c == p1 or c == p2:
                continue
            if child_of(g1, g2, family_dict[c]):
                graph[p1].add(p2)
                graph[p2].add(p1)

                graph[p1].add(c)
                graph[c].add(p1)

                graph[p2].add(c)
                graph[c].add(p2)

    # Get largest connected component
    visited = set()
    largest_size = 0

    for start in ids:
        if start in visited:
            continue

        queue = deque([start])
        component = []

        while queue:
            x = queue.popleft()
            if x in visited:
                continue
            visited.add(x)
            component.append(x)
            for nxt in graph[x]:
                if nxt not in visited:
                    queue.append(nxt)

        largest_size = max(largest_size, sum(component))

    return largest_size

print("Quest 09, P1:", basic_family(input_data_p1))
print("Quest 09, P2:", build_family_tree(input_data_p2))
print("Quest 09, P3:", find_largest_family(input_data_p3))

print(f"Execution Time: {time.time() - start_time:5f}s")
