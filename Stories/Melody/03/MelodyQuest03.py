"""Everybody Codes - Quest 3, Story Melody Made of Code
Solution Started: March 6, 2026
Puzzle Link: https://everybody.codes/story/3/quests/3
Solution by: Abbas Moosajee
Brief: [Plug and Play]"""

#!/usr/bin/env python3
from pathlib import Path

input_files = ["Quest03_input_p1.txt", "Quest03_input_p2.txt", "Quest03_input_p3.txt"]

# Read and split the input data into individual lists
input_data_p1, input_data_p2, input_data_p3 = [
    open(Path(__file__).parent / file).read().strip().split('\n')
    for file in input_files
]

def parse_node(line):
    record = {}
    for entry in line.split(', '):
        k, v = entry.split('=')
        record[k] = v
    return record

def inorder(tree, lut, out=None):
    if out is None:
        out = []
    left = tree.get('left')
    if left is not None:
        inorder(lut[left], lut, out)
    out.append(tree['id'])
    right = tree.get('right')
    if right is not None:
        inorder(lut[right], lut, out)
    return out

def strong_match(a, b):
    return a == b

def weak_match(a, b):
    color_a, shape_a = a.split()
    color_b, shape_b = b.split()
    return color_a == color_b or shape_a == shape_b

def strict_weak_match(a, b):
    color_a, shape_a = a.split()
    color_b, shape_b = b.split()
    return (color_a == color_b) != (shape_a == shape_b)

node_list_p1 = list(map(parse_node, input_data_p1))
node_lut_p1  = {d['id']: d for d in node_list_p1}
root_p1      = node_list_p1[0]

def link_node_p1(tree, new_node):
    left = tree.get('left')
    if left is not None:
        if link_node_p1(node_lut_p1[left], new_node):
            return True
    else:
        if strong_match(new_node['plug'], tree['leftSocket']):
            tree['left'] = new_node['id']
            return True
    right = tree.get('right')
    if right is not None:
        if link_node_p1(node_lut_p1[right], new_node):
            return True
    else:
        if strong_match(new_node['plug'], tree['rightSocket']):
            tree['right'] = new_node['id']
            return True
    return False

for node in node_list_p1[1:]:
    result = link_node_p1(root_p1, node)
    assert result

order_p1 = inorder(root_p1, node_lut_p1)
answer_p1 = sum(i * int(j) for i, j in enumerate(order_p1, start=1))

print("Melody Quest 03, P1:", answer_p1)

node_list_p2 = list(map(parse_node, input_data_p2))
node_lut_p2  = {d['id']: d for d in node_list_p2}
root_p2      = node_list_p2[0]

def link_node_p2(tree, new_node):
    left = tree.get('left')
    if left is not None:
        if link_node_p2(node_lut_p2[left], new_node):
            return True
    else:
        if weak_match(new_node['plug'], tree['leftSocket']):
            tree['left'] = new_node['id']
            return True
    right = tree.get('right')
    if right is not None:
        if link_node_p2(node_lut_p2[right], new_node):
            return True
    else:
        if weak_match(new_node['plug'], tree['rightSocket']):
            tree['right'] = new_node['id']
            return True
    return False

for node in node_list_p2[1:]:
    result = link_node_p2(root_p2, node)
    assert result

order_p2 = inorder(root_p2, node_lut_p2)
answer_p2 = sum(i * int(j) for i, j in enumerate(order_p2, start=1))

print("Melody Quest 03, P2:", answer_p2)

node_list_p3 = list(map(parse_node, input_data_p3))
node_lut_p3  = {d['id']: d for d in node_list_p3}
root_p3      = node_list_p3[0]

def link_node_p3(tree, new_node):
    left = tree.get('left')
    if left is None:
        if weak_match(new_node['plug'], tree['leftSocket']):
            tree['left'] = new_node['id']
            return None
    elif strict_weak_match(node_lut_p3[left]['plug'], tree['leftSocket']) and strong_match(new_node['plug'], tree['leftSocket']):
        tree['left'] = new_node['id']
        new_node = node_lut_p3[left]
    else:
        new_node = link_node_p3(node_lut_p3[left], new_node)
    if new_node is None:
        return None
    right = tree.get('right')
    if right is None:
        if weak_match(new_node['plug'], tree['rightSocket']):
            tree['right'] = new_node['id']
            return None
    elif strict_weak_match(node_lut_p3[right]['plug'], tree['rightSocket']) and strong_match(new_node['plug'], tree['rightSocket']):
        tree['right'] = new_node['id']
        new_node = node_lut_p3[right]
    else:
        new_node = link_node_p3(node_lut_p3[right], new_node)
    return new_node

for node in node_list_p3[1:]:
    while node:
        node = link_node_p3(root_p3, node)

order_p3 = inorder(root_p3, node_lut_p3)
answer_p3 = sum(i * int(j) for i, j in enumerate(order_p3, start=1))

print("Melody Quest 03, P3:", answer_p3)