import sys
import json

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def generateScoreDict(sent_data):
    afinnfile = open(sent_data)
    scores = {}
    for line in afinnfile:
        term, score = line.split("\t")
        scores[term] = int(score)
    return scores

def readTweetData(tweet_file):
    tweets = []
    for line in open(tweet_file, 'r'):
        tweets.append(json.loads(line))
    return tweets

def main():
    scores = generateScoreDict(sys.argv[1])
    tweets = readTweetData(sys.argv[2])
    for tweet in tweets:
        for key, value in tweet.iteritems():
            if key == 'text':
                word_sentiment_score = {}
                tweet_sentiment_score = float(0)
                tweet_text = value.encode('utf-8')
                tweet_words = tweet_text.split()
                word_count = 0
                for word in tweet_words:
                    word_count += 1
                    if word in scores:
                        tweet_sentiment_score += scores[word]
                for word in tweet_words:
                    if word in scores:
                        word_sentiment_score[word] = float(scores[word])
                    else:
                        #print word, tweet_sentiment_score, word_count
                        non_sentiment_value = tweet_sentiment_score/word_count
                        word_sentiment_score[word] = non_sentiment_value
                for key, value in word_sentiment_score.iteritems():
                    print key, value 
                     
if __name__ == '__main__':
    main()
