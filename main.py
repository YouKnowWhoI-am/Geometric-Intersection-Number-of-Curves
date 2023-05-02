import sys
import DList
import Sys_of_Quads
import numpy as np

# The input is of the form abAcdBCD, where a, b, c, d represents arrow pointing clockwise, A, B, C, D represents arrow pointing counterclockwise.
# The input is asked as a list of tuples, where (1,1) stands for a, (-1,1) stands for A, (1,2) stands for b, (-1,2) stands for B, (1,3) stands for c, (-1,3) stands for C, and so on.
# Essentially, the first element of the tuple is the direction of the arrow and the second element is the identification of the arrow.
print("Enter the Euler characteristic of the surface, whether it is negative: '-1' or non-negative: '1'.")
euler = int(input('Enter Euler characteristic: '))

if euler == -1:
    print("Enter the fundamental polygon as a list of tuples after entering the genus.")
    Matrix = list(tuple(map(int, input().split())) for r in range(4 * int(input('Enter genus: ')))) 
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

M = Sys_of_Quads.Manifold(Matrix)    
M.check_valid()
M.Sys_of_Quads()

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
c1 = list(int(input()) for r in range(int(input('Enter length: '))))
isCombinatorialCurve(c1)
print("Enter second Combinatorial Curve:")
c2 = list(int(input()) for r in range(int(input('Enter length: '))))
isCombinatorialCurve(c2)

# O(1) time complexity.
def turn(e1, v, e2):
    # e1 and e2 are the edges that are incident to v, and e1 is the edge that is traversed before e2.
    # The function returns the turn from e1 to e2 at v.
    if e1 == e2:
        return 0
    if v == 1: # v is the vertex z
        if e2 - e1 <= len(M.matrix) // 2 and e2 - e1 >= -len(M.matrix) // 2:
            return e2 - e1
        elif e2 - e1 > len(M.matrix) // 2:
            return e2 - e1 - len(M.matrix)
        else:
            return e2 - e1 + len(M.matrix)
    else: # v is the vertex a
        if M.index_a[e2] - M.index_a[e1] <= len(M.matrix) // 2 and M.index_a[e2] - M.index_a[e1] >= -len(M.matrix) // 2:
            return M.index_a[e2] - M.index_a[e1]
        elif M.index_a[e2] - M.index_a[e1] > len(M.matrix) // 2:
            return M.index_a[e2] - M.index_a[e1] - len(M.matrix)
        else:
            return M.index_a[e2] - M.index_a[e1] + len(M.matrix)

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
    dlist = DList.DoublyLinkedList(M.index_a, M.nbr_a)
    for i in range(len(turn_seq)):
        if i == 0:
            dlist.insertEnd(c[i], turn_seq[i], 1)
        elif turn_seq[i] != turn_seq[i - 1]:
            dlist.insertEnd(c[i], turn_seq[i], 1)
        elif turn_seq[i] == turn_seq[i - 1]:
            dlist.updateEnd()
    return dlist

def toTurn_sequence(dlist):
    # dlist is the run length encoding of a cycle c.
    # The function returns the turn sequence of c.
    turn_seq = [0] * dlist.total_length()
    temp = dlist.start
    counter = 0
    while temp.next != dlist.start:
        for i in range(temp.run_length):
            turn_seq[counter] = temp.turn
            counter += 1
        temp = temp.next
    for i in range(temp.run_length):
        turn_seq[counter] = temp.turn
        counter += 1
    return turn_seq

def toEdge_sequence(dlist):
    # dlist is the run length encoding of a cycle c.
    # The function returns the edge sequence of c.
    edge_seq = [0] * (dlist.total_length())
    turn_seq = toTurn_sequence(dlist)
    edge_seq[0] = dlist.start_edge
    # edge_seq[dlist.total_length()] = dlist.start_vertex # The parity of the first vertex.
    for i in range(1, dlist.total_length()):
        if i % 2 == 1:
            edge_seq[i] = (edge_seq[i - 1] + turn_seq[i]) % len(M.matrix)
        else:
            edge_seq[i] = M.nbr_a[(M.index_a[edge_seq[i - 1]] + turn_seq[i]) % len(M.matrix)]
    return edge_seq

