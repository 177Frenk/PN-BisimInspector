from collections import Counter

def parse_net(data):
    """Take a Petri Net JSON from online editor in input and return a new, cleaned and improved Petri Net JSON"""

    net_to_return = {}
    start_connections = []
    finish_connections = []
    complete_connections = []

    for key in data:    #cycling through all keys in the net dictionary
        if key == "places" or key == "transitions" or key == "arcs":    #cleaning places, transitions and arcs keys keeping only useful information
            net_to_return[key] = []    #creating a new key: list inside the net to return dictionary
            match key:
                case "places":
                    for subdict in range(data["nPlaces"]):    #cycling through all places using the nPlaces key
                        net_to_return[key].append({})    #creating a new place: dictionary inside the new places list for every place
                        for subkey in data["places"][subdict]:    #cycling through all key of a single place
                            if subkey == "id" or subkey == "name" or subkey == "nTokens":
                                net_to_return[key][subdict][subkey] = data["places"][subdict][subkey]    #if key is one of the three simply adding it to the new dictionary
                            elif subkey == "connections":
                                for connection in data[key][subdict][subkey]:    #for every connection in the connection key we check if it's a start or finish connection
                                    if connection[0] == "S":
                                        new_connection = f"{data["places"][subdict]["name"]} - {connection.split()[1]} {connection.split()[2]}"
                                        start_connections.append(new_connection)    #adding the connection to the start connections helper list
                                    else:
                                        new_connection = f"{connection.split()[1]} {connection.split()[2]} - {data["places"][subdict]["name"]}"
                                        finish_connections.append(new_connection)    #adding the connection to the finish connections helper list
                case "transitions":    #transitions get the same treatment as places
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

                case "arcs":    #keeping only id, name, start, end and weight for the arcs
                    for subdict in range(data["nArcs"]):
                        net_to_return[key].append({})
                        for subkey in data["arcs"][subdict]:
                            if subkey == "id" or subkey == "name" or subkey == "start" or subkey == "end" or subkey == "weight":
                                net_to_return[key][subdict][subkey] = data["arcs"][subdict][subkey]
        else:
            net_to_return[key] = data[key]    #keeping nPlaces, nTransitions and nArcs unchanged

    for start_connection in start_connections:    #formatting all connections for better understanding
        starting_point = start_connection.split(" - ")[0]    #isolating place or transition in starting point
        arc = start_connection.split(" - ")[1]    #isolating arc for later use
        complete_connection = f"{starting_point} -> "    #add the starting point for the complete connection i.e. place1 -> ... | transition1 -> ...

        for finish_connection in finish_connections:    #cycling on the finish connections to add the landing point to the complete connection
            same_arc = finish_connection.split(" - ")[0]    #isolating arc to match with previous arc
            finish_point = finish_connection.split(" - ")[1]    #isolating place or transition in finish point
            if same_arc == arc:    #if the arc is the same of the same_arc we got the correct landing point
                complete_connection += f"{finish_point}"    #adding the landing point to the complete connection i.e. place1 -> transition1 | transition1 -> place1

        complete_connections.append(complete_connection)

    net_to_return["start_connections"] = start_connections
    net_to_return["finish_connections"] = finish_connections
    net_to_return["complete_connections"] = complete_connections

    return net_to_return    #return the new formatted net dictionary with only the useful information

def build_start_marking(net):
    """Take a Petri Net dictionary and return the initial marking m0 for that net"""
    l = []
    for place in net["places"]:
        for _ in range(place["nTokens"]):
            l.append(place["name"])    #append to l the place name n times as there are tokens in that place so that passing l to Counter() will give us the mark for that place
    return Counter(l)