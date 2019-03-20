import numpy

""" Our approach to solving this problem is as follows:
    1. If we can solve this problem for a one dimensional platform, we can extend it to a second dimension or
        even to an 'n' dimensional platform 
    2. Therefore, we write the method "find_amount_one_d(self,i)" which solves this problem for a one dimensional platform. 
        Concretely, it returns the amount of water held by the element at a given position 'i' in a one dimensioal platform
    3. To extend our solution to two dimensions, we write the method "find_amount_two_d(self,i,j)" which determines the 
        amount of water held at the position (i,j) by finding the amount of water held by element (i,j) taking only its row into consideration
        and also by finding the amount by taking only its column into consideration and taking the minimum of the two
    4. So far, we have not fully considered the fact that the element with a value of '0' represents a drain in our platform.
        To add this feature to our model, we write the method "flow_up(self,i,j)". To understand this method, we should imagine water flowing OUT of the drain
        instead of the water flowing into it! We know that water can only flow into the drain by means of a slope or a gradient. Therefore,
        we trace all of the elements where the gradient is STRICTLY INCREASING, with the drain (element '0') as our starting point! 
    5. The "drain(self)" method drains all of the water from our platfrom by finding all of the places with a drainhole and calling the method "flow_up(self,i,j):"           
    6. The "find_edges(self)" method finds the edges of our two dimensional platform.
    7. The method "WaterStoredInPlatform(self)" brings all of the pieces together and returns the total amount of water stored in our platform! 

 """

