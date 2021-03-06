#region Imports
import time
import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from pymongo import MongoClient
from datetime import datetime
#endregion

#region Initialisation
LogDir = "./Source Code/Logs/"

lstTrackingFor = ["migrants", "migration crisis",  "migration flow",  "refugees",  "#RefugeeCrisis",
                                "#refugeesGr",  "#refugeeswelcome",  "#WelcomeRefugees",  "#ProMuslimRefugees",
                                "asylum seekers",  "human rights",  "#helpiscoming",  "solidarity",
                                "#solidaritywithrefugees",  "Balkan route",  "irregular migrants",  "borders",
                                "open borders",  "border closure",  "border share",  "No borders",  "#OpentheBorders",
                                "Syria",  "Iraq",  "Afghanistan",  "Pakistan",  "islamists",  "ISIS",  "daesh",
                                "muslims",  "Idomeni",  "Calais",  "Lesbos",  "Lesvos",  "Lesbosisland",
                                "migrant camps",  "refugee camps",  "#safepassage",  "rapefugees",  "#antireport ",
                                "Aylan",  "European Mobilisation",  "Amnesty International",  "Frontex",  "UNHCR",
                                "UN Refugee Agency",  "#FortressEurope",  "@MovingEurope"]

MongoDBCon = MongoClient() #Lack of arguments defaults to localhost:27017
MongoDBDatabase = MongoDBCon['RefugeeCrisisCon']
RawTweetsJSON_coll = MongoDBDatabase['RawTweetsJSON']

#We need the consumer key, consumer secret, access token, access secret.
ckey = "ro4d6rvefo412pnYxNV3Xb5ej"
csecret = "H5f9qKWMZuW5Re4NgE2m9ODDNe6XfqmmOg68C46bY2Ro6fCwWN"
atoken = "1211288082-kE6J6vqU1dzf9KHBEY3uC4wDg0zzrOZc4hA067N"
asecret = "quZJdlpEUGlQUwe4m9oZr7GVImDx16OuXptADBh6wXzWu"
#endregion

#region Listener
#Creating the Listener with the actual steps implementation in it
class listener(StreamListener):

    #Defining what to do when data become available
    def on_data(self, data):

        try:
            all_data = json.loads(data)
            #Inserting them to the MongoDB database
            result = RawTweetsJSON_coll.insert_one(all_data)  #The Full JSON format

            try:
                print(all_data["text"])
            except Exception as ex:
                print ("Error on printing the tweet: ", str(ex))

            return True

        #in case internet drops or something, let's not stop the whole procedure
        except BaseException as e:
            print ('failed with error: ', str(e))
            saveFile = open(LogDir + 'Streaming_Listener_Problems.txt', 'a')
            eMessage = 'Time of Error: ' + str(datetime.now()) + '\n' + str(e) + '\n\n'
            saveFile.write(eMessage)
            saveFile.close()
            time.sleep(0.5)

    #Defining what to do in case of an error
    def on_error(self, status):
        print ("on_error: " + str(status))

#endregion

#region Main
try:
    #Authenticating ourselves for the API
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    twitterStream = Stream(auth, listener())

except Exception as e:
    print (str(e))
    saveFile = open(LogDir + 'Streaming_APIAuthenticating_Problems.txt', 'a')
    eMessage = 'Time of Error: ' + str(datetime.now()) + '\n' + str(e) + '\n\n'
    saveFile.write(eMessage)
    saveFile.close()

while True:
    try:
        twitterStream.filter(languages=["en"], track = lstTrackingFor)
    except Exception as e:
        print (str(e))

        saveFile = open(LogDir + 'Streaming_Main_Problems.txt', 'a')
        eMessage = 'Time of Error: ' + str(datetime.now()) + '\n' + str(e) + '\n\n'
        saveFile.write(eMessage)
        saveFile.close()
        continue
#endregion