# O(l) time complexity.
def isPrimitive(c):
    # c is a combinatorial curve
    # The function returns c if c is primitive, and (d, k) if c = d^{k} for some primitive curve d.
    for i in range(len(c)):
        if i % 2 == 0 and i != 0:
            if turn(c[i - 1], 0, c[i]) != 0:
                return c

def invert(dlist):
    # Input is a combinatorial curve c.
    # The function returns c^{-1}.
    if dlist.start_vertex == 0:
        if dlist.start_edge - dlist.start.turn < 0:
            edge = dlist.start_edge - dlist.start.turn + len(M.matrix)
        else:
            edge = dlist.start_edge - dlist.start.turn
    else:
        if M.index_a[dlist.start_edge] - dlist.start.turn < 0:
            edge = M.nbr_a[M.index_a[dlist.start_edge] - dlist.start.turn + len(M.matrix)]
        else:
            edge = M.nbr_a[M.index_a[dlist.start_vertex] - dlist.start.turn]
    dlist_inverse = DList.DoublyLinkedList(M.index_a, M.nbr_a, edge, dlist.start_vertex)
    temp = dlist.start
    while (temp.prev != dlist.start):
        dlist_inverse.insertEnd(edge, temp.turn, temp.run_length)
        temp = temp.prev
    dlist_inverse.insertEnd(edge, temp.turn, temp.run_length)
    return dlist_inverse


def helper(match, k, l, length, D, c, d):
    for i in range(len(c) * len(d)): # We haven't reached the top right corner of the grid.
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

def nbr(e1, e2, v):
    if v == 1:
        if e1 - e2 == 1 or e1 - e2 == -1:
            return 1    
    elif v == 0:
        if M.index_a[e1] - M.index_a[e2] == 1 or M.index_a[e1] - M.index_a[e2] == -1:
            return 1    
    else:
        return 0

def isCLW(e_1, e_2, e_3, v):
    if v == 1:
        E_3 = (e_3 + (len(M.matrix) - e_1)) % len(M.matrix)
        E_2 = (e_2 + (len(M.matrix) - e_1)) % len(M.matrix)
        if E_2 > 0 and E_3 > E_2:
            return 1
    elif v == 0:
        E_3 = (M.index_a[e_3] + (len(M.matrix) - M.index_a[e_1])) % len(M.matrix)
        E_2 = (M.index_a[e_2] + (len(M.matrix) - M.index_a[e_1])) % len(M.matrix)
        if E_2 > 0 and E_3 > E_2:
            return 1

def isCCW(e_1, e_2, e_3, v):
    return isCLW(e_3, e_2, e_1, v)

