# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 23:01:53 2015

@author: jak

time to make html!
"""

def makeGameSortedList(bygames, humanGames, humanNames):
    gameRow = u"""\t<tr>
\t\t<td><img src = "app/%s" /></td>
\t\t<td>%s</td>
\t\t<td>%s</td>
\t</tr>"""
    peopleRow = """<img src = "avatar/%s.png" width=50px height=50px />%s<br />"""
    
    start = u"""<table>"""
    end = u"""</table>"""
    
    mostCommonGamesDesc = sorted(bygames, key = lambda x: len(bygames[x]), reverse=True)
    for appid in mostCommonGamesDesc:
        game = humanGames[appid]
        picture = str(appid) + "_header.jpg"
        people = {uid:humanNames[uid] for uid in bygames[appid]}        
        peopleSt = "\n".join([peopleRow % (uid, peep) for uid, peep in people.items()])
        start += gameRow % (picture, game, peopleSt)
    start += end
    return start
    
    
    
def makeHTMLPage(title, fname, fcn, *args):
    page = u"""<html>
<head>
\t<title>%s</title>
\t<style>
\t\ttable {border-collapse: collapse;}
 \t\ttr {
 \t\t\t   border: 1px solid black;
\t\t}
\t</style>
</head>
<body>
%s
</body>
</html>
"""
    with open(fname, "wb") as f:
        content = page % (title, fcn(*args))
        f.write(content.encode("utf8"))

