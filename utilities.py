from collections import Counter

def parse_net(data):
    """Take a Petri Net JSON from online editor in input and return a new, cleaned and improved Petri Net JSON"""

    net_to_return = {}
    start_connections = []
    finish_connections = []
    complete_connections = []

    for key in data:
        if key == "places" or key == "transitions" or key == "arcs":
            net_to_return[key] = []
            match key:
                case "places":
                    for subdict in range(data["nPlaces"]):
                        net_to_return[key].append({})
                        for subkey in data["places"][subdict]:
                            if subkey == "id" or subkey == "name" or subkey == "nTokens":
                                net_to_return[key][subdict][subkey] = data["places"][subdict][subkey]
                            elif subkey == "connections":
                                for connection in data[key][subdict][subkey]:
                                    if connection[0] == "S":
                                        new_connection = f"{data["places"][subdict]["name"]} - {connection.split()[1]} {connection.split()[2]}"
                                        start_connections.append(new_connection)
                                    else:
                                        new_connection = f"{connection.split()[1]} {connection.split()[2]} - {data["places"][subdict]["name"]}"
                                        finish_connections.append(new_connection)
                case "transitions":
                    for subdict in range(data["nTransitions"]):
                        net_to_return[key].append({})
                        for subkey in data["transitions"][subdict]:
                            if subkey == "id" or subkey == "name":
                                net_to_return[key][subdict][subkey] = data["transitions"][subdict][subkey]
                            elif subkey == "connections":
                                for connection in data[key][subdict][subkey]:
                                    if connection[0] == "S":
                                        new_connection = f"{data["transitions"][subdict]["name"]} - {connection.split()[1]} {connection.split()[2]}"
                                        start_connections.append(new_connection)
                                    else:
                                        new_connection = f"{connection.split()[1]} {connection.split()[2]} - {data["transitions"][subdict]["name"]}"
                                        finish_connections.append(new_connection)

                case "arcs":
                    for subdict in range(data["nArcs"]):
                        net_to_return[key].append({})
                        for subkey in data["arcs"][subdict]:
                            if subkey == "id" or subkey == "name" or subkey == "start" or subkey == "end" or subkey == "weight":
                                net_to_return[key][subdict][subkey] = data["arcs"][subdict][subkey]
        else:
            net_to_return[key] = data[key]

    for start_connection in start_connections:
        starting_point = start_connection.split(" - ")[0]
        arc = start_connection.split(" - ")[1]
        complete_connection = f"{starting_point} -> "

        for finish_connection in finish_connections:
            same_arc = finish_connection.split(" - ")[0]
            finish_point = finish_connection.split(" - ")[1]
            if same_arc == arc:
                complete_connection += f"{finish_point}"

        complete_connections.append(complete_connection)

    net_to_return["start_connections"] = start_connections
    net_to_return["finish_connections"] = finish_connections
    net_to_return["complete_connections"] = complete_connections

    return net_to_return

def build_start_marking(net):
    """Take a Petri Net dictionary and return the initial marking m0 for that net"""
    l = []
    for place in net["places"]:
        for _ in range(place["nTokens"]):
            l.append(place["name"])
    return Counter(l)