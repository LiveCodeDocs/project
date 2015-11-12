'''
@author: bonattt
'''

import unittest
import codeChanges
from Queue import Queue

def enqueueSomeChanges(code):
       
    change1 = codeChanges.Change(0, codeChanges.Change.insert, 13, " -- this line has been changed")
    change2 = codeChanges.Change(1, codeChanges.Change.insert, 13, " -- this line has been changed")
    change3 = codeChanges.Change(2, codeChanges.Change.insert, 13, " -- this line has been changed")
        
    code.enqueueChange(change1)
    code.enqueueChange(change2)
    code.enqueueChange(change3)
    
def printLinesOfCode(loc):
    for k in range(len (loc)):
        print(loc[k])

def main():
		setUp()
		testInsertMultipleLinesInsertsMultipleLinesEndOfALine()
		testInsertMultipleLinesInsertsMultipleLinesMiddleOfALine()
		testInsertMultipleLinesInsertsMultipleLinesBeginningOfALine()
		testDeleteMultipleLinesDeletesMultipleLines1()
		testRemoveFromZeroToZeroRemovesNothing()
	    testGetCodeGetsCode()
	    testDequeueChangeRemovesChange()
	    testDequeueChangeReturnsFirstAdded()
	    testRemoveLineShiftsLinesBelow()
	    testRemoveLineDoesNotShiftLinesAbove()
	    testNewLineShiftsLinesBelow()
	    testNewLineDoesNotShiftLinesAbove()
	    testApplyInsertChangesCorrectLine()
	    testInsertInsertsAtCorrectIndex1()
	    testInsertInsertsAtCorrectIndex2()
	    testApplyInsertMakesCorrectChanges()
	    testApplyRemoveRemovesFromCorrectLine()
	    testApplyRemoveCorrectCode1()
	    testApplyRemoveCorrectCode2()
	    testApplyChangeDoesNotChangeOtherLines()
	    testNewLineInTheMiddleOfALineSplitsTheLine()
	    testNewLineSplitMaintainsCode()
	    testDeleteLineMergesLines()
	    testNewLineIncreasesLengthOfCode()
	    testRemoveLineDecreasesLengthOfCode()
	    testBensCode01()
	    testBensCode02()
	    testBensCode03()
	    testBensCode04()
	    testBensCode05()

class TestCodeChanges(unittest.TestCase):
    
    def setUp(self):
        self.code = codeChanges.Code(Queue(), Queue(), Queue(), "", 0)
        self.code.linesOfCode = ["this is line 1",
                            "this is line 2",
                            "this is line 3",
                            "this is line 4",
                            "this is line 5",
                            "this is line 6",
                            "this is line 7"]
        
    def testInsertMultipleLinesInsertsMultipleLinesEndOfALine(self):
        expected  = ["this is line 1",
                    "this is line 2",
                    "this is line 3-- edit",  # 2
                    "still editing",    # 3
                    "-- ",        # 4
                    "this is line 4",
                    "this is line 5",
                    "this is line 6",
                    "this is line 7"]
        change = codeChanges.Change((2,4), codeChanges.Change.insert, 14, "-- edit\nstill editing\n-- ")
        self.code.enqueueChange(change)
        self.code.handleChanges()
        
#         print("INSERT")
#         print("expected: ")
#         printLinesOfCode(expected)
#         print("\nactual: ")
#         printLinesOfCode(self.code.linesOfCode)
        
        self.assertEqual(len(expected), len(self.code.linesOfCode))
        
        for k in range(len(expected)):
            self.assertEqual(expected[k], self.code.linesOfCode[k])
        
    def testInsertMultipleLinesInsertsMultipleLinesMiddleOfALine(self):
        expected  = ["this is line 1",
                    "this is line 2",
                    "this is -- edit",  # 2
                    "still editing",    # 3
                    "-- line 3",        # 4
                    "this is line 4",
                    "this is line 5",
                    "this is line 6",
                    "this is line 7"]
        change = codeChanges.Change((2,4), codeChanges.Change.insert, 8, "-- edit\nstill editing\n-- ")
        self.code.enqueueChange(change)
        self.code.handleChanges()
        
