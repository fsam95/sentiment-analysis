import re
# [I, me, my, mine, we, us, our, ours]
# First person pronouns: PRP (I, me)
# PRP$ (my)
# TODO: match uppercase
def feat1(tweet):
  matches = re.findall(r"\b(I|me|my|mine|we|us|our|ours)/", tweet, flags=re.IGNORECASE)
  return len(matches)


# Second person pronouns: [you, your, yours, u, ur, urs]
def feat2(tweet):
  matches = re.findall(r"\b(you|your|yours|u|ur|urs)/", tweet, flags=re.IGNORECASE)
  return len(matches)

# Third person: [he, him, his, she, her, hers, it, its, they, them, their, theirs]
def feat3(tweet):
  matches = re.findall(r"\b(he|him|his|she|her|hers|it|its|they|them|their|theirs)/", tweet, flags=re.IGNORECASE)
  return len(matches)

# Coordinating conjunctions
def feat4(tweet):
  matches = re.findall(r"/CC", tweet)
  return len(matches)

def feat5(tweet): 
  matches = re.findall(r"/VBD", tweet)
  return len(matches)

def feat6(tweet):
  matches = re.findall(r"('ll|will|gonna|going/VBG\sto/TO\s\w+/VB)", tweet, flags=re.IGNORECASE) 
  return len(matches)

def feat7(tweet):
  matches = re.findall(r",/,", tweet)
  return len(matches)

def feat8(tweet):
  matches = re.findall(r"(;/;|:/:)", tweet)
  return len(matches)

def feat9(tweet):
  matches = re.findall(r"-/-", tweet)



if __name__ == '__main__':
  # buildarff.py train.twt train.arff
  # buildarff.py test.twt some.arff 50
  if len(sys.argv) == 4:
    max_tweets = sys.argv[3]
    
  with open(sys.argv[1], 'rb') as preprocessed_set:
    data = preprocessed_set.read()
    tweets = re.split(r"<A=\d>", data)[1:]

#  for tweet in tweets:

