#! /usr/bin/python3
import json
import random
import csv
import sys
import linecache
from faker import Faker


# INIT Faker / Rand
random.seed(random.randint(0,999))
Faker.seed(random.randint(0,999))
fake = Faker()


# Random ID
def rand_ID():
	id = 0
	for i in range(19):
		nb = random.randint(0,9)
		id = int(str(id) + str(nb))
	return str(id)


# Random Localisation
def rand_geo():
	file = open("US.tsv")
	num_lines = sum(1 for line in file)
	choice = random.randint(0,num_lines)
	file.close()

	line = linecache.getline("US.tsv",choice)
	tab_geo = line.split('\t')
	return tab_geo


# Func map space
def map_space(n):
	return " " + n


# Random Text
def rand_text_longlat():
	geo = rand_geo()
	coords = []
	coords.append(geo[9])
	coords.append(geo[10])

	connecteur = ["at", "near to", "on", "placed at", "situated at", "in", "appearing in", "next to", "close to", "around", "located in"]
	hashtag = ["Avalanche","Cataclysm","Catastrophe","Cyclones","Earthquakes","Eruption","Extreme Precipitation","Flood","Flooding","Floodwater","Hailstorm","Hurricanes","Landfall","Landslides","Lava","Mudslide","Seismic Wave","Snowstorm","Storm","Tidal Wave","Tornado","Tropical Cyclone","Tropical Storm","Tsunamis","Twitster","Typhoon","Volcanic ","Volcanic Eruptions","Volcanoes","Wildfires","Wind Wave"]

	rand_c = random.choice(connecteur) + " " + geo[2]
	rand_h = '#' + random.choice(hashtag)

	text_array = [fake.sentence(), fake.sentence(), fake.sentence(), rand_h, rand_c]
	random.shuffle(text_array)
	text_map_array = map(map_space, text_array)
	text_join = ''.join(text_map_array)
	text = text_join[1:]

	return [text, geo[2], coords]


##
##
## Valid tweet
##
##


# Tweet to JSON
def fake_tweet_creation():
	infos = rand_text_longlat()
	tweet_data = {
		"author_id": rand_ID(),
		"geo": infos[2],
		"id": rand_ID(),
		"place": "NULL",
		"place_user": infos[1],
		"real": "False",
		"text": infos[0],
		"valid": "?"
	}
	return tweet_data;

# Main
def main():
	if(len(sys.argv) != 2):
		print("Passez en argument le nombre de FakeTweet à générer")
	else:
		x = int(sys.argv[1])
		if(x < 0):
			print("Passez en argument un nombre positif")
		else:
			tweet_list = []
			for i in range(x):
				tweet_list.append(fake_tweet_creation())

			json_obj = json.dumps(tweet_list, indent = 4)
			with open("fakeTweet.json","w") as outfile:
				outfile.write(json_obj)

if __name__ == "__main__":
    main()
