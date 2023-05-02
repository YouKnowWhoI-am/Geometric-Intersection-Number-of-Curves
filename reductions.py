import DList

# node is a node in the run-length encoding of a cycle \alpha, at which the respective objects of interest start.
# Take a note of changes like: dlist.change_turn_all(node.next.next, n + 1), at the beginning of most functions.
# This avoids unnecessary merging, since n + 1 will never occur in the turn sequence.
# It is finally fixed in the end of the function.
# Also the order of changes insie each function is important, since it avoids unnecessary merging and pointer traversal errors.
# All have O(1) time complexity.

# Need to debug whether return statements are necessary or not. 

def std_spur(dlist, node):
    # x, 0 , y --> x + y
    dlist.decrease_run_length_by(node, 1)
    dlist.decrease_run_length_by(node.next.next, 1)
    dlist.change_turn_all(node.next, node.turn + node.next.next.turn)

def near_cyclic_spur(dlist, node):
    # (0, 0) --> ()
    dlist.decrease_run_length_by(node, 2) 

def std_rt_bracket(dlist, node, n):
    # x, \vbar{1}, \vbar{2}^r, \vbar{1}, y --> x + 1, 2^r , y + 1
    dlist.change_turn_all(node.next.next, n + 1)  
    dlist.decrease_run_length_by(node.next.next.next, 1)
    dlist.decrease_run_length_by(node.next, 1)
    dlist.change_turn_one_start(node, node.turn + 1)
    dlist.change_turn_one_end(node.next.next, node.next.next.turn + 1)
    dlist.change_turn_all(node.next, 2) 

def cyclic_rt_bracket(dlist, node, n):
    # (\vbar{1}, \vbar{2}^r) --> (3, 2^{r - 2})
    dlist.change_turn_all(node, n + 1) 
    dlist.decrease_run_length_by(node.next, 2)
    dlist.change_turn_all(node.next, 2)
    dlist.change_turn_all(node, 3)

def near_cyclic_rt_bracket(dlist, node, n):
    # (x, \vbar{1}, \vbar{2}^r, \vbar{1}) --> (x + 2, 2^r)
    dlist.change_turn_all(node.next.next, n + 1) 
    dlist.decrease_run_length_by(node.next.next.next, 1)
    dlist.decrease_run_length_by(node.next, 1)
    dlist.change_turn_all(node, node.turn + 2)
    dlist.change_turn_all(node.next, 2)

def std_lt_bracket(dlist, node, n):
    # x, 1, 2^r, 1, y --> x - 1, \vbar{2}^r, y - 1
    dlist.change_turn_all(node.next.next, n + 1) 
    dlist.decrease_run_length_by(node.next.next.next, 1)
    dlist.decrease_run_length_by(node.next, 1)
    dlist.change_turn_one_start(node, node.turn - 1)
    dlist.change_turn_one_end(node.next.next, node.next.next.turn - 1)
    dlist.change_turn_all(node.next, -2)

def cyclic_lt_bracket(dlist, node, n):
    # (1, 2^r) --> (\vbar{3}, \vbar{2}^{r - 2})
    dlist.change_turn_all(node, n + 1) 
    dlist.decrease_run_length_by(node.next, 2)
    dlist.change_turn_all(node.next, -2)
    dlist.change_turn_all(node, -3)

def near_cyclic_lt_bracket(dlist, node, n):
    # (x, 1, 2^r, 1) --> (x - 2, \vbar{2}^r)
    dlist.change_turn_all(node.next.next, n + 1) 
    dlist.decrease_run_length_by(node.next.next.next, 1)
    dlist.decrease_run_length_by(node.next, 1)
    dlist.change_turn_all(node, node.turn - 2)
    dlist.change_turn_all(node.next, -2)

def rt_shift_1(dlist, node, n):
    # x, \vbar{2}^s, \vbar{1}, \vbar{2}^t, y --> x + 1, 1, 2^{s - 1}, 3, 2^{t - 1}, 1, y + 1
    dlist.change_turn_all(node.next, n + 1) 
    dlist.change_turn_all(node.next.next.next, n + 1) 
    dlist.change_turn_all(node.next.next, 3)
    dlist.change_turn_one_start(node, node.turn + 1)
    dlist.change_turn_one_end(node.next.next.next.next.turn, node.next.next.next.next.turn + 1)
    dlist.insertAfter(node, 1, 1)
    dlist.insertAfter(node.next.next.next.next, 1, 1)
    dlist.change_turn_all(node.next.next, 2)
    dlist.change_turn_all(node.next.next.next.next, 2)
    dlist.decrease_run_length_by(node.next.next, 1)
    dlist.decrease_run_length_by(node.next.next.next.next, 1)

def rt_shift_2(dlist, node, n):
    # x, \vbar{1}, \vbar{2}^t, y --> x + 1, 2^{t}, 1, y + 1
    dlist.change_turn_all(node.next.next, n + 1)
    dlist.change_turn_all(node.next, n + 2)
    dlist.change_turn_one_start(node, node.turn + 1)
    dlist.change_turn_one_end(node.next.next.next, node.next.next.next.turn + 1)
    dlist.decrease_run_length_by(node.next.next, node.next.next.run_length - 1)
    dlist.decrease_run_length_by(node.next, 1 - node.next.next.run_length) # Basically, increasing run length
    dlist.change_turn_all(node.next, 2)
    dlist.change_turn_all(node.next.next, 1)

def rt_shift_3(dlist, node, n):
    # x, \vbar{2}^s, \vbar{1}, y --> x + 1, 1, 2^{s}, y + 1
    dlist.change_turn_all(node.next.next, n + 1)
    dlist.change_turn_all(node.next, n + 2)
    dlist.change_turn_one_start(node, node.turn + 1)
    dlist.change_turn_one_end(node.next.next.next, node.next.next.next.turn + 1)
    dlist.decrease_run_length_by(node.next, node.next.run_length - 1)
    dlist.decrease_run_length_by(node.next.next, 1 - node.next.run_length) # Basically, increasing run length
    dlist.change_turn_all(node.next, 1)
    dlist.change_turn_all(node.next.next, 2)

def rt_shift_4(dlist, node, n):
    # (x, \vbar{2}^s, \vbar{1}, \vbar{2}^t) --> (x + 2, 1, 2^{s - 1}, 3, 2^{t - 1}, 1)
    dlist.change_turn_all(node.next, n + 1) 
    dlist.change_turn_all(node.next.next.next, n + 1) 
    dlist.change_turn_all(node.next.next, 3)
    dlist.change_turn_all(node, node.turn + 2)
    dlist.insertAfter(node, 1, 1)
    dlist.insertAfter(node.next.next.next.next, 1, 1)
    dlist.change_turn_all(node.next.next, 2)
    dlist.change_turn_all(node.next.next.next.next, 2)
    dlist.decrease_run_length_by(node.next.next, 1)
    dlist.decrease_run_length_by(node.next.next.next.next, 1)

def rt_shift_5(dlist, node, n):
    # (x, \vbar{1}, \vbar{2}^t) --> (x + 2, 2^{t}, 1)
    dlist.change_turn_all(node.next.next, n + 1)
    dlist.change_turn_all(node.next, n + 2)
    dlist.change_turn_all(node, node.turn + 2)
    dlist.decrease_run_length_by(node.next.next, node.next.next.run_length - 1)
    dlist.decrease_run_length_by(node.next, 1 - node.next.next.run_length) # Basically, increasing run length
    dlist.change_turn_all(node.next, 2)
    dlist.change_turn_all(node.next.next, 1)

def rt_shift_6(dlist, node, n):
    # (x, \vbar{2}^s, \vbar{1}) --> (x + 2, 1, 2^{s})
    dlist.change_turn_all(node.next.next, n + 1)
    dlist.change_turn_all(node.next, n + 2)
    dlist.change_turn_all(node, node.turn + 2)
    dlist.decrease_run_length_by(node.next, node.next.run_length - 1)
    dlist.decrease_run_length_by(node.next.next, 1 - node.next.run_length) # Basically, increasing run length
    dlist.change_turn_all(node.next, 1)
    dlist.change_turn_all(node.next.next, 2)

def rt_shift_7(dlist, node, n):
    # (3, \vbar{2}^s, \vbar{1}, \vbar{2}^t) --> (1, 2^{s}, 3, 2^{t})
    dlist.change_turn_all(node.next, n + 1)
    dlist.change_turn_all(node.next.next.next, n + 1)
    dlist.change_turn_all(node.next.next, 3)
    dlist.change_turn_all(node, 1)
    dlist.change_turn_all(node.next, 2)
    dlist.change_turn_all(node.next.next.next, 2)

def rt_shift_8(dlist, node, n):
    # (\vbar{2}^l) --> (2^{l})
    dlist.change_turn_all(node, 2)