#         print("INSERT")
#         print("expected: ")
#         printLinesOfCode(expected)
#         print("\nactual: ")
#         printLinesOfCode(self.code.linesOfCode)
        
        self.assertEqual(len(expected), len(self.code.linesOfCode))
        
        for k in range(len(expected)):
            self.assertEqual(expected[k], self.code.linesOfCode[k])
        
    def testInsertMultipleLinesInsertsMultipleLinesBeginningOfALine(self):
        expected  = ["this is line 1",
                    "this is line 2",
                    "-- edit",  # 2
                    "still editing",    # 3
                    "-- this is line 3",        # 4
                    "this is line 4",
                    "this is line 5",
                    "this is line 6",
                    "this is line 7"]
        change = codeChanges.Change((2,4), codeChanges.Change.insert, 0, "-- edit\nstill editing\n-- ")
        self.code.enqueueChange(change)
        self.code.handleChanges()
        
#         print("INSERT")
#         print("expected: ")
#         printLinesOfCode(expected)
#         print("\nactual: ")
#         printLinesOfCode(self.code.linesOfCode)
        
        self.assertEqual(len(expected), len(self.code.linesOfCode))
        
        for k in range(len(expected)):
            self.assertEqual(expected[k], self.code.linesOfCode[k])
        
    def testDeleteMultipleLinesDeletesMultipleLines1(self):
        expected  = ["this is line 1",
                    "this is line 2",
                    "this is line 5",
                    "this is line 6",
                    "this is line 7"]
        change = codeChanges.Change((2,4), codeChanges.Change.delete, (0, 0))
        self.code.enqueueChange(change)
        self.code.handleChanges()
        
        print("DELETE")
        print("expected: ")
        printLinesOfCode(expected)
        print("\nactual: ")
        printLinesOfCode(self.code.linesOfCode)
        
        self.assertEqual(expected, self.code.linesOfCode)
    
    def testRemoveFromZeroToZeroRemovesNothing(self):
        expected = ["this is line 1",
                    "this is line 2",
                    "this is line 3",
                    "this is line 4",
                    "this is line 5",
                    "this is line 6",
                    "this is line 7"]
        change = codeChanges.Change(2, codeChanges.Change.delete, (0,0))
        self.code.enqueueChange(change)
        self.code.handleChanges()
        self.assertEqual(len(expected), len(self.code.linesOfCode))
        for k in range(len(expected)):
            self.assertEqual(expected[k], self.code.linesOfCode[k])
        
    def testGetCodeGetsCode(self):
        expected = "this is line 1\nthis is line 2\nthis is line 3\nthis is line 4\nthis is line 5\nthis is line 6\nthis is line 7\n"
        self.assertEqual(expected, self.code.getCode())
        
    def testDequeueChangeRemovesChange(self):
        enqueueSomeChanges(self.code)
        initialLength = len(self.code.queueOfChanges)
        self.code.dequeueChange()
        self.assertEqual(initialLength - 1, len(self.code.queueOfChanges))
        
    def testDequeueChangeReturnsFirstAdded(self):
        
        change1 = codeChanges.Change(3, codeChanges.Change.insert, 13, " -- this line has been changed")
        self.code.enqueueChange(change1)
        enqueueSomeChanges(self.code)
        self.assertTrue(self.code.dequeueChange() is change1)

    def testRemoveLineShiftsLinesBelow(self):
        change1 = codeChanges.Change(0, codeChanges.Change.insert, 13, " -- this line has been changed")
        change2 = codeChanges.Change(1, codeChanges.Change.insert, 13, " -- this line has been changed")
        change3 = codeChanges.Change(5, codeChanges.Change.insert, 13, " -- this line has been changed")
        change4 = codeChanges.Change(6, codeChanges.Change.insert, 13, " -- this line has been changed")
        self.code.enqueueChange(change1)
        self.code.enqueueChange(change2)
        self.code.enqueueChange(change3)
        self.code.enqueueChange(change4)
        
        original3 = change3.lineNumber
        original4 = change4.lineNumber
        
        self.code.removeLineAt(4)
        self.assertEqual(original3 -1, change3.lineNumber)
        self.assertEqual(original4 -1, change4.lineNumber)
    
    def testRemoveLineDoesNotShiftLinesAbove(self):
        change1 = codeChanges.Change(0, codeChanges.Change.insert, 13, " -- this line has been changed")
        change2 = codeChanges.Change(1, codeChanges.Change.insert, 13, " -- this line has been changed")
        change3 = codeChanges.Change(5, codeChanges.Change.insert, 13, " -- this line has been changed")
        change4 = codeChanges.Change(6, codeChanges.Change.insert, 13, " -- this line has been changed")
        self.code.enqueueChange(change1)
        self.code.enqueueChange(change2)
        self.code.enqueueChange(change3)
        self.code.enqueueChange(change4)
        
        original1 = change1.lineNumber
        original2 = change2.lineNumber
        
        self.code.removeLineAt(4)
        self.assertEqual(original1, change1.lineNumber)
        self.assertEqual(original2, change2.lineNumber)
    
    def testNewLineShiftsLinesBelow(self):
        change1 = codeChanges.Change(0, codeChanges.Change.insert, 13, " -- this line has been changed")
        change2 = codeChanges.Change(1, codeChanges.Change.insert, 13, " -- this line has been changed")
        change3 = codeChanges.Change(5, codeChanges.Change.insert, 13, " -- this line has been changed")
        change4 = codeChanges.Change(6, codeChanges.Change.insert, 13, " -- this line has been changed")
        self.code.enqueueChange(change1)
        self.code.enqueueChange(change2)
        self.code.enqueueChange(change3)
        self.code.enqueueChange(change4)
        
        original3 = change3.lineNumber
        original4 = change4.lineNumber
        
        self.code.newLineAt(4)
        self.assertEqual(original3 + 1, change3.lineNumber)
        self.assertEqual(original4 + 1, change4.lineNumber)
        
    def testNewLineDoesNotShiftLinesAbove(self):
        change1 = codeChanges.Change(0, codeChanges.Change.insert, 13, " -- this line has been changed")
        change2 = codeChanges.Change(1, codeChanges.Change.insert, 13, " -- this line has been changed")
        change3 = codeChanges.Change(5, codeChanges.Change.insert, 13, " -- this line has been changed")
        change4 = codeChanges.Change(6, codeChanges.Change.insert, 13, " -- this line has been changed")
        self.code.enqueueChange(change1)
        self.code.enqueueChange(change2)
        self.code.enqueueChange(change3)
        self.code.enqueueChange(change4)
        
        original1 = change1.lineNumber
        original2 = change2.lineNumber
        
        self.code.newLineAt(4)
        self.assertEqual(original1, change1.lineNumber)
        self.assertEqual(original2, change2.lineNumber)
    
    def testApplyInsertChangesCorrectLine(self):
        change = codeChanges.Change(0, codeChanges.Change.insert, 13, " -- this line has been changed")
        self.code.applyChange(change)
        self.assertNotEqual("this is line 1", self.code.linesOfCode[0])
        
    def testInsertInsertsAtCorrectIndex1(self):
        change = codeChanges.Change(0, codeChanges.Change.insert, 0, "changed -- ")
        self.code.applyChange(change)
        self.assertEqual("changed -- this is line 1", self.code.linesOfCode[0])
    
    def testInsertInsertsAtCorrectIndex2(self):
        change = codeChanges.Change(0, codeChanges.Change.insert, len(self.code.linesOfCode[0]), " -- changed")
        self.code.applyChange(change)
        self.assertEqual("this is line 1 -- changed", self.code.linesOfCode[0])
        
    def testApplyInsertMakesCorrectChanges(self):
        change = codeChanges.Change(0, codeChanges.Change.insert, 14, " -- this line has been changed")
        self.code.applyChange(change)
        self.assertEqual("this is line 1 -- this line has been changed", self.code.linesOfCode[0])

    def testApplyRemoveRemovesFromCorrectLine(self):
        change = codeChanges.Change(0, codeChanges.Change.delete, (2, 8), "")
        self.code.applyChange(change)
        self.assertNotEqual("this is line 1", self.code.linesOfCode[0])
        
    def testApplyRemoveCorrectCode1(self):
        change = codeChanges.Change(0, codeChanges.Change.delete, (8, 13), "")
        self.code.applyChange(change)
        self.assertEqual("this is 1", self.code.linesOfCode[0])
    
    def testApplyRemoveCorrectCode2(self):
        change = codeChanges.Change(0, codeChanges.Change.delete, (0, 5), "")
        self.code.applyChange(change)
        self.assertEqual("is line 1", self.code.linesOfCode[0])
        
    def testApplyChangeDoesNotChangeOtherLines(self):
        change = codeChanges.Change(0, codeChanges.Change.insert, 13, " -- this line has been changed")
        self.code.applyChange(change)
        for i in range(1, 7):
            self.assertEqual("this is line " + str(i+1), self.code.linesOfCode[i])
            
    def testNewLineInTheMiddleOfALineSplitsTheLine(self):
        change = codeChanges.Change(4, codeChanges.Change.newLine, 7, "")
        self.code.applyChange(change)
        self.assertEqual("this is", self.code.linesOfCode[4])
        self.assertEqual(" line 5", self.code.linesOfCode[5])

    def testNewLineSplitMaintainsCode(self):
        change = codeChanges.Change(4, codeChanges.Change.newLine, 7, "")
        originalLine = self.code.linesOfCode[4]
        self.code.applyChange(change)
        self.assertEqual(originalLine, self.code.linesOfCode[4] + self.code.linesOfCode[5])

    def testDeleteLineMergesLines(self):
        change = codeChanges.Change(4, codeChanges.Change.deleteLine, 0, "")
        self.code.applyChange(change)
        self.assertEqual("this is line 5this is line 6", self.code.linesOfCode[4])
        
    def testNewLineIncreasesLengthOfCode(self):
        initialLength = len(self.code.linesOfCode)
        change = codeChanges.Change(4, codeChanges.Change.newLine)
        self.code.applyChange(change)
        self.assertEqual(initialLength + 1, len(self.code.linesOfCode))
        
    def testRemoveLineDecreasesLengthOfCode(self):
        initialLength = len(self.code.linesOfCode)
        change = codeChanges.Change(4, codeChanges.Change.deleteLine)
        self.code.applyChange(change)
        self.assertEqual(initialLength - 1, len(self.code.linesOfCode))
        
    def testBensCode01(self):
        expected = ["print 'hello world'a"]
         
        code = codeChanges.Code(Queue(), Queue(), Queue(), "print 'hello world'", 1)
        change = codeChanges.Change(0, 0, 19, 'a')
        code.enqueueChange(change)
        code.handleChanges()
