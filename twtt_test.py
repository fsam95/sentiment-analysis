import unittest
import twtt

class TypicalTestCase(unittest.TestCase):
  
  def setUp(self):
    self.tweet_with_char_codes = "watching &quot;House&quot;"

  def testStripCharCodes(self):
    expected_tweet = 'watching "House"'
    actual = twtt.strip_char_codes(self.tweet_with_char_codes)
    self.assertEqual(actual, expected_tweet) 

  def testRemoveUrls(self):
    tweet_with_urls = "Broadband plan 'a massive broken promise' http://tinyurl.com/dcuc33 via www.diigo.com/~tautao Still waiting for broadband we are " 
    expected = "Broadband plan 'a massive broken promise'  via  Still waiting for broadband we are " 
    actual = twtt.remove_urls(tweet_with_urls)
    self.assertEqual(actual, expected)

  def testRemoveHashAndAt(self):
    tweet_with_at_hash = "@markhardy1974 Me too  #itm"
    expected = "markhardy1974 Me too  itm"
    self.assertEqual(twtt.remove_hash_and_at(tweet_with_at_hash), expected)

  def testNewlineOnBoundaries(self):
    simple_tweet = "Damn! The grind is inspirational and saddening at the same time.  Don't want you to stop cuz I like what u do! Much love"
    expected_tweet = "Damn!\n The grind is inspirational and saddening at the same time.\n  Don't want you to stop cuz I like what u do!\n Much love"
    boundaries = [4, 63, 109]
    actual_tweet = twtt.place_newline_on_boundaries(simple_tweet, boundaries)
    self.assertEqual(actual_tweet, expected_tweet)

  def testNaiveSentenceBoundaries(self):
    simple_tweet = "Damn! The grind is inspirational and saddening at the same time.  Don't want you to stop cuz I like what u do! Much love"
    expected_boundaries = [4, 63, 109]
    actual_boundaries = twtt.naive_sentence_boundaries(simple_tweet)
    self.assertEqual(actual_boundaries, expected_boundaries)

  def testAdjustBoundariesInQuotes(self):
    simple_tweet = "'Damn!' The grind is inspirational and saddening at the same time.  Don't want you to stop cuz I like what u do! Much love"
    expected_boundaries = [5, 63, 109]
    actual_boundaries = twtt.adjust_boundaries_in_quotes(tweet, [4, 63, 109])
    self.assertEqual(actual_boundaries, expected_boundaries)

  def testRemoveIncorrectPreemptiveBoundaries(self):
    simple_tweet = "Don't think thats the right name for Mr. Brooks."
    preemptive_boundaries = [39. 47]
    expected_boundaries = [47]
    self.assertEqual



if __name__ == '__main__':
  unittest.main(exit=False)

