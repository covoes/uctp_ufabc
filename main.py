# PERGUNTAS:
# 1.Podem haver materias repetidas vindas do arquivo? Devo tratalas? Removelas?
# 2.Cuidar das conexoes como numeros (e procurar nas listas), ponteiro, copia dos objetos?
# 3.Cuidar para ter todos os professores logo na primeira populacao? Pode acontecer de um nao entrar por ser randomico?
# 4.Colocar tmb no calculo de Fitness se ha ou nao todos os professores (deve haver todos)

# filter subjects graduation and computing only;
# So....level = 'G' and code = {'MCTA', 'MCZA'} 'BCM'?, 'MCTB'?;
# Code where 2 first letters (period 'D' or 'N', class 'A' or 'B' etc);
# and maybe one number before the code itself of subjects;
# Example: DA1MCTA0001;
# Every professor must have name, period and charge -> error if not;
# Every subject must have level, code, name, quadri, period, campus and charge -> error if not;
# Transform every letter to Uppercase;

from copy import copy
from random import Random
from random import randrange
import csv
import os
import sys

# Keep the details of a professor
class Prof:
    def __init__(self, name, period, charge, quadriSabbath):
        self.name = name
        self.period = period
        self.charge = charge
        self.quadriSabbath = quadriSabbath
        #self.prefSubject = prefSubject
        #self.research = research
     
    def get(self):
        return self.name, self.period, self.charge, self.quadriSabbath

# Keep the details of a subject
class Subject:
    def __init__(self, level, code, name, quadri, period, campus, charge):
        self.level = level
        self.code = code
        self.name = name
        self.quadri = quadri
        self.period = period
        self.campus = campus
        self.charge = charge
    
    def get(self):
        return self.level, self.code, self.name, self.quadri, self.period, self.charge    

# Keep the details of a Candidate
class Candidate:
    def __init__(self):
        self.listRelations = []
        self.pop = None
        self.fitness = 0
    
    def get(self):
        return self.listRelations
    
    def setFeas(self):
        self.pop = 'f'

    def setInfeas(self):
        self.pop = 'i'
        
    def getIF(self):
        return self.pop
        
    def resetPop(self):
        self.pop = None
    
    def setFitness(self, fit): 
        self.fitness = fit   
    
    def getFitness(self): 
        return self.fitness
            
    def add(self, Subject, Prof):
        relation = [Subject, Prof]
        self.listRelations.append(relation)
        
    def remove(self, relation):
        self.listRelations.remove(relation)
    
    def update(self, old, new):
        index = self.listRelations.index(old)
        self.listRelations.remove(old)
        self.listRelations.insert(index, new)        
                
# Keep all Candidates obtained during a run of the algorithm
class Solutions:
    def __init__(self):
        self.listCandidates = []
    
    def get(self):
        return self.listCandidates
    
    def add(self, candidate):
        self.listCandidates.append(candidate)
        
    def remove(self, candidate):
        self.listCandidates.remove(candidate)
    
    def update(self, old, new):
        index = self.listCandidates.index(old)
        self.listCandidates.remove(old)
        self.listCandidates.insert(index, new)            

