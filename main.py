import json
import utilities

with open('nets/first_net.json', 'r') as file:
    raw_first_net = json.load(file)

with open('nets/second_net.json', 'r') as file:
    raw_second_net = json.load(file)

first_net = utilities.parse_net(raw_first_net)
second_net = utilities.parse_net(raw_second_net)

first_net_m0 = utilities.build_start_marking(first_net)
second_net_m0 = utilities.build_start_marking(second_net)

transitions_post_pre_sets = {}

for transition in first_net["transitions"]:
    transitions_post_pre_sets[transition["name"]] = {"preset": [], "postset": []}
    for arc in first_net["arcs"]:
        if transition["id"] == arc["end"]:
            transitions_post_pre_sets[transition]["preset"].add(arc["start"])
        else:
            transitions_post_pre_sets[transition]["postset"].add(arc["end"])




print(json.dumps(first_net, indent=2))
print(transitions_post_pre_sets)