class Platform(object):

    def __init__(self, two_d_array): #Initializing our Platfrom and setting up useful attributes
        
        self.two_d_array = two_d_array 

        if self.two_d_array.size == 1:  #(m,n) is the shape of our platform where, m=No. of rows and n=No. of columns
            (self.m, self.n) = (1,1)
            
        elif self.two_d_array.size == 2:
            (self.m,self.n) = (1,2)
             
        else:
            (self.m,self.n) = two_d_array.shape

        self.edges = self.find_edges()
        self.amounts = numpy.ones((self.m,self.n)) #Initializing the "amounts" matrix

    def find_edges(self):
        """ Returns the set of all edges of our Platform """
        edges = []
        m = self.m
        n = self.n

        for a in range(n-1):
            edges.append((0,a))
            edges.append((m-1,a))
        for b in range(m-1):
            edges.append((b,0))
            edges.append((b,n-1))
        edges = set(edges)        
        return edges

        
    def flow_up(self,i,j):
        """ 
        Simulates water 'flowing up' the drain, thereby setting the amount of water held by the elements which allow this
        to be zero. We assume that the water can only flow up a STRICTLY INCREASING gradient.
        Parameters: (i,j = Position of the drain in our platform) 
        """
    
        two_d_array = self.two_d_array
        amounts = self.amounts
        (m,n) = (self.m,self.n)

        current_left_peak = 0  #We update the peaks in all fours directions as we traverse up the gradient in each direction
        current_right_peak = 0 
        current_upper_peak = 0
        current_lower_peak = 0

        for left_column in reversed(range(0,j)):
            if two_d_array[i, left_column] < current_left_peak:
                break
            if two_d_array[i, left_column] >= current_left_peak:
                current_left_peak = two_d_array[i,left_column]
                amounts[i,left_column] = 0  

                for u_row in reversed(range(0,i)): #Simulating the flow of water from the upper and lower rows on the left side of the drain to the row with the drain in it
                    u_largest = two_d_array[i, left_column]
                    if two_d_array[u_row, left_column] >= u_largest:
                        u_largest = two_d_array[u_row, left_column]
                        amounts[u_row, left_column] = 0
                for l_row in range(i+1,m):
                    l_largest = two_d_array[i, left_column]    
                    if two_d_array[l_row, left_column] >= l_largest:
                        l_largest = two_d_array[l_row, left_column]
                        amounts[l_row, left_column] = 0             

        for right_column in range(j+1,n):
            if two_d_array[i, right_column] < current_right_peak:
                break
            if two_d_array[i, right_column] >= current_right_peak:
                current_right_peak = two_d_array[i, right_column]
                amounts[i, right_column] = 0

                for u_row in reversed(range(0,i)): #Simulating the flow of water from the upper and lower rows on the right side of the drain to the row with the drain in it
                    u_largest = two_d_array[i, right_column]
                    if two_d_array[u_row, right_column] >= u_largest:
                        u_largest = two_d_array[u_row, right_column]
                        amounts[u_row, right_column] = 0
                for l_row in range(i+1,m):
                    l_largest = two_d_array[i, right_column]    
                    if two_d_array[l_row, right_column] >= l_largest:
                        l_largest = two_d_array[l_row, right_column]
                        amounts[l_row, right_column] = 0
                     
                
        for upper_row in reversed(range(0,i)):
            if two_d_array[upper_row,j ] < current_upper_peak:
                break
            if two_d_array[upper_row, j] >= current_upper_peak:
                current_upper_peak = two_d_array[upper_row, j]
                amounts[upper_row, j] = 0
                
        for lower_row in range(i+1,m):
            if two_d_array[lower_row,j ] < current_lower_peak:
                break
            if two_d_array[lower_row, j] >= current_lower_peak:
                current_lower_peak = two_d_array[lower_row, j]
                amounts[lower_row, j] = 0
  
        return True

    def drain(self):
        """ 
        "Drains" the water in our platfrom by finding the drains and calling "flow_up(i,j)" on that position
        """
        (m,n) = (self.m,self.n)
        two_d_array = self.two_d_array

        for i in range(m):
            for j in range(n):
                if two_d_array[i,j] ==0:
                    self.flow_up(i,j)     

    def find_amount_one_d(self,one_d_array, i):
        """ 
        Returns the amount of water stored by element 'i' in a one dimesional array by looking at the left half and the right half of the array to find 
        the "significant wall": that is the minimum of the walls with the maximum height on either side of element 'i' and subtracting the height of element 'i' from the height of the "significant wall" 
        Parameters: (one_d_array = one dimentional numpy array object, i = position of the element whose amount is to be calculated)  
        """
     
        if i == 0 or i == one_d_array.size-1 or one_d_array[i]==0:
            amount = 0
        else:
            start = 0
            mid = i
            end = one_d_array.size
            
            if start == mid:
                max_left = one_d_array[start]
            if mid+1 == end:
                max_right = one_d_array[end]

            else:
                if 0 not in one_d_array[0:mid]:    #Find the maximum on the left side of element 'i'
                    max_left = numpy.max(one_d_array[start:mid])
                else:
                    max_left = 0
                    for wall_index in reversed(range(0,mid)):
                        if one_d_array[wall_index] == 0:
                            break
                        else:
                            if one_d_array[wall_index] > max_left:
                                max_left = one_d_array[wall_index]


            
                if 0 not in one_d_array[mid+1:end]: #Find the maximum on the right side of element 'i'
                    max_right = numpy.max(one_d_array[mid+1:end])
                else:
                    max_right = 0
                    for wall_index in range(mid+1,end):
                        if one_d_array[wall_index] == 0:
                            break
                        else:
                            if one_d_array[wall_index] > max_right:
                                max_right = one_d_array[wall_index]    
            
            sig_wall = min(max_left, max_right) #Find the "significant" wall
            amount = sig_wall - one_d_array[i]  
            
            if amount <= 0:
                amount = 0
        return amount    

    def find_amount_two_d(self,i,j):
        """ 
        Returns the amount of water held by element(i,j) in a two dimensional platform  
        """
        (m,n) = (self.m,self.n)
        edges = self.edges
        two_d_array = self.two_d_array
    

        if (i,j) in edges:
            amount_row = 0
            amount_col = 0 
        else:
            amount_row = self.find_amount_one_d(two_d_array[i, 0:n],j) #Amount of water held by element (i,j) taking only its row into consideration
            amount_col = self.find_amount_one_d(two_d_array[0:m, j],i) #Amount of water held by element (i,j) taking only its column into consideration   

        if amount_row <= 0 or amount_col <= 0:
            amount = 0
        else:
            amount = min(amount_row,amount_col)  #Amount of water held by element (i,j)
        return amount

    def get_amounts(self):
        """ 
        Returns "amounts", which is an m x n dimensional matrix, each of whose elements corresponds to the amount of water 
        held by the corresponding element in our two dimensional platform
        That is, amounts[i,j] = amount of water held by the element (i,j) in the platform 
        """
        
        (m,n) = (self.m, self.n)
        amounts = self.amounts

        if self.two_d_array.size <= 4: #A platform of size <= 4 cannot hold water
            amounts = 0
            return amounts

        for i in range(m):
            for j  in range(n):
                amounts[i,j] = self.find_amount_two_d(i,j)
        self.drain()
        self.amounts = amounts        
        return amounts

    def WaterStoredInPlatform(self):
        """ 
        Computes and returns the total amount of water held by our platform by summing the amount of water held by
        each of the individual elements
        """
        amounts = self.get_amounts()
        return numpy.sum(amounts)    



