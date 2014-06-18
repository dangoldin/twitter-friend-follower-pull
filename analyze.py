import tweepy, time

from config import CONSUMER_KEY, CONSUMER_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth)

already_processed = set()
to_process = list()

def get_followers(api, user):
    c = tweepy.Cursor(api.followers_ids, id=user).items()
    followers = []
    while True:
        try:
            f = c.next()
            followers.append( f )
        except tweepy.TweepError:
            print 'Sleeping for 15 min'
            time.sleep(60 * 15)
            continue
        except StopIteration:
            break
    print 'Retrieved', len(followers), 'followers for', user
    return followers

def get_friends(api, user):
    c = tweepy.Cursor(api.friends_ids, id=user).items()
    friends = []
    while True:
        try:
            f = c.next()
            friends.append( f )
        except tweepy.TweepError:
            print 'Sleeping for 15 min'
            time.sleep(60 * 15)
            continue
        except StopIteration:
            break
    print 'Retrieved', len(friends), 'friends for', user
    return friends

to_process.append('dangoldin')

while len(to_process) > 0:
    user = to_process.pop()
    if user not in already_processed:
        print 'Retrieving data for user', user
        followers = get_followers(api, user)
        friends = get_friends(api, user)
        with open('followers-%s.txt' % str(user), 'w') as f:
            f.write("\n".join(str(f) for f in followers))
        with open('friends-%s.txt' % str(user), 'w') as f:
            f.write("\n".join(str(f) for f in friends))
        to_process.extend(followers)
        to_process.extend(friends)
    already_processed.add(user)
