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

node_list_p1 = list(map(parse_node, input_data_p1))
node_lut_p1  = {d['id']: d for d in node_list_p1}
root_p1      = node_list_p1[0]

def link_strong(tree, new_node, lut):
    left = tree.get('left')
    if left is not None:
        if link_strong(lut[left], new_node, lut):
            return True
    else:
        if new_node['plug'] == tree['leftSocket']:
            tree['left'] = new_node['id']
            return True
    right = tree.get('right')
    if right is not None:
        if link_strong(lut[right], new_node, lut):
            return True
    else:
        if new_node['plug'] == tree['rightSocket']:
            tree['right'] = new_node['id']
            return True
    return False

for node in node_list_p1[1:]:
    result = link_strong(root_p1, node, node_lut_p1)
    assert result

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

order_p1 = inorder(root_p1, node_lut_p1)
answer_p1 = sum(i * int(j) for i, j in enumerate(order_p1, start=1))

print("Melody Quest 03, P1:", answer_p1)

node_list_p2 = list(map(parse_node, input_data_p2))
node_lut_p2  = {d['id']: d for d in node_list_p2}
root_p2      = node_list_p2[0]

def link_weak(tree, new_node, lut):
    color_new, shape_new = new_node['plug'].split()
    left = tree.get('left')
    if left is not None:
        if link_weak(lut[left], new_node, lut):
            return True
    else:
        color_sock, shape_sock = tree['leftSocket'].split()
        if color_new == color_sock or shape_new == shape_sock:
            tree['left'] = new_node['id']
            return True
    right = tree.get('right')
    if right is not None:
        if link_weak(lut[right], new_node, lut):
            return True
    else:
        color_sock, shape_sock = tree['rightSocket'].split()
        if color_new == color_sock or shape_new == shape_sock:
            tree['right'] = new_node['id']
            return True
    return False

for node in node_list_p2[1:]:
    result = link_weak(root_p2, node, node_lut_p2)
    assert result

order_p2 = inorder(root_p2, node_lut_p2)
answer_p2 = sum(i * int(j) for i, j in enumerate(order_p2, start=1))

print("Melody Quest 03, P2:", answer_p2)
