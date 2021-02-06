#! /usr/bin/python3
import json
import random
import csv
import linecache
from faker import Faker


#INIT Faker / Rand
random.seed(random.randint(0,999))
Faker.seed(random.randint(0,999))
fake = Faker()


#Random ID
def rand_ID():
	id = 0
	for i in range(19):
		nb = random.randint(0,9)
		id = int(str(id) + str(nb))
	return str(id)


#Random Localisation
def rand_geo():
	file = open("US.tsv")
	num_lines = sum(1 for line in file)
	choice = random.randint(0,num_lines)
	file.close()

	line = linecache.getline("US.tsv",choice)
	tab_geo = line.split('\t')
	return tab_geo


#Func map space
def map_space(n):
	return " " + n


#Random Text
def rand_text_longlat():
	geo = rand_geo()
	coords = []
	coords.append(geo[4])
	coords.append(geo[5])

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


#Valid tweet
##
##
##


#Tweet to JSON
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

	json_obj = json.dumps(tweet_data, indent = 4)
	with open("fakeTweet.json","a+") as outfile:
		outfile.write(json_obj)



#MAIN()
for i in range(10):
	fake_tweet_creation()
