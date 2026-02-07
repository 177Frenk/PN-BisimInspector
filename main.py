import json
from src.utils.petri_parser import parse_net
from src.core.place_bisimulation import find_bisimulation

with open('nets/first_net.json', 'r') as file:
    raw_first_net = json.load(file)

with open('nets/second_net.json', 'r') as file:
    raw_second_net = json.load(file)

first_net = parse_net(raw_first_net)
second_net = parse_net(raw_second_net)

final_set, message = find_bisimulation(net1=first_net, net2=second_net)

if len(final_set) > 0:
    print(f"We got a solution! {final_set}\n"
          f"The two nets are place bisimilar!")
else:
    print(f"Impossible to find a solution.\n"
          f"The two nets are not place bisimilar because {message}.")