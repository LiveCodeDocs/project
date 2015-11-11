'''
@author: bonattt
'''
import threading
from Queue import Queue

#from test.test_importlib.source.test_source_encoding import LineEndingTest
class Code(threading.Thread):
    
    def __init__(self, changeQueue, codeRequestQueue, outputQueue, codeStr, fileID):
	threading.Thread.__init__(self, args=(), kwargs=None)
	self.changeQueue = changeQueue
	self.codeRequestQueue = codeRequestQueue
	self.outputQueue = outputQueue
        self.fileID = fileID
        self.linesOfCode = codeStr.split("\n")
        self.queueOfChanges = []
        self.exitFlag = False
        
    def run(self):
	while True:
	   while not self.changeQueue.empty():
	        newChange = self.changeQueue.get()
		print 'handling change: ' + str(newChange)
		self.enqueueChange(newChange)
		#self.enqueueChange(self.changeQueue.get())
	   if not self.codeRequestQueue.empty():
		while not self.codeRequestQueue.empty():
		  self.codeRequestQueue.get()
		self.outputQueue.put(self.getCode())
	   self.handleChanges()
	    		

    def keepCodeUpToDate(self):
        while not self.exitFlag:
            self.handleChanges()
 
    def getCode(self):
        codeStr = ""
        for k in range(len(self.linesOfCode)):
            codeStr = codeStr + self.linesOfCode[k] + "\n"
        return codeStr
        
    def enqueueChange(self, change):
        if type(change.lineNumber) == tuple:
            self._expandMultiLinedChange_(change)
        else:
            self.queueOfChanges.append(change)
        
    def _expandMultiLinedChange_(self, change):

        if change.type == Change.insert:
            if type(change.index) != int:
                raise ChangeIncorrectArgument("index should be int for multiple line insert: ", change.index)
            self._expandMultiLineInsert_(change)
        if change.type == Change.delete:
            if type(change.index) != tuple:
                raise ChangeIncorrectArgument("index should be tuple for multiple line delete: ", change.index)
            self._expandMultiLineDelete_(change)
        if change.type == Change.deleteLine:
            raise InvalidCaseForTupleTypeLineNumber()
        if change.type == Change.newLine:
            raise InvalidCaseForTupleTypeLineNumber()
            
    def _expandMultiLineInsert_(self, change):
        self.handleChanges()
        insertedLines = str.split(change.string, "\n")
        for k in range(change.lineNumber[0], change.lineNumber[1]):
#             if k == change.lineNumber[0]:
#                 index = change.index
#             else:
#                 index = 0
            self.enqueueChange(Change(change.lineNumber[0], Change.newLine, change.index))

        self.handleChanges()

        for k in range(change.lineNumber[0], change.lineNumber[1]+1):
            string = insertedLines[k - change.lineNumber[0]]
            
            if k == change.lineNumber[0]:
                index = change.index
            else:
                index = 0
            self.enqueueChange(Change(k, Change.insert, index, string))
            
        self.handleChanges()
                    
    def _expandMultiLineDelete_(self, change):
        
        if change.lineNumber[0] == change.lineNumber[1]:
            self.enqueueChange(Change(change.lineNumber[0], change.type, change.index, change.string))
            return

        for k in range(change.lineNumber[0], change.lineNumber[1]+1):
            if k == change.lineNumber[0]:
                index = (change.index[0], len(self.linesOfCode[k]))
            elif k == change.lineNumber[1]:
                index = (0, change.index[1])
            else:
                index = (0, len(self.linesOfCode[k]))
                
            currentChange = Change(k, Change.delete, index)
            self.enqueueChange(currentChange)
        for k in range(change.lineNumber[0], change.lineNumber[1]):
            self.enqueueChange(Change(k, Change.deleteLine))
        
    def dequeueChange(self):
        val = self.queueOfChanges[0]
        self.queueOfChanges.remove(val)
        return val
        
    def handleChanges(self):
        while len(self.queueOfChanges) > 0:
            change = self.dequeueChange()
            self.applyChange(change)
        return True
        
    def applyChange(self, change):
        if change.lineNumber >= len(self.linesOfCode):
            return
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
            return	
	    raise ChangeIndexOutOfBoundsException()
        lineEdited = self.linesOfCode[change.lineNumber]
        list1 = list(lineEdited[0 : change.index])
        list2 = list(lineEdited[change.index:])
        for k in range(len(change.string)):
            list1.append(change.string[k])
        self.linesOfCode[change.lineNumber] = "".join(list1 + list2)
    
    def _applyRemove_(self, change):
        if type(change.lineNumber) == tuple:
            self._applyRemoveOnMultipleLines_(change)
            return
        lineEdited = self.linesOfCode[change.lineNumber]
#         if change.index[0] < 0 or change.index[1] >= len(lineEdited):
#             raise ChangeIndexOutOfBoundsException()
        
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
    
    def __repr__(self):
        return 'lineNo: ' + str(self.lineNumber) + ', string: ' + self.string  + ', index: ' + str(self.index) + ', type: ' + str(self.type)	
 
    def __checkInputs__(self, lineNo, index, string, changeType):
        pass
#         if not (type(lineNo) == int or type(lineNo) == tuple):
#             raise ChangeIncorrectArgument("lineNo", lineNo)
#         elif not type(changeType) == int:
#             raise ChangeIncorrectArgument("changeType", changeType)
#         elif not (type(index) == int or (type(index) == tuple and changeType == Change.delete)):
#             raise ChangeIncorrectArgument("index", index)
#         elif not type(string) == str:
#             raise ChangeIncorrectArgument("string", string)
        
class NonexistantChangeTypeException(Exception):
    pass 
class ChangeIndexOutOfBoundsException(Exception):
    pass
class ChangeLineOutOfBoundsException(Exception):
    pass
class InvalidCaseForTupleTypeLineNumber(Exception):
    pass
class SinglePointIndexUsedForMultipleLinesException(Exception):
    pass

class ChangeIncorrectArgument(Exception):
    
    def __init__(self, arg, value):
        super(ChangeIncorrectArgument, self).__init__(arg + str(value))
