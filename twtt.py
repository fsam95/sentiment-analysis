import HTMLParser
import NLPlib
import csv
import re
import sys

"""
Regex url taken from http://flanders.co.nz/2009/11/08/a-good-url-regular-expression-repost/
"""
# Replace html tags; Step 1
def twtt1(tweet):
  return re.sub(r"/<[^>]+>/", "", tweet)

# Character codes are removed; Step 2
def twtt2(tweet):
  h = HTMLParser.HTMLParser()
  return h.unescape(tweet)

# URLs removed; Step 3
def twtt3(tweet):
  url_regex = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
  return re.sub(url_regex, "", tweet) 

# Remove # and @; Step 4
def twtt4(tweet):
  removed_hash = re.sub(r"#", "", tweet)
  return re.sub(r"@", "", removed_hash)

# Put each step on a new line; Step 5
def twtt5(tweet):
  tweet = re.sub(r"\s+", " ", tweet)
  # Tagging all '.' and '!'
  sentence_boundaries = naive_sentence_boundaries(tweet)
  sentence_boundaries = adjust_boundaries_in_quotes(tweet, sentence_boundaries)
  # Watching out for Titles (e.g Dr.) 
  sentence_boundaries = remove_abbreviation_boundaries(tweet, sentence_boundaries)
  # Check if ellipses or multiple exclamations
  final_boundaries = adjust_multiple_punctuation(tweet, sentence_boundaries)
  return put_newlines_on_boundaries(tweet, final_boundaries)

def twtt7(tweet):
  return space_tokens(tweet)

def twtt8(tweet):
  return tag_tokens(tweet)

#TODO: twtt9

def remove_abbreviation_boundaries(tweet, boundaries): 
  # Load abbreviations
  abbrevs_followed_by_cap = [] # e.g Mr. Sir
  abbrevs_followed_by_lower = [] # e.g e.g. 
  with open('abbrev.english', 'rb') as abbrevs:

    for line in abbrevs:
      if line[0].isupper():
        abbrevs_followed_by_cap.append(line.strip(".\n"))
      else: 
        abbrevs_followed_by_lower.append(line.strip(".\n"))

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

def adjust_multiple_punctuation(tweet, boundaries):
  new_boundaries = []
  remove = []
  for i in range(0, len(boundaries)):
    if boundaries[i] != len(tweet) - 1 and tweet[boundaries[i]] == "!" and tweet[boundaries[i] + 1] == "!":
      remove.append(boundaries[i])
    if boundaries[i] != len(tweet) - 1 and tweet[boundaries[i]] == "." and tweet[boundaries[i] + 1] == ".":
      remove.append(boundaries[i])
  for i in range(len(boundaries)):
    if boundaries[i] not in remove:
      new_boundaries.append(boundaries[i])
  return new_boundaries

def put_newlines_on_boundaries(tweet, boundaries):
  # Construct tweet where every sentence is on newline
  newlined_string = ""
  i = 0
  while i < len(tweet):
    if boundaries != [] and i == boundaries[0]:
      newlined_string += tweet[i]
      newlined_string += "\n"
      i += 2
      boundaries = boundaries[1:]
    else: 
      newlined_string += tweet[i]
      i += 1
  return newlined_string

#TODO: DO NOT SPACE ELIPSES
def space_tokens(tweet):
  #####
  spaced_periods_tweet  = re.sub(r"(?P<periods>\.*\.\n)", " \g<periods> ", tweet)
  spaced_exclaims_tweet = re.sub(r"(?P<exclaims>(!)*!\n)", " \g<exclaims> ", spaced_periods_tweet)
  spaced_colons_tweet = re.sub(r":", " :", spaced_exclaims_tweet)
  spaced_semicolons_tweet = re.sub(r";", " ;", spaced_colons_tweet)
  spaced_commas_tweet = re.sub(r",", " ,", spaced_semicolons_tweet)
  return re.sub(r"(?P<clitic>(n't|'))", " \g<clitic>", re.sub(r"( )+", " ", spaced_commas_tweet))

  #######
  #
    
  # for char in tweet:
  #  if char == "." or char == "!":
#  spaced_tweet = ""
#  for i in range(len(tweet) - 1):
#    spaced_tweet += tweet[i]
#    if tweet[i + 1] == "." or tweet[i + 1] == "!" or tweet[i + 1] == "," or tweet[i+1] == ";" or tweet[i+1] == ":":
#      spaced_tweet += " "
#    if i < len(tweet) - 2 and tweet[i+2] == "'" and tweet[i+1] == "n": #don't becomes do n't 
#      spaced_tweet += " "
#    if tweet[i+1] == "'" and tweet[i] != "n": # dogs' becomes dogs '
#      spaced_tweet += " "
#  if tweet[len(tweet) - 1] == "."or tweet[len(tweet) - 1] == "!":
#    spaced_tweet += " "
#  spaced_tweet += tweet[len(tweet) - 1]
#  return spaced_tweet


def tag_tokens(spaced_tweet):
  print spaced_tweet
  #tagger = NLPlib.NLPlib()
  removed_newlines = spaced_tweet.replace("\n", "")
  tags = tagger.tag(removed_newlines.split(" "))

  tagged_spaced_tweet = ""
  for i in range(len(spaced_tweet)):
    if spaced_tweet[i] == "\n" and tags != []:
      tagged_spaced_tweet += "/"
      tagged_spaced_tweet += tags[0]
      tags = tags[1:]
    if spaced_tweet[i] == " " and spaced_tweet[i-1] != "\n" and tags != []:
      tagged_spaced_tweet += "/"
      tagged_spaced_tweet += tags[0]
      tags = tags[1:]
    tagged_spaced_tweet += spaced_tweet[i]
    if i == len(spaced_tweet) - 1 and tags != []:
      tagged_spaced_tweet += "/"
      tagged_spaced_tweet += tags[0]
  return tagged_spaced_tweet

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
    if sentence_boundaries[i] + 1 < len(tweet) - 1 and tweet[sentence_boundaries[i] + 1] == "'":
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

def process(tweet):
  proc_1 = twtt1(tweet)
  proc_2 = twtt2(proc_1)
  proc_3 = twtt3(proc_2)
  proc_4 = twtt4(proc_3)
  proc_5 = twtt5(proc_4)
  proc_7 = twtt7(proc_5)
  proc_8 = twtt8(proc_7)
  return proc_8

if __name__ == '__main__':  
  tagger = NLPlib.NLPlib()
  count = 0
  stunum = sys.argv[2]
  outfile_name = sys.argv[3]
  outfile = open(outfile_name, 'w')
  with open(sys.argv[1], 'rb') as training_set: 
    training_set_reader = csv.reader(training_set)
    for row in training_set_reader:
      count += 1
      polarity = row[0]
      tweet = row[5]
      preprocessed_tweet = "<A={}>\n".format(polarity) + process(tweet) + "\n"
      outfile.write(preprocessed_tweet)
      if count > 1:
        break

