import StringUtils as sUtil
import post as p
import read
import reads_list
import reads_list_list

import urllib
import urllib.request
import time
import pyperclip
import csv
import json


@staticmethod
def decode_readslistlist(dct):
    if "reads_lists" in dct:
        result = reads_list_list.ReadsListList()
        result.reads_lists = dct["reads_lists"]
        return result
    elif "miscthoughts" in dct:
        result = reads_list.ReadsList()
        result.reads = dct["reads"]
        result.miscthoughts = dct["miscthoughts"]
        return result
    elif "player" in dct:
        result = read.Read(dct["player"], dct["tier"], dct["thoughts"])
        return result
    else:
        return dct


def readslistlist_encoder(obj):
    if isinstance(obj, reads_list_list.ReadsListList):
        return {"reads_lists": obj.reads_lists}
    elif isinstance(obj, reads_list.ReadsList):
        return {"reads" : obj.reads, "miscthoughts" : obj.miscthoughts}
    elif isinstance(obj, read.Read):
        return {"player" : obj.player, "tier" : obj.tier, "thoughts" : obj.thoughts}
    else:
        raise TypeError(f"Object of type {type(obj)} is not serializiable.")


@staticmethod
def fromFiles(filenameCSV: str, filenameJSON: str, includePosts=True):
    """
    Given a filename of a csv file, and the filename of a json file,
    returns a Game from the data stored in those files.
    This game is linked to the csv file, so that changes to the Game are immediately reflected there.
    The json however is not linked; you must call saveJSON() to update it.
    """
    csvfile = open(filenameCSV, 'r')
    csvreader = csv.reader(csvfile, delimiter=",")
    links = []
    aliases = dict()
    alignments = dict()
    defaultAlignment = 'u'
    for line in csvreader:
        if line == []:
            pass
        elif line[0] == "link":
            links.append(line[1])
        elif line[0] == "alias":
            aliases.update([(line[1], line[2])])
        elif line[0] == "alignment":
            alignments.update([(line[1], line[2])])
        elif line[0] == "removeAlias":
            aliases.pop(line[1])
        elif line[0] == "defaultAlignment":
            defaultAlignment = line[1]
        elif line[0] == "clearAlignments":
            alignments = dict()
            defaultAlignment = 'u'
        elif line[0] == "unlink":
            try:
                links.remove(line[1])
            except:
                print("Something strange has occured while restoring the game; this should never happen (unless you have messed with the files). Hopefully nothing has broken...")
    gameObject = Game(links[0], getPosts=includePosts)
    for num in range(1, len(links)):
        gameObject.addLink(links[num])
        print("Pausing for some time to avoid too many requests")
        time.sleep(5)
    gameObject.aliases = aliases
    gameObject.alignments = alignments
    gameObject.defaultAlignment = defaultAlignment
    gameObject.csvName = filenameCSV
    gameObject.jsonName = filenameJSON
    #BEGIN potentially buggy code
    fixedAliases = dict() #This is aliases, but with aliases removed if they reference a player not in the playerlist, which can 
    #happen when links get removed.
    for alias in gameObject.aliases:
        if gameObject.playerExists(gameObject.resolveAlias(alias)):
            fixedAliases[alias] = gameObject.aliases[alias]
    gameObject.aliases = fixedAliases
    #END potentially buggy code

    try:
        readsFile = open(filenameJSON, "r")
    except:
        readsFile = open(filenameJSON, "w")
        readsFile.close()
        time.sleep(1)
        readsFile = open(filenameJSON, "r")
    try:
        gameObject.readslistlist = json.load(readsFile, object_hook=decode_readslistlist)
    except:
        pass
    gameObject.toCSV(gameObject.csvName)
    return gameObject


