#!/usr/bin/python

import sys


class NFA:
    def __init__(self):
        self.start_states = []
        self.final_states = []
        self.transition_function = []
        self.states = []


def preprocess(regex):
    concatRegex = "("
    for i in range(len(regex)):
        curChar = regex[i]
        concatRegex += curChar
        if i+1 != len(regex):
            nextChar = regex[i+1]
        else:
            continue
        if (curChar.isnumeric() or curChar.islower() or curChar == ')') and (nextChar.isnumeric() or nextChar.islower() or nextChar == '('):
            concatRegex += '.'
        elif curChar == '*' and (nextChar.isnumeric() or nextChar.islower() or nextChar == '('):
            concatRegex += '.'
    concatRegex += ')'
    return concatRegex


def postfix(regex):
    postfixRegex = ""
    stack = []
    for i in range(len(regex)):
        if regex[i] == '+':
            while(len(stack) and stack[-1] != '('):
                postfixRegex += stack.pop()
            stack.append(regex[i])
        elif regex[i] == ')':
            while(len(stack) and stack[-1] != '('):
                postfixRegex += stack.pop()
            stack.pop()
        elif regex[i] == '.':
            while(len(stack) and stack[-1] == '.'):
                postfixRegex += stack.pop()
            stack.append(regex[i])
        elif regex[i] == '(':
            stack.append(regex[i])
        else:
            postfixRegex += regex[i]
    while(len(stack)):
        postfixRegex += stack.pop()
    return postfixRegex


def reg_nfa(regularExp):
    nfa_stack = []
    states = 0
    for i in regularExp:
        if i == '.':
            nfa_2 = nfa_stack.pop()
            nfa_1 = nfa_stack.pop()
            nfa_new = NFA()
            nfa_new.start_states = nfa_1.start_states.copy()
            nfa_new.final_states = nfa_2.final_states.copy()
            nfa_1.states.extend(nfa_2.states)
            nfa_1.transition_function.extend(nfa_2.transition_function)
            nfa_new.states = nfa_1.states.copy()
            nfa_new.transition_function = nfa_1.transition_function.copy()
            for start in nfa_1.final_states:
                for end in nfa_2.start_states:
                    nfa_new.transition_function.append([start, '$', end])
            nfa_stack.append(nfa_new)
        elif i == '*':
            nfa_new = NFA()
            nfa_1 = nfa_stack.pop()
            nfa_new.transition_function = nfa_1.transition_function.copy()
            for start in nfa_1.final_states:
                for end in nfa_1.start_states:
                    nfa_new.transition_function.append([start, '$', end])
            nfa_new.final_states = nfa_1.final_states.copy()  # new
            nfa_new.start_states.append(states)
            nfa_new.final_states.append(states)
            states += 1
            # nfa_new.final_states.append(states)
            for end in nfa_1.start_states:
                nfa_new.transition_function.append([states-1, '$', end])
            # for start in nfa_1.final_states:
            #     nfa_new.transition_function.append([start, '$', states])
            # states += 1
            nfa_stack.append(nfa_new)
        elif i == '+':
            nfa_2 = nfa_stack.pop()
            nfa_1 = nfa_stack.pop()
            nfa_new = NFA()
            nfa_1.transition_function.extend(nfa_2.transition_function)
            nfa_new.transition_function = nfa_1.transition_function.copy()
            nfa_new.final_states = nfa_1.final_states.copy()  # new
            nfa_new.final_states.extend(nfa_2.final_states.copy())  # new
            nfa_new.start_states.append(states)
            states += 1
            # nfa_new.final_states.append(states)
            for end in nfa_1.start_states:
                nfa_new.transition_function.append([states-1, '$', end])
            # for start in nfa_1.final_states:
            #     nfa_new.transition_function.append([start, '$', states])
            for end in nfa_2.start_states:
                nfa_new.transition_function.append([states-1, '$', end])
            # for start in nfa_2.final_states:
            #     nfa_new.transition_function.append([start, '$', states])
            # states += 1
            nfa_stack.append(nfa_new)
        else:
            nfa = NFA()
            nfa.start_states.append(states)
            nfa.states.append(states)
            states += 1
            nfa.final_states.append(states)
            nfa.transition_function.append([states-1, i, states])
            states += 1
            nfa_stack.append(nfa)

    return nfa_stack.pop()


def main():
    regex = input("Enter the regex expression: ")
    regex = preprocess(regex)
    regularExp = postfix(regex)
    final_nfa = reg_nfa(regularExp)
    print(final_nfa.start_states)
    print(final_nfa.final_states)
    print(final_nfa.transition_function)


main()
