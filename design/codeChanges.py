'''
@author: bonattt
'''
class Code():
    
    def __init__(self):
        
        self.linesOfCode = []
        self.queueOfChanges = []
        
    def enqueueChange(self, change):
        self.queueOfChanges.append(change)
        
    def dequeueChange(self):
        val = self.queueOfChanges[0]
        self.queueOfChanges.remove(val)
        return val
        
    def handleChanges(self):
        while len(self.queueOfChanges) > 0:
            change = self.dequeueChange()
            self.applyChange(change)
        
    def applyChange(self, change):
        pass
        
    def removeLineAt(self, lineNumber,  index=0, linesRemoved=1):
        for k in range(len(self.queueOfChanges)):
            if lineNumber < self.queueOfChanges[k].lineNumber:
                self.queueOfChanges[k].lineNumber -= linesRemoved
    def newLineAt(self, lineNumber, index=0, linesAdded=1):
        for k in range(len(self.queueOfChanges)):
            if lineNumber < self.queueOfChanges[k].lineNumber:
                self.queueOfChanges[k].lineNumber += linesAdded
        
class Change():
    add = 0
    remove = 1
    
    def __init__(self, lineNo, index, string, changeType):
        self.lineNumber = lineNo
        self.range = range
        self.str = str
