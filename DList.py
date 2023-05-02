import reductions

# Except for self.start.edge every other node.edge might just be garbage.
# We need the self.start.edge to compute the geodesic from the turn sequence. 
# We don't bother to update the edge of the other nodes, as they will make the running time of the algorithm O(l^2) instead of O(l).
# It also makes the code much simpler.
# Same goes about the vertex of the nodes. We only need the vertex of the self.start node to compute the geodesic from the turn sequence.

# Structure of a Node
class Node:
    def __init__(self, turn, run_length):
        self.turn = turn
        self.run_length = run_length
        self.mark_1 = False # mark_1 is for removing spurs and brackets to obtain a geodesic.
        self.mark_2 = False # mark_2 is for elementary right shifts to obtain a canonical geodesic.
        self.next = None
        self.prev = None
	
class DoublyLinkedList:
    def __init__(self, index_a, nbr_a, start_edge, start_vertex):
        self.start = None
        self.index_a = index_a
        self.nbr_a = nbr_a
        self.start_edge = start_edge
        self.start_vertex = start_vertex

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
    
    def start_list(self, edge, turn, run_length):
        new_node = Node(turn, run_length)
        new_node.next = new_node.prev = new_node
        self.start = new_node
        self.start_edge = edge
        self.start_vertex = 0
    
    def insertEnd(self, edge, turn, run_length):
    # If the list is empty, create a single node circular and doubly linked list
        if (self.start == None):
            self.start_list(edge, turn, run_length)
        else:	 
            last = (self.start).prev # If list is not empty find last node
            new_node = Node(turn, run_length)
            new_node.next = self.start
            (self.start).prev = new_node
            new_node.prev = last
            last.next = new_node
    
    def updateEnd(self):
        last = (self.start).prev
        last.run_length += 1

    def insertAfter(self, node, turn, run_length):
        if node == None:
            return
        new_node = Node(turn, run_length)
        new_node.next = node.next
        new_node.prev = node
        node.next.prev = new_node
        node.next = new_node

    def deleteNode(self, node):
        if (self.start == None or node == None):
            return
        # If node to be deleted is start node
        if (self.start == node):
            self.start = node.next 

            for i in range(node.run_length):
                if i % 2 == 1:
                    edge = (edge + node.turn) % len(self.nbr_a) # Note len(self.nbr_a) = len(nbr_z) = len(M)
                else:
                    edge = self.nbr_a[(self.index_a[edge] + node.turn) % len(self.nbr_a)]
            self.start_edge = edge
            self.start_vertex = (self.start_vertex + (node.run_length % 2)) % 2 

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
    
    def change_turn_all(self, node, new_turn):
        node.turn = new_turn
        # Merge Operations
        if node.next.turn == new_turn:
            node.run_length += node.next.run_length
            self.deleteNode(node.next)
        if node.prev.turn == new_turn:
            node.prev.run_length += node.run_length
            self.deleteNode(node)
    
    def change_turn_one_start(self, node, new_turn):
        if node.run_length == 1:
            node.turn = new_turn
            # Merge Operations
            if node.next.turn == new_turn:
                node.run_length += node.next.run_length
                self.deleteNode(node.next)
            if node.prev.turn == new_turn:
                node.prev.run_length += node.run_length
                self.deleteNode(node)
        else:
            new_node = Node(new_turn, 1)

            # insert new_node between temp and next.
            new_node.next = node.next
            new_node.prev = node
            node.next.prev = new_node
            node.next = new_node

            node.run_length -= 1
    
    def change_turn_one_end(self, node, new_turn):
        if node.run_length == 1:
            node.turn = new_turn
            # Merge Operations
            if node.next.turn == new_turn:
                node.run_length += node.next.run_length
                self.deleteNode(node.next)
            if node.prev.turn == new_turn:
                node.prev.run_length += node.run_length
                self.deleteNode(node)
        else:
            new_node = Node(new_turn, 1)

            # insert new_node between temp and next.
            new_node.next = node
            new_node.prev = node.prev
            node.prev.next = new_node
            node.prev = new_node

            node.run_length -= 1         
  
    # O(l) time complexity.
    # Remember when we delete the start node from a circular doubly linked list, we update the start pointer as the next pointer.
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

        elif self.number_of_runs() == 2:
            if self.start.turn == 0 and self.start.next.turn == 0:
                reductions.near_cyclic_spur(self, self.start)

            elif self.start.turn == 1 and self.start.next.turn == 2:
                reductions.cyclic_lt_bracket(self, self.start, n)
            elif self.start.turn == 2 and self.start.next.turn == 1:
                reductions.cyclic_lt_bracket(self, self.start.next, n)

            elif self.start.turn == -1 and self.start.next.turn == -2:
                reductions.cyclic_rt_bracket(self, self.start, n)
            elif self.start.turn == -2 and self.start.next.turn == -1:
                reductions.cyclic_rt_bracket(self, self.start.next, n)

        elif self.number_of_runs() == 4:
            if self.start.next.turn == 1 and self.start.next.next.turn == 2 and self.start.next.next.next.turn == 1:
                reductions.near_cyclic_lt_bracket(self, self.start, n)
            elif self.start.turn== 1 and self.start.next.turn == 2 and self.start.next.next.turn == 1:
                reductions.near_cyclic_lt_bracket(self, self.start.prev, n)
            elif self.start.turn == 2 and self.start.next.turn == 1 and self.start.prev.turn == 1:
                reductions.near_cyclic_lt_bracket(self, self.start.prev.prev, n)
            elif self.start.turn == 1 and self.start.prev.turn == 2 and self.start.prev.prev.turn == 1:
                reductions.near_cyclic_lt_bracket(self, self.start.next, n)

            elif self.start.next.turn == -1 and self.start.next.next.turn == -2 and self.start.next.next.next.turn == -1:
                reductions.near_cyclic_rt_bracket(self, self.start, n)
            elif self.start.turn == -1 and self.start.next.turn == -2 and self.start.next.next.turn == -1:
                reductions.near_cyclic_rt_bracket(self, self.start.prev, n)
            elif self.start.turn == -2 and self.start.next.turn == -1 and self.start.prev.turn == -1:
                reductions.near_cyclic_rt_bracket(self, self.start.prev.prev, n)
            elif self.start.turn == -1 and self.start.prev.turn == -2 and self.start.prev.prev.turn == -1:
                reductions.near_cyclic_rt_bracket(self, self.start.next, n)

        elif self.number_of_runs() == 5:
            if self.start.next.turn == 1 and self.start.next.next.turn == 2 and self.start.next.next.next.turn == 1:
                reductions.std_lt_bracket(self, self.start, n)
            elif self.start.turn == 1 and self.start.next.turn == 2 and self.start.next.next.turn == 1:
                reductions.std_lt_bracket(self, self.start.prev, n)
            elif self.start.turn == 2 and self.start.next.turn == 1 and self.start.prev.turn == 1:
                reductions.std_lt_bracket(self, self.start.prev.prev, n)
            elif self.start.turn == 1 and self.start.prev.turn == 2 and self.start.prev.prev.turn == 1:
                reductions.std_lt_bracket(self, self.start.prev.prev.prev, n)
            elif self.start.prev.turn == 1 and self.start.prev.prev.turn == 2 and self.start.prev.prev.prev.turn == 1:
                reductions.std_lt_bracket(self, self.start.next, n)

            elif self.start.next.turn == -1 and self.start.next.next.turn == -2 and self.start.next.next.next.turn == -1:
                reductions.std_rt_bracket(self, self.start, n)
            elif self.start.turn == -1 and self.start.next.turn == -2 and self.start.next.next.turn == -1:
                reductions.std_rt_bracket(self, self.start.prev, n)
            elif self.start.turn == -2 and self.start.next.turn == -1 and self.start.prev.turn == -1:
                reductions.std_rt_bracket(self, self.start.prev.prev, n)
            elif self.start.turn == -1 and self.start.prev.turn == -2 and self.start.prev.prev.turn == -1:
                reductions.std_rt_bracket(self, self.start.prev.prev.prev, n)
            elif self.start.prev.turn == -1 and self.start.prev.prev.turn == -2 and self.start.prev.prev.prev.turn == -1:
                reductions.std_rt_bracket(self, self.start.next, n)

    # O(l) time complexity.
    def canonical(self, M):
        n = len(M.matrix)
        # Input is a geodesic freely homotopic to c.
        # The function returns a canonical geodesic freely homotopic to c.
        if self.check_empty():
            return 0
        elif self.number_of_runs() > 4:
            temp = self.start
            while (self.number_of_runs() > 4 and (temp != self.start.prev or (temp == self.start.prev and temp.mark_2 == False))):
                if temp.next.turn == -2 and temp.next.next.turn == -1 and temp.next.next.next.turn == -2:
                    reductions.rt_shift_1(self, temp, n)
                elif temp.turn == -2 and temp.next.turn == -1 and temp.next.next.turn == -2:
                    reductions.rt_shift_1(self, temp.prev, n)
                elif temp.turn == -1 and temp.next.turn == -2 and temp.prev.turn == -2:
                    reductions.rt_shift_1(self, temp.prev.prev, n)
                elif temp.turn == -2 and temp.prev.turn == -1 and temp.prev.prev.turn == -2:
                    reductions.rt_shift_1(self, temp.prev.prev.prev, n)
                elif temp.prev.turn == -2 and temp.prev.prev.turn == -1 and temp.prev.prev.prev.turn == -2:
                    reductions.rt_shift_1(self, temp.prev.prev.prev.prev, n)
                
                elif temp.next.turn == -1 and temp.next.next.turn == -2:
                    reductions.rt_shift_2(self, temp, n)
                elif temp.turn == -1 and temp.next.turn == -2:
                    reductions.rt_shift_2(self, temp.prev, n)
                elif temp.turn == -2 and temp.prev.turn == -1:
                    reductions.rt_shift_2(self, temp.prev.prev, n)
                elif temp.prev.turn == -1 and temp.prev.prev.turn == -2:
                    reductions.rt_shift_2(self, temp.prev.prev.prev, n)

                elif temp.next.turn == -2 and temp.next.next.turn == -1:
                    reductions.rt_shift_3(self, temp, n)
                elif temp.turn == -2 and temp.next.turn == -1:
                    reductions.rt_shift_3(self, temp.prev, n)
                elif temp.turn == -1 and temp.prev.turn == -2:
                    reductions.rt_shift_3(self, temp.prev.prev, n)
                elif temp.prev.turn == -2 and temp.prev.prev.turn == -1:
                    reductions.rt_shift_3(self, temp.prev.prev.prev, n)
                
                else:
                    temp = temp.next
                    temp.mark_2 = True

        elif self.number_of_runs() == 1:
            if self.start.turn == -2:
                self.start.turn = 2

        elif self.number_of_runs() == 3:
            if self.start.turn != -3 and self.start.next.turn == -1 and self.start.next.next.turn == -2:
                reductions.rt_shift_5(self, self.start, n)
            elif self.start.turn == -1 and self.start.next.turn == -2 and self.start.next.next.turn != -3:
                reductions.rt_shift_5(self, self.start.prev, n)
            elif self.start.turn == -2 and self.start.next.turn != -3 and self.start.prev.turn == -1:
                reductions.rt_shift_5(self, self.start.prev.prev, n)
            
            elif self.start.turn != -3 and self.start.next.turn == -2 and self.start.next.next.turn == -1:
                reductions.rt_shift_6(self, self.start, n)
            elif self.start.turn == -2 and self.start.next.turn == -1 and self.start.next.next.turn != -3:
                reductions.rt_shift_6(self, self.start.prev, n)
            elif self.start.turn == -1 and self.start.next.turn != -3 and self.start.prev.turn == -2:
                reductions.rt_shift_6(self, self.start.prev.prev, n)
        
        elif self.number_of_runs() == 4:
            if self.start.turn != -3 and self.start.next.turn == -2 and self.start.next.next.turn == -1 and self.start.next.next.next.turn == -2:
                reductions.rt_shift_4(self, self.start, n)
            elif self.start.turn == -2 and self.start.next.turn == -1 and self.start.next.next.turn == -2 and self.start.next.next.next.turn != -3:
                reductions.rt_shift_4(self, self.start.prev, n)
            elif self.start.turn == -1 and self.start.next.turn == -2 and self.start.next.next.turn != -3 and self.start.prev.turn == -2:
                reductions.rt_shift_4(self, self.start.prev.prev, n)
            elif self.start.turn == -2 and self.start.next.turn != -3 and self.start.prev.turn == -1 and self.start.prev.prev.turn == -2:
                reductions.rt_shift_4(self, self.start.next, n)

            elif self.start.turn == -3 and self.start.next.turn == -2 and self.start.next.next.turn == -1 and self.start.next.next.next.turn == -2:
                reductions.rt_shift_7(self, self.start, n)
            elif self.start.turn == -2 and self.start.next.turn == -1 and self.start.next.next.turn == -2 and self.start.next.next.next.turn == -3:
                reductions.rt_shift_7(self, self.start.prev, n)
            elif self.start.turn == -1 and self.start.next.turn == -2 and self.start.next.next.turn == -3 and self.start.prev.turn == -2:
                reductions.rt_shift_7(self, self.start.prev.prev, n)
            elif self.start.turn == -2 and self.start.next.turn == -3 and self.start.prev.turn == -1 and self.start.prev.prev.turn == -2:
                reductions.rt_shift_7(self, self.start.next, n)

    def display(self):
        temp = self.start

        print("Traversal in forward direction:")
        while (temp.next != self.start):
            print('(' + str(temp.turn) + ',' + str(temp.run_length) + ')', end=" ")
            temp = temp.next
        print('(' + str(temp.turn) + ',' + str(temp.run_length) + ')', end=" ")

        print("\nTraversal in reverse direction:")
        last = self.start.prev
        temp = last
        while (temp.prev != last):
            print('(' + str(temp.turn) + ',' + str(temp.run_length) + ')', end=" ")
            temp = temp.prev
        print('(' + str(temp.turn) + ',' + str(temp.run_length) + ')', end=" ")
        print("\n")
