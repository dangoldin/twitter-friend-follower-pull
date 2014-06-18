import tweepy, time, sys, argparse

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Analyze Twitter friends and followers""")
    parser.add_argument('-u', type=str, dest='username', default='', help='Username')
    parser.add_argument('-d', type=int, dest='depth', default=1, help='Depth')
    parser.add_argument('-no-followers', action='store_false', dest='followers', default=True)
    parser.add_argument('-no-friends', action='store_false', dest='friends', default=True)
    args = parser.parse_args()

    max_depth = args.depth
    username  = args.username

    print 'Retrieving data for',username,'with max depth',max_depth

    to_process.append((username,max_depth))

    while len(to_process) > 0:
        user, depth = to_process.pop()
        if user not in already_processed:
            print 'Retrieving data for user', user
            followers = []
            friends = []
            if args.followers:
                followers = get_followers(api, user)
                with open('followers-%s.txt' % str(user), 'w') as f:
                    f.write("\n".join(str(f) for f in followers))
            if args.friends:
                friends = get_friends(api, user)
                with open('friends-%s.txt' % str(user), 'w') as f:
                    f.write("\n".join(str(f) for f in friends))
            if depth > 0:
                to_process.extend((f,depth-1) for f in followers)
                to_process.extend((f,depth-1) for f in friends)
        already_processed.add(user)
