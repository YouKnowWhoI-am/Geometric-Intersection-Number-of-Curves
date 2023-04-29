import sys
import DList, reductions
import numpy as np

# The input is of the form abAcdBCD, where a, b, c, d represents arrow pointing clockwise, A, B, C, D represents arrow pointing counterclockwise.
# The input is asked as a list of tuples, where (1,1) stands for a, (-1,1) stands for A, (1,2) stands for b, (-1,2) stands for B, (1,3) stands for c, (-1,3) stands for C, and so on.
# Essentially, the first element of the tuple is the direction of the arrow and the second element is the identification of the arrow.
print("Enter the Euler characteristic of the surface, whether it is negative: '-1' or non-negative: '1'.")
euler = int(input('Enter Euler characteristic: '))

if euler == -1:
    print("Enter the fundamental polygon as a list of tuples after entering the genus.")
    M = list(tuple(map(int, input().split())) for r in range(4*int(input('Enter genus: ')))) # Debug global scope of M. I mean we need it to be global.
else:
    print("Enter the fundamental polygon according to the following convention: \n")
    print("1 if it's a sphere or a disk.\n")
    print("2 if it's a cylinder.\n")
    print("3 if it's a projective plane.\n")
    print("4 if it's a torus.\n")
    print("5 if it's a Klein bottle.\n")
    type = int(input('Enter type: '))
    if type == 1:
        print("The interesection number is 0")
        sys.exit()
    elif type == 2:
        print("Enter the number of sides of the cylinder.")
    elif type == 3:
        intersection = int(input('Enter 1 to calculate self intersection number, 2 to calculate intersection number between two curves: '))
        if intersection == 1:
            print("The self intersection number of any curve is 0.")
        else:
            print("The intersection number between any two curves is 1.")       
        sys.exit()
    elif type == 4:
        print("Let a and b be the generators of the fundamental group of the torus.\n")
        print("Enter x and y, where the curve is a^x*b^y.\n")
        intersection = int(input('Enter 1 to calculate self intersection number, 2 to calculate intersection number between two curves: '))
        if intersection == 1:
            x = int(input('Enter x: '))
            y = int(input('Enter y: '))
            print("The self intersection number of a^x*b^y is ", np.gcd(x,y) - 1)
        else:
            x1 = int(input('Enter x1: '))
            y1 = int(input('Enter y1: '))
            x2 = int(input('Enter x2: '))
            y2 = int(input('Enter y2: '))
            print("The intersection number between a^x1*b^y1 and a^x2*b^y2 is ", np.absolute(np.linalg.det([x1, y1],[x2,y2])))
        sys.exit()
    elif type == 5:
        print("Let a and b be the generators of the fundamental group of the Klein bottle.\n")

# O(n) time complexity.
def isCombinatorialSurface(M):
    # Input must be of even length.
    if len(M) %2 == 1:
        sys.exit("Invalid Input: Input must be of even length.")
    elif len(M) % 2 == 0:
    # Check if the input has adjacent duplicates.
        if M[0] == M[-1]: sys.exit("Invalid Input: Adjacent sides can'turn_seq be identical.")
        for i in range(len(M)-2):
            if M[i] == M[i+1]: sys.exit("Invalid Input: Adjacent sides can'turn_seq be identical.")
    # Check if the input has each letter twice, ignoring case.
    counter = [0] * len(M)
    for x in M:
        if x[1] > int(len(M)/2):
            sys.exit("Re-enter Input: Please follow convention of serially naming the edges without skipping any intergers in between.")
        counter[x[1]-1] = counter[x[1]-1] + 1
    for i in range(len(counter)):
        if counter[M[i][1]-1] != 2 and counter[M[i][1]-1] != 0:
            sys.exit("Invalid Input: Number of edges not equal to 4*genus")       
    
isCombinatorialSurface(M)

# Vertex neighbourhood of z is {0} \cup [len(M)-1], in that order.
# We need a set of faces of the system of quads.

index_a = [0] * len(M) # To ensure the function turn, defined later, runs in O(1) time, we need to store the index of each edge in the cycle.
nbr_a = [0] * len(M) #nbr_z is the list {0, 1, ..., len(M)-1} in the order of the edges in the cycle.
spoke = [set() for j in range(len(M))] # spoke[i] stores the unique set of 4 neighbours of the edge i. We are not worried about the order.
# These three are declared as global so that their original copy is modified by every function that calls them.

# O(n) time complexity.
def Sys_of_Quads(M):
    faces = [[0 for i in range(4)] for j in range(int((len(M)/2)))] # 2D list of faces
    count = [0] * int(len(M)/2)
    for i in range(len(M)):
        if count[M[i][1]-1] == 0: #if i'th edge has not occured yet
            if M[i][0] == 1: #Edge oriented Clockwise
                faces[M[i][1]-1][0] = i
                faces[M[i][1]-1][1] = (i + 1) % len(M)
                count[M[i][1]-1] = 1 #Mark i'th edge as occured once clockwise
            elif M[i][0] == -1: #Edge oriented Anti-Clockwise
                faces[M[i][1]-1][0] = i
                faces[M[i][1]-1][1] = (i + 1) % len(M)
                count[M[i][1]-1] = 2 #Mark i'th edge as occured once anti-clockwise
        elif count[M[i][1]-1] != 0: #This edge has already occured once
            if M[i][0] == 1: #Edge oriented Clockwise
                if count[M[i][1]-1] == 1: #Previously it also occured clockwise
                    faces[M[i][1]-1][2] = (i + 1) % len(M)
                    faces[M[i][1]-1][3] = i 
                elif count[M[i][1]-1] == 2: #Previously it occured anti-clockwise
                    faces[M[i][1]-1][2] = i
                    faces[M[i][1]-1][3] = (i + 1) % len(M)
            elif M[i][0] == -1: #Edge oriented Anti-Clockwise
                if count[M[i][1]-1] == 1: #Previously it occured clockwise
                    faces[M[i][1]-1][2] = i
                    faces[M[i][1]-1][3] = (i + 1) % len(M)
                elif count[M[i][1]-1] == 2: #Previously it also occured anti-clockwise
                    faces[M[i][1]-1][2] = (i + 1) % len(M)
                    faces[M[i][1]-1][3] = i
    for i in range(len(M)):
        if i != 0:
            nbr_a[i] = faces[f - 1][3 - l]
            if M[nbr_a[i]][1] != f:
                f = M[nbr_a[i]][1]
            else:
                f = M[nbr_a[i] - 1][1]
            for j in range(4):
                if faces[f - 1][j] == nbr_a[i]:
                     l = j 
        elif i == 0: # Currently f and l are configured according to nbr_a[i-1]
            nbr_a[i] = faces[i][1]
            f = i + 1 # f is the index of the face that contains the edge i
            l = 1 # l is the index of the edge in the face that contains the edge i
    for i in range(len(M)):
        index_a[i] = nbr_a.index(i)

    for i in range(len(M)):
        for j in range(4):
            if j == 0:
                spoke[faces[i][j]].add(faces[i][1])
                spoke[faces[i][j]].add(faces[i][3])
            elif j == 1 or j == 2:
                spoke[faces[i][j]].add(faces[i][j - 1])
                spoke[faces[i][j]].add(faces[i][j + 1])
            elif j == 3:
                spoke[faces[i][j]].add(faces[i][2])
                spoke[faces[i][j]].add(faces[i][0])


