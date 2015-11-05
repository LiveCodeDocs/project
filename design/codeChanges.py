'''
@author: bonattt
'''
#from test.test_importlib.source.test_source_encoding import LineEndingTest
class Code():
    
    def __init__(self, fileID):
        
        self.fileID = fileID
        self.linesOfCode = []
        self.queueOfChanges = []
        
    def getCode(self):
        codeStr = ""
        for k in range(len(self.linesOfCode)):
            codeStr = codeStr + self.linesOfCode[k] + "\n"
        return codeStr
        
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
        if change.lineNumber >= len(self.linesOfCode) - 1:
            raise ChangeLineOutOfBoundsException()
        
        if change.type == Change.insert:
            self._applyInsert_(change)
        elif change.type == Change.delete:
            self._applyRemove_(change)
        elif change.type == Change.newLine:
            self.newLineAt(change.lineNumber, change.index)
        elif change.type == Change.deleteLine:
            self.removeLineAt(change.lineNumber)
        else:
            raise NonexistantChangeTypeException()
        
    def _applyInsert_(self, change):
        if change.index > len(self.linesOfCode[change.lineNumber]):
            raise ChangeIndexOutOfBoundsException()
        lineEdited = self.linesOfCode[change.lineNumber]
        list1 = list(lineEdited[0 : change.index])
        list2 = list(lineEdited[change.index:])
        for k in range(len(change.string)):
            list1.append(change.string[k])
        self.linesOfCode[change.lineNumber] = "".join(list1 + list2)
    
    def _applyRemove_(self, change):
        lineEdited = self.linesOfCode[change.lineNumber]
        if change.index[0] < 0 or change.index[1] >= len(lineEdited):
            raise ChangeIndexOutOfBoundsException()
        
        str1 = lineEdited[0 : change.index[0]]
        str2 = lineEdited[change.index[1] : ]
        self.linesOfCode[change.lineNumber] = str1 + str2
        
    def removeLineAt(self, lineNumber):
        secondLine = self.linesOfCode[lineNumber + 1]
        self.linesOfCode.remove(secondLine)
        self.linesOfCode[lineNumber] = self.linesOfCode[lineNumber] + secondLine
        
        for k in range(len(self.queueOfChanges)):
            if lineNumber < self.queueOfChanges[k].lineNumber:
                self.queueOfChanges[k].lineNumber -= 1
        
    def newLineAt(self, lineNumber, index=0, linesAdded=1):
        secondLine = self.linesOfCode[lineNumber][index :]
        firstLine = self.linesOfCode[lineNumber][0 : index]
        self.linesOfCode.insert(lineNumber+1, secondLine)
        self.linesOfCode[lineNumber] = firstLine #self.linesOfCode[lineNumber][0 : index-1]
        
        for k in range(len(self.queueOfChanges)):
            if lineNumber < self.queueOfChanges[k].lineNumber:
                self.queueOfChanges[k].lineNumber += linesAdded
        
        
class Change():
    insert = 0
    delete = 1
    newLine = 2
    deleteLine = 3
    
    def __init__(self, lineNo, changeType, index=0, string=""):
        self.__checkInputs__(lineNo, index, string, changeType)
        self.lineNumber = lineNo
        self.index = index
        self.string = string
        self.type = changeType
        
    def __checkInputs__(self, lineNo, index, string, changeType):
        if not type(lineNo) == int:
            raise ChangeIncorrectConstructorArgument("lineNo", lineNo)
        elif not type(changeType) == int:
            raise ChangeIncorrectConstructorArgument("changeType", changeType)
        elif not (type(index) == int or (type(index) == tuple and changeType == Change.delete)):
            raise ChangeIncorrectConstructorArgument("index", index)
        elif not type(string) == str:
            raise ChangeIncorrectConstructorArgument("string", string)
        
class NonexistantChangeTypeException(Exception):
    pass 
class ChangeIndexOutOfBoundsException(Exception):
    pass
class ChangeLineOutOfBoundsException(Exception):
    pass
class ChangeIncorrectConstructorArgument(Exception):
    
    def __init__(self, arg, value):
        super(ChangeIncorrectConstructorArgument, self).__init__(arg + str(value))
