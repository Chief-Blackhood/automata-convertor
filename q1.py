#!/usr/bin/python
import copy
import json
import sys


class NFA:
    def __init__(self):
        self.start_states = []
        self.final_states = []
        self.transition_function = []


def preprocess(regex):
    input_elm = set()
    concat_regex = "("
    for i in range(len(regex)):
        cur_char = regex[i]
        concat_regex += cur_char
        if cur_char.isnumeric() or cur_char.islower():
            input_elm.add(cur_char)
        if i+1 != len(regex):
            next_char = regex[i+1]
        else:
            continue
        if (cur_char.isnumeric() or cur_char.islower() or cur_char == ')') and\
                (next_char.isnumeric() or next_char.islower() or next_char == '('):
            concat_regex += '.'
        elif cur_char == '*' and (next_char.isnumeric() or next_char.islower() or next_char == '('):
            concat_regex += '.'
    concat_regex += ')'
    return concat_regex, input_elm


def postfix(regex):
    postfix_regex = ""
    stack = []
    for i in range(len(regex)):
        if regex[i] == '+':
            while len(stack) and stack[-1] != '(':
                postfix_regex += stack.pop()
            stack.append(regex[i])
        elif regex[i] == ')':
            while len(stack) and stack[-1] != '(':
                postfix_regex += stack.pop()
            stack.pop()
        elif regex[i] == '.':
            while len(stack) and stack[-1] == '.':
                postfix_regex += stack.pop()
            stack.append(regex[i])
        elif regex[i] == '(':
            stack.append(regex[i])
        else:
            postfix_regex += regex[i]
    while len(stack):
        postfix_regex += stack.pop()
    return postfix_regex


def reg_nfa(regular_exp):
    nfa_stack = []
    states = 0
    for i in regular_exp:
        if i == '.':
            nfa_2 = nfa_stack.pop()
            nfa_1 = nfa_stack.pop()
            nfa_new = NFA()
            nfa_new.start_states = nfa_1.start_states.copy()
            nfa_new.final_states = nfa_2.final_states.copy()
            nfa_1.transition_function.extend(nfa_2.transition_function)
            nfa_new.transition_function = copy.deepcopy(nfa_1.transition_function)
            for start in nfa_1.final_states:
                for end in nfa_2.start_states:
                    nfa_new.transition_function.append([start, '$', end])
            nfa_stack.append(nfa_new)
        elif i == '*':
            nfa_new = NFA()
            nfa_1 = nfa_stack.pop()
            nfa_new.transition_function = copy.deepcopy(nfa_1.transition_function)
            for start in nfa_1.final_states:
                for end in nfa_1.start_states:
                    nfa_new.transition_function.append([start, '$', end])
            nfa_new.final_states = nfa_1.final_states.copy()
            nfa_new.start_states.append(states)
            nfa_new.final_states.append(states)
            states += 1
            for end in nfa_1.start_states:
                nfa_new.transition_function.append([states-1, '$', end])
            nfa_stack.append(nfa_new)
        elif i == '+':
            nfa_2 = nfa_stack.pop()
            nfa_1 = nfa_stack.pop()
            nfa_new = NFA()
            nfa_1.transition_function.extend(nfa_2.transition_function)
            nfa_new.transition_function = copy.deepcopy(nfa_1.transition_function)
            nfa_new.final_states = nfa_1.final_states.copy()
            nfa_new.final_states.extend(nfa_2.final_states)
            nfa_new.start_states.append(states)
            states += 1
            for end in nfa_1.start_states:
                nfa_new.transition_function.append([states-1, '$', end])
            for end in nfa_2.start_states:
                nfa_new.transition_function.append([states-1, '$', end])
            nfa_stack.append(nfa_new)
        else:
            nfa = NFA()
            nfa.start_states.append(states)
            states += 1
            nfa.final_states.append(states)
            nfa.transition_function.append([states-1, i, states])
            states += 1
            nfa_stack.append(nfa)

    return nfa_stack.pop()


def main():
    with open(sys.argv[1], "r") as inp:
        data = json.load(inp)
    regex = data["regex"]
    if regex == "":
        final_nfa_dict = {
            'states': [],
            'letters': [],
            'transition_function': [],
            'start_states': [],
            'final_states': []
        }
        with open(sys.argv[2], "w") as out:
            json.dump(final_nfa_dict, out)
        return
    regex, input_elm = preprocess(regex)
    regular_exp = postfix(regex)
    final_nfa = reg_nfa(regular_exp)
    all_states = set()
    for transition in final_nfa.transition_function:
        all_states.update(['Q'+str(transition[0]), 'Q'+str(transition[2])])
        transition[0] = 'Q'+str(transition[0])
        transition[2] = 'Q'+str(transition[2])
    final_nfa.transition_function.sort(key=lambda e: e[0])

    final_nfa.start_states.sort()
    final_nfa.final_states.sort()
    final_nfa.start_states = ['Q'+str(i) for i in final_nfa.start_states]
    final_nfa.final_states = ['Q'+str(i) for i in final_nfa.final_states]
    final_nfa_dict = {
        'states': list(all_states),
        'letters': list(input_elm),
        'transition_function': final_nfa.transition_function,
        'start_states': final_nfa.start_states,
        'final_states': final_nfa.final_states
    }
    with open(sys.argv[2], "w") as out:
        json.dump(final_nfa_dict, out)


main()
