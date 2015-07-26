# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 20:31:14 2015

@author: Jak
"""

import pprint
import sys

import os
import itertools
import json

import requests

import makeHTML

with open("STEAMAPI.txt", "rb") as f:
    STEAMKEY = f.read().rstrip("\n").lstrip(" ")

appListRaw = requests.get("http://api.steampowered.com/ISteamApps/GetAppList/v0001/").json()
appList = appListRaw["applist"]["apps"]["app"]
#convert into a dict of {id: name}
apps = {x["appid"]: x["name"] for x in appList}

#read userids from a file
with open("userids.txt", "rb") as f:
    userids =  list(f)
userids = [uid.rstrip("\n") for uid in userids]



def humanGame(appid):
    return apps[appid]

def humanGamesInCommon(group):
    return [humanGame(appid) for appid in group]

url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=%s&steamid=%s&format=json"

def getGamesInfo(userids):
    """Gets a list of users games, with game count and time played
    userids = [strid1, strid2]
    peopleData = {id: {games_count: number, games: [g1, g2]}}
        where g1 = {appid: #, playtime_forever: #}
    """
    
    peopleData = {}
    for userid in userids:
        d = requests.get(url %(STEAMKEY, userid))
        peopleData[userid] = d.json()["response"]
    return peopleData
    
def getGameSet(gamesInfo):
    """From GamesInfo, returns a set of game appids"""
    return set([x["appid"] for x in gamesInfo["games"]])    
    
def getUserData(userids):
    url =  "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%s&format=json"
    if len(userids) < 100:
        #steam can fetch up to 100 userid peoples stuff at once
        uid = ",".join(userids)
        d = requests.get(url %(STEAMKEY, uid))
        #players is a list of data, with order corresponding to the userids input
        players = d.json()["response"]["players"]
        playerData = {i["steamid"]: i for i in players}
        return playerData
    else:
        raise "d"
        
def getPlayerDataThatICareAbout(playerData):
    data = {}
    data["name"] = playerData["personaname"]
    data["avatar"] = playerData["avatarfull"]
    return data

#pprint.pprint([humanGame(x["appid"]) for x in userGames])

def downloadAvatars(playerData):
    """Downloads player avatars, saves as ID.png
    playerData = {id: {"avatar": url, "name": name}}
    """
    for key in playerData.keys():
        response = requests.get(playerData[key]["avatar"])
        if response.status_code == 200:
            #"200 OK" -- it worked.
            with open("avatar" + os.sep + key + ".png", "wb") as f:
                f.write(response.content)
                
                
def downloadGameHeader(appid, size="largest"):
    """Downloads the header image/logo for a game, based on appid.
    Uses steam's CDN, not the steam api
    """
    sizeIndex = {"largest" : "header.jpg", "large": "header_292x136.jpg"}
    urlbase = "http://cdn.akamai.steamstatic.com/steam/apps/%s/%s"
    response = requests.get(urlbase % (appid, sizeIndex[size]))
    if response.status_code == 200:
        #it worked
        with open("app" + os.sep + str(appid) + "_" + sizeIndex[size], "wb") as f:
            f.write(response.content)
    
    



if __name__ == "__main__":
    #get information about each players games
    playerData = getUserData(userids)
    data = {x: getPlayerDataThatICareAbout(playerData[x]) for x in playerData}    #downloadAvatars(data)
    humanNames = {x: data[x]["name"] for x in data.keys()}
    #downloadAvatars(data)

    peopleGameInfo = getGamesInfo(userids)
    setsOfGames = {key: getGameSet(peopleGameInfo[key]) for key in peopleGameInfo.keys()}

    #find all combinations of more than 1 player
    combsOverall = set()
    for maxNum in xrange(2, len(userids)+1):
        combinations = itertools.combinations(userids, maxNum)
        flattened = set(combinations)
        combsOverall = combsOverall.union(flattened)
    #find the games in common for each combination of players 
    gamesInCommon = {}
    for s in combsOverall:
        key = ",".join(s)
        gameSets = [setsOfGames[x] for x in s]
        gamesInCommon[key] = gameSets[0].intersection(*gameSets[1:])
    #humanReadableGames = {x: humanGamesInCommon(gamesInCommon[x]) for x in gamesInCommon.keys()}
    #humanReadable = {",".join([humanNames[uid] for uid in x.split(",")]): humanReadableGames[x] for x in humanReadableGames.keys()}

    #Make the select people -> games in common page
    
    #Write the games in common for each combination

    index = {}
    ind = 0
    for comb, gameList in gamesInCommon.iteritems():
        comb = [int(uid) for uid in comb.split(",")]
        comb.sort()
        comb = ",".join([str(uid) for uid in comb])
        with open(os.path.join("combs", str(ind) + ".html"), "wb") as f:
            if len(gameList) > 0:
                f.write(makeHTML.makeGamesList(gameList, apps))
            else:
                f.write("No games in common")
        index[comb] = ind
        ind += 1
    with open("combs" + os.sep + "index.json", "wb") as indexFile:
        json.dump(index, indexFile)
        
    #make the GUI front-end
    makeHTML.makePeopleChooser(userids, humanNames)



    #find what people in common each game has
    peopleInCommon = {}
    for uid in setsOfGames.keys():
        for appid in setsOfGames[uid]:
            try:
                peopleInCommon[appid].append(uid)
            except KeyError:
                peopleInCommon[appid] = [uid]
    #pprint.pprint(peopleInCommon)
        
    makeHTML.makeHTMLPage("GameSorted", "gsorted.html", makeHTML.makeGameSortedList, peopleInCommon, apps, humanNames)
    #makeHTML.makeGameSortedListJinja(peopleInCommon, apps, humanNames)
    
    

        
        
        
    
        
        
    #total games - every unique game between all userids
    #totalGames = set()
    #for userid in userids:
    #    totalGames = totalGames.union(setsOfGames[userid])
    #for game in totalGames:
    #    downloadGameHeader(game)
    
    