if __name__ == "__main__":   #Testing our implementation


    test_platform0 = numpy.array([1])
    test_platform1 = numpy.array([[1,2],[2,1]])
    test_platform2 = numpy.array([[1,2],[2,3],[4,5]])
    test_platform3 = numpy.array([[2,2,2],[2,2,2],[2,2,2]])
    test_platform4 = numpy.array([[2,2,2],[2,1,2],[2,2,2]])
    test_platform5 = numpy.array([[3,3,3,3,3,3],[3,1,2,3,1,3],[3,1,2,3,1,3],[3,3,3,1,3,3]])
    test_platform6 = numpy.array([[3,3,3,3,5,3],[3,0,2,3,1,3],[3,1,2,3,1,3],[3,3,3,1,3,3]])
    test_platform7 = numpy.array([[4,4,4,4,4,5],[5,4,0,4,3,5],[4,4,4,4,4,5]])
    test_platform8 = numpy.array([[5,5,5,5,5],[9,1,1,1,5],[5,1,5,1,5],[5,1,1,1,5],[5,5,5,5,5]])
    test_platform9 = numpy.array([[5,5,5,5,5],[9,1,1,1,5],[5,1,0,1,5],[5,1,1,1,5],[5,5,5,5,5]])
    test_platform10 = numpy.array([[1,2,3,4],[2,4,2,5],[3,1,1,6],[4,5,6,7]])
    test_platform11 = numpy.array([[9,9,9,9,9,9,9],[9,1,2,6,3,4,9],[9,1,2,6,3,4,9],[9,1,2,6,3,4,9],[9,1,2,6,3,4,9],[9,9,9,9,9,9,9]])
    
    test_cases = [test_platform0,test_platform1,test_platform2,test_platform3,test_platform4,test_platform5,test_platform6,test_platform7,test_platform8,test_platform9,test_platform10, test_platform11]
    
    
    
    for test_case in test_cases:
    
        platform = Platform(test_case)

        print("The test platform is:\n", platform.two_d_array)
        print("The amount of water held at every position is:\n", platform.get_amounts())
        print("The total amount of water stored in the platform is: ", platform.WaterStoredInPlatform(), "cubic units")
        print("=====================================================================================================\n")


""" 
Alternative approaches: 
One can also think of solving this probelem by using the Sobel operator on our two dimensional array. The sobel operator works by convolving two 3x3 kernels with our matrix
to approximate the derivative, thereby detecting an edge by measuring the steepness at any given element. This algorithm is used in Computer Vision to detect the edges in a grayscale image. 
The same approach can be used to solve this problem. However, certain complications may arise when trying to gauge the exact depth or the gradient at each element.

A more ambitious approach would be to train a neural network to detect a closed loop and calculate the depth of each element automatically. But this will require
a large labeled data set and considerable amount of time to accomplish the task with good test set accuracy.

-Syed M. Peeran
"""
