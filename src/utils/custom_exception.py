class LabelMismatchException(Exception):
    def __init__(self, first_net_place, second_net_place, first_net_label, second_net_label):
        self.first_net_place = first_net_place
        self.second_net_place = second_net_place
        self.first_net_label = first_net_label
        self.second_net_label = second_net_label

    def get_error_message(self):
        return (f"the place in the first net ({self.first_net_place}) transition is labeled as '{self.first_net_label}',"
                f" while the place in the second net ({self.second_net_place}) transition is labeled as '{self.second_net_label}'")

class MarkingSizeException(Exception):
    def __init__(self, p1, p2, label):
        self.p1 = p1
        self.p2 = p2
        self.label = label

    def get_error_message(self):
        return (f"for place '{self.p1}' in the first net and '{self.p2}' in the second net the transition labeled "
                f"as '{self.label}' produce markings not in R+ (additive closure)")

class DifferentTransitionsException(Exception):
    def __init__(self, couples):
        self.couples = couples

    def get_error_message(self):
        formatted_couples = ", ".join([f"[{couple}]" for couple in self.couples])

        return f"the couples {formatted_couples} can't perform the same transitions" if len(self.couples) > 1 else \
            f"the couple {formatted_couples} can't perform the same transitions"