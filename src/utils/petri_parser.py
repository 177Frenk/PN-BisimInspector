def parse_net(data):
    """Take a Petri Net JSON from online editor in input and return a new and cleaned Petri Net dictionary"""

    net_to_return = {}

    # cycling through all keys in the net dictionary
    for key in data:
        # cleaning places, transitions and arcs keys keeping only useful information
        if key == "places" or key == "transitions" or key == "arcs":
            # creating a new key: list inside the net to return dictionary
            net_to_return[key] = []
            match key:
                case "places":
                    # cycling through all places using the nPlaces key
                    for subdict in range(data["nPlaces"]):
                        # creating a new place: dictionary inside the new places list for every place
                        net_to_return[key].append({})
                        # cycling through all key of a single place
                        for subkey in data["places"][subdict]:
                            if subkey == "id" or subkey == "name" or subkey == "nTokens":
                                # if key is one of the three simply adding it to the new dictionary
                                net_to_return[key][subdict][subkey] = data["places"][subdict][subkey]
                # transitions get the same treatment as places
                case "transitions":
                    for subdict in range(data["nTransitions"]):
                        net_to_return[key].append({})
                        for subkey in data["transitions"][subdict]:
                            if subkey == "id" or subkey == "name":
                                net_to_return[key][subdict][subkey] = data["transitions"][subdict][subkey]
                # keeping only id, name, start, end and weight for the arcs
                case "arcs":
                    for subdict in range(data["nArcs"]):
                        net_to_return[key].append({})
                        for subkey in data["arcs"][subdict]:
                            if subkey == "id" or subkey == "name" or subkey == "start" or subkey == "end" or subkey == "weight":
                                net_to_return[key][subdict][subkey] = data["arcs"][subdict][subkey]
        else:
            # keeping nPlaces, nTransitions and nArcs unchanged
            net_to_return[key] = data[key]

    # return the new formatted net dictionary with only the useful information
    return net_to_return