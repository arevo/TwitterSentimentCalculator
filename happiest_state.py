import sys
import json
import warnings

def states_mapper(user_location):
    states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
    }
    for key, value in states.iteritems():
        if key in user_location:
            return key
        if value in user_location:
            return key
    return 'NaN'
    
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

def tweetsWithLocationInfo(tweets):
    valid_tweet = []
    state_key = u'state'
    for tweet in tweets:
        #tweet_coordinates = tweet['coordinates']
        #if tweet_coordinates:
        #    coordinate_key = 'coordinates'
        #    if coordinate_key in tweet_coordinates:
        #        fixes = tweet_coordinates[coordinate_key]
        #        longitude = fixes[0]
        #        latitude = fixes[1]
        #        location_address = geolocator.reverse(latitude, longitude)
        #        location_state = states_mapper(location_address)
        #        if location_state != 'NaN':
        #            tweet[state_key] = location_state
        #            valid_tweet.append(tweet)
        #            break
        user_key = u'user'
        if user_key in tweet:
            tweet_user = tweet[u'user']
            if tweet_user:
                location_key = u'location'
                if location_key in tweet_user:
                    if tweet_user[location_key]:
                        tweet_state = states_mapper(tweet_user[location_key])
                        #print 'Tweet state from user info: ', tweet_state
                        if tweet_state != 'NaN':
                            tweet[state_key] = tweet_state
                            valid_tweet.append(tweet)
                            break
        place_key = u'place'
        if place_key in tweet:
            tweet_place = tweet[u'place']
            if tweet_place:
                if tweet_place[u'country_code']:
                    if tweet_place[u'country_code']=='US':
                        tweet_state = states_mapper(tweet_place[u'full_name'])
                        #print 'Tweet state from place: ', tweet_state
                        if tweet_state != 'NaN':
                            tweet[state_key] = tweet_state
                            valid_tweet.append(tweet)
                            break

    for tweet in valid_tweet:
        if state_key not in tweet:
            print 'State key is missing'
    return valid_tweet

def calculateSentiment(valid_location_tweets, scores):
    state_sentiment_dict = {}
    for tweet in valid_location_tweets:
        tweet_text = tweet['text'].encode('utf-8')
        tweet_sentiment=0
        tweet_words = tweet_text.split()
        for word in tweet_words:
            if word in scores:
                tweet_sentiment += scores[word]
        state_key = u'state'
        tweet_location = tweet[state_key].encode('utf-8')
        if tweet_location:
            state_name = tweet_location
            if state_name in state_sentiment_dict:
                current_sentiment = state_sentiment_dict[state_name]
                state_sentiment_dict[state_name] = current_sentiment + tweet_sentiment
            else:
                state_sentiment_dict[state_name]=tweet_sentiment
    return state_sentiment_dict

def main():
    scores = generateScoreDict(sys.argv[1])
    all_tweets = readTweetData(sys.argv[2])
    valid_location_tweets = tweetsWithLocationInfo(all_tweets)
    state_sentiment_dict = calculateSentiment(valid_location_tweets, scores)
    max_sentiment = -1000
    happiest_state = 'NA'    
    for key, value in state_sentiment_dict.iteritems():
        #print key, value
        if value>=max_sentiment:
            happiest_state = key
            max_sentiment=value
    print happiest_state

if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    main()