# The input cycle \alpha is an alternating cyclic sequence (v_0, e_1, v_1, e_2, ..., e_l) of vertices and edges.
# Because \alpha is a cycle in a system of quads, l must be even; v_i = a for all even i and v_i = z for all odd i.
# Hence, the input is asked as a list of integers (e_1, e_2, ..., e_l).

# O(l) time complexity.
def isCombinatorialCurve(c):
    if len(c) == 0:
        sys.exit("Invalid Input: Input must be a non-empty list.")
    if len(c) % 2 == 1:
        sys.exit("Invalid Input: Input must be of even length.")

print("Enter first Combinatorial Curve:")
c1 = list(map(int, input()) for r in range(int(input('Enter length: '))))
isCombinatorialCurve(c1)
print("Enter second Combinatorial Curve:")
c2 = list(map(int, input()) for r in range(int(input('Enter length: '))))
isCombinatorialCurve(c2)

# O(1) time complexity.
def turn(e1, v, e2):
    # e1 and e2 are the edges that are incident to v, and e1 is the edge that is traversed before e2.
    # The function returns the turn from e1 to e2 at v.
    if e1 == e2:
        return 0
    if v == 1: # v is the vertex z
        return e2 - e1
    else: # v is the vertex a
        return index_a[e2] - index_a[e1]

# O(l) time complexity.
def turn_sequence(c):
    # c is a combinatorial curve
    # The function returns the turn sequence of c.
    turn_seq = [0] * len(c)
    for i in range(len(c)):
        if i % 2 == 0 and i != 0:
            turn_seq[i] = turn(c[i - 1], 0, c[i])
        elif i % 2 == 0 and i == 0:
            turn_seq[i] = turn(c[len(c) - 1], 0, c[i])
        elif i % 2 == 1:
            turn_seq[i] = turn(c[i - 1], 1, c[i])
    return turn_seq

# O(l) time complexity.
def run_length_encoding(c, turn_seq):
    # turn_seq is a turn sequence
    # The function returns the run-length encoding of turn_seq which is a circular doubly linked list.
    dlist = DList.DoublyLinkedList()
    for i in range(len(turn_seq)):
        if i == 0:
            dlist.insertEnd(c[i], turn_seq[i], 1)
        elif turn_seq[i] != turn_seq[i - 1]:
            dlist.insertEnd(c[i], turn_seq[i], 1)
        elif turn_seq[i] == turn_seq[i - 1]:
            dlist.updateEnd()
    return dlist

def toEdge_sequence(dlist):
    # dlist is the run length encoding of a cycle c.
    # The function returns the edge sequence of c.
    edge_seq = [0] * (dlist.total_length() + 1)
    temp = dlist.start
    edge_seq[0] = temp.edge
    edge_seq[dlist.total_length()] = temp.vertex # The parity of the first vertex.
    counter = 1
    i = 1
    while i < dlist.total_length():
        while counter <= temp.run_length:
            if i % 2 == 0:
                edge_seq[i] = edge_seq[i] + temp.turn
            else:
                edge_seq[i] = nbr_a[index_a[edge_seq[i - 1]] + temp.turn]
            counter += 1
            i += 1
        temp = temp.next
    return edge_seq

# O(l) time complexity.
def isPrimitive(c):
    # c is a combinatorial curve
    # The function returns c if c is primitive, and (d, k) if c = d^{k} for some primitive curve d.
    for i in range(len(c)):
        if i % 2 == 0 and i != 0:
            if turn(c[i - 1], 0, c[i]) != 0:
                return c