# O(l^2) time complexity
def Primitive_intersection(C, D):
    # Input is two primitive combinatorial curves x and y.
    # The function returns the intersection number of x and y.
    D.canonical(M)
    d = toEdge_sequence(D)

    C_inverse = invert(C)
    C_inverse.canonical(M)
    c_L_inverse = toEdge_sequence(C_inverse)

    C_L = invert(C_inverse) # C_inverse is now already canonical, we just need to invert and use it.
    c_L = toEdge_sequence(C_L)

    C.canonical(M)
    c_R = toEdge_sequence(C)

    # We create a grid of size (len(c_R) x len(d)). Operating on the grid gives us overall a O(l^2) time complexity.
    match = [[0 for i in range(len(d))] for j in range(len(c_R))] # For D_plus.
    match_2 = [[0 for i in range(len(d))] for j in range(len(c_L_inverse))] # For D_minus.

    # We fill the grid if there is a match of edges as well as the parity of the vertices between the two curves.
    # match[i][j] = 1 if there is a match of edges and the parity of the vertices is 0.
    # match[i][j] = 2 if there is a match of edges and the parity of the vertices is 1.
    for i in range(len(c_R)):
        for j in range(len(d)):
            if c_R[i] == d[j] and (C.start_vertex + i % 2) % 2 == (D.start_vertex + j % 2) % 2: # We check if there is a match of edges and the parity of the vertices is the same.
                match[i][j] = 1 + ((C.start_vertex + i % 2) % 2) 

    for i in range(len(c_L_inverse)):
        for j in range(len(d)):
            if c_L_inverse[i] == d[j] and (C_inverse.start_vertex + i % 2) % 2 == (D.start_vertex + j % 2) % 2: # We check if there is a match of edges and the parity of the vertices is the same.
                match_2[i][j] = 1 + ((C_inverse.start_vertex + i % 2) % 2)
    
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
    for i in range(len(c_R)):
        for j in range(len(d)):

            # Recall, in the last entry of a curve we store the parity of the starting vertex.
            ccw = (isCCW(c_R[i - 1], d[j - 1], c_R[i], (D.start_vertex + j % 2) % 2) and isCCW(d[j - 1], c_R[i], d[j], (D.start_vertex + j % 2) % 2))
            clw = (isCLW(c_R[i - 1], d[j - 1], c_R[i], (D.start_vertex + j % 2) % 2) and isCLW(d[j - 1], c_R[i], d[j], (D.start_vertex + j % 2) % 2))
            # We need to check whether 4 edges are CCW or CLW, hence I broke it up into two cases of 3 edges.

            if C.start_vertex == D.start_vertex: # Starting vertex has same parity.
                
                # (i + j) % 2 == 0 ensures i, j have the same parity, given that the starting vertex has the same parity.
                if (i + j) % 2 == 0 and (ccw or clw): # (i, j) is a crossing double point of c_R and d.
                    if (i + C_L.start_vertex) % 2 == 0:
                        if (nbr(c_L[i], c_R[i], 0) and c_L[i - 1] == c_R[i - 1] and d[j] == c_L[i]) or (nbr(c_L[i - 1], c_R[i - 1], 0) and c_L[i] == c_R[i] and d[j - 1] == c_L[i - 1]):
                            d_0 += 1
                    elif (i + C_L.start_vertex) % 2 == 1:
                        if (nbr(c_L[i], c_R[i], 1) and c_L[i - 1] == c_R[i - 1] and d[j] == c_L[i]) or (nbr(c_L[i - 1], c_R[i - 1], 1) and c_L[i] == c_R[i] and d[j - 1] == c_L[i - 1]):
                            d_0 += 1
                    # nbr(c_L[i], c_R[i], 0) and c_L[i - 1] == c_R[i - 1] checks if the two boundaries of \Delta concide AT \Delta_L[i] = \Delta_R[i].

                    elif {c_R[i - 1], c_L[i - 1]}.issubset(M.spoke[d[j - 1]]) or {c_R[i], c_L[i - 2]}.issubset(M.spoke[d[j - 1]]): # When the M.spoke is (c_R[i], c_L[i - 1]).
                        if d[j - 2] == c_L[i - 2]:
                            d_0 += 1
                    elif {c_R[i - 1], c_L[i + 1]}.issubset(M.spoke[d[j - 1]]) or {c_R[i], c_L[i]}.issubset(M.spoke[d[j - 1]]): # When the M.spoke is (c_R[i], c_L[i + 1]).
                        if d[j - 2] == c_L[i]:
                            d_0 += 1
                    elif {c_R[i - 1], c_L[i - 1]}.issubset(M.spoke[d[j]]) or {c_R[i], c_L[i - 2]}.issubset(M.spoke[d[j]]): # When the M.spoke is (c_R[i], c_L[i - 1]).
                        if d[j + 1] == c_L[i - 2]:
                            d_0 += 1
                    elif {c_R[i - 1], c_L[i + 1]}.issubset(M.spoke[d[j]]) or {c_R[i], c_L[i]}.issubset(M.spoke[d[j]]): # When the M.spoke is (c_R[i], c_L[i + 1]).
                        if d[j + 1] == c_L[i]:
                            d_0 += 1

            else: # Starting vertex has different parity.
                
                # (i + j) % 2 == 1 ensures i, j have same parity, given that the starting vertex has different parity.
                if (i + j) % 2 == 1 and (ccw or clw): # (i, j) is a crossing double point of c_R and d.
                    if (i + C_L.start_vertex) % 2 == 0:
                        if (nbr(c_L[i], c_R[i], 0) and c_L[i - 1] == c_R[i - 1] and d[j] == c_L[i]) or (nbr(c_L[i - 1], c_R[i - 1], 0) and c_L[i] == c_R[i] and d[j - 1] == c_L[i - 1]):
                            d_0 += 1
                    elif (i + C_L.start_vertex) % 2 == 1:
                        if (nbr(c_L[i], c_R[i], 1) and c_L[i - 1] == c_R[i - 1] and d[j] == c_L[i]) or (nbr(c_L[i - 1], c_R[i - 1], 1) and c_L[i] == c_R[i] and d[j - 1] == c_L[i - 1]):
                            d_0 += 1
                    # nbr(c_L[i], c_R[i], 0) and c_L[i - 1] == c_R[i - 1] checks if the two boundaries of \Delta concide AT \Delta_L[i] = \Delta_R[i].
                    
                    elif {c_R[i - 1], c_L[i - 1]}.issubset(M.spoke[d[j - 1]]) or {c_R[i], c_L[i - 2]}.issubset(M.spoke[d[j - 1]]): # When the M.spoke is (c_R[i], c_L[i - 1]).
                        if d[j - 2] == c_L[i - 2]:
                            d_0 += 1
                    elif {c_R[i - 1], c_L[i + 1]}.issubset(M.spoke[d[j - 1]]) or {c_R[i], c_L[i]}.issubset(M.spoke[d[j - 1]]): # When the M.spoke is (c_R[i], c_L[i + 1]).
                        if d[j - 2] == c_L[i]:
                            d_0 += 1
                    elif {c_R[i - 1], c_L[i - 1]}.issubset(M.spoke[d[j]]) or {c_R[i], c_L[i - 2]}.issubset(M.spoke[d[j]]): # When the M.spoke is (c_R[i], c_L[i - 1]).
                        if d[j + 1] == c_L[i - 2]:
                            d_0 += 1
                    elif {c_R[i - 1], c_L[i + 1]}.issubset(M.spoke[d[j]]) or {c_R[i], c_L[i]}.issubset(M.spoke[d[j]]): # When the M.spoke is (c_R[i], c_L[i + 1]).
                        if d[j + 1] == c_L[i]:
                            d_0 += 1
    
    # To update d_minus.

    #First we count the number of crossing double points of c_L_inverse and d, satisfying the desired conditions.
    L = len(c_L_inverse)
    for i in range(len(c_L_inverse)):
        for j in range(len(d)):

            n1 = 0
            n2 = 0

            # Recall, in the last entry of a curve we store the parity of the starting vertex.
            ccw = (isCCW(c_L_inverse[i - 1], d[j - 1], c_L_inverse[i], (D.start_vertex + j % 2) % 2) and isCCW(d[j - 1], c_L_inverse[i], d[j], (D.start_vertex + j % 2) % 2))
            clw = (isCLW(c_L_inverse[i - 1], d[j - 1], c_L_inverse[i], (D.start_vertex + j % 2) % 2) and isCLW(d[j - 1], c_L_inverse[i], d[j], (D.start_vertex + j % 2) % 2))
            # We need to check whether 4 edges are CCW or CLW, hence I broke it up into two cases of 3 edges.

            if C_inverse.start_vertex == D.start_vertex: # Starting vertex has same parity.
                
                # (i + j) % 2 == 0 ensures i, j have the same parity, given that the starting vertex has the same parity.
                if (i + j) % 2 == 0 and (ccw or clw): # (i, j) is a crossing double point of c_L_inverse and d.

                    # D_minus[i][0] is the index of the starting vertex of the double path in c_L_inverse.
                    if (D_minus[i][0] + C_inverse.start_vertex) % 2 == 0:
                        if (nbr(c_L_inverse[D_minus[i][0]], c_R[L - (D_minus[i][0] - 1)], 0) and c_L_inverse[D_minus[i][0] - 1] == c_R[L - D_minus[i][0]] and d[D_minus[i][1] - 1] == c_R[L - (D_minus[i][0] - 1)]):
                            n1 = 1
                    elif (D_minus[i][0] + C_inverse.start_vertex) % 2 == 1:
                        if (nbr(c_L_inverse[D_minus[i][0]], c_R[L - (D_minus[i][0] - 1)], 1) and c_L_inverse[D_minus[i][0] - 1] == c_R[L - D_minus[i][0]] and d[D_minus[i][1] - 1] == c_R[L - (D_minus[i][0] - 1)]):
                            n1 = 1

                    if {c_L_inverse[D_minus[i][0]], c_R[(L - D_minus[i][0]) + 1]}.issubset(M.spoke[d[j - 1]]) or {c_L_inverse[D_minus[i][0] - 1], c_R[(L - D_minus[i][0])]}.issubset(M.spoke[d[j - 1]]):
                        if d[j - 2] == c_R[(L - D_minus[i][0])]:
                            n2 = 1 
                    elif {c_L_inverse[D_minus[i][0]], c_R[(L - D_minus[i][0]) - 1]}.issubset(M.spoke[d[j - 1]]) or {c_L_inverse[D_minus[i][0] - 1], c_R[(L - D_minus[i][0]) - 2]}.issubset(M.spoke[d[j - 1]]):
                        if d[j - 2] == c_R[(L - D_minus[i][0]) - 2]:
                            n2 = 1
                    
                    if n1 == 0 and n2 == 0:
                        d_minus += 1                    

            else: # Starting vertex has different parity.
                
                # (i + j) % 2 == 1 ensures i, j have same parity, given that the starting vertex has different parity.
                if (i + j) % 2 == 1 and (ccw or clw):

                    # D_minus[i][0] is the index of the starting vertex of the double path in c_L_inverse.
                    if (D_minus[i][0] + C_inverse.start_vertex) % 2 == 0:
                        if (nbr(c_L_inverse[D_minus[i][0]], c_R[L - (D_minus[i][0] - 1)], 0) and c_L_inverse[D_minus[i][0] - 1] == c_R[L - D_minus[i][0]] and d[D_minus[i][1] - 1] == c_R[L - (D_minus[i][0] - 1)]):
                            n1 = 1
                    elif (D_minus[i][0] + C_inverse.start_vertex) % 2 == 1:
                        if (nbr(c_L_inverse[D_minus[i][0]], c_R[L - (D_minus[i][0] - 1)], 1) and c_L_inverse[D_minus[i][0] - 1] == c_R[L - D_minus[i][0]] and d[D_minus[i][1] - 1] == c_R[L - (D_minus[i][0] - 1)]):
                            n1 = 1

                    if {c_L_inverse[D_minus[i][0]], c_R[(L - D_minus[i][0]) + 1]}.issubset(M.spoke[d[j - 1]]) or {c_L_inverse[D_minus[i][0] - 1], c_R[(L - D_minus[i][0])]}.issubset(M.spoke[d[j - 1]]):
                        if d[j - 2] == c_R[(L - D_minus[i][0])]:
                            n2 = 1 
                    elif {c_L_inverse[D_minus[i][0]], c_R[(L - D_minus[i][0]) - 1]}.issubset(M.spoke[d[j - 1]]) or {c_L_inverse[D_minus[i][0] - 1], c_R[(L - D_minus[i][0]) - 2]}.issubset(M.spoke[d[j - 1]]):
                        if d[j - 2] == c_R[(L - D_minus[i][0]) - 2]:
                            n2 = 1
                    
                    if n1 == 0 and n2 == 0:
                        d_minus += 1

    L = len(c_L_inverse)
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
                if (D_minus[i][0] + C_inverse.start_vertex) % 2 == 0:
                    if (nbr(c_L_inverse[D_minus[i][0]], c_R[L - (D_minus[i][0] - 1)], 0) and c_L_inverse[D_minus[i][0] - 1] == c_R[L - D_minus[i][0]] and d[D_minus[i][1] - 1] == c_R[L - (D_minus[i][0] - 1)]):
                        m1 = 1
                elif (D_minus[i][0] + C_inverse.start_vertex) % 2 == 1:
                    if (nbr(c_L_inverse[D_minus[i][0]], c_R[L - (D_minus[i][0] - 1)], 1) and c_L_inverse[D_minus[i][0] - 1] == c_R[L - D_minus[i][0]] and d[D_minus[i][1] - 1] == c_R[L - (D_minus[i][0] - 1)]):
                        m1 = 1

                if (D_minus[i][0] + D_minus[i][2] + C_inverse.start_vertex) % 2 == 0:
                    if (nbr(c_L_inverse[D_minus[i][0] + D_minus[i][2] - 1], c_R[L - (D_minus[i][0] + D_minus[i][2])], 0) and c_L_inverse[D_minus[i][0] + D_minus[i][2]] == c_R[L - (D_minus[i][0] + D_minus[i][2]) - 1] and d[D_minus[i][1] + D_minus[i][2]] == c_R[L - (D_minus[i][0] + D_minus[i][2])]):
                        m2 = 1
                elif (D_minus[i][0] + D_minus[i][2] + C_inverse.start_vertex) % 2 == 1:
                    if (nbr(c_L_inverse[D_minus[i][0] + D_minus[i][2] - 1], c_R[L - (D_minus[i][0] + D_minus[i][2])], 1) and c_L_inverse[D_minus[i][0] + D_minus[i][2]] == c_R[L - (D_minus[i][0] + D_minus[i][2]) - 1] and d[D_minus[i][1] + D_minus[i][2]] == c_R[L - (D_minus[i][0] + D_minus[i][2])]):
                        m2 = 1
                
                if {c_L_inverse[D_minus[i][0]], c_R[(L - D_minus[i][0]) + 1]}.issubset(M.spoke[d[j - 1]]) or {c_L_inverse[D_minus[i][0] - 1], c_R[(L - D_minus[i][0])]}.issubset(M.spoke[d[j - 1]]):
                    if d[j - 2] == c_R[(L - D_minus[i][0])]:
                        m3 = 1 
                elif {c_L_inverse[D_minus[i][0]], c_R[(L - D_minus[i][0]) - 1]}.issubset(M.spoke[d[j - 1]]) or {c_L_inverse[D_minus[i][0] - 1], c_R[(L - D_minus[i][0]) - 2]}.issubset(M.spoke[d[j - 1]]):
                    if d[j - 2] == c_R[(L - D_minus[i][0]) - 2]:
                        m3 = 1

                if {c_L_inverse[D_minus[i][0] + D_minus[i][2]], c_R[(L - D_minus[i][0] - D_minus[i][2]) + 1]}.issubset(M.spoke[d[j + D_minus[i][2]]]) or {c_L_inverse[D_minus[i][0] + D_minus[i][2] - 1], c_R[(L - D_minus[i][0] - D_minus[i][2])]}.issubset(M.spoke[d[j + D_minus[i][2]]]):
                    if d[j + D_minus[i][2] + 1] == c_R[(L - D_minus[i][0] - D_minus[i][2]) + 1]:
                        m4 = 1
                elif {c_L_inverse[D_minus[i][0] + D_minus[i][2]], c_R[(L - D_minus[i][0] - D_minus[i][2]) - 1]}.issubset(M.spoke[d[j + D_minus[i][2]]]) or {c_L_inverse[D_minus[i][0] + D_minus[i][2] - 1], c_R[(L - D_minus[i][0] - D_minus[i][2]) - 2]}.issubset(M.spoke[d[j + D_minus[i][2]]]):
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
