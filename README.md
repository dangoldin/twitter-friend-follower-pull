twitter-friend-follower-pull
============================

Retrieve friends and followers for a starting user going 2 levels deep (friends of followers, etc)

To use:

1. Install the requirements file: "pip install -r requirements.txt"

2. Enter your credentials into the config.py file

3. Run analyze.py with the starting username: "python analyze.py -u username -d depth"

4. Optional options include "-no-followers" and "-no-friends" (ie "python analyze.py -u username -d depth -no-friends" will only pull folowers)