# O(l) time complexity.
# Remember when we delete the start node from a circular doubly linked list, we update the start pointer as the next pointer.
def geodesic(dlist):
    n = len(M)
    # dlist is the run length encoding of a cycle c.
    # The function returns a reduced cycle freely homotopic to c.
    if dlist.check_empty():
        return 0
    elif dlist.number_of_runs() > 5:
        temp = dlist.start
        while (dlist.number_of_runs() > 5 and (temp != dlist.start.prev or (temp == dlist.start.prev and temp.mark_1 == False))):
            if temp.next.turn == 0:
                reductions.std_spur(dlist, temp)
            elif temp.turn == 0:
                reductions.std_spur(dlist, temp.prev)
            elif temp.prev.turn == 0:
                reductions.std_spur(dlist, temp.prev.prev)

            elif temp.next.turn == 1 and temp.next.next.turn == 2 and temp.next.next.next.turn == 1:
                reductions.std_lt_bracket(dlist, temp, n)
            elif temp.turn == 1 and temp.next.turn == 2 and temp.next.next.turn == 1:
                reductions.std_lt_bracket(dlist, temp.prev, n)
            elif temp.prev.turn == 1 and temp.turn == 2 and temp.next.turn == 1:
                reductions.std_lt_bracket(dlist, temp.prev.prev, n)
            elif temp.prev.prev.turn == 1 and temp.prev.turn == 2 and temp.turn == 1:
                reductions.std_lt_bracket(dlist, temp.prev.prev.prev, n)
            elif temp.prev.prev.prev.turn == 1 and temp.prev.prev.turn == 2 and temp.prev.turn == 1:
                reductions.std_lt_bracket(dlist, temp.prev.prev.prev.prev, n)
            
            elif temp.next.turn == n - 1 and temp.next.next.turn == n - 2 and temp.next.next.next.turn == n - 1:
                reductions.std_rt_bracket(dlist, temp, n)
            elif temp.turn == n - 1 and temp.next.turn == n - 2 and temp.next.next.turn == n - 1:
                reductions.std_rt_bracket(dlist, temp.prev, n)
            elif temp.prev.turn == n - 1 and temp.turn == n - 2 and temp.next.turn == n - 1:
                reductions.std_rt_bracket(dlist, temp.prev.prev, n)
            elif temp.prev.prev.turn == n - 1 and temp.prev.turn == n - 2 and temp.turn == n - 1:
                reductions.std_rt_bracket(dlist, temp.prev.prev.prev, n)
            elif temp.prev.prev.prev.turn == n - 1 and temp.prev.prev.turn == n - 2 and temp.prev.turn == n - 1:
                reductions.std_rt_bracket(dlist, temp.prev.prev.prev.prev, n)

            else:
                temp = temp.next
                temp.mark_1 = True

    elif dlist.number_of_runs() == 2:
        if dlist.start.turn == 0 and dlist.start.next.turn == 0:
            reductions.near_cyclic_spur(dlist, dlist.start)

        elif dlist.start.turn == 1 and dlist.start.next.turn == 2:
            reductions.cyclic_lt_bracket(dlist, dlist.start, n)
        elif dlist.start.turn == 2 and dlist.start.next.turn == 1:
            reductions.cyclic_lt_bracket(dlist, dlist.start.next, n)

        elif dlist.start.turn == n - 1 and dlist.start.next.turn == n - 2:
            reductions.cyclic_rt_bracket(dlist, dlist.start, n)
        elif dlist.start.turn == n - 2 and dlist.start.next.turn == n - 1:
            reductions.cyclic_rt_bracket(dlist, dlist.start.next, n)

    elif dlist.number_of_runs() == 4:
        if dlist.start.next.turn == 1 and dlist.start.next.next.turn == 2 and dlist.start.next.next.next.turn == 1:
            reductions.near_cyclic_lt_bracket(dlist, dlist.start, n)
        elif dlist.start.turn== 1 and dlist.start.next.turn == 2 and dlist.start.next.next.turn == 1:
            reductions.near_cyclic_lt_bracket(dlist, dlist.start.prev, n)
        elif dlist.start.turn == 2 and dlist.start.next.turn == 1 and dlist.start.prev.turn == 1:
            reductions.near_cyclic_lt_bracket(dlist, dlist.start.prev.prev, n)
        elif dlist.start.turn == 1 and dlist.start.prev.turn == 2 and dlist.start.prev.prev.turn == 1:
            reductions.near_cyclic_lt_bracket(dlist, dlist.start.next, n)

        elif dlist.start.next.turn == n - 1 and dlist.start.next.next.turn == n - 2 and dlist.start.next.next.next.turn == n - 1:
            reductions.near_cyclic_rt_bracket(dlist, dlist.start, n)
        elif dlist.start.turn == n - 1 and dlist.start.next.turn == n - 2 and dlist.start.next.next.turn == n - 1:
            reductions.near_cyclic_rt_bracket(dlist, dlist.start.prev, n)
        elif dlist.start.turn == n - 2 and dlist.start.next.turn == n - 1 and dlist.start.prev.turn == n - 1:
            reductions.near_cyclic_rt_bracket(dlist, dlist.start.prev.prev, n)
        elif dlist.start.turn == n - 1 and dlist.start.prev.turn == n - 2 and dlist.start.prev.prev.turn == n - 1:
            reductions.near_cyclic_rt_bracket(dlist, dlist.start.next, n)

    elif dlist.number_of_runs() == 5:
        if dlist.start.next.turn == 1 and dlist.start.next.next.turn == 2 and dlist.start.next.next.next.turn == 1:
            reductions.std_lt_bracket(dlist, dlist.start, n)
        elif dlist.start.turn == 1 and dlist.start.next.turn == 2 and dlist.start.next.next.turn == 1:
            reductions.std_lt_bracket(dlist, dlist.start.prev, n)
        elif dlist.start.turn == 2 and dlist.start.next.turn == 1 and dlist.start.prev.turn == 1:
            reductions.std_lt_bracket(dlist, dlist.start.prev.prev, n)
        elif dlist.start.turn == 1 and dlist.start.prev.turn == 2 and dlist.start.prev.prev.turn == 1:
            reductions.std_lt_bracket(dlist, dlist.start.prev.prev.prev, n)
        elif dlist.start.prev.turn == 1 and dlist.start.prev.prev.turn == 2 and dlist.start.prev.prev.prev.turn == 1:
            reductions.std_lt_bracket(dlist, dlist.start.next, n)

        elif dlist.start.next.turn == n - 1 and dlist.start.next.next.turn == n - 2 and dlist.start.next.next.next.turn == n - 1:
            reductions.std_rt_bracket(dlist, dlist.start, n)
        elif dlist.start.turn == n - 1 and dlist.start.next.turn == n - 2 and dlist.start.next.next.turn == n - 1:
            reductions.std_rt_bracket(dlist, dlist.start.prev, n)
        elif dlist.start.turn == n - 2 and dlist.start.next.turn == n - 1 and dlist.start.prev.turn == n - 1:
            reductions.std_rt_bracket(dlist, dlist.start.prev.prev, n)
        elif dlist.start.turn == n - 1 and dlist.start.prev.turn == n - 2 and dlist.start.prev.prev.turn == n - 1:
            reductions.std_rt_bracket(dlist, dlist.start.prev.prev.prev, n)
        elif dlist.start.prev.turn == n - 1 and dlist.start.prev.prev.turn == n - 2 and dlist.start.prev.prev.prev.turn == n - 1:
            reductions.std_rt_bracket(dlist, dlist.start.next, n)

