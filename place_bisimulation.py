from collections import Counter

class PlaceBisimulation:

    def __init__(self, net1, net2):
        self.net1 = net1
        self.net2 = net2

        # build initial markings for both nets
        self.net1_m0, self.net2_m0 = self._build_start_marking()

        # build presets, postsets and label for every transition in both nets

    def _build_start_marking(self):
        """Return the initial marking m0 for both nets"""
        l1 = []
        l2 = []
        for i in range (2):
            if i == 0:
                for place in self.net1["places"]:
                    for _ in range(place["nTokens"]):
                        l1.append(place["name"])  # append to l the place name n times as there are tokens in that place so that passing l to Counter() will give us the mark for that place
            elif i == 1:
                for place in self.net2["places"]:
                    for _ in range(place["nTokens"]):
                        l2.append(place["name"])

        return Counter(l1), Counter(l2)
