import sys
import json

def hashtagFrequency(tweet_file):
    tweets = []
    frequency = {}
    for line in open(tweet_file, 'r'):
        tweets.append(json.loads(line))
    for tweet in tweets:
        if u'entities' in tweet:
            entities_value = tweet[u'entities']
            #print entities_value
            if 'hashtags' in entities_value:
                hashtag_list = entities_value[u'hashtags']
                for hashtag_obj in hashtag_list:
                    if u'text' not in hashtag_obj:
                        break
                    hashtag = hashtag_obj[u'text']
                    if hashtag in frequency:
                        frequency[hashtag] = frequency[hashtag] + 1
                    else:
                        frequency[hashtag] = 1
    return frequency

def main():
    count = 0
    hashtag_count = hashtagFrequency(sys.argv[1])
    for w in sorted(hashtag_count, key=hashtag_count.get, reverse=True):
        print w, hashtag_count[w]
        count += 1
        if count == 10:
            break
    #for key, value in hashtag_count.iteritems():
    #    print key, value

if __name__ == '__main__':
    main()
