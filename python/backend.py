from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from wrapper import Api
import json
import os
import sys
import pymongo

hostName = "localhost"
serverPort = 8080
class MyServer(BaseHTTPRequestHandler):

    def do_POST(self):
        # récupération des données
        content_length = int(self.headers['Content-Length'])
        json_post = json.loads(self.rfile.read(content_length));
        
        # Execution de l'extraction
        client = pymongo.MongoClient(json_post["db_url"]) #connexion
        db = client["disastweet"] #selection de la bdd
        collection = db.spacetweets #selection de la collection

        api = Api(json_post["bearer_token"], True)
        tweet_fields = "expansions=geo.place_id&tweet.fields=geo,entities,author_id"
        max_results = 50
        max_pages = int(json_post["max_pages"])
        search = json_post["keyword"]

        query = search+"&max_results="+str(max_results)
        response = api.get_yielded_recent_search(query,tweet_fields,max_pages)
        #envoie de la réussite de connexion
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        #traitement
        for tweets in response:
            try:
                collection.insert_many(tweets) #insertion multiple
            except Exception as e:
                print(e)
            
            
        #envoie de la fin de traitement. rencontre un Timed Out
        self.wfile.write(bytes('{"reussite" : true}', "utf-8"))
if __name__ == "__main__":        
    webServer = ThreadingHTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
