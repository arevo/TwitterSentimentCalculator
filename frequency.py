import sys
import json

def computeFrequency(tweet_file):
    tweets = []
    frequency = {}
    for line in open(tweet_file, 'r'):
        tweets.append(json.loads(line))
    for tweet in tweets:
        for key, value in tweet.iteritems():
            if key == 'text':
                tweet_text = value.encode('utf-8')
                tweet_words = tweet_text.split()
                for word in tweet_words:
                    if word in frequency:
                        frequency[word] = frequency[word] + 1
                    else:
                        frequency[word] = 1
    return frequency

def main():
    total_word_count = float(0)
    frequency = computeFrequency(sys.argv[1])
    for key, value in frequency.iteritems():
        total_word_count += value
    for key, value in frequency.iteritems():
        word_freq = value/total_word_count
        print key, word_freq
if __name__ == '__main__':
    main()
