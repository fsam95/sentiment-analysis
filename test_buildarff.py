import unittest
import buildarff

class TypicalTestCase(unittest.TestCase):

  def setUp(self):
  	self.tweet1 = "switchfoot/NN /NN -/: Awww,/NN that/IN 's/POS a/DT bummer/NN ./.\n /NN You/PRP shoulda/NN got/VBD David/NNP Carr/NNP of/IN Third/NNP Day/NNP to/TO do/VBP it/PRP ./.\n ;D/NN"
  	self.tweet2 = "Kenichan/NN I/PRP dived/VBD many/JJ times/NNS for/IN the/DT ball/NN ./.\n Managed/VBN to/TO save/VB 50%/NN /NN The/DT rest/NN go/VB out/IN of/IN bounds/NNS"
        self.tweet3 = "makeherfamous/NNS hmm/NN /NN ,/, do/VBP u/PRP really/RB enjoy/VB being/VBG with/IN him/PRP ?/. if/IN the/DT problems/NNS are/VBP too/RB constants/NNS u/PRP should/MD think/VBP things/NNS more/JJR ,/, find/VB someone/NN ulike/NN"
        self.tweet4 = "stark/JJ YOU/PRP do/VBP n't/RB follow/VB me/PRP ,/, either/DT /NN and/CC i/NN work/NN for/IN you/PRP !/."
        self.tweet5 = "Going/VBG to/TO sleep/VB ./."
        self.tweet6 = "Helloooooo/NN :/: ./."

  def testFeat1(self):
  	self.assertEqual(buildarff.feat1(self.tweet1), 0)
  	self.assertEqual(buildarff.feat1(self.tweet2), 1)

  def testFeat2(self):
    self.assertEqual(buildarff.feat2(self.tweet1), 1)

  def testFeat3(self):
    self.assertEqual(buildarff.feat3(self.tweet3), 1)
    self.assertEqual(buildarff.feat1(self.tweet1), 0)
  
  def testFeat4(self):
    self.assertEqual(buildarff.feat4(self.tweet4), 1)

  def testFeat5(self):
    self.assertEqual(buildarff.feat5(self.tweet1), 1)

  def testFeat6(self):
    self.assertEqual(buildarff.feat6(self.tweet5), 1)
    
  def testFeat7(self):
    self.assertEqual(buildarff.feat7(self.tweet4), 1)

  def testFeat8(self):
    self.assertEqual(buildarff.feat8(self.tweet6), 1)



if __name__ == '__main__':
	unittest.main(exit=False)