#         print("expected: ", end="")
#         print(expected)
#         print("actual: ", end="")
#         print(code.linesOfCode)
        self.assertEqual(expected, code.linesOfCode)
         
    def testBensCode02(self):
        expected = ["print 'hello world'"]
         
        code = codeChanges.Code(Queue(), Queue(), Queue(), "print 'hello world'a", 2)
        change = codeChanges.Change((0, 0), 1, (19, 20))
        code.enqueueChange(change)
        code.handleChanges()
         
        self.assertEqual(expected, code.linesOfCode)
         
    def testBensCode03(self):
        expected = ["print 'hello world'", "a"]
          
        code = codeChanges.Code(Queue(), Queue(), Queue(), "print 'hello world'", 3)
        code.enqueueChange(codeChanges.Change(0, 2, 19))
        code.handleChanges()
        code.enqueueChange(codeChanges.Change(1, 0, 0, 'a'))
        code.handleChanges()
          
        self.assertEqual(expected, code.linesOfCode)
         
    def testBensCode04(self):
        expected = ["print 'hello world'", "aasdasda"]
         
        code = codeChanges.Code(Queue(), Queue(), Queue(), "print 'hello world'\na", 4)
        code.enqueueChange(codeChanges.Change(1, 0, 1, 'a'))
        code.enqueueChange(codeChanges.Change(1, 0, 2, 's'))
        code.enqueueChange(codeChanges.Change(1, 0, 3, 'd'))
        code.enqueueChange(codeChanges.Change(1, 0, 4, 'a'))
        code.enqueueChange(codeChanges.Change(1, 0, 5, 's'))
        code.enqueueChange(codeChanges.Change(1, 0, 6, 'd'))
        code.enqueueChange(codeChanges.Change(1, 0, 7, 'a'))
        code.handleChanges()
         
        self.assertEqual(expected, code.linesOfCode)
         
    def testBensCode05(self):
        expected = ["print "]
         
        code = codeChanges.Code(Queue(), Queue(), Queue(), "print 'hello world'\naasdasda", 5)
        code.enqueueChange(codeChanges.Change((0, 1), 1, (6, 8)))
        code.handleChanges()
         
        self.assertEqual(expected, code.linesOfCode)

if __name__ == '__main__':
    unittest.main()