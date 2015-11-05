'''
@author: bonattt
'''

import unittest
import codeChanges as c

def enqueueSomeChanges(code):
       
    change1 = c.Change(0, c.Change.insert, 13, " -- this line has been changed")
    change2 = c.Change(1, c.Change.insert, 13, " -- this line has been changed")
    change3 = c.Change(2, c.Change.insert, 13, " -- this line has been changed")
        
    code.enqueueChange(change1)
    code.enqueueChange(change2)
    code.enqueueChange(change3)

class TestCodeChanges(unittest.TestCase):
    
    def setUp(self):
        self.code = c.Code("", 0)
        self.code.linesOfCode = ["this is line 1",
                            "this is line 2",
                            "this is line 3",
                            "this is line 4",
                            "this is line 5",
                            "this is line 6",
                            "this is line 7"]
        
    def testGetCodeGetsCode(self):
        expected = "this is line 1\nthis is line 2\nthis is line 3\nthis is line 4\nthis is line 5\nthis is line 6\nthis is line 7\n"
        self.assertEqual(expected, self.code.getCode())
        
    def testDequeueChangeRemovesChange(self):
        enqueueSomeChanges(self.code)
        initialLength = len(self.code.queueOfChanges)
        self.code.dequeueChange()
        self.assertEqual(initialLength - 1, len(self.code.queueOfChanges))
        
    def testDequeueChangeReturnsFirstAdded(self):
        
        change1 = c.Change(3, c.Change.insert, 13, " -- this line has been changed")
        self.code.enqueueChange(change1)
        enqueueSomeChanges(self.code)
        self.assertTrue(self.code.dequeueChange() is change1)
        
    def testRemoveLineShiftsLinesBelow(self):
        change1 = c.Change(0, c.Change.insert, 13, " -- this line has been changed")
        change2 = c.Change(1, c.Change.insert, 13, " -- this line has been changed")
        change3 = c.Change(5, c.Change.insert, 13, " -- this line has been changed")
        change4 = c.Change(6, c.Change.insert, 13, " -- this line has been changed")
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
        change1 = c.Change(0, c.Change.insert, 13, " -- this line has been changed")
        change2 = c.Change(1, c.Change.insert, 13, " -- this line has been changed")
        change3 = c.Change(5, c.Change.insert, 13, " -- this line has been changed")
        change4 = c.Change(6, c.Change.insert, 13, " -- this line has been changed")
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
        change1 = c.Change(0, c.Change.insert, 13, " -- this line has been changed")
        change2 = c.Change(1, c.Change.insert, 13, " -- this line has been changed")
        change3 = c.Change(5, c.Change.insert, 13, " -- this line has been changed")
        change4 = c.Change(6, c.Change.insert, 13, " -- this line has been changed")
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
        change1 = c.Change(0, c.Change.insert, 13, " -- this line has been changed")
        change2 = c.Change(1, c.Change.insert, 13, " -- this line has been changed")
        change3 = c.Change(5, c.Change.insert, 13, " -- this line has been changed")
        change4 = c.Change(6, c.Change.insert, 13, " -- this line has been changed")
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
        change = c.Change(0, c.Change.insert, 13, " -- this line has been changed")
        self.code.applyChange(change)
        self.assertNotEqual("this is line 1", self.code.linesOfCode[0])
        
    def testInsertInsertsAtCorrectIndex1(self):
        change = c.Change(0, c.Change.insert, 0, "changed -- ")
        self.code.applyChange(change)
        self.assertEqual("changed -- this is line 1", self.code.linesOfCode[0])
    
    def testInsertInsertsAtCorrectIndex2(self):
        change = c.Change(0, c.Change.insert, len(self.code.linesOfCode[0]), " -- changed")
        self.code.applyChange(change)
        self.assertEqual("this is line 1 -- changed", self.code.linesOfCode[0])
        
    def testApplyInsertMakesCorrectChanges(self):
        change = c.Change(0, c.Change.insert, 14, " -- this line has been changed")
        self.code.applyChange(change)
        self.assertEqual("this is line 1 -- this line has been changed", self.code.linesOfCode[0])
        
    def testApplyRemoveRemovesFromCorrectLine(self):
        change = c.Change(0, c.Change.delete, (2, 8), "")
        self.code.applyChange(change)
        self.assertNotEqual("this is line 1", self.code.linesOfCode[0])
        
    def testApplyRemoveCorrectCode1(self):
        change = c.Change(0, c.Change.delete, (8, 13), "")
        self.code.applyChange(change)
        self.assertEqual("this is 1", self.code.linesOfCode[0])
    
    def testApplyRemoveCorrectCode2(self):
        change = c.Change(0, c.Change.delete, (0, 5), "")
        self.code.applyChange(change)
        self.assertEqual("is line 1", self.code.linesOfCode[0])
        
    def testApplyChangeDoesNotChangeOtherLines(self):
        change = c.Change(0, c.Change.insert, 13, " -- this line has been changed")
        self.code.applyChange(change)
        for i in range(1, 7):
            self.assertEqual("this is line " + str(i+1), self.code.linesOfCode[i])
            
    def testNewLineInTheMiddleOfALineSplitsTheLine(self):
        change = c.Change(4, c.Change.newLine, 7, "")
        self.code.applyChange(change)
        self.assertEqual("this is", self.code.linesOfCode[4])
        self.assertEqual(" line 5", self.code.linesOfCode[5])

    def testNewLineSplitMaintainsCode(self):
        change = c.Change(4, c.Change.newLine, 7, "")
        originalLine = self.code.linesOfCode[4]
        self.code.applyChange(change)
        self.assertEqual(originalLine, self.code.linesOfCode[4] + self.code.linesOfCode[5])

    def testDeleteLineMergesLines(self):
        change = c.Change(4, c.Change.deleteLine, 0, "")
        self.code.applyChange(change)
        self.assertEqual("this is line 5this is line 6", self.code.linesOfCode[4])
        
    def testNewLineIncreasesLengthOfCode(self):
        initialLength = len(self.code.linesOfCode)
        change = c.Change(4, c.Change.newLine)
        self.code.applyChange(change)
        self.assertEqual(initialLength + 1, len(self.code.linesOfCode))
        
    def testRemoveLineDecreasesLengthOfCode(self):
        initialLength = len(self.code.linesOfCode)
        change = c.Change(4, c.Change.deleteLine)
        self.code.applyChange(change)
        self.assertEqual(initialLength - 1, len(self.code.linesOfCode))
        
if __name__ == '__main__':
    unittest.main()