import os
import json
import getpass
print(getpass.getuser())
with open("/home/terl3/www/site/disastweet/python/oui.json", "w") as outfile:
    json.dump("tweet", outfile)
print("test")