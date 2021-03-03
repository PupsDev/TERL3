from database import Database

# with data
db = Database("saisir l'uri ici. sans oublier de mettre le fichier TLS")

# with json file
db.select_database("disastweet")

db.select_collection("test")

db._insert("testdata/get_tweets_with_fields.json")

found = db.find_from_collection()

db.print_found(found)