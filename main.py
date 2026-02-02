import json
from petri_parser import parse_net
from place_bisimulation import find_bisimulation

with open('nets/coffeenet.json', 'r') as file:
    raw_first_net = json.load(file)

with open('nets/coffeeteanet.json', 'r') as file:
    raw_second_net = json.load(file)

first_net = parse_net(raw_first_net)
second_net = parse_net(raw_second_net)

#print(json.dumps(second_net, indent=2))

final_set, message = find_bisimulation(net1=first_net, net2=second_net)

if len(final_set) > 0:
    print(f"We got a solution! {final_set}\n"
          f"The two nets are place bisimilar!")
else:
    print(f"Impossible to find a solution.\n"
          f"The two nets are not place bisimilar because {message}.")