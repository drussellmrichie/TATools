"""
Russell Richie
github.com/drussellmrichie
drussellmrichie@gmail.com

A super quick and dirty implementation of the Cohort Model of word recognition, devised
by William Marslen-Wilson. For example:

http://psycholinguistics.wikifoundry.com/page/The+Cohort+Model+of+Word+Recognition
"""

def cohortModel(word, EnglishWords):
    if len(EnglishWords) < 30:
        print ("Our lexicon is", EnglishWords)
    soFar = ''                                 # when we start, we haven't heard anything yet, so we'll represent that as an empty string
    candidates = list(EnglishWords)            # we'll start by assuming all the words we know are possible
    for letter in word:                        # then start listening to the word letter by letter
        soFar += letter                        # add the newly heard letter to the portion of the word heard so far
        for word in list(candidates):          # now look through the candidate words
            if not word.startswith(soFar):     # if the word seen so far is NOT consistent with a word we know
                candidates.remove(word)        # remove the word from the candidates
        print("These are the possible words when we've heard '{}' so far:\n{}".format(str(soFar),str(candidates)))
    print("After hearing everything, the only possible word(s) are {}".format(candidates))
    return candidates

def main():
	"""
	Test the cohort model with a fragment of English
	"""
	EnglishWords = ['cathedral', 'cat','dog','catheter']
	word = 'cathedral'
	cohortModel(word, EnglishWords)
	
if __name__ == '__main__':
	main()