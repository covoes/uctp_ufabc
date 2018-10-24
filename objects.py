# Objects used on UCTP algorithm

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
        