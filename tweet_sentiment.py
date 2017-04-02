import sys
import json

def hw():
    print 'Hello, world!'

def generateScoreDict(sent_data):
    afinnfile = open(sent_data)
    scores = {}
    for line in afinnfile:
        term, score = line.split("\t")
        scores[term]=int(score)
    return scores

def readTweetData(tweet_file):
    tweets = []
    for line in open(tweet_file, 'r'):
        tweets.append(json.loads(line))
    return tweets

def lines(fp):
    print str(len(fp.readlines()))

def main():
    scores = generateScoreDict(sys.argv[1])
    tweets = readTweetData(sys.argv[2])
    for tweet in tweets:
        for key, value in tweet.iteritems():
            if key == "text":
                tweet_sentiment_score = 0
                tweet_text = value.encode('utf-8')
                tweet_words = tweet_text.split()
                for word in tweet_words:
                    if word in scores:
                        tweet_sentiment_score += scores[word]
                print tweet_sentiment_score
                #print tweet_text

if __name__ == '__main__':
    main()
