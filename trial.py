import sys
#for i in range(8): print(i)

# Check if the input has duplicates.
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
print(2 - 3)
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


