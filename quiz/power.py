 #Figure out the size, N
def yieldAllCombos(items):
    """
      Generates all combinations of N items into two bags, whereby each 
      item is in one or zero bags.

      Yields a tuple, (bag1, bag2), where each bag is represented as 
      a list of which item(s) are in each bag.
    """
    size_n = len(items)

    #A function to generate a base 3 value of length n
    def base3(val: int, n:int):
        base3result = ""
        new_val = val

        for i in range(n):
            integer_quotient, remainder = divmod(new_val, 3)
            base3result = str(remainder) + base3result
            new_val = integer_quotient
        print(f"{base3result=}")
        return base3result
    
    #For every value in range 3^N,
    for i in range(3**size_n):
        #Generate a base 3 number/string that is length N (pad with leading 0s to make length N)
        base3string = base3(i, size_n)
        
        #Within the loop, initialize bag 1 and bag 2 as empty lists
        bag1 = []
        bag2 = []
    

        #For character j in N, if it is 1, put the item j in bag 1
        #Elif if character j is 2, put the item j in bag 2
        #Else, the item is in no bag
        for j in range(size_n):
            if base3string[j] == '1':
                bag1.append(items[j])
            elif base3string[j] == '2':
                bag2.append(items[j])
            #else: #else not required; item is in neither bag, so do nothing
        tuple_result = (bag1, bag2)
        yield tuple_result

def yieldAllCombos2(items):
    n = len(items)
    for i in range(3**n):
        bag_1 = []
        bag_2 = []
          
        for j in range(n):
            if (i // 3**j) % 3 == 0:
                bag_1.append(items[j])
            elif (i // 3**j) % 3 == 1:
                bag_2.append(items[j])
        yield (bag_1, bag_2)

if __name__ == "__main__":
    items = ['apple', 'banana', 'orange']
    for combo in yieldAllCombos2(items):
        print(combo)