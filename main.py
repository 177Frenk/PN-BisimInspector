import json
from pathlib import Path
from src.utils.petri_mapper import map_net
from src.core.place_bisimulation import find_bisimulation

# Path configuration
folder = Path('nets')
files = list(folder.glob('*.json'))
count = len(files)

# Check on files count
if count <= 1:
    print(f"Error: {count} net found. Please insert at least 2 .json files in '{folder}' folder.")
    exit()

elif count == 2:
    # Automatically select the only two files in the folder
    first_net_path = files[0]
    second_net_path = files[1]
    print(f"Exactly 2 nets found. Analyzing: {first_net_path.name} and {second_net_path.name}")

else:
    # More than 2 files, asking for input
    print(f"Found {count} nets.")

    in1 = input("Provide the first net (without .json): ")
    in2 = input("Provide the second net (without .json): ")

    # Selection of defaults file if input don't exist
    p1 = folder / f"{in1}.json"
    p2 = folder / f"{in2}.json"

    if p1.exists():
        first_net_path = p1
    else:
        first_net_path = folder / "first_net.json"
        print(f"Warning: '{in1}.json' not found. Utilizing default: {first_net_path.name}")

    if p2.exists():
        second_net_path = p2
    else:
        second_net_path = folder / "second_net.json"
        print(f"Warning: '{in2}.json' not found. Utilizing default: {second_net_path.name}")

    print(f"Analysing: {first_net_path.name} and {second_net_path.name}")

try:
    with open(first_net_path, 'r') as f1, open(second_net_path, 'r') as f2:
        raw_first_net = json.load(f1)
        raw_second_net = json.load(f2)
except FileNotFoundError:
    print("Critical error: No default files found.")
    exit()

first_net = map_net(raw_first_net)
second_net = map_net(raw_second_net)

final_set, message = find_bisimulation(net1=first_net, net2=second_net)

if len(final_set) > 0:
    print(f"We got a solution!\n{final_set}\n"
          f"The two nets are place bisimilar!")
else:
    print(f"Impossible to find a solution.\n"
          f"The two nets are not place bisimilar because {message}.")