# Main Methods
class UCTP:
               
    # Get all data to work
    def getData(self, subj, prof):
        # Remove accents of datas
        #from unicodedata import normalize 
        #def remove_accent(txt):
        #    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
        
        # Read the data of professors and subjects and create the respective objects
        print "Getting datas of Professors...",
        with open('professors.csv') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            print "Setting Professors...",
            for row in spamreader:
                datas = [row[0].upper(), row[1].upper(), row[2].upper(), row[3].upper()]
                if(not datas.__contains__('')):
                    prof.append(Prof(datas[0], datas[1], datas[2], datas[3]))
                    print datas
        csvfile.close() 
            
        print(" ")
        print "Getting datas of Subjects...",
        with open('subjects.csv') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            print "Setting Subjects...",
            for row in spamreader:
                datas = [row[0].upper(), row[1].upper(), row[2].upper(), row[3].upper(), row[4].upper(), row[5].upper(), row[6].upper()]
                if(not datas.__contains__('') and row[0] == 'G' and ('MCTA' in row[1] or 'MCZA' in row[1])):
                    subj.append(Subject(datas[0], datas[1], datas[2], datas[3], datas[4], datas[5], datas[6]))
                    print datas       
        csvfile.close()
            
        print ("Data Obtained!")        
        return subj, prof
    
    # Export Candidates in differents generations into CSV files
    def outData(self, solutions, num):
        print "Exporting data....",
        
        # get current directory and creating new 'generationsCSV' dir
        currentDir = os.getcwd()
        newDir = currentDir + os.sep + 'generationsCSV' + os.sep
        if not os.path.exists(newDir):
                os.makedirs(newDir)
        
        # In 'generationsCSV' dir, create new 'gen' dir
        newDir = newDir + 'gen' + str(num) + os.sep
        if not os.path.exists(newDir):
            os.makedirs(newDir)
        
        # All Candidates of a Generation
        i = 0
        for cand in solutions.get():            
            outName = newDir + 'gen' +  str(num) + '_cand' +  str(i) + '.csv'
            with open(outName, 'wb') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(['sLevel', 'sCode', 'sName', 'sQuadri', 'sPeriod', 'sCharge', 'pName', 'pPeriod', 'pCharge', 'pQuadriSabbath'])
                # All relations in a Candidate of a Generation
                for s, p in cand.get():
                    row = s.get() + p.get()
                    spamwriter.writerow(row)
                spamwriter.writerow(" ")
                if cand.getIF() is 'f':
                    spamwriter.writerow(['Feasible', cand.getFitness()])
                elif cand.getIF() is 'i':
                    spamwriter.writerow(['Infeasible', cand.getFitness()])
                else:
                    spamwriter.writerow(['Error', cand.getFitness()])   
            # print("Created: " + outName + "in" + newDir + "...")
            i = i + 1
            csvfile.close()
            
        # All Fitness in a Generation
        outName = newDir + 'gen' +  str(num) + '.csv'
        with open(outName, 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['Candidate', 'Population', 'Fitness'])
            i = 0
            for cand in solutions.get():            
                if cand.getIF() is 'f':
                    spamwriter.writerow([i,'Feasible', cand.getFitness()])
                elif cand.getIF() is 'i':
                    spamwriter.writerow([i,'Infeasible', cand.getFitness()])
                else:
                    spamwriter.writerow([i,'Error', cand.getFitness()])
                i = i + 1       
        # print("Created: " + outName + "in" + newDir + "...")
        csvfile.close()
                
        print ("Data Exported!")    
        
    def printOneCand(self, candidate):
        for s, p in candidate.get():
            print s.get(), p.get()
    
    def printAllCand(self, solutions):
        for cand in solutions.get():
            self.printOneCand(cand)
            print ("--------")
    
    def printOneFit(self, cand):
        if cand.getIF() is 'f':
           print (': Feasible, ', str(cand.getFitness()))
        elif cand.getIF() is 'i':
            print (': Infeasible, ', str(cand.getFitness()))
        else:
            print (': Error, ', str(cand.getFitness()))     
            
    def printAllFit(self, solutions):
        n = 1
        for cand in solutions.get():
            if cand.getIF() is 'f':
               print str(n), ': Feasible, ', str(cand.getFitness()), ' / ',
            elif cand.getIF() is 'i':
                print str(n), ': Infeasible, ', str(cand.getFitness()), ' / ',
            else:
                print str(n), ': Error, ', str(cand.getFitness()), ' / ',       
            n = n + 1
            
    # Create the first generation of solutions
    def start(self, solutions, subj, prof, num):        
        print "Creating first generation...",
        n = 0
        while(n!=num):
            candidate = Candidate()
            for sub in subj:
                candidate.add(sub, prof[randrange(len(prof))])
            solutions.add(candidate)
            n = n+1
        print ("Created first generation!")    
        #self.printAllCand(solutions)
           
        return solutions
    
    # Reset Populations Separation to allow new separation
    def resetPop(self, solutions):
        newSol = Solutions()
        for cand in solutions.get():
            newCand = cand
            newCand.resetPop()
            newSol.add(newCand)      
        return newSol
    
    # Separation of solutions into 2 populations
    def two_pop(self, solutions, prof):
        newSol = Solutions()
        for cand in solutions.get():
            newCand = self.in_feasible(cand, prof)
            newSol.add(cand)
        return newSol
    
    # Detect the violation of a Restriction into a candidate
    def in_feasible(self, candidate, prof):
        # List used to relate with the position of Professors in 'prof' list 
        prof_total_charge = []
        n=0
        for n in range(len(prof)):
            prof_total_charge.append(0)
            n = n+1
            
        for s, p in candidate.get():
            sLevel, sCode, sName, sQuadri, sPeriod, sCharge = s.get()
            pName, pPeriod, pCharge, pQuadriSabbath = p.get()
            if(('NEGOCI' not in pPeriod) and (pPeriod != sPeriod)):
                candidate.setInfeas()
                return candidate
            elif(pQuadriSabbath == sQuadri):
                candidate.setInfeas()
                return candidate
            index = prof.index(p)
            prof_total_charge[index] = (prof_total_charge[index]+ int(sCharge))
        
        n=0
        for n in range(len(prof)):
            pName, pPeriod, pCharge, pQuadriSabbath = prof[n].get()
            if(pCharge < prof_total_charge[n]):
                candidate.setInfeas()
                return candidate
            n = n+1
            
        candidate.setFeas()            
        return candidate
    
    # Calculate the Fitness of the candidate
    def calc_fit(self, solutions):
        newSol = Solutions()
        for cand in solutions.get():
            newCand = cand
            if newCand.getIF() is 'f':
                newCand.setFitness(self.calc_fitFeas(newCand))
            elif newCand.getIF() is 'i':
                newCand.setFitness(self.calc_fitInfeas(newCand))
            else:
                print "ERROR: no Fitness, solution is not in a population!"
            newSol.add(newCand)
        return newSol
    
    def calc_fitFeas(self, candidate):
        return 1
    
    def calc_fitInfeas(self, candidate):
        return -1
    
    # Generate new solutions from the actual population
    def new_generation(self, solutions, nMut, nCross):
        newSol = Solutions()
        i=0
        for i in range(nMut):
            list = solutions.get()
            newCand = self.mutation(list[randrange(len(list))])
            newSol.add(newCand)
            
        i=0
        for i in range(nCross):
            list = solutions.get()
            newCand1, newCand2 = self.crossover(list[randrange(len(list))], list[randrange(len(list))])  
            newSol.add(newCand1)
            newSol.add(newCand2)
        
        for newCand in newSol.get():
            solutions.add(newCand)
            
        return solutions
            
    # Make a mutation into a solution
    def mutation(self, candidate):
        relations = candidate.get()
        return candidate
    
    # Make a crossover between two solutions    
    def crossover(self, cand1, cand2):
        relation1 = cand1.get()
        relation2 = cand2.get()
        return cand1, cand2
    
    # Make a random selection into the solutions
    def selection(self, solutions, min, max):
        originalSize = len(solutions.get())
        while(originalSize > max):
            list = solutions.get()
            cand = list[randrange(len(list))]
            solutions.remove(cand)
            originalSize = originalSize-1
            print "Candidate removed by Selection...."
            self.printOneFit(cand)
        return solutions
    
    # Detect the stop condition
    def stop(self, iteration, total, solutions):
        for cand in solutions.get():
            if cand.getFitness() >= 100:
                return False
        if(iteration == total):
            return False
        else:
            return True
    
