'''
Name : sorting.py
Author  : AJ Hunt
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
                bid = Bid(entry.get('auctionid',None),entry.get('auctiontitle',""),entry.get('fund',""),str2float(entry.get('winningbid','0.0'),['$',',']))
                bids.append(bid)
    except Exception as ex:
        print(f"exception occurred, {ex}")

    return bids

# FIXME (1a): Implement the selection sort logic over bid.title
def selectionSort(bids: List) -> None:
    '''
    Perform a selection sort on bid title
    Average performance: O(n^2))
    Worst case performance O(n^2))
    @param bid address of the vector<Bid> instance to be sorted
    '''
    # for each position in the array
    for i in range(len(bids)):

        # find the lowest value in the list
        j = i + 1

        while j < len(bids):
            # swap the lower elements into the current i index whenever found
            if bids[j].title < bids[i].title:
                temp = bids[i]
                bids[i] = bids[j]
                bids[j] = temp
            j += 1
    return bids

#FIXME (2a): Implement the quick sort logic over bid.title
def quickSort(bids: List) -> None:
    '''
    Perform a quick sort on bid title
    Average performance: O(n log(n))
    Worst case performance O(n^2))
    @param bids ref to the bids List to be sorted
    '''
    def partition(bids: List, begin: int, end: int) -> int:
        '''
        Partition the vector of bids into two parts, low and high
        @param bids ref to the bids List to be partitioned
        @param begin Beginning index to partition
        @param end Ending index to partition
        '''
        #set low and high equal to begin and end
        #NOTE: we use (begin + 1) because the pivot element will be in index 'begin' after swapping
        low, hi = begin + 1, end

        #pick the middle element as pivot point
        pivot = begin + (end - begin) // 2
        pivot_val = bids[pivot]


        # move the pivot element out of the way of the sorting by swapping it with the first element
        bids[pivot], bids[begin] = bids[begin], bids[pivot]

        done = False

        # while not done, i.e., our low index is still left of our high index
        while not done:

            #keep incrementing low index while bids[low] < bids[pivot]
            # i.e., if the bid at our (low) index is less than the pivot bid, move (low) index right one
            while low <= hi and bids[low].title <= pivot_val.title:
                low += 1

            #keep decrementing high index while bids[pivot] < bids[high]
            # i.e., if the bid at our (high) index is greater than the pivot bid, move (high) index left one
            while low <= hi and bids[hi].title >= pivot_val.title:
                hi -= 1

            #If there are zero or one elements remaining, all bids are partitioned. Return high
            if hi < low:
                done = True

            #else swap the low and high bids (built in vector method)
            else:
                bids[low], bids[hi] = bids[hi], bids[low]

        # put the partition element back into the list by swapping with the nearest less-than element at index 'hi'
        bids[begin], bids[hi] = bids[hi], bids[begin]

        # return the index 'hi', the index of the now-correctly-sorted element
        return hi

    def qSort(bids: List, begin: int, end: int) -> None:
        '''
        Helper function, perform a quickSort recursively
        @param bids ref to the bids List to be partitioned
        @param begin Beginning index to partition
        @param end Ending index to partition
        '''
        # Base case: if begin is greater than or equal to end then return
        if begin >= end:
            return

        #Partition bids into low and high such that midpoint is location of last element in low
        mid = partition(bids, begin, end)

        #recursively sort low partition (begin to mid)
        qSort(bids, begin, mid - 1)

        #recursively sort high partition (mid+1 to end)
        qSort(bids, mid + 1, end)

    # Call the helper function
    qSort(bids, 0, len(bids) - 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process cmd line arguments')
    parser.add_argument('-p','--path', default='eBid_Monthly_Sales_Dec.csv',
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
            # break
        elif selection == '9':
            print("Bye!")
            break
        else:
            print("Unknown Option Selected!")