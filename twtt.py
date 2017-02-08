import HTMLParser
import csv
import re

"""
Regex url taken from http://flanders.co.nz/2009/11/08/a-good-url-regular-expression-repost/
"""
def strip_char_codes(tweet):
  h = HTMLParser.HTMLParser()
  return h.unescape(tweet)

def replace_html_tags(tweet):
  return re.sub(r"/<[^>]+>/", "", tweet)

def remove_urls(tweet):
  url_regex = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
  return re.sub(url_regex, "", tweet) 

def remove_hash_and_at(tweet):
  removed_hash = re.sub(r"#", "", tweet)
  return re.sub(r"@", "", removed_hash)

"""
Cases:  '.' Used for an abbreviation and the next word starts with a capital: use abbrev.english (probably the hardest case)
        '.' Used for an abbreivation and the next word does NOT start with a capital (easy to detect)
        Ending with ? or !
"""
# TODO: Break this into separate cases
     
def remove_abbreviation_boundaries(tweet, boundaries): 
  # TODO: Figure out how to decalre aabbrevs as global variables
  new_boundaries = []
  for boundary_index in boundaries:
    preceding_word = find_preceding_word(tweet, boundary_index)
    if preceding_word in abbrevs_followed_by_cap:
      if tweet[boundary_index + 2].isupper():
        continue
    elif preceding_word in abbrevs_followed_by_lower:
      if tweet[boundary_index + 2].islower():
        continue
    new_boundaries.append(boundary_index)
  return new_boundaries

def add_sentence_boundary(tweet):

  sentence_boundaries = naive_sentence_boundaries(tweet)

  sentence_boundaries = adjust_boundaries_in_quotes(tweet, sentence_boundaries)

  # Watching out for Titles (e.g Dr. and stuff)
  new_sentence_boundaries = []
  for boundary_index in sentence_boundaries:     
    # find the preceding word
    preceding_word = find_preceding_word(tweet, boundary)
    if preceding_word in abbrevs_followed_by_cap:
      # Need to check if the next word is capitalized
      if tweet[boundary_index + 2].isupper():
        continue #don't add it to new_sentence_boundaries # don't add it to new_sentence_boundaries because it follows form Mr. Sir
    elif preceding_word in abbrevs_followed_by_lower:
      if tweet[boundary_index + 2].islower():
        continue #don't add it to new_sentence_boundaries because it follows form: i.e. something something
    new_sentence_boundaries.append(boundary_index)  

  # Check if ellipses or multiple exclamations
  for i in range(0, len(new_sentence_boundaries)):
    if tweet[new_sentence_boundaries[i] + 1] == '!': # !!
      incrementor = 1
      while tweet[new_sentence_boundaries[i] + incrementor] == '!':
        incrementor = incrementor + 1
      new_sentence_boundaries[i] = incrementor - 1
    elif tweet[new_sentence_boundaries[i] + 1] == '.': # ....
      incrementor = 1
      while tweet[new_sentence_boundaries[i] + incrementor] == '.':
        incrementor = incrementor + 1
      new_sentence_boundaries[i] = incrementor - 1
   
  # Construct tweet where every sentence is on newline
  newlined_string = ""
  i = 0
  while i != len(tweet):
    if new_sentence_boundaries != [] or i == new_sentence_boundaries[0]:
      newlined_string += ".\n"
      i += 1
      new_sentence_boundaries = new_sentence_boundaries[1:]
    else: 
      newlined_string = tweet[count]

def find_preceding_word(tweet, boundary):
  preceding_word = ""
  i = boundary - 1
  while i != -1 and tweet[i] != " ":
    preceding_word = tweet[i] + preceding_word
    i -= 1
  return preceding_word

def naive_sentence_boundaries(tweet):
  sentence_boundaries = []
  for i in range(0, len(tweet)): # putative sentence boundaries
    if tweet[i] == "." or tweet[i] == "!" or tweet[i] == "!":
      sentence_boundaries.append(i)
  return sentence_boundaries

def adjust_boundaries_in_quotes(tweet, sentence_boundaries):
  for i in range(0, len(sentence_boundaries)): # ending at quote
    if tweet[sentence_boundaries[i] + 1] == "'":
      sentence_boundaries[i] = sentence_boundaries[i] + 1
  return sentence_boundaries
   
def place_newline_on_boundaries(tweet, boundaries):
  newlined_string = ""
  i = 0
  while i != len(tweet):
    if boundaries != [] and i == boundaries[0]:
      newlined_string += tweet[i]
      newlined_string += "\n"
      boundaries = boundaries[1:]
    else: 
      newlined_string += tweet[i]
    i += 1
  return newlined_string

def space_every_token(tweet):
  spaced_tweet = ""
  for char in tweet: 
    if char == "'":
      spaced_tweet += " '"
    if tweet == ".":
      return
      # Check if ellipse 

if __name__ == '__main__':  
  with open(sys.argv[1], 'rb') as training_set: 
    training_set_reader = csv.reader(training_set)
    for row in training_set_reader:
      tweet = row[5]

  # TODO: fix this up 
  abbrevs_followed_by_cap = [] # e.g Mr. Sir
  abbrevs_followed_by_lower = [] # e.g e.g. 
  with open('abbrev.english', 'rb') as abbrevs:

    for line in abbrevs:
      if line[0].isupper():
        abbrevs_followed_by_cap.append(line.strip("."))
      else: 
        abbrevs_followed_by_lower.append(line.strip("."))
