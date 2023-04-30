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
# print("Enter second Combinatorial Curve:")
# c2 = list(int(input()) for r in range(int(input('Enter length: '))))
# print("Combinatorial Curve 1: ", c1)

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
    dlist = DList.DoublyLinkedList(M.index_a, M.nbr_a)
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

# def change(dlist):
#     dlist.start.turn = 12
# change(dlist)
# dlist.display()

def geodesic(self, M):
    n = len(M.matrix)
    # The function returns a reduced cycle freely homotopic to c.
    if self.check_empty():
        return 0
    elif self.number_of_runs() > 5:
        temp = self.start
        while (self.number_of_runs() > 5 and (temp != self.start.prev or (temp == self.start.prev and temp.mark_1 == False))):
            if temp.next.turn == 0:
                reductions.std_spur(self, temp)
            elif temp.turn == 0:
                reductions.std_spur(self, temp.prev)
            elif temp.prev.turn == 0:
                reductions.std_spur(self, temp.prev.prev)

            elif temp.next.turn == 1 and temp.next.next.turn == 2 and temp.next.next.next.turn == 1:
                reductions.std_lt_bracket(self, temp, n)
            elif temp.turn == 1 and temp.next.turn == 2 and temp.next.next.turn == 1:
                reductions.std_lt_bracket(self, temp.prev, n)
            elif temp.prev.turn == 1 and temp.turn == 2 and temp.next.turn == 1:
                reductions.std_lt_bracket(self, temp.prev.prev, n)
            elif temp.prev.prev.turn == 1 and temp.prev.turn == 2 and temp.turn == 1:
                reductions.std_lt_bracket(self, temp.prev.prev.prev, n)
            elif temp.prev.prev.prev.turn == 1 and temp.prev.prev.turn == 2 and temp.prev.turn == 1:
                reductions.std_lt_bracket(self, temp.prev.prev.prev.prev, n)
            
            elif temp.next.turn == -1 and temp.next.next.turn == -2 and temp.next.next.next.turn == -1:
                reductions.std_rt_bracket(self, temp, n)
            elif temp.turn == -1 and temp.next.turn == -2 and temp.next.next.turn == -1:
                reductions.std_rt_bracket(self, temp.prev, n)
            elif temp.prev.turn == -1 and temp.turn == -2 and temp.next.turn == -1:
                reductions.std_rt_bracket(self, temp.prev.prev, n)
            elif temp.prev.prev.turn == -1 and temp.prev.turn == -2 and temp.turn == -1:
                reductions.std_rt_bracket(self, temp.prev.prev.prev, n)
            elif temp.prev.prev.prev.turn == -1 and temp.prev.prev.turn == -2 and temp.prev.turn == -1:
                reductions.std_rt_bracket(self, temp.prev.prev.prev.prev, n)

            else:
                temp = temp.next
                temp.mark_1 = True

reductions.std_rt_bracket(dlist, dlist.start.next, 20)
# geodesic(dlist, M)
dlist.display()

# def toEdge_sequence(dlist):
#     # dlist is the run length encoding of a cycle c.
#     # The function returns the edge sequence of c.
#     edge_seq = [0] * (dlist.total_length() + 1)
#     temp = dlist.start
#     edge_seq[0] = temp.edge
#     edge_seq[dlist.total_length()] = temp.vertex # The parity of the first vertex.
#     counter = 1
#     i = 1
#     while i < dlist.total_length():
#         while counter < temp.run_length:
#             if (temp.vertex + counter) % 2 == 0:
#                 edge_seq[i] = edge_seq[i - 1] + temp.turn
#             else:
#                 edge_seq[i] = M.nbr_a[M.index_a[edge_seq[i - 1]] + temp.turn]
#             counter += 1
#             i += 1
#         temp = temp.next
#         counter = 0
#         i += 1
#     return edge_seq

# print(toEdge_sequence(dlist))

# dlist.geodesic(M)
# dlist.display()