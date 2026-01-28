import itertools
from collections import Counter

class PlaceBisimulation:

    def __init__(self, net1, net2):
        self.net1 = net1
        self.net2 = net2

        # build initial markings for both nets
        self.net1_m0, self.net2_m0 = self._build_start_marking()

        # build presets, postsets and label for every transition in both nets
        self.net1_presets, self.net1_postsets, self.net1_labels = self._extract_transition_info(net1)
        self.net2_presets, self.net2_postsets, self.net2_labels = self._extract_transition_info(net2)

    def _build_start_marking(self):
        """Return the initial marking m0 for both nets"""
        l1 = []
        l2 = []
        for i in range (2):
            if i == 0:
                for place in self.net1["places"]:
                    for _ in range(place["nTokens"]):
                        # append to l the place name n times as there are tokens in that place so that passing
                        # l to Counter() will give us the mark for that place
                        l1.append(place["name"])
            elif i == 1:
                for place in self.net2["places"]:
                    for _ in range(place["nTokens"]):
                        l2.append(place["name"])

        return Counter(l1), Counter(l2)

    def _extract_transition_info(self, net):
        """Extract and build presets, postsets and label for every transition"""
        presets = {}
        postsets = {}
        labels = {}

        # cycling through all transitions
        for transition in net["transitions"]:
            t_id = transition["id"]
            t_name = transition["name"]

            preset = []
            postset = []

            # cycling through all arcs
            for arc in net["arcs"]:
                weight = arc.get("weight", 1)

                # arcs getting in the transition give us places in preset
                if arc["end"] == t_id:
                    place_name = self._get_place_name(net, arc["start"])
                    # creating a list with as many equal places as is the arc weight and then adding all of them
                    # individually to preset list
                    preset.extend([place_name] * weight)

                # arcs getting out the transition give us places in postset
                elif arc["start"] == t_id:
                    place_name = self._get_place_name(net, arc["end"])
                    postset.extend([place_name] * weight)

            # using transitions id as the key due to the possibility of multiple transitions equally labeled
            presets[t_id] = Counter(preset)
            postsets[t_id] = Counter(postset)
            labels[t_id] = t_name

        return presets, postsets, labels

    def _get_place_name(self, net, place_id):
        """Return a place name given a net and a place id"""
        for place in net["places"]:
            if place["id"] == place_id:
                return place["name"]
        return None

    def build_rr(self, first_net_transition_postset, second_net_transition_postset):
        """Build RR set"""
        l1 = []
        l2 = []

        if first_net_transition_postset is None and second_net_transition_postset is None:
            l1 = self.net1_m0.keys()
            l2 = self.net2_m0.keys()
        else:
            l1 = first_net_transition_postset.keys()
            l2 = second_net_transition_postset.keys()

        return list(itertools.product(l1, l2))

    def transitions_4_preset_place(self, first_place, second_place):
        """Returns a list containing all the transitions for which the place is in the preset"""
        labels1 = []
        labels2 = []
        id1 = []
        id2 = []

        # cycling through the preset dictionary and looking if the place is present. If so, adding the transition
        for transition in self.net1_presets:
            pl = list(self.net1_presets[transition].keys())

            if first_place in pl:
                labels1.append(self.net1_labels[transition])
                id1.append(transition)

        for transition in self.net2_presets:
            pl = list(self.net2_presets[transition].keys())

            if second_place in pl:
                labels2.append(self.net2_labels[transition])
                id2.append(transition)

        return labels1, id1, labels2, id2

    def try_bisimulation(self, rr):
        """Implements the main cycle where tests the forward and backward behavior"""
        r = []

        while len(rr) > 0:
            rel = rr.pop(0)

            if rel not in r:
                can_add_rel = True

                (first_place_transitions_label, first_place_transitions_id,
                 second_place_transitions_label, second_place_transitions_id) = self.transitions_4_preset_place(rel[0],
                                                                                                                rel[1])

                # if a place in a net is preset for a transition that the other place isn't preset for then we discard
                # the relation. e.g. A = ['prod'], B = ['prod', 'prod'] ok, instead if B = ['prod', 'prod', 'del'] no
                if Counter(first_place_transitions_label).keys() == Counter(second_place_transitions_label).keys():
                    # forward check
                    for transition1 in first_place_transitions_id:
                        first_net_transition_label = self.net1_labels[transition1]
                        first_net_transition_postset = self.net1_postsets[transition1]
                        for transition2 in second_place_transitions_id:
                            second_net_transition_label = self.net2_labels[transition2]
                            second_net_transition_postset = self.net2_postsets[transition2]

                            # check if labels are equal and in |m| are equal. If not dump the couple
                            if (first_net_transition_label == second_net_transition_label
                                    and sum(first_net_transition_postset.values())
                                    == sum(second_net_transition_postset.values())):
                                new_rrs = self.build_rr(first_net_transition_postset, second_net_transition_postset)

                                # every new couple still not in rr will be added to be checked later
                                for new_rr in new_rrs:
                                    if new_rr not in rr:
                                        rr.append(new_rr)
                            else:
                                can_add_rel = False

                    # backward check
                    for transition1 in second_place_transitions_id:
                        second_net_transition_label = self.net2_labels[transition1]
                        second_net_transition_postset = self.net2_postsets[transition1]

                        for transition2 in first_place_transitions_id:
                            first_net_transition_label = self.net1_labels[transition2]
                            first_net_transition_postset = self.net1_postsets[transition2]

                            if second_net_transition_label == first_net_transition_label:
                                new_rrs = self.build_rr(first_net_transition_postset, second_net_transition_postset)

                                for new_rr in new_rrs:
                                    if new_rr not in rr:
                                        rr.append(new_rr)
                            else:
                                can_add_rel = False
                else:
                    can_add_rel = False

                if can_add_rel:
                    r.append(rel)

        return r

    def refine_solution_set(self, r):
        """Perform last check on solution set R to see if the two nets are bisimilar"""

        refined_r = r

        for couple in r:
            (first_place_transitions_label, first_place_transitions_id,
             second_place_transitions_label, second_place_transitions_id) = self.transitions_4_preset_place(couple[0],
                                                                                                            couple[1])
            for transition1 in first_place_transitions_id:
                first_net_transition_postset = self.net1_postsets[transition1]
                for transition2 in second_place_transitions_id:
                    second_net_transition_postset = self.net2_postsets[transition2]

                    new_rrs = self.build_rr(first_net_transition_postset, second_net_transition_postset)

                    if not any(couple in r for couple in new_rrs):
                        refined_r.remove(couple)

        return refined_r

    def print_information(self):
        print(f"net1m0: {self.net1_m0}\n"
              f"net1presets: {self.net1_presets}\n"
              f"net1postsets: {self.net1_postsets}\n"
              f"net1labels: {self.net1_labels}")
        print("\n"*10)
        print(f"net1m0: {self.net2_m0}\n"
              f"net1presets: {self.net2_presets}\n"
              f"net1postsets: {self.net2_postsets}\n"
              f"net1labels: {self.net2_labels}")

def find_bisimulation(net1, net2):
    pb = PlaceBisimulation(net1=net1, net2=net2)

    # verifying additive closure for the two initial markings. If they differ we terminate, there is no
    # place bisimilarity
    if sum(pb.net1_m0.values()) != sum(pb.net2_m0.values()):
        return []

    rr = pb.build_rr(first_net_transition_postset=None, second_net_transition_postset=None)
    r = pb.try_bisimulation(rr)
    refined_r = pb.refine_solution_set(r)

    return refined_r