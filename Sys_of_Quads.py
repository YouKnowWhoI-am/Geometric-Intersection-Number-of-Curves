import sys

class Manifold:
    def __init__(self, Matrix):
        self.matrix = Matrix

    # O(n) time complexity.
    def check_valid(self):
        # Input must be of even length.
        if len(self.matrix) %2 == 1:
            sys.exit("Invalid Input: Input must be of even length.")
        elif len(self.matrix) % 2 == 0:
        # Check if the input has adjacent duplicates.
            if self.matrix[0] == self.matrix[-1]: sys.exit("Invalid Input: Adjacent sides can't be identical.")
            for i in range(len(self.matrix)-2):
                if self.matrix[i] == self.matrix[i+1]: sys.exit("Invalid Input: Adjacent sides can't be identical.")
        # Check if the input has each letter twice, ignoring case.
        counter = [0] * len(self.matrix)
        for x in self.matrix:
            if x[1] > int(len(self.matrix)/2):
                sys.exit("Re-enter Input: Please follow convention of serially naming the edges without skipping any intergers in between.")
            counter[x[1]-1] = counter[x[1]-1] + 1
        for i in range(len(counter)):
            if counter[self.matrix[i][1]-1] != 2 and counter[self.matrix[i][1]-1] != 0:
                sys.exit("Invalid Input: Number of edges not equal to 4*genus")       

    # O(n) time complexity.
    def Sys_of_Quads(self):
        self.faces = [[0 for i in range(4)] for j in range(int((len(self.matrix)/2)))] # 2D list of self.faces
        count = [0] * int(len(self.matrix)/2)
        for i in range(len(self.matrix)):
            if count[self.matrix[i][1]-1] == 0: #if i'th edge has not occured yet
                if self.matrix[i][0] == 1: #Edge oriented Clockwise
                    self.faces[self.matrix[i][1]-1][0] = i
                    self.faces[self.matrix[i][1]-1][1] = (i + 1) % len(self.matrix)
                    count[self.matrix[i][1]-1] = 1 #Mark i'th edge as occured once clockwise
                elif self.matrix[i][0] == -1: #Edge oriented Anti-Clockwise
                    self.faces[self.matrix[i][1]-1][0] = i
                    self.faces[self.matrix[i][1]-1][1] = (i + 1) % len(self.matrix)
                    count[self.matrix[i][1]-1] = 2 #Mark i'th edge as occured once anti-clockwise
            elif count[self.matrix[i][1]-1] != 0: #This edge has already occured once
                if self.matrix[i][0] == 1: #Edge oriented Clockwise
                    if count[self.matrix[i][1]-1] == 1: #Previously it also occured clockwise
                        self.faces[self.matrix[i][1]-1][2] = (i + 1) % len(self.matrix)
                        self.faces[self.matrix[i][1]-1][3] = i 
                    elif count[self.matrix[i][1]-1] == 2: #Previously it occured anti-clockwise
                        self.faces[self.matrix[i][1]-1][2] = i
                        self.faces[self.matrix[i][1]-1][3] = (i + 1) % len(self.matrix)
                elif self.matrix[i][0] == -1: #Edge oriented Anti-Clockwise
                    if count[self.matrix[i][1]-1] == 1: #Previously it occured clockwise
                        self.faces[self.matrix[i][1]-1][2] = i
                        self.faces[self.matrix[i][1]-1][3] = (i + 1) % len(self.matrix)
                    elif count[self.matrix[i][1]-1] == 2: #Previously it also occured anti-clockwise
                        self.faces[self.matrix[i][1]-1][2] = (i + 1) % len(self.matrix)
                        self.faces[self.matrix[i][1]-1][3] = i

        self.index_a = [0] * len(self.matrix) # To ensure the function turn, defined later, runs in O(1) time, we need to store the index of each edge in the cycle.
        self.nbr_a = [0] * len(self.matrix) #nbr_z is the list {0, 1, ..., len(M)-1} in the order of the edges in the cycle.
        self.spoke = [set() for j in range(len(self.matrix))] # spoke[i] stores the unique set of 4 neighbours of the edge i. We are not worried about the order.

        for i in range(len(self.matrix)):
            if i != 0:
                self.nbr_a[i] = self.faces[f - 1][3 - l]
                if self.matrix[self.nbr_a[i]][1] != f:
                    f = self.matrix[self.nbr_a[i]][1]
                else:
                    f = self.matrix[self.nbr_a[i] - 1][1]
                for j in range(4):
                    if self.faces[f - 1][j] == self.nbr_a[i]:
                        l = j 
            elif i == 0: # Currently f and l are configured according to self.nbr_a[i-1]
                self.nbr_a[i] = self.faces[i][1]
                f = i + 1 # f is the index of the face that contains the edge i
                l = 1 # l is the index of the edge in the face that contains the edge i
        for i in range(len(self.matrix)):
            self.index_a[i] = self.nbr_a.index(i)

        for i in range(len(self.matrix)):
            for j in range(4):
                if j == 0:
                    self.spoke[self.faces[i][j]].add(self.faces[i][1])
                    self.spoke[self.faces[i][j]].add(self.faces[i][3])
                elif j == 1 or j == 2:
                    self.spoke[self.faces[i][j]].add(self.faces[i][j - 1])
                    self.spoke[self.faces[i][j]].add(self.faces[i][j + 1])
                elif j == 3:
                    self.spoke[self.faces[i][j]].add(self.faces[i][2])
                    self.spoke[self.faces[i][j]].add(self.faces[i][0])