# O(l) time complexity.
def canonical(dlist):
    n = len(M)
    # Input is a geodesic freely homotopic to c.
    # The function returns a canonical geodesic freely homotopic to c.
    if dlist.check_empty():
        return 0
    elif dlist.number_of_runs() > 4:
        temp = dlist.start
        while (dlist.number_of_runs() > 4 and (temp != dlist.start.prev or (temp == dlist.start.prev and temp.mark_2 == False))):
            if temp.next.turn == n - 2 and temp.next.next.turn == n - 1 and temp.next.next.next.turn == n - 2:
                reductions.rt_shift_1(dlist, temp, n)
            elif temp.turn == n - 2 and temp.next.turn == n - 1 and temp.next.next.turn == n - 2:
                reductions.rt_shift_1(dlist, temp.prev, n)
            elif temp.turn == n - 1 and temp.next.turn == n - 2 and temp.prev.turn == n - 2:
                reductions.rt_shift_1(dlist, temp.prev.prev, n)
            elif temp.turn == n - 2 and temp.prev.turn == n - 1 and temp.prev.prev.turn == n - 2:
                reductions.rt_shift_1(dlist, temp.prev.prev.prev, n)
            elif temp.prev.turn == n - 2 and temp.prev.prev.turn == n - 1 and temp.prev.prev.prev.turn == n - 2:
                reductions.rt_shift_1(dlist, temp.prev.prev.prev.prev, n)
            
            elif temp.next.turn == n - 1 and temp.next.next.turn == n - 2:
                reductions.rt_shift_2(dlist, temp, n)
            elif temp.turn == n - 1 and temp.next.turn == n - 2:
                reductions.rt_shift_2(dlist, temp.prev, n)
            elif temp.turn == n - 2 and temp.prev.turn == n - 1:
                reductions.rt_shift_2(dlist, temp.prev.prev, n)
            elif temp.prev.turn == n - 1 and temp.prev.prev.turn == n - 2:
                reductions.rt_shift_2(dlist, temp.prev.prev.prev, n)

            elif temp.next.turn == n - 2 and temp.next.next.turn == n - 1:
                reductions.rt_shift_3(dlist, temp, n)
            elif temp.turn == n - 2 and temp.next.turn == n - 1:
                reductions.rt_shift_3(dlist, temp.prev, n)
            elif temp.turn == n - 1 and temp.prev.turn == n - 2:
                reductions.rt_shift_3(dlist, temp.prev.prev, n)
            elif temp.prev.turn == n - 2 and temp.prev.prev.turn == n - 1:
                reductions.rt_shift_3(dlist, temp.prev.prev.prev, n)
            
            else:
                temp = temp.next
                temp.mark_2 = True

    elif dlist.number_of_runs() == 1:
        if dlist.start.turn == n - 2:
            dlist.start.turn = 2

    elif dlist.number_of_runs() == 3:
        if dlist.start.turn != n - 3 and dlist.start.next.turn == n - 1 and dlist.start.next.next.turn == n - 2:
            reductions.rt_shift_5(dlist, dlist.start, n)
        elif dlist.start.turn == n - 1 and dlist.start.next.turn == n - 2 and dlist.start.next.next.turn != n - 3:
            reductions.rt_shift_5(dlist, dlist.start.prev, n)
        elif dlist.start.turn == n - 2 and dlist.start.next.turn != n - 3 and dlist.start.prev.turn == n - 1:
            reductions.rt_shift_5(dlist, dlist.start.prev.prev, n)
        
        elif dlist.start.turn != n - 3 and dlist.start.next.turn == n - 2 and dlist.start.next.next.turn == n - 1:
            reductions.rt_shift_6(dlist, dlist.start, n)
        elif dlist.start.turn == n - 2 and dlist.start.next.turn == n - 1 and dlist.start.next.next.turn != n - 3:
            reductions.rt_shift_6(dlist, dlist.start.prev, n)
        elif dlist.start.turn == n - 1 and dlist.start.next.turn != n - 3 and dlist.start.prev.turn == n - 2:
            reductions.rt_shift_6(dlist, dlist.start.prev.prev, n)
    
    elif dlist.number_of_runs() == 4:
        if dlist.start.turn != n - 3 and dlist.start.next.turn == n - 2 and dlist.start.next.next.turn == n - 1 and dlist.start.next.next.next.turn == n - 2:
            reductions.rt_shift_4(dlist, dlist.start, n)
        elif dlist.start.turn == n - 2 and dlist.start.next.turn == n - 1 and dlist.start.next.next.turn == n - 2 and dlist.start.next.next.next.turn != n - 3:
            reductions.rt_shift_4(dlist, dlist.start.prev, n)
        elif dlist.start.turn == n - 1 and dlist.start.next.turn == n - 2 and dlist.start.next.next.turn != n - 3 and dlist.start.prev.turn == n - 2:
            reductions.rt_shift_4(dlist, dlist.start.prev.prev, n)
        elif dlist.start.turn == n - 2 and dlist.start.next.turn != n - 3 and dlist.start.prev.turn == n - 1 and dlist.start.prev.prev.turn == n - 2:
            reductions.rt_shift_4(dlist, dlist.start.next, n)

        elif dlist.start.turn == n - 3 and dlist.start.next.turn == n - 2 and dlist.start.next.next.turn == n - 1 and dlist.start.next.next.next.turn == n - 2:
            reductions.rt_shift_7(dlist, dlist.start, n)
        elif dlist.start.turn == n - 2 and dlist.start.next.turn == n - 1 and dlist.start.next.next.turn == n - 2 and dlist.start.next.next.next.turn == n - 3:
            reductions.rt_shift_7(dlist, dlist.start.prev, n)
        elif dlist.start.turn == n - 1 and dlist.start.next.turn == n - 2 and dlist.start.next.next.turn == n - 3 and dlist.start.prev.turn == n - 2:
            reductions.rt_shift_7(dlist, dlist.start.prev.prev, n)
        elif dlist.start.turn == n - 2 and dlist.start.next.turn == n - 3 and dlist.start.prev.turn == n - 1 and dlist.start.prev.prev.turn == n - 2:
            reductions.rt_shift_7(dlist, dlist.start.next, n)

def invert(dlist):
    # Input is a combinatorial curve c.
    # The function returns c^{-1}.
    dlist_inverse = DList.DoublyLinkedList()
    temp = dlist.start
    while (temp.prev != dlist.start):
        dlist_inverse.insertEnd(temp.edge, temp.turn, temp.run_length)
        temp = temp.prev
    dlist_inverse.insertEnd(temp.edge, temp.turn, temp.run_length)
    return dlist_inverse

def helper(match, k, l, length, D, c, d):
    while k < len(c) and l < len(d):
        if k != 0 or l != len(d) - 1: # We haven't reached the top right corner of the grid.
            if match[k][l] != 0: # We found a match.
                length += 1 # We increase the length of the double path.
                if k == len(c) - 1 or l == len(d) - 1: # We reached the top or the right side of the grid.
                    D.append([k - length, l - length, length]) # We append the first vertex pair of double path of length 'length'.
                    if k == len(c) - 1: # We reached the right side of the grid.
                        k = k - l - 1 
                        l = 0
                    else: # We reached the top of the grid.
                        l = l - k - 1
                        k = 0
                    # move to the next right slash diagonal.
                else: # We haven't reached the top or the right side of the grid.
                    k += 1 
                    l += 1
                    # We move to the next vertex pair on the diagonal.
            else: # We didn't find a match.
                if length != 0: # Double path of length 'length' ended.
                    D.append([k - length, l - length, length])
                length = 0
                if k == len(c) - 1: # We reached the right side of the grid.
                    k = k - l - 1
                    l = 0
                elif l == len(d) - 1: # We reached the top of the grid.
                    l = l - k - 1
                    k = 0
                else: # We haven't reached the top or the right side of the grid.
                    k += 1
                    l += 1
        else: # k == 0 and l == len(d) - 1 
            break # We finished scanning the grid and found all the double paths.

def nbr(e1, e2, v):
    if v == 1:
        if e1 - e2 == 1 or e1 - e2 == -1:
            return 1
    
    elif v == 0:
        if index_a[e1] - index_a[e2] == 1 or index_a[e1] - index_a[e2] == -1:
            return 1
    
    else:
        return 0


def isCLW(e_1, e_2, e_3, v):
    if v == 1:
        E_3 = (e_3 + (len(M) - e_1)) % len(M)
        E_2 = (e_2 + (len(M) - e_1)) % len(M)
        if E_2 > 0 and E_3 > E_2:
            return 1
    elif v == 0:
        E_3 = (index_a[e_3] + (len(M) - index_a[e_1])) % len(M)
        E_2 = (index_a[e_2] + (len(M) - index_a[e_1])) % len(M)
        if E_2 > 0 and E_3 > E_2:
            return 1

def isCCW(e_1, e_2, e_3, v):
    return isCLW(e_3, e_2, e_1, v)

