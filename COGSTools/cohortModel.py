"""
Russell Richie
https://github.com/drussellmrichie
drussellmrichie@gmail.com

A super quick and dirty implementation of the Cohort Model of word recognition, devised
by William Marslen-Wilson. For example:

http://psycholinguistics.wikifoundry.com/page/The+Cohort+Model+of+Word+Recognition

This was written to be readable with minimal Python knowledge. Hence no example is defined
in a `def main()` chunk, nor is there a `if __name__ == "__main__" chunk at the end.

How might you, clever reader, modify this model? What about human word recognition seems
missing here?
"""

def cohortModel(word, EnglishWords):
    print ("Our lexicon is", EnglishWords)
    soFar = ''                                 # when we start listening to a word, we of course haven't heard anything yet, so we'll represent that as an empty string
    candidates = list(EnglishWords)            # we'll start by assuming all the words we know are possible
    for letter in word:                        # then start listening to the word letter by letter
        soFar = soFar + letter                 # add the newly heard letter to the portion of the word heard so far
        for word in list(candidates):          # now look through the candidate words
            if not word.startswith(soFar):     # if the word seen so far is NOT consistent with a word we know
                candidates.remove(word)        # remove the word from the candidates
        print("When we've heard '{}' so far, the canddiates are:\n{}".format(soFar,candidates))
    print("After hearing everything, the only possible word(s): {}".format(candidates))
    return candidates

# Test the cohort model with a fragment of English
EnglishWords = ['cathedral', 'cat','dog','catheter']
word = 'cathedral'
cohortModel(word, EnglishWords)