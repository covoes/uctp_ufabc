from objects import *
from uctp import *
from ioData import *
import os

prt = 1
      
#==============================================================================================================            
# Run with <python -m cProfile -s cumtime main.py>
#RESOLVER: Problema das cargas (v1) no calculo de fitness dos feasibles

# main
class main: 
    # to access UCTP Main methods and creating Solutions (List of Candidates)
    uctp = UCTP()
    # Main candidates of a generation
    solutionsI = Solutions()
    solutionsF = Solutions()
    # Candidates without classification 
    solutionsNoPop = Solutions()
    # Candidates generated in a iteration (will be selected to be, or not, in the main List of Candidates)
    infPool = Solutions()
    feaPool = Solutions()
    
    # Base Lists of Professors and Subjects - never modified through the run
    prof = []
    subj = []
    
    # Max Number of iterations to get a solution
    iterations = 20000
    # Number of candidates in a generation (same for each Feas/Inf.)
    numCand = 20
    # Percentage of candidates from Feasible Pop. that will be selected, to become Parents and make Crossovers, through a Roulette Wheel with Reposition
    # Must be between '0' and '100'
    pctRouletteCross = 50
    # Percentage of mutation that maybe each child generated through 'offspringF' process will suffer
    # Must be between '0' and '100' 
    pctMut = 15
    
    # Weights (!!!must be float!!!)
    w_alpha = 2.0
    w_beta = 3.0
    w_gamma = 1.0
    w_delta = 1.0
    w_omega = 1.0
    w_sigma = 1.0
    w_pi = 1.0
    w_rho = 1.0
    weights = [w_alpha, w_beta, w_gamma, w_delta, w_omega, w_sigma, w_pi, w_rho]
    
    # Start of the works
    # Getting data
    getData(subj, prof)
    
    # Creating the first 'numCand' candidates (First Generation)
    uctp.start(solutionsNoPop, subj, prof, numCand)
    # Classification and calculating this first candidates
    uctp.twoPop(solutionsNoPop, solutionsI, solutionsF, prof, subj, weights)
    uctp.calcFit(solutionsI, solutionsF, prof, subj, weights)
    # Print and export generated data
    if(prt==1): print('Iteration: 0')
    outDataMMA(solutionsI, solutionsF, 0)
    # printAllFit(solutionsI, solutionsF)
    
    # Main work - iterations of GA-Algorithm to find a solution
    if(prt==1): 
        print(" ")
        print("Starting hard work...")
        print(" ")
    
    firstFeasSol = -1
    t = 1;
    while(uctp.stop(t, iterations, solutionsI, solutionsF)):
        # Some good information to follow the run
        if(prt==1): 
            print('Iteration:', t, 'of', iterations, '/ Working with (Prof/Subj):', len(prof), '/', len(subj))
            if(firstFeasSol!=-1): print('First Feasible Sol. at (iteration): ', firstFeasSol)
        # Choosing Parents to generate children (solutionsNoPop) 
        uctp.offspringI(solutionsNoPop, solutionsI, prof, subj) 
        uctp.offspringF(solutionsNoPop, solutionsF, prof, subj, pctMut, pctRouletteCross, numCand)
        # Classification and calculating this new candidates  
        uctp.twoPop(solutionsNoPop, infPool, feaPool, prof, subj, weights)
        print(len(solutionsNoPop.getList()), len(infPool.getList()))
        uctp.calcFit(infPool, feaPool, prof, subj, weights)
        print(len(solutionsNoPop.getList()), len(infPool.getList()))
        # Selecting between parents (old generation) and children (new candidates) to create the new generation
        uctp.selectionI(infPool, solutionsI, numCand)
        uctp.selectionF(feaPool, solutionsF, numCand)
        # Print and export generated data
        outDataMMA(solutionsI, solutionsF, t)
        # Register of the Iteration when appears the first Feas Sol
        if(firstFeasSol==-1 and len(solutionsF.getList())!=0):
                firstFeasSol=t
                beep = lambda x: os.system("echo -n '\a';sleep 0.2;" * x)
                beep(3)
        # Next Iteration
        t = t+1
        if(prt==1): print(" ")
    # End While (Iterations) - Stop condition verified
     
    # Export last generation of candidates (with a Solution)  
    outData(solutionsI, solutionsF, t)        
    if(prt==1): print("End of works")
          
#==============================================================================================================