class Game:
    """
        This class represents a Mafia Game.
        csvName is the name of the csv this Game is stored in.
        link is the URL of the game.
        topicNumber is the topic number, as a string.
        players is all accounts who have posted in the thread 
            (this includes taking actions such as locking); all players in this list are lowercase.
        playersCaseFixer is a dictionary that maps lowercase playernames to their proper casing.
        aliases is a dictionary, supplied by the user, that maps nicknames/aliases onto their players (both are made lowercase).
    """
    def __init__(self, link, getPosts=True):
        self.csvName = None
        self.jsonName = None
        self.links = [self.getLinkToFirstPost(link)]
        self.topicNumbers = [self.getTopicNumber(link)]
        self.players = set()
        self.playersCaseFixer = dict()
        self.aliases = dict()
        self.alignments = dict()
        self.defaultAlignment = 'u'
        self.readslistlist = reads_list_list.ReadsListList()
        if getPosts:
            self.posts = self.initializePosts(self.topicNumbers[0], self.links[0])
        else:
            try:
                self.getPage(1, "https://www.fortressoflies.com/raw/" + self.topicNumbers[0], recoverFromError=False)
            except:
                raise Exception

    def clearAlignments(self):
        self.alignments = dict()
        self.defaultAlignment = "u"
        if self.csvName != None:
            csvfile = open(self.csvName, 'a')
            csvwriter = csv.writer(csvfile, delimiter=",")
            csvwriter.writerow(["clearAlignments"])


    def changeDefaultAlignment(self, newDefault: str) -> bool:
        newDefault = newDefault.lower()
        possibleAlignments = ['u', 'h', 't', 'n', 'm']
        if newDefault not in possibleAlignments:
            return False
        self.defaultAlignment = newDefault
        if self.csvName != None:
            csvfile = open(self.csvName, 'a')
            csvwriter = csv.writer(csvfile, delimiter=",")
            csvwriter.writerow(["defaultAlignment", newDefault])
        return True

    #returns all posts that pass the filter
    #filter must be a function that returns True for all desired posts
    def filterPosts(self, filter) -> list[p.Post]:
        filteredPosts = []
        for post in self.posts:
            if filter(post):
                filteredPosts.append(post)
        return filteredPosts
    
    def getAlignment(self, player: str) -> str:
        player = player.lower()
        player = self.resolveAlias(player)
        try:
            return self.alignments.get(player, None).upper()
        except:
            return self.defaultAlignment

    def linkValid(self, link: str) -> bool:
        """
        Returns True iff the provided link is a valid link to a game. This is tested through trying to access the link,
        so if there is no internet, the link will be deemed invalid.
        """
        try:
            self.getPage(1, "https://www.fortressoflies.com/raw/" + self.getTopicNumber(link), recoverFromError=False)
            return True
        except:
            return False

    def addLink(self, newLink: str):
        newLink = self.getLinkToFirstPost(newLink)
        self.links.append(newLink)
        newTopicNumber = self.getTopicNumber(newLink)
        self.topicNumbers.append(newTopicNumber)
        self.posts = self.posts + self.initializePosts(newTopicNumber, newLink)
        if self.csvName != None:
            csvfile = open(self.csvName, 'a')
            csvwriter = csv.writer(csvfile, delimiter=",")
            csvwriter.writerow(["link", newLink])


    def removeLink(self, index: int) -> bool:
        if index < 0 or index >= len(self.links) or len(self.links) == 1:
            return False
        linkToRemove = self.links.pop(index)
        if self.csvName != None:
            csvfile = open(self.csvName, 'a')
            csvwriter = csv.writer(csvfile, delimiter=",")
            csvwriter.writerow(["unlink", linkToRemove])
        return True


    
    def resolveAlias(self, name: str, implictAliases=False) -> str:
        """
        Resolves the input name to the corresponding player. If implicitAliases is set to
        True, also resolve by unique substrings, even if the user has not defined these aliases.
        """
        if not implictAliases:
            return self.aliases.get(name, name)
        
        possibleName = self.aliases.get(name, None)
        if possibleName != None:
            return possibleName
        try:
            return self.resolveSubstringAlias(name)
        except:
            return name

    def playerExists(self, player: str) -> bool:
        try:
            player = player.lower()
            return self.players.issuperset([player])
        except:
            return False

    def aliasExists(self, alias: str) -> bool:
        alias = alias.lower()
        return self.aliases.get(alias) != None

    def addAlias(self, player: str, alias: str) -> None:
        alias = alias.lower()
        player = player.lower()
        if alias != "unvote":
            self.aliases.update([(alias, player)])
            if self.csvName != None:
                csvfile = open(self.csvName, 'a')
                csvwriter = csv.writer(csvfile, delimiter=",")
                csvwriter.writerow(["alias", alias, player])
    
    def addAlignment(self, player: str, alignment: str) -> None:
        player = player.lower()
        alignment = alignment.lower()
        self.alignments.update([(player, alignment)])
        if self.csvName != None:
                csvfile = open(self.csvName, 'a')
                csvwriter = csv.writer(csvfile, delimiter=",")
                csvwriter.writerow(["alignment", player, alignment])
    
    def removeAlias(self, alias: str):
        alias = alias.lower()
        self.aliases.pop(alias)
        if self.csvName != None:
                csvfile = open(self.csvName, 'a')
                csvwriter = csv.writer(csvfile, delimiter=",")
                csvwriter.writerow(["removeAlias", alias])

    def resolveSubstringAlias(self, name):
        matchingNames = []
        for player in self.players:
            if player.lower().find(name.lower()) != -1:
                matchingNames.append(player)
        if len(matchingNames) == 1:
            return matchingNames[0]
        else:
            raise Exception("Zero or multiple players matched this substring!")

    def getPlayerlist(self):
        return self.players
    
    def printAliases(self):
        for alias in self.aliases:
            print(f"Alias: {alias} -- Player: {self.aliases.get(alias)}")

    def printAlignments(self):
        for player in self.alignments:
            print(f"Player: {player} -- Alignment: {self.alignments.get(player)}")
    
    #given the link of the thread, returns the topic number.
    def getTopicNumber(self, gameLink) -> str:
        remainder, discard, discard2 = sUtil.splitOnce(gameLink, "#")
        discard, remainder, discard2 = sUtil.splitOnce(remainder, "fortressoflies.com/t/")
        discard, remainder, discard2 = sUtil.splitOnce(remainder, "/")
        result, discard, discard2 = sUtil.splitOnce(remainder, "/")
        result, discard, discard2 = sUtil.splitOnce(result, "?")
        return result

    #given the link of the thread, returns the link to the first post.
    def getLinkToFirstPost(self, gameLink) -> str:
        topicNumber = self.getTopicNumber(gameLink)
        baseLinkMinusTopicNumber, discard, discard2 = sUtil.splitOnce(gameLink, "/" + topicNumber)
        return baseLinkMinusTopicNumber + "/" + topicNumber + "/"

    #given the pagenumber and the base raw link, returns the content on that page.
    def getPage(self, pageNumber, link, recoverFromError=True):
        try:
            f = urllib.request.urlopen(link + "?page=" + str(pageNumber))
        except Exception:
            if recoverFromError:
                restart = input("There has been an error fetching this link. If you'd like to continue, enter 'y'. Enter anything else to quit (and crash): ").lower() == 'y'
                if not restart:
                    raise
                else:
                    print("Resumed.")
                    return self.getPage(pageNumber, link, recoverFromError=True)
            else:
                raise
        return str(f.read(), 'utf-8')
    
    def getFirstPoster(self, playersInQuestion: list[str], doAliases=False, implicitAliases=False) -> str | None:
        if doAliases:
            playersInQuestion = list(map(lambda player : self.resolveAlias(player, implictAliases=implicitAliases), playersInQuestion))
        for post in self.posts:
            for player in playersInQuestion:
                if post.poster.lower() == player.lower():
                    return player
        return None
            

    #returns the starting post array and the topic number
    def initializePosts(self, topicNumber: str, linkToFirstPost: str, setPlayers=True) -> list[p.Post]:
        postStrings = []
        link = "https://www.fortressoflies.com/raw/" + topicNumber
        page = 1
        while(True):
            nextPageOfPosts = self.getPage(page, link)
            if nextPageOfPosts == "":
                break
            postStrings = postStrings + nextPageOfPosts.split("\n\n-------------------------\n\n")
            print(f"Accessed posts {(page * 100) - 99} to {(page * 100) + 1}")
            page += 1
            if (page % 40 == 0):
                print("Pausing for some time to avoid too many requests.")
                time.sleep(5)

        result = []
        for postString in postStrings:
            assert type(postString) == str
            if postString.find("#") ==  -1:
                continue
            toBeAdded, remainder, discard = sUtil.splitOnce(postString, " | ")
            poster = toBeAdded
            toBeAdded, remainder, discard = sUtil.splitOnce(remainder, " | #")
            timestamp = toBeAdded
            toBeAdded, remainder, discard = sUtil.splitOnce(remainder, "\n\n")
            postNumber = str(sUtil.cleanNumber(toBeAdded))
            content = remainder

            self.players.add(poster.lower())
            self.playersCaseFixer.update([(poster.lower(), poster)])
            
            result.append(p.Post(poster, timestamp, postNumber, content, topicNumber, linkToFirstPost))
        return result
    
    # #returns all posts by input players, displays/outputs if applicable
    # def multiISO(self, doDisplay=False, copyQuotes=False, copyLinks=False):
    #     players = []
    #     while(True):
    #         player = input("Individually enter the name of each player you want to ISO. Enter -1 to stop. ").lower()
    #         if player == "-1":
    #             break
    #         player = self.resolveAlias(player, implictAliases=True)
    #         players.append(player)
    #     filteredPosts = []
    #     for post in self.posts:
    #         if post.poster.lower() in players:
    #             filteredPosts.append(post)
    #     self.outputPosts(filteredPosts, doDisplay, copyQuotes, copyLinks)
    #     return filteredPosts
    
    def multiISO_good_oop(self, players: list[str], copyQuotes=True) -> bool:
        """
        This function copies all posts made by specified players.

        If copyQutoes is True, then quotes of the posts are copied. If copyQuotes is False, then
        links to the posts are copied.

        Returns True if copying was successful, and False otherwise.
        """
        filteredPosts = []
        for post in self.posts:
            if post.poster.lower() in players:
                filteredPosts.append(post)
        return self.outputPosts(filteredPosts, doDisplay=False, copyQuotes=copyQuotes, copyLinks=not copyQuotes)


    #this method should output the posts. if copyQuotes is true, all posts have their
    #quotes copied to the clipboard. if copyLinks is true, all posts have their links copied to the clipboard.
    #if doDisplay is true, posts are also displayed
    def outputPosts(self, posts: list[p.Post], doDisplay=True, copyQuotes=False, copyLinks=False) -> bool:
        if doDisplay:
            for post in posts:
                print(post.displayString() + "\n")
        if copyQuotes:
            toBeCopied = ""
            for post in posts:
                toBeCopied += post.quoteString()
            try:
                pyperclip.copy(toBeCopied)
            except:
                print("Clipboard access is not working...")
                return False
        if copyLinks:
            toBeCopied = ""
            for post in posts:
                toBeCopied = toBeCopied + post.linkToFirstPost + post.postNumber + "\n"
            try:
                pyperclip.copy(toBeCopied)
            except:
                print("Clipboard access is not working...")
                return False
        return True
    
    def getCertainPosts(self, posters: list[str]) -> list[p.Post]:
        """
        Returns all posts by people in the provided list of posters. Aliases are not applied.
        """
        result = []
        posters = list(map(lambda string : string.lower(), posters))
        for post in self.posts:
            if post.poster.lower() in posters:
                result.append(post)
        return result

    def getAllVotes(self) -> list[list[str]]:
        """
        Returns all votes, in a list
        A vote is in the format [votingPlayer, votingPlayerAlignment, votedPlayer, votedPlayerAlignment, postNumber]
        """
        votes = []
        for post in self.posts:
            if post.vote != None:
                votingPlayer = post.poster #always the actual username, so never a need to do aliases
                votingPlayerAlignment = self.getAlignment(votingPlayer)
                votedPlayer = self.resolveAlias(post.vote.lower(), implictAliases=True)
                votedPlayer = self.playersCaseFixer.get(votedPlayer, votedPlayer)
                votedPlayerAlignment = self.getAlignment(votedPlayer)
                postNumber = post.postNumber
                votes.append([votingPlayer, votingPlayerAlignment, votedPlayer, votedPlayerAlignment, postNumber])
        return votes
    
    def getCertainVotes(self, votingPlayers=None, votingPlayerAlignments=None, votedPlayers=None, votedPlayersAlignment=None):
        votes = self.getAllVotes()
        if votingPlayers != None:
            for num in range(len(votingPlayers)):
                votingPlayers[num] = self.aliases.get(votingPlayers[num], votingPlayers[num])
        if votedPlayers != None:
            for num in range(len(votedPlayers)):
                votedPlayers[num] = self.aliases.get(votedPlayers[num], votedPlayers[num])
        filteredVotes = []
        for vote in votes:
            if (votingPlayers == None or vote[0].lower() in votingPlayers) and (votingPlayerAlignments == None or vote[1] in votingPlayerAlignments) and (votedPlayers == None or vote[2].lower() in votedPlayers) and (votedPlayersAlignment == None or vote[3] in votedPlayersAlignment):
                filteredVotes.append(vote)
        return filteredVotes

    def getCertainVotesNew(self, votingPlayers: list[str], votedPlayers: list[str], requiredSatisfaction: int):
        """
        Returns all votes that satisfy at least requiredSatisfaction specified properties.

        Properties:
        Being in votingPlayers
        Being in votedPlayers
        
        """
        votes = self.getAllVotes()
        votingPlayers = list(map(lambda player : self.resolveAlias(player), votingPlayers))
        votedPlayers = list(map(lambda player : self.resolveAlias(player), votedPlayers))
        filteredVotes = []
        for vote in votes:
            complies_count = 0
            complies_count += 1 if (vote[0].lower() in votingPlayers) else 0
            complies_count += 1 if (vote[2].lower() in votedPlayers) else 0
            if complies_count >= requiredSatisfaction:
                filteredVotes.append(vote)
        return filteredVotes


    def toCSV(self, filename: str):
        csvfile = open(filename, 'w')
        csvwriter = csv.writer(csvfile, delimiter=",")
        for link in self.links:
            csvwriter.writerow(["link", link])
        for alias in self.aliases:
            csvwriter.writerow(["alias", alias, self.aliases.get(alias)])
        for player in self.alignments:
            csvwriter.writerow(["alignment", player, self.alignments.get(player)])
        csvwriter.writerow(["defaultAlignment", self.defaultAlignment])
        # for read in self.reads:
        #     csvwriter.writerow(["read", read, self.reads.get(read)])
        # for thought in self.thoughts:
        #     csvwriter.writerow(["thought", thought])
        csvfile.close()

    def saveJSON(self):
        if self.jsonName == None:
            raise Exception("JSON name does not exist, but this object has been told to save itself to a JSON file.")
        jsonfile = open(self.jsonName, "w")
        json.dump(self.readslistlist, jsonfile, default=readslistlist_encoder, indent=4)
     
    def countOccurances(self, string, ignoreCase=True):
        total = 0
        for post in self.posts:
            total += post.stringCount(string, ignoreCase=ignoreCase)
        return total
    

    def getReadsListList(self):
        return self.readslistlist
        

            
        


