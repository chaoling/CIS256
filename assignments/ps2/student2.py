'''
Name : sorting.py
Author  : Michael Moschetta
Version : 1.0
Description : Apply Sorting Algorithms to the csv data set
'''

# importing DictReader class from csv module
import csv
from typing import List
import argparse
import time

# class to hold bid information
class Bid(object):
    def __init__(self,id=None,title=None,fund=None,amt=0.0):
        self.bidId = id
        self.title = title
        self.fund = fund
        self.amount = amt

    def __str__(self):
        return f"ID: {self.bidId}, Title: {self.title}, Fund: {self.fund}, Amount: {self.amount}"

def str2float(origin: str, ch: List) ->str:
    #Convert string to float, stripping ch. e.g: '$6,000.00 ' -> 6000.00
    for c in ch:
        origin = origin.replace(c,'')

    return float(origin.strip())

def logtime(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        total_time = time.time() - start_time
        with open('timelog.txt','a') as outfile:
            #timestamp, func name, time spent
            record = f'at {time.time()}:\t{func.__name__}\t time spent: {total_time}(sec)\n'
            print(record)
            outfile.write(record)
        return result
    return wrapper


@logtime
def loadBids(csvPath: str) -> List:
    '''
    Load a CSV file containing bids into a container
    @param csvPath the path to the CSV file
    @return a container holding all the bids read
    '''
    # opening csv file
    print(f"now loading csv file {csvPath}...")
    bids = []
    try:
        with open(csvPath,'r') as file:
            #reader = DictReader(file)
            reader = csv.reader(file)
            header = next(reader)
            # clean up the header as keys
            keys = [key.replace(" ","").lower() for key in header]
            # print(keys)
            # printing each row of table
            for row in reader:
                entry = dict(zip(keys,row))
                bid = Bid(entry.get('auctionid',""),entry.get('auctiontitle',None),entry.get('fund',""),str2float(entry.get('winningbid','0.0'),['$',',']))
                bids.append(bid)
    except Exception as ex:
        print(f"excetion occurred, {ex}")

    return bids

# FIXME (1a): Impement the selection sort logic over bid.title
def selectionSort(bids: List) -> None:

  n = len(bids)

#Loops through each bid and finds the smallest in the unsorted
  for i in range(n):
    min_index = i
    for j in range(i + 1, n):
      if bids[j].title < bids[min_index].title:
        min_index = j
    if min_index != i:
      bids[i], bids[min_index] = bids[min_index], bids[i]
    '''
    Perform a selection sort on bid title
    Average performance: O(n^2))
    Worst case performance O(n^2))
    @param bid address of the vector<Bid> instance to be sorted
    '''

#FIXME (2a): Implement the quick sort logic over bid.title
def quickSort(bids: List) -> None:
    '''
    Perform a quick sort on bid title
    Average performance: O(n log(n))
    Worst case performance O(n^2))
    @param bids ref to the bids List to be sorted
    '''
    def partition(bids: List, begin: int, end: int) -> int:

      #Uses the middle element as a pivot
      pivot = bids[(begin + end) // 2].title
      low = begin
      high = end
      while True:
        #Increments the low index while it is less than pivot
        while bids[low].title < pivot:
          low += 1
        #Decrements the high index while it is greater than pivot
        while bids[high].title > pivot:
          high -= 1
        #If the elements cross each other it is completed
        if low >= high:
          return high

        #Swaps the elements at low and high
        bids[low], bids[high] = bids[high], bids[low]
        low += 1
        high -= 1
        '''
        Partition the vector of bids into two parts, low and high
        @param bids ref to the bids List to be partitioned
        @param begin Beginning index to partition
        @param end Ending index to partition
        '''
        #set low and high equal to begin and end

        #pick the middle element as pivot point

        # while not done
            #keep incrementing low index while bids[low] < bids[pivot]

            #keep decrementing high index while bids[pivot] < bids[high]

            #If there are zero or one elements remaining, all bids are partitioned. Return high

            #else swap the low and high bids (built in vector method)

            #move low and high closer ++low, --high

        #return high;

    def qSort(bids: List, begin: int, end: int) -> None:

      if begin < end:
        #Partitions the list and gets the pivot index
        pivot_index = partition(bids, begin, end)
        #Recusively sorts the low partition
        qSort(bids, begin, pivot_index)
        #Recusively sorts the high partition
        qSort(bids, pivot_index + 1, end)

    qSort(bids, 0, len(bids) - 1)
    '''
        Helper function, perform a quickSort recursively
        @param bids ref to the bids List to be partitioned
        @param begin Beginning index to partition
        @param end Ending index to partition
      '''

        #Base case: If there are 1 or zero bids to sort,
        #partition is already sorted otherwise if begin is greater than or equal to end then return

        #Partition bids into low and high such that midpoint is location of last element in low

        #recursively sort low partition (begin to mid)

        #recursively sort high partition (mid+1 to end)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process cmd line arguments')
    parser.add_argument('-p','--path', default='eBid_Monthly_Sales.csv',
                    help='path to the csv file')


    args = parser.parse_args(args=[])
    menu = {}
    menu['1']="Load Bids"
    menu['2']="Display All Bids"
    menu['3']="Selection Sort All Bids"
    menu['4']="Quick Sort All Bids"
    menu['9']="Exit"

    while True:
        options=menu.keys()
        for entry in options:
            print(entry, menu[entry]) #display the menu item

        selection=input("Enter choices: ")
        if selection =='1':
            bids = loadBids(args.path)
        elif selection == '2':
            print("display bids....")
            for bid in bids:
                print(bid)
        elif selection == '3':
            print("selection sort...")
            selectionSort(bids)
        elif selection == '4':
            print("quick sort...")
            quickSort(bids)
            break
        elif selection == '9':
            print("Bye!")
            break
        else:
            print("Unknown Option Selected!")