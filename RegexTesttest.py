import re

tweets = [r'snarf\n@snarfy_\n·\n1m\nexsqueeze me, lizard guy\n0:07\n1',r"mr. lizard\n@nikesonmytweet\n·\n1m\n“Black owned business” is what I was told\nQuote Tweet\nGigan\n@FriendlyNerd\n · 2m\nWait it's cool to clown them now? I thought Lavar was a genius? Didn't Jay-Z buy a bunch of his shoes? What gives guys? https://twitter.com/TheNBACentral/status/1230195817069383682…", r'@_MonaLizard\n·\n1m\nDon’t be calling me baby you dumb bitch', r'Never Beta Again Youngboy\n@Olive__Autist\n·\n2m\nReplying to \n@Polganghonkler\ndid u have a pet lizard as a kid', r'Lizard Grip\n@relativelycheap\n·\n2m\nReplying to \n@bigbabyblack\nhes already gone. i hope someone answered u', r"EzeeEP\n@Ezee_EP\n·\n2m\nReplying to \n@CardsnDerby\nWOW! I'll take a chicken tender sandwich, potato wedges,  slice of carrot cake and 1 green lizard (Heineken) plez.", r'lizard kween\n@lizardkween\n·\n2m\nthe bigger picture staring back at me', r"NullRhea\n@NullRhea\n·\n2m\nReplying to \n@scolopendaddy\nIf you didn't feed cigarette butts to your lizard he wouldn't be so aggressive come on"]

tweet_dict = {
    "name": re.compile(r'(?P<name>[a-zA-z0-9 _.]{,50})'), #Needs to find the FIRST one per line
    "username": re.compile(r'(?P<username>@[a-zA-Z_0-9]{,15})'),
    "text": re.compile(r'(?P<before>(\d(s|m|h|d))|(>@[a-zA-Z_0-9]{,15})|(and \d others))(?P<text>.{,280})'),
}

for i in tweets:
    for key, tweet in tweet_dict.items():
        match = tweet.search(i)
        match = match.group(0)
        if match:
            print(f"{key.upper()}: {match}")
        else:
            print (f"NO {key.upper()}")
    print("")

