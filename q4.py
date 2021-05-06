import copy
import json
import sys


def main():
    with open(sys.argv[1], "r") as inp:
        data = json.load(inp)

    state_connections = {}
    for state in data["states"]:
        state_connections[state] = {}

    for transition in data["transition_function"]:
        state_connections[transition[0]][transition[1]] = transition[2]
    reachable_states = set()
    new_states = set()
    for s_state in data["start_states"]:
        reachable_states.add(s_state)
        new_states.add(s_state)
    while new_states != set():
        temp = set()
        for state in new_states:
            for letter in data["letters"]:
                if letter in state_connections[state].keys():
                    temp.add(state_connections[state][letter])
        new_states = temp.difference(reachable_states)
        reachable_states = reachable_states.union(new_states)
    partition = [set(), set()]
    for state in reachable_states:
        if state in data["final_states"]:
            partition[0].add(state)
        else:
            partition[1].add(state)
    W = copy.deepcopy(partition)
    while len(W):
        set_to_remove = W.pop()
        X = set()
        for letter in data["letters"]:
            for state in reachable_states:
                if state_connections[state][letter] in set_to_remove:
                    X.add(state)
        state_sets_to_add = []
        state_sets_to_remove = []
        for states_set in partition:
            if bool(states_set.intersection(X)) and bool(states_set.difference(X)):
                state_sets_to_remove.append(states_set)
                state_sets_to_add.append(states_set.intersection(X))
                state_sets_to_add.append(states_set.difference(X))
                if states_set in W:
                    W.remove(states_set)
                    W.append(states_set.intersection(X))
                    W.append(states_set.difference(X))
                else:
                    if len(states_set.intersection(X)) <= len(states_set.difference(X)):
                        W.append(states_set.intersection(X))
                    else:
                        W.append(states_set.difference(X))
        for i in state_sets_to_remove:
            partition.remove(i)
        for i in state_sets_to_add:
            partition.append(i)

    partition = [list(i) for i in partition]
    transition_function = []
    start_state = []
    for state_p in partition:
        if data["start_states"][0] in state_p:
            start_state.extend(state_p)
        for letter in data["letters"]:
            state_to_go = []
            for states in partition:
                if state_connections[state_p[0]][letter] in states:
                    state_to_go = states
                    break
            transition_function.append([state_p, letter, state_to_go])

    final_states = []
    for i in partition:
        for state in i:
            if state in data["final_states"]:
                final_states.append(i)
                break

    final_optimized_dfa_dict = {
        'states': partition,
        'letters': data["letters"],
        'transition_function': transition_function,
        'start_states': [start_state],
        'final_states': final_states
    }
    with open(sys.argv[2], "w") as out:
        json.dump(final_optimized_dfa_dict, out)


main()