# main
class main:
    # to access main methods and creating Solutions (List of Candidates)
    uctp = UCTP()
    solutions = Solutions()
    
    # Max Number of iterations to get a solution
    total = 100;
    # number of initial candidates (first generation)
    num = 50
    # Min and Max number of candidates in a generation
    min = 50
    max = 100
    # Number of Mutations and Crossover
    nMut = 10
    nCross = 10
    
    # Base Lists of Professors and Subjects
    prof = []
    subj = []
    
    # Start of the works
    subj, prof = uctp.getData(subj, prof)
    
    # First generation
    solutions = uctp.start(solutions, subj, prof, num)
    solutions = uctp.two_pop(solutions, prof)
    solutions = uctp.calc_fit(solutions)
    #uctp.outData(solutions, 0)
    uctp.printAllFit(solutions)
    
    # Main work - iterations to find a solution
    print(" ")
    print("Starting hard work...")
    t = 0;
    while(uctp.stop(t, total, solutions)):
        print 'Iteration:', t+1
        solutions = uctp.new_generation(solutions, nMut, nCross)
        solutions = uctp.selection(solutions, min, max) 
        solutions = uctp.resetPop(solutions)
        solutions = uctp.two_pop(solutions, prof)
        solutions = uctp.calc_fit(solutions)     
        #uctp.outData(solutions, t)
        uctp.printAllFit(solutions)
        print(" ")
        t = t+1
            
    print("FIM")
    
