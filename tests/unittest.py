import unittest

class SampleTestMethods(unittest.TestCase):

  def test_upper(self):
      self.assertEqual(1 + 1, 2)

if __name__ == '__main__':
    unittest.main()