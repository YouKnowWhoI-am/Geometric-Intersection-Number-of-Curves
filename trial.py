import sys
import DList
import reductions
import Sys_of_Quads

'''
seen = set()
for x in M:
    if x in seen:
        sys.exit("Invalid Input: Input has duplicates.")
    else:
        seen.add(x)
    seen.clear()   
'''
#M = [1,2,3,4]
#print(len(M))

# faces = [[0] * 4] * int((len(M)/2)) (SHALLOW COPY, DOESN'T WORK)
#spoke = [[[0, 0][0, 0]] for j in range(5)]
#print(spoke)
#print(2 - 3)
'''
class Node:
	def __init__(self, data):
		self.data = data
		self.next = None
		self.prev = None

class DoublyLinkedList:
	def __init__(self):
		self.head = None

	def insert_at_head(self, value):
		n = Node(value)
		n.next = self.head
		if(self.head != None):
			self.head.prev = n
		self.head = n

	def insert_at_tail(self, value):

		n = Node(value)

		if self.head is None:
			self.head = n
			return

		last = self.head
		while (last.next):
			last = last.next

		last.next = n

	def display(self):
		temp = self.head
		while(temp):
			print(temp.data, end=" ")
			temp = temp.next

if __name__ == '__main__':
	dllist = DoublyLinkedList()
	dllist.insert_at_tail(1)
	dllist.insert_at_tail(2)
	dllist.insert_at_tail(3)
	dllist.insert_at_tail(4)
	dllist.insert_at_tail(5)
	print("After insertion at tail: ")
	dllist.display()
	dllist.insert_at_head(0)
	print("\nAfter insertion at head: ")
	dllist.display()


n = 5
def change(n):
	n = 3
change(n)
print(n)

arr = [1,2,3,4,5]
def change(arr):
	arr[0] = 3
change(arr)
print(arr)

print("Hello World\n")
print("Hello World2\n")
'''

Matrix = list(tuple(map(int, input().split())) for r in range(4 * int(input('Enter genus: ')))) 
M = Sys_of_Quads.Manifold(Matrix) 
M.check_valid()
M.Sys_of_Quads() 
print(M.faces)
print(M.spoke)
print(M.index_a)
print(M.nbr_a)

print("Enter first Combinatorial Curve:")
c1 = list(int(input()) for r in range(int(input('Enter length: '))))
print("Enter second Combinatorial Curve:")
c2 = list(int(input()) for r in range(int(input('Enter length: '))))
print("Combinatorial Curve 1: ", c1)

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

print(turn_sequence(c1))

def run_length_encoding(c, turn_seq):
    # turn_seq is a turn sequence
    # The function returns the run-length encoding of turn_seq which is a circular doubly linked list.
    dlist = DList.DoublyLinkedList(0, 0, M.index_a, M.nbr_a)
    for i in range(len(turn_seq)):
        if i == 0:
            dlist.insertEnd(c[i], turn_seq[i], 1)
        elif turn_seq[i] != turn_seq[i - 1]:
            dlist.insertEnd(c[i], turn_seq[i], 1)
        elif turn_seq[i] == turn_seq[i - 1]:
            dlist.updateEnd()
    return dlist

dlist = run_length_encoding(c1, turn_sequence(c1))
dlist.display()
dlist_ = run_length_encoding(c2, turn_sequence(c2))
dlist_.display()

# def change(dlist):
#     dlist.start.turn = 12
# change(dlist)
# dlist.display()

# reductions.std_rt_bracket(dlist, dlist.start.next, 20)
# dlist.geodesic(M)
# dlist.display()
# dlist.canonical(M)
# dlist.display()

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

print(toTurn_sequence(dlist))
# toEdge_sequence(dlist)
# print(toEdge_sequence(dlist))

dlist.geodesic(M)
dlist.display()

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