import json
import utilities
import itertools

with open('nets/first_net.json', 'r') as file:
    raw_first_net = json.load(file)

with open('nets/second_net.json', 'r') as file:
    raw_second_net = json.load(file)

first_net = utilities.parse_net(raw_first_net)
second_net = utilities.parse_net(raw_second_net)

first_net_m0 = utilities.build_start_marking(first_net)
second_net_m0 = utilities.build_start_marking(second_net)

#first_net_pre_post_sets = utilities.build_transitions_pre_post_sets(first_net)
#second_net_pre_post_sets = utilities.build_transitions_pre_post_sets(second_net)

#print(f"first: {json.dumps(first_net_pre_post_sets)}")
#print(f"second: {second_net_pre_post_sets}")


print(first_net_m0)
print(second_net_m0)
print(json.dumps(second_net, indent=2))

prova = list(first_net_m0.keys()) + list(second_net_m0.keys())
prova = list(itertools.combinations(prova, 2))
print(prova)
