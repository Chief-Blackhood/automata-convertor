import json
import sys


def main():
    with open(sys.argv[1], "r") as inp:
        data = json.load(inp)
    for state in data["start_states"]:
        data["transition_function"].append(["Qs", "$", state])
    for state in data["final_states"]:
        data["transition_function"].append([state, "$", "Qf"])
    for state in data["states"]:
        into = {}
        outgoing = {}
        loop = ""
        transitions_to_remove = []
        for index, transition in enumerate(data["transition_function"]):
            if transition[0] == state and transition[2] == state:
                if len(loop) == 0:
                    loop += transition[1]
                else:
                    loop += "+" + transition[1]
                transitions_to_remove.append(index)
            elif transition[0] == state:
                if transition[2] in outgoing.keys():
                    outgoing[transition[2]] += "+" + transition[1]
                else:
                    outgoing[transition[2]] = transition[1]
                transitions_to_remove.append(index)
            elif transition[2] == state:
                if transition[0] in into.keys():
                    into[transition[0]] += "+" + transition[1]
                else:
                    into[transition[0]] = transition[1]
                transitions_to_remove.append(index)

        data["transition_function"] = [i for index, i in enumerate(data["transition_function"]) if
                                       index not in transitions_to_remove]
        for i in into:
            for j in outgoing:
                if len(into[i]) != 1:
                    into[i] = "(" + into[i] + ")"
                if len(outgoing[j]) != 1:
                    outgoing[j] = "(" + outgoing[j] + ")"
                if loop != "":
                    if len(loop) != 1:
                        loop = "(" + loop + ")"
                    data["transition_function"].append([i, into[i] + loop + "*" + outgoing[j], j])
                else:
                    data["transition_function"].append([i, into[i] + outgoing[j], j])
    regex = ""
    for transition in data["transition_function"]:
        regex += transition[1]+"+"
    regex = regex[:-1]
    final_regex_dict = {
        'regex': regex,
    }
    with open(sys.argv[2], "w") as out:
        json.dump(final_regex_dict, out)


main()
