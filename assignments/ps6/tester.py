from ps6_solution import *



if __name__ == '__main__':

  print("here before")
  simulationWithoutDrug(100, 1000, 0.1, 0.05, 5)  
  simulationWithDrug(100, 1000,0.1, 0.05,{'guttagonol':False}, 0.005,20)
  print("here after")