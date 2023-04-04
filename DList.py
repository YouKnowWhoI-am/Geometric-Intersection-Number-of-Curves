import main
# Maybe need to break this into two files, to avoid circular import.

index_a = main.index_a
nbr_a = main.nbr_a

# Except for self.start.edge every other node.edge might just be garbage.
# We need the self.start.edge to compute the geodesic from the turn sequence. 
# We don't bother to update the edge of the other nodes, as they will make the running time of the algorithm O(l^2) instead of O(l).
# It also makes the code much simpler.
# Same goes about the vertex of the nodes. We only need the vertex of the self.start node to compute the geodesic from the turn sequence.

# Structure of a Node
class Node:
    def __init__(self, vertex, edge, turn, run_length, mark_1 = False, mark_2 = False):
        self.vertex = vertex # Vertex at the beginning of the run
        self.edge = edge # Edge into the run
        self.turn = turn
        self.run_length = run_length
        self.mark_1 = mark_1 # mark_1 is for removing spurs and brackets to obtain a geodesic.
        self.mark_2 = mark_2 # mark_2 is for elementary right shifts to obtain a canonical geodesic.
        self.next = None
        self.prev = None
	
class DoublyLinkedList:
    def __init__(self):
        self.start = None

    def check_empty(self):
        if self.start == None:
            return True
        else:
            return False
        
    def number_of_runs(self):
        temp = self.start
        total = 0
        while (temp.next != self.start):
            total += 1
            temp = temp.next
        total += 1
        return total

    def total_length(self):
        temp = self.start
        total = 0
        while (temp.next != self.start):
            total += temp.run_length
            temp = temp.next
        total += temp.run_length
        return total
    
    def insertEnd(self, edge, turn, run_length):
    # If the list is empty, create a single node circular and doubly linked list
        if (self.start == None):
            new_node = Node(edge, turn, run_length)
            new_node.next = new_node.prev = new_node
            self.start = new_node
            return
	 
        last = (self.start).prev # If list is not empty find last node
        new_node = Node(edge, turn, run_length)
        new_node.next = self.start
        (self.start).prev = new_node
        new_node.prev = last
        last.next = new_node
    
    def updateEnd(self):
        last = (self.start).prev
        last.run_length += 1

    def insertBegin(self, edge, turn, run_length):
        last = (self.start).prev
        new_node = Node(edge, turn, run_length)
        new_node.next = self.start
        new_node.prev = last
        last.next = (self.start).prev = new_node
        self.start = new_node

    # Function to insert node with value as value1.The new node is inserted after the node with value2
    def insertAfter(self, node, edge, turn, run_length):
        new_node = Node(edge, turn, run_length)

        # insert new_node between temp and next.
        new_node.next = node.next
        new_node.prev = node
        node.next.prev = new_node
        node.next = new_node

    def deleteNode(self, node):
        edge = node.edge
        if (self.start == None or node == None):
            return
        # If node to be deleted is start node
        if (self.start == node):
            self.start = node.next 

            for i in range(node.run_length):
                if i % 2 == 1:
                    edge = (edge + node.turn) % len(nbr_a) # Note len(nbr_a) = len(nbr_z) = len(M)
                else:
                    edge = nbr_a[(index_a[edge] + node.turn) % len(nbr_a)]
            self.start.edge = edge
            self.start.vertex = (self.start.vertex + (node.run_length % 2)) % 2 

            node.prev.next = node.next
            node.next.prev = node.prev        
        # If node to be deleted is not start node
        else:
            node.prev.next = node.next
            node.next.prev = node.prev

    def decrease_run_length_by(self, node, value):
        if node.run_length > value:
            node.run_length -= value
        else:
            self.deleteNode(node)
    
    def change_turn(self, node, new_turn):
        node.turn = new_turn
        # Merge Operations
        if node.next.turn == new_turn:
            node.run_length += node.next.run_length
            self.deleteNode(node.next)
        if node.prev.turn == new_turn:
            node.prev.run_length += node.run_length
            self.deleteNode(node)

    def display(self):
        temp = self.start

        print("Traversal in forward direction:")
        while (temp.next != self.start):
            print('(' + str(temp.turn) + ',' + str(temp.run_length) + ')', end=" ")
            temp = temp.next
        print('(' + str(temp.turn) + ',' + str(temp.run_length) + ')', end=" ")

        print("Traversal in reverse direction:")
        last = self.start.prev
        temp = last
        while (temp.prev != last):
            print('(' + str(temp.turn) + ',' + str(temp.run_length) + ')', end=" ")
            temp = temp.prev
        print('(' + str(temp.turn) + ',' + str(temp.run_length) + ')', end=" ")
