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
    
def makeGamesList(gameList, humanGames):
    """Makes a list of games, with header image and title, for the iterable appids gameList"""
    imgsrc = """<img src = "app/%s_header.jpg" alt="%s" />"""
    gameRow = """<p>%s <br /> %s </p>"""
    rows = [gameRow % (imgsrc % (appid, humanGames[appid]), humanGames[appid]) for appid in gameList]
    return """<div class=gamesList> %s
</div>""" % "\n".join(rows)

def makePeopleChooser(userids, humanNames):
    from jinja2 import Template
    """Makes the HTML to select people, then view the common games"""
    peepLayout = """<li class="ui-state-default" id="%s">%s</li>"""
    peepAvatarImg = """<img src="avatar/%s.png" alt="%s" id="%s" width=70px height=70px/>"""
    people = [peepLayout % (uid, peepAvatarImg % (uid, humanNames[uid], uid)) for uid in userids]
    
    #open template, and fill it in
    with open("peepSelect.htm", "rb") as f:    
        t = Template(f.read())
    with open("peepSelect.html", "wb") as f:
        content = t.render({"box": "\n".join(people)})
        f.write(content.encode("utf8"))
    
def makeGameSortedListJinja(bygames, humanGames, humanNames):
    from jinja2 import Template
    with open("gameSortedTemplate.htm", "rb") as f:
        t = Template(f.read())
    mostCommonGamesDesc = sorted(bygames, key = lambda x: len(bygames[x]), reverse=True)
    
    
    #do the tabs header
    tabsHeaderLayout = """\t\t<li><a href="#tabs-%s">%s</a></li>"""
    tabsHeaderContentLayout = """<img src="app/%s_header.jpg" alt="%s" />"""
    tabsHeaderContent = [tabsHeaderContentLayout % (appid, humanGames[appid]) for appid in mostCommonGamesDesc]
    tabs = "\n".join([tabsHeaderLayout % (mostCommonGamesDesc[i], tabsHeaderContent[i]) for i in xrange(len(mostCommonGamesDesc))])
    
    #do each tabs content
    tabContentLayout = """\t\t<div id="tabs-%s">
\t\t\t<h2>%s</h2>
\t\t\t<p>%s</p>
\t\t</div>"""
    personRow = """<img src = "avatar/%s.png" width=50px height=50px />%s<br />"""
    tabContent = {appid: [personRow % (uid, humanNames[uid]) for uid in bygames[appid]] for appid in mostCommonGamesDesc}
    
    tabsContentCombined = "\n".join([tabContentLayout % (key, humanGames[key], "<br />\n".join(value)) for key, value in tabContent.iteritems()])
    
    
    
    
    
    with open("gameSorted.html", "wb") as f:
        content = t.render({"tabsContent":tabsContentCombined, "tabs": tabs})
        f.write(content.encode("utf8"))

    
    
    
    
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

