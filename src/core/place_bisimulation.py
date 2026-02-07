import itertools
from collections import Counter
from src.utils.custom_exception import LabelMismatchException, MarkingSizeException, DifferentTransitionsException


class PlaceBisimulation:

    def __init__(self, net1, net2):
        self.net1 = net1
        self.net2 = net2

        # build initial markings for both nets
        self.net1_m0, self.net2_m0 = self._build_start_marking()

        # build presets, postsets and label for every transition in both nets
        self.net1_presets, self.net1_postsets, self.net1_labels = extract_transition_info(net1)
        self.net2_presets, self.net2_postsets, self.net2_labels = extract_transition_info(net2)

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

    def build_rr(self, first_net_transition_postset, second_net_transition_postset):
        """Build only valid RR set. If transitions differ then the couple is pruned."""

        if first_net_transition_postset is None and second_net_transition_postset is None:
            l1 = self.net1_m0.keys()
            l2 = self.net2_m0.keys()
        else:
            l1 = first_net_transition_postset.keys()
            l2 = second_net_transition_postset.keys()

        # create all the possible sets from the initial markings
        possibilities = [set(zip(l1, p)) for p in itertools.permutations(l2)]
        refined_possibilities = []
        discarded_couples = []

        # refinement step to prune unextendable sets due to possible transitions difference
        for p in possibilities:
            refined_possibility = set()
            possibility_is_valid = True

            for couple in p:
                # extract the transitions labels
                (first_place_transitions_label, second_place_transitions_label) = self.transitions_4_preset_place(
                    couple[0], couple[1],True)

                # check if the labels coincide. If so is a valid couple, if not the couple is discarded.
                if check_labels(first_place_transitions_label, second_place_transitions_label):
                    refined_possibility.add(couple)
                else:
                    discarded_couples.append(couple)
                    possibility_is_valid = False
                    break
            if possibility_is_valid:
                refined_possibilities.append(refined_possibility)


        return refined_possibilities, discarded_couples

    def transitions_4_preset_place(self, first_place, second_place, only_labels):
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

        if only_labels:
            return labels1, labels2
        else:
            return labels1, id1, labels2, id2

    def try_bisimulation(self, rr):
        """Implements the main cycle where tests the forward and backward behavior"""
        r = []
        expanded_couples = []
        message = ""

        while len(rr) > 0:
            possible_solution = rr.pop()

            # check if every couple in the possible solution has been expanded
            all_couple_expanded = all(couple in expanded_couples for couple in possible_solution)

            if not all_couple_expanded:
                for couple in possible_solution:
                    # check if the selected couple has already been expanded. If so it tries to expand it, otherwise it goes to the next couple
                    if couple not in expanded_couples:
                        try:
                            (first_place_transitions_label,
                             first_place_transitions_id,
                             second_place_transitions_label,
                             second_place_transitions_id) = self.transitions_4_preset_place(
                                couple[0],
                                couple[1],
                                False)

                            # check for a label mismatch. If present raise a Label Mismatch Exception
                            if not check_labels(first_place_transitions_label, second_place_transitions_label):
                                raise LabelMismatchException(first_net_place=couple[0], second_net_place=couple[1],
                                                             first_net_label=first_place_transitions_label,
                                                             second_net_label=second_place_transitions_label)

                            # start cycling through all transitions in both nets for the couple under examination
                            for transition1 in first_place_transitions_id:
                                first_net_transition_label = self.net1_labels[transition1]
                                first_net_transition_postset = self.net1_postsets[transition1]
                                for transition2 in second_place_transitions_id:
                                    second_net_transition_label = self.net2_labels[transition2]
                                    second_net_transition_postset = self.net2_postsets[transition2]

                                    # check if the post sets produced are in R+. If not raises a Marking Size Exception
                                    if (first_net_transition_label == second_net_transition_label
                                            and sum(first_net_transition_postset.values())
                                            == sum(second_net_transition_postset.values())):

                                        # expands the couple and return new valid couples to be attached to the solution and the discarded ones due to transitions labels difference
                                        new_couples, discarded_couples = self.build_rr(
                                            first_net_transition_postset,
                                            second_net_transition_postset)

                                        # if there isn't at least one new valid couple then it raises a Different Transitions Exception
                                        if not new_couples:
                                            raise DifferentTransitionsException(discarded_couples)

                                        # for every new valid couple it extends the current solution with the new couple creating new possible solutions to be examined
                                        for n_c in new_couples:
                                            current_solution = possible_solution.copy()

                                            current_solution.update(n_c)

                                            # add the new possible solution to RR only if not already present
                                            if current_solution not in rr:
                                                rr.append(current_solution)
                                    else:
                                        raise MarkingSizeException(p1=couple[0], p2=couple[1],
                                                                      label=first_net_transition_label)

                        # for every exception it updates the error message to be displayed to the user and remove the invalid solutions from RR
                        except (LabelMismatchException, MarkingSizeException, DifferentTransitionsException) as e:
                            message = e.get_error_message()
                            rr = [x for x in rr if couple not in x]

                        # when the expansion finish without problems it marks the couple as expanded
                        else:
                            expanded_couples.append(couple)
                            # if the expansion has ended correctly because we were in a couple with no transitions it adds again the solution to RR in order to expand the other couples
                            if not first_place_transitions_id:
                                rr.append(possible_solution)

                        # break the cycle in order to check a new solution
                        break
            else:
                r = possible_solution

        return r, message

def check_labels(first_place_transitions_label, second_place_transitions_label):
    """If a place in a net is preset for a transition that the other place isn't preset for, then we discard
    the relation. e.g. A = ['prod'], B = ['prod', 'prod'] ok, instead if B = ['prod', 'prod', 'del'] no"""

    return Counter(first_place_transitions_label).keys() == Counter(second_place_transitions_label).keys()

def get_place_name(net, place_id):
    """Return a place name given a net and a place id"""
    for place in net["places"]:
        if place["id"] == place_id:
            return place["name"]
    return None

def extract_transition_info(net):
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
                place_name = get_place_name(net, arc["start"])
                # creating a list with as many equal places as is the arc weight and then adding all of them
                # individually to preset list
                preset.extend([place_name] * weight)

            # arcs getting out the transition give us places in postset
            elif arc["start"] == t_id:
                place_name = get_place_name(net, arc["end"])
                postset.extend([place_name] * weight)

        # using transitions id as the key due to the possibility of multiple transitions equally labeled
        presets[t_id] = Counter(preset)
        postsets[t_id] = Counter(postset)
        labels[t_id] = t_name

    return presets, postsets, labels

def find_bisimulation(net1, net2):
    pb = PlaceBisimulation(net1=net1, net2=net2)

    # verifying additive closure for the two initial markings. If they differ we terminate, there is no
    # place bisimilarity
    if sum(pb.net1_m0.values()) != sum(pb.net2_m0.values()):
        return [], "the initial markings are not in R+ (additive closure) so the two nets cannot be place bisimilar"

    rr, _ = pb.build_rr(first_net_transition_postset=None, second_net_transition_postset=None)
    r, message = pb.try_bisimulation(rr)

    return r, message
