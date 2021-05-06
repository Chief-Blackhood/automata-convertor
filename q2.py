import itertools
import sys
import json


class DFA:
    def __init__(self):
        self.start_states = []
        self.final_states = []
        self.transition_function = []


class Graph:
    def __init__(self, vertices):
        self.vertices = len(vertices)
        self.adj = {}
        self.connections = {}
        self.epsilon_covers = {}
        for i in vertices:
            self.connections[i] = {}
            self.epsilon_covers[i] = {}
            self.epsilon_covers[i]['$'] = [i]
            self.adj[i] = []

    def add_edge(self, u, v, input_elm):
        self.adj[u].append([v, input_elm])

    def epsilon_cover(self, source, input_elm, all_states):
        visited = {}
        for state in all_states:
            visited[state] = False

        stack = [source]
        visited[source] = True
        for data in self.adj[source]:
            if data[1] == input_elm:
                stack.append(data[0])
                self.epsilon_covers[source][input_elm].append(data[0])
                visited[data[0]] = True

        while len(stack):
            s = stack.pop()

            if not visited[s]:
                self.epsilon_covers[source][input_elm].append(s)
                visited[s] = True

            for node in self.adj[s]:
                if not visited[node[0]] and node[1] == '$':
                    stack.append(node[0])

    def dfs(self, source, input_elm, all_states):
        visited = {}
        for state in all_states:
            visited[state] = 0

        stack = []
        self.connections[source][input_elm] = []
        for data in self.adj[source]:
            if data[1] == input_elm:
                stack.append(data[0])
                visited[data[0]] += 1

        while len(stack):
            s = stack.pop()

            if visited[s] != 2:
                self.connections[source][input_elm].append(s)
                visited[s] += 1

            for node in self.adj[s]:
                if visited[node[0]] != 2 and node[1] == '$':
                    stack.append(node[0])

        self.connections[source][input_elm] = list(set(self.connections[source][input_elm]))


def main():
    with open(sys.argv[1], "r") as inp:
        data = json.load(inp)
    graph = Graph(data["states"])
    dfa = DFA()
    for transition in data["transition_function"]:
        graph.add_edge(transition[0], transition[2], transition[1])
    for transition in data["transition_function"]:
        if transition[1] != '$':
            graph.dfs(transition[0], transition[1], data["states"])
        else:
            graph.epsilon_cover(transition[0], transition[1], data["states"])
    all_combinations = []
    for size in range(len(data["states"]) + 1):
        combination_object = itertools.combinations(data["states"], size)
        combination_list = list(combination_object)
        all_combinations += combination_list
    all_states = [list(ele) for ele in all_combinations]
    print(graph.connections, graph.adj)
    for state in all_states:
        for letter in data["letters"]:
            states_to_go = []
            for elm in state:
                if letter in graph.connections[elm].keys():
                    states_to_go.extend(graph.connections[elm][letter])
            states_to_go = list(set(states_to_go))
            dfa.transition_function.append([state, letter, states_to_go])
    final_states = []
    for elm in all_states:
        for nfa_f_states in data["final_states"]:
            if nfa_f_states in elm:
                final_states.append(elm)
                break
    final_dfa_dict = {
        'states': all_states,
        'letters': data["letters"],
        'transition_function': dfa.transition_function,
        'start_states': [list(set(graph.epsilon_covers[data["start_states"][0]]['$']))],
        'final_states': final_states
    }
    with open(sys.argv[2], "w") as out:
        json.dump(final_dfa_dict, out)


main()
