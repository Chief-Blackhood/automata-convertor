## Q1: Regular expression to NFA

- First if a null string is provided then I just return an NFA without any states, letters, transition_function, start_states or final_states.
- If the regex provided is valid then, I preprocess the regex and add a ('.') symbol wherever a  concatenation is implicit.
- Then I convert the regex into its postfix format so as to process it in a stack
- Then the reg_nfa function is called with iterates over the postfix regex and depending on the character creates a new NFA and add the NFA to the stack.
- If the character is not a operation then I just create a new NFA with a single start state, final state and a transition function between the two.
- Otherwise I add the states and transition as taught in class.

## Q2: NFA to DFA

- I store all the states that are reachable from a single state on a particular input using dfs on a graph made of edges between 2 states having a transition between them.
- Then I also find the epsilon cover of the start state by a similar dfs method.
- I create all the possible combination of states and find the state reachable by all these combination given a particular input. This forms my transition_function.
- Final states are all the states that contain at least on final state of the NFA given.

## Q3: DFA to regular expression

- I create a GNFA by adding two more states Qs and Qf and adding epsilon transitions from Qs to each start state and from each final state to Qf.
- Then I select one of the state present in the given DFA to remove.
- I iterate over all the possible combinations and find the tuples where the state selected to be removed has an incoming edge and a single outgoing edge(multiple edges can be made into one using union).
- I then add an edge over the states from where the incoming and outgoing edges are coming and the value of the transition is (incoming_edge_value).(looping_inside_the_state_to_be_removed)*(outgoing_edge_value)
- I do this until all the states given in the DFA are removed and only Qs and Qf remain.
- Then the regex formed will be the union of all the edges from Qs and Qf.

## Q4: DFA to optimal DFA

- I followed the Hopcroft's algorithm to get the minimum partitions possible.
- I first removed all the states that are unreachable from the start states by doing a somewhat dfs.
- I make two copies of the set [final_states, reachable_states-final_states] (partition, W). One is the actual partition and the other tell when no further partition is possible.
- I select one set to remove from W and find all the states that are reachable to the state being removed by a letter input. If the intersection and set difference is not empty then it means the set being removed can be partitioned.
- Then I update the set W and partition set accordingly.