# O(l^2) time complexity
def Primitive_intersection(C, D):
    # Input is two primitive combinatorial curves x and y.
    # The function returns the intersection number of x and y.
    canonical(D)
    d = toEdge_sequence(D)

    C_inverse = invert(C)
    canonical(C_inverse)
    c_L_inverse = toEdge_sequence(C_inverse)

    C_L = invert(C_inverse) # C_inverse is now already canonical, we just need to invert and use it.
    c_L = toEdge_sequence(C_L)

    canonical(C)
    c_R = toEdge_sequence(C)

    # We create a grid of size (len(c_R) x len(d)). Operating on the grid gives us overall a O(l^2) time complexity.
    match = [[0 for i in range(len(d))] for j in range(len(c_R))] # For D_plus.
    match_2 = [[0 for i in range(len(d))] for j in range(len(c_L_inverse))] # For D_minus.

    # We fill the grid if there is a match of edges as well as the parity of the vertices between the two curves.
    # match[i][j] = 1 if there is a match of edges and the parity of the vertices is 0.
    # match[i][j] = 2 if there is a match of edges and the parity of the vertices is 1.
    for i in range(len(c_R) - 1):
        for j in range(len(d) - 1):
            if c_R[i] == d[j] and (c_R[len(c_R)] + i % 2) % 2 == (d[len(d)] + j % 2) % 2: # We check if there is a match of edges and the parity of the vertices is the same.
                match[i][j] = 1 + ((c_R[len(c_R)] + i % 2) % 2) 

    for i in range(len(c_L_inverse) - 1):
        for j in range(len(d) - 1):
            if c_L_inverse[i] == d[j] and (c_L_inverse[len(c_L_inverse)] + i % 2) % 2 == (d[len(d)] + j % 2) % 2: # We check if there is a match of edges and the parity of the vertices is the same.
                match_2[i][j] = 1 + ((c_L_inverse[len(c_L_inverse)] + i % 2) % 2)
    
    k = len(c_R) - 1 # Counter for the rows of the grid, numbering the edges of c_R.
    l = 0 # Counter for the columns of the grid, numbering the edges of d.
    length = 0 # The length of the double path, in terms of number of edges. 
    D_plus = [] # For D_plus.
    helper(match, k, l, length, D_plus, c_R, d)

    # Reuse the counter variables.
    k = len(c_L_inverse) - 1
    l = 0
    length = 0 
    D_minus = [] # For D_minus.
    helper(match_2, k, l, length, D_minus, c_L_inverse, d)

    # We now have all the double paths in D, D_minus.
    # We need to find the number of crossing double paths satisfying the desired conditions.
    
    d_plus = 0
    d_0 = 0
    d_minus = 0

    # To update d_plus.
    for i in range(len(D_plus)):
        if D_plus[i][2] != 0: # Double Paths of positive length.
        # Actually D_plus[i][2] will never be zero, as we are only considering the positive length double paths in the helper function.
        # If you notice, we only append when D_plus[i][2] = length != 0.

            # First three arguments are edges and the last argument is the parity of the vertex.
            i_1 = isCLW(c_R[D_plus[i][0] - 1], d[D_plus[i][1] - 1], c_R[D_plus[i][0]], match[D_plus[i][0]][D_plus[i][1]])         
            i_2 = isCCW(c_R[D_plus[i][0] - 1], d[D_plus[i][1] - 1], c_R[D_plus[i][0]], match[D_plus[i][0]][D_plus[i][1]])
            i_3 = isCLW(c_R[D_plus[i][0] + D_plus[i][2]], d[D_plus[i][1] + D_plus[i][2]], c_R[D_plus[i][0] + D_plus[i][2] - 1], match[D_plus[i][0] + D_plus[i][2]][D_plus[i][1] + D_plus[i][2]])
            i_4 = isCCW(c_R[D_plus[i][0] + D_plus[i][2]], d[D_plus[i][1] + D_plus[i][2]], c_R[D_plus[i][0] + D_plus[i][2] - 1], match[D_plus[i][0] + D_plus[i][2]][D_plus[i][1] + D_plus[i][2]])
            if i_1 == 1 and i_3 == 1: # If the first and last edges are both CLW.
                d_plus += 1
            elif i_2 == 1 and i_4 == 1: # If the first and last edges are both CCW.
                d_plus += 1 

    # To update d_0.
    for i in range(len(c_R) - 1):
        for j in range(len(d) - 1):

            # Recall, in the last entry of a curve we store the parity of the starting vertex.
            ccw = (isCCW(c_R[i - 1], d[j - 1], c_R[i], (d(len(d)) + j % 2) % 2) and isCCW(d[j - 1], c_R[i], d[j], (d(len(d)) + j % 2) % 2))
            clw = (isCLW(c_R[i - 1], d[j - 1], c_R[i], (d(len(d)) + j % 2) % 2) and isCLW(d[j - 1], c_R[i], d[j], (d(len(d)) + j % 2) % 2))
            # We need to check whether 4 edges are CCW or CLW, hence I broke it up into two cases of 3 edges.

            if c_R(len(c_R)) == d(len(d)): # Starting vertex has same parity.
                
                # (i + j) % 2 == 0 ensures i, j have the same parity, given that the starting vertex has the same parity.
                if (i + j) % 2 == 0 and (ccw or clw): # (i, j) is a crossing double point of c_R and d.
                    if (i + c_L[len(c_L)]) % 2 == 0:
                        if (nbr(c_L[i], c_R[i], 0) and c_L[i - 1] == c_R[i - 1] and d[j] == c_L[i]) or (nbr(c_L[i - 1], c_R[i - 1], 0) and c_L[i] == c_R[i] and d[j - 1] == c_L[i - 1]):
                            d_0 += 1
                    elif (i + c_L[len(c_L)]) % 2 == 1:
                        if (nbr(c_L[i], c_R[i], 1) and c_L[i - 1] == c_R[i - 1] and d[j] == c_L[i]) or (nbr(c_L[i - 1], c_R[i - 1], 1) and c_L[i] == c_R[i] and d[j - 1] == c_L[i - 1]):
                            d_0 += 1
                    # nbr(c_L[i], c_R[i], 0) and c_L[i - 1] == c_R[i - 1] checks if the two boundaries of \Delta concide AT \Delta_L[i] = \Delta_R[i].

                    elif {c_R[i - 1], c_L[i - 1]}.issubset(spoke[d[j - 1]]) or {c_R[i], c_L[i - 2]}.issubset(spoke[d[j - 1]]): # When the spoke is (c_R[i], c_L[i - 1]).
                        if d[j - 2] == c_L[i - 2]:
                            d_0 += 1
                    elif {c_R[i - 1], c_L[i + 1]}.issubset(spoke[d[j - 1]]) or {c_R[i], c_L[i]}.issubset(spoke[d[j - 1]]): # When the spoke is (c_R[i], c_L[i + 1]).
                        if d[j - 2] == c_L[i]:
                            d_0 += 1
                    elif {c_R[i - 1], c_L[i - 1]}.issubset(spoke[d[j]]) or {c_R[i], c_L[i - 2]}.issubset(spoke[d[j]]): # When the spoke is (c_R[i], c_L[i - 1]).
                        if d[j + 1] == c_L[i - 2]:
                            d_0 += 1
                    elif {c_R[i - 1], c_L[i + 1]}.issubset(spoke[d[j]]) or {c_R[i], c_L[i]}.issubset(spoke[d[j]]): # When the spoke is (c_R[i], c_L[i + 1]).
                        if d[j + 1] == c_L[i]:
                            d_0 += 1

            else: # Starting vertex has different parity.
                
                # (i + j) % 2 == 1 ensures i, j have same parity, given that the starting vertex has different parity.
                if (i + j) % 2 == 1 and (ccw or clw): # (i, j) is a crossing double point of c_R and d.
                    if (i + c_L[len(c_L)]) % 2 == 0:
                        if (nbr(c_L[i], c_R[i], 0) and c_L[i - 1] == c_R[i - 1] and d[j] == c_L[i]) or (nbr(c_L[i - 1], c_R[i - 1], 0) and c_L[i] == c_R[i] and d[j - 1] == c_L[i - 1]):
                            d_0 += 1
                    elif (i + c_L[len(c_L)]) % 2 == 1:
                        if (nbr(c_L[i], c_R[i], 1) and c_L[i - 1] == c_R[i - 1] and d[j] == c_L[i]) or (nbr(c_L[i - 1], c_R[i - 1], 1) and c_L[i] == c_R[i] and d[j - 1] == c_L[i - 1]):
                            d_0 += 1
                    # nbr(c_L[i], c_R[i], 0) and c_L[i - 1] == c_R[i - 1] checks if the two boundaries of \Delta concide AT \Delta_L[i] = \Delta_R[i].
                    
                    elif {c_R[i - 1], c_L[i - 1]}.issubset(spoke[d[j - 1]]) or {c_R[i], c_L[i - 2]}.issubset(spoke[d[j - 1]]): # When the spoke is (c_R[i], c_L[i - 1]).
                        if d[j - 2] == c_L[i - 2]:
                            d_0 += 1
                    elif {c_R[i - 1], c_L[i + 1]}.issubset(spoke[d[j - 1]]) or {c_R[i], c_L[i]}.issubset(spoke[d[j - 1]]): # When the spoke is (c_R[i], c_L[i + 1]).
                        if d[j - 2] == c_L[i]:
                            d_0 += 1
                    elif {c_R[i - 1], c_L[i - 1]}.issubset(spoke[d[j]]) or {c_R[i], c_L[i - 2]}.issubset(spoke[d[j]]): # When the spoke is (c_R[i], c_L[i - 1]).
                        if d[j + 1] == c_L[i - 2]:
                            d_0 += 1
                    elif {c_R[i - 1], c_L[i + 1]}.issubset(spoke[d[j]]) or {c_R[i], c_L[i]}.issubset(spoke[d[j]]): # When the spoke is (c_R[i], c_L[i + 1]).
                        if d[j + 1] == c_L[i]:
                            d_0 += 1
    
    # To update d_minus.

    #First we count the number of crossing double points of c_L_inverse and d, satisfying the desired conditions.
    for i in range(len(c_L_inverse) - 1):
        for j in range(len(d) - 1):

            n1 = 0
            n2 = 0

            # Recall, in the last entry of a curve we store the parity of the starting vertex.
            ccw = (isCCW(c_L_inverse[i - 1], d[j - 1], c_L_inverse[i], (d(len(d)) + j % 2) % 2) and isCCW(d[j - 1], c_L_inverse[i], d[j], (d(len(d)) + j % 2) % 2))
            clw = (isCLW(c_L_inverse[i - 1], d[j - 1], c_L_inverse[i], (d(len(d)) + j % 2) % 2) and isCLW(d[j - 1], c_L_inverse[i], d[j], (d(len(d)) + j % 2) % 2))
            # We need to check whether 4 edges are CCW or CLW, hence I broke it up into two cases of 3 edges.

            if c_L_inverse(len(c_L_inverse)) == d(len(d)): # Starting vertex has same parity.
                
                # (i + j) % 2 == 0 ensures i, j have the same parity, given that the starting vertex has the same parity.
                if (i + j) % 2 == 0 and (ccw or clw): # (i, j) is a crossing double point of c_L_inverse and d.

                    # D_minus[i][0] is the index of the starting vertex of the double path in c_L_inverse.
                    if (D_minus[i][0] + c_L_inverse[len(c_L_inverse)]) % 2 == 0:
                        if (nbr(c_L_inverse[D_minus[i][0]], c_R[L - (D_minus[i][0] - 1)], 0) and c_L_inverse[D_minus[i][0] - 1] == c_R[L - D_minus[i][0]] and d[D_minus[i][1] - 1] == c_R[L - (D_minus[i][0] - 1)]):
                            n1 = 1
                    elif (D_minus[i][0] + c_L_inverse[len(c_L_inverse)]) % 2 == 1:
                        if (nbr(c_L_inverse[D_minus[i][0]], c_R[L - (D_minus[i][0] - 1)], 1) and c_L_inverse[D_minus[i][0] - 1] == c_R[L - D_minus[i][0]] and d[D_minus[i][1] - 1] == c_R[L - (D_minus[i][0] - 1)]):
                            n1 = 1

                    if {c_L_inverse[D_minus[i][0]], c_R[(L - D_minus[i][0]) + 1]}.issubset(spoke[d[j - 1]]) or {c_L_inverse[D_minus[i][0] - 1], c_R[(L - D_minus[i][0])]}.issubset(spoke[d[j - 1]]):
                        if d[j - 2] == c_R[(L - D_minus[i][0])]:
                            n2 = 1 
                    elif {c_L_inverse[D_minus[i][0]], c_R[(L - D_minus[i][0]) - 1]}.issubset(spoke[d[j - 1]]) or {c_L_inverse[D_minus[i][0] - 1], c_R[(L - D_minus[i][0]) - 2]}.issubset(spoke[d[j - 1]]):
                        if d[j - 2] == c_R[(L - D_minus[i][0]) - 2]:
                            n2 = 1
                    
                    if n1 == 0 and n2 == 0:
                        d_minus += 1                    

            else: # Starting vertex has different parity.
                
                # (i + j) % 2 == 1 ensures i, j have same parity, given that the starting vertex has different parity.
                if (i + j) % 2 == 1 and (ccw or clw):

                    # D_minus[i][0] is the index of the starting vertex of the double path in c_L_inverse.
                    if (D_minus[i][0] + c_L_inverse[len(c_L_inverse)]) % 2 == 0:
                        if (nbr(c_L_inverse[D_minus[i][0]], c_R[L - (D_minus[i][0] - 1)], 0) and c_L_inverse[D_minus[i][0] - 1] == c_R[L - D_minus[i][0]] and d[D_minus[i][1] - 1] == c_R[L - (D_minus[i][0] - 1)]):
                            n1 = 1
                    elif (D_minus[i][0] + c_L_inverse[len(c_L_inverse)]) % 2 == 1:
                        if (nbr(c_L_inverse[D_minus[i][0]], c_R[L - (D_minus[i][0] - 1)], 1) and c_L_inverse[D_minus[i][0] - 1] == c_R[L - D_minus[i][0]] and d[D_minus[i][1] - 1] == c_R[L - (D_minus[i][0] - 1)]):
                            n1 = 1

                    if {c_L_inverse[D_minus[i][0]], c_R[(L - D_minus[i][0]) + 1]}.issubset(spoke[d[j - 1]]) or {c_L_inverse[D_minus[i][0] - 1], c_R[(L - D_minus[i][0])]}.issubset(spoke[d[j - 1]]):
                        if d[j - 2] == c_R[(L - D_minus[i][0])]:
                            n2 = 1 
                    elif {c_L_inverse[D_minus[i][0]], c_R[(L - D_minus[i][0]) - 1]}.issubset(spoke[d[j - 1]]) or {c_L_inverse[D_minus[i][0] - 1], c_R[(L - D_minus[i][0]) - 2]}.issubset(spoke[d[j - 1]]):
                        if d[j - 2] == c_R[(L - D_minus[i][0]) - 2]:
                            n2 = 1
                    
                    if n1 == 0 and n2 == 0:
                        d_minus += 1

    L = len(c_L_inverse) - 1
    # Now we count the number of crossing double paths of c_L_inverse and d, satisfying the desired conditions, i.e., when l > 0.
    for i in range(len(D_minus)):
        if D_minus[i][2] != 0: # Double Paths of positive length.
        # Actually D_minus[i][2] will never be zero, as we are only considering the positive length double paths in the helper function.
        # If you notice, we only append when D_minus[i][2] = length != 0.

            m1 = 0
            m2 = 0
            m3 = 0
            m4 = 0

            # First three arguments are edges and the last argument is the parity of the vertex.
            i_1 = isCLW(c_L_inverse[D_minus[i][0] - 1], d[D_minus[i][1] - 1], c_L_inverse[D_minus[i][0]], match[D_minus[i][0]][D_minus[i][1]])         
            i_2 = isCCW(c_L_inverse[D_minus[i][0] - 1], d[D_minus[i][1] - 1], c_L_inverse[D_minus[i][0]], match[D_minus[i][0]][D_minus[i][1]])
            i_3 = isCLW(c_L_inverse[D_minus[i][0] + D_minus[i][2]], d[D_minus[i][1] + D_minus[i][2]], c_L_inverse[D_minus[i][0] + D_minus[i][2] - 1], match[D_minus[i][0] + D_minus[i][2]][D_minus[i][1] + D_minus[i][2]])
            i_4 = isCCW(c_L_inverse[D_minus[i][0] + D_minus[i][2]], d[D_minus[i][1] + D_minus[i][2]], c_L_inverse[D_minus[i][0] + D_minus[i][2] - 1], match[D_minus[i][0] + D_minus[i][2]][D_minus[i][1] + D_minus[i][2]])
            # Now we don't need to do explicit vertex parity checks between c_L_inverse and d, like for the case of d_0, cause it is already take caren of in the helper function while building D_minus.
            # We never do parity checks between c_L and c_R, as i' is chosen such that the parity of the vertex is the same for both c_L and c_R.

            if (i_1 == 1 and i_3 == 1) or (i_2 == 1 and i_4 == 1): # At (i, j) we have a crossing double path of c_L_inverse and d.

                # D_minus[i][0] is the index of the starting vertex of the double path in c_L_inverse.
                if (D_minus[i][0] + c_L_inverse[len(c_L_inverse)]) % 2 == 0:
                    if (nbr(c_L_inverse[D_minus[i][0]], c_R[L - (D_minus[i][0] - 1)], 0) and c_L_inverse[D_minus[i][0] - 1] == c_R[L - D_minus[i][0]] and d[D_minus[i][1] - 1] == c_R[L - (D_minus[i][0] - 1)]):
                        m1 = 1
                elif (D_minus[i][0] + c_L_inverse[len(c_L_inverse)]) % 2 == 1:
                    if (nbr(c_L_inverse[D_minus[i][0]], c_R[L - (D_minus[i][0] - 1)], 1) and c_L_inverse[D_minus[i][0] - 1] == c_R[L - D_minus[i][0]] and d[D_minus[i][1] - 1] == c_R[L - (D_minus[i][0] - 1)]):
                        m1 = 1

                if (D_minus[i][0] + D_minus[i][2] + c_L_inverse[len(c_L_inverse)]) % 2 == 0:
                    if (nbr(c_L_inverse[D_minus[i][0] + D_minus[i][2] - 1], c_R[L - (D_minus[i][0] + D_minus[i][2])], 0) and c_L_inverse[D_minus[i][0] + D_minus[i][2]] == c_R[L - (D_minus[i][0] + D_minus[i][2]) - 1] and d[D_minus[i][1] + D_minus[i][2]] == c_R[L - (D_minus[i][0] + D_minus[i][2])]):
                        m2 = 1
                elif (D_minus[i][0] + D_minus[i][2] + c_L_inverse[len(c_L_inverse)]) % 2 == 1:
                    if (nbr(c_L_inverse[D_minus[i][0] + D_minus[i][2] - 1], c_R[L - (D_minus[i][0] + D_minus[i][2])], 1) and c_L_inverse[D_minus[i][0] + D_minus[i][2]] == c_R[L - (D_minus[i][0] + D_minus[i][2]) - 1] and d[D_minus[i][1] + D_minus[i][2]] == c_R[L - (D_minus[i][0] + D_minus[i][2])]):
                        m2 = 1
                
                if {c_L_inverse[D_minus[i][0]], c_R[(L - D_minus[i][0]) + 1]}.issubset(spoke[d[j - 1]]) or {c_L_inverse[D_minus[i][0] - 1], c_R[(L - D_minus[i][0])]}.issubset(spoke[d[j - 1]]):
                    if d[j - 2] == c_R[(L - D_minus[i][0])]:
                        m3 = 1 
                elif {c_L_inverse[D_minus[i][0]], c_R[(L - D_minus[i][0]) - 1]}.issubset(spoke[d[j - 1]]) or {c_L_inverse[D_minus[i][0] - 1], c_R[(L - D_minus[i][0]) - 2]}.issubset(spoke[d[j - 1]]):
                    if d[j - 2] == c_R[(L - D_minus[i][0]) - 2]:
                        m3 = 1

                if {c_L_inverse[D_minus[i][0] + D_minus[i][2]], c_R[(L - D_minus[i][0] - D_minus[i][2]) + 1]}.issubset(spoke[d[j + D_minus[i][2]]]) or {c_L_inverse[D_minus[i][0] + D_minus[i][2] - 1], c_R[(L - D_minus[i][0] - D_minus[i][2])]}.issubset(spoke[d[j + D_minus[i][2]]]):
                    if d[j + D_minus[i][2] + 1] == c_R[(L - D_minus[i][0] - D_minus[i][2]) + 1]:
                        m4 = 1
                elif {c_L_inverse[D_minus[i][0] + D_minus[i][2]], c_R[(L - D_minus[i][0] - D_minus[i][2]) - 1]}.issubset(spoke[d[j + D_minus[i][2]]]) or {c_L_inverse[D_minus[i][0] + D_minus[i][2] - 1], c_R[(L - D_minus[i][0] - D_minus[i][2]) - 2]}.issubset(spoke[d[j + D_minus[i][2]]]):
                    if d[j + D_minus[i][2] + 1] == c_R[(L - D_minus[i][0] - D_minus[i][2]) - 1]:
                        m4 = 1

            if m1 == 0 and m2 == 0 and m3 == 0 and m4 == 0:
                d_minus += 1

    return d_plus + d_0 + d_minus

# Need to take care of the case whether curves are two sided or not.
def intersection(x, y):
    (c, p) = isPrimitive(x)
    (d, q) = isPrimitive(y)
    if c != d and p != q:
        return p*q*Primitive_intersection(c, d)
    elif c == d and p != q:
        if p % 2 == 1 and q % 2 == 1:
            return 2*p*q*Primitive_intersection(c, d) + min(p, q)
        else:
            return 2*p*q*Primitive_intersection(c, d)
    elif c == d and p == q:
        return p*q*Primitive_intersection(c, d)
