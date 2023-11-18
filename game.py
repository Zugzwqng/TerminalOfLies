import urllib
import StringUtils as sUtil
import time
import post as p
import pyperclip
import csv

@staticmethod
def fromCSV(filename: str):
    csvfile = open(filename, 'r')
    csvreader = csv.reader(csvfile, delimiter=",")
    link = None
    aliases = dict()
    alignments = dict()
    currentChoice = 0
    for line in csvreader:
        if line == []:
            pass
        elif line == ["---------"]:
            currentChoice += 1
        elif currentChoice == 0:
            link = line[0]
        elif currentChoice == 1:
            aliases.update([line])
        elif currentChoice == 2:
            alignments.update([line])
    gameObject = Game(link)
    gameObject.aliases = aliases
    gameObject.alignments = alignments
    gameObject.csvName = filename
    return gameObject


class Game:
    def __init__(self, link):
        self.csvName = None
        self.link = self.getLinkToFirstPost(link)
        self.topicNumber = self.getTopicNumber(link)
        self.players = set()
        self.playersCaseFixer = dict()
        self.aliases = dict()
        self.alignments = dict()
        self.posts = self.initializePosts(self.topicNumber)

    def playerExists(self, player):
        player = player.lower()
        return self.players.issuperset([player])

    def aliasExists(self, alias: str):
        alias = alias.lower()
        return self.aliases.get(alias) != None

    def addAlias(self, player, alias):
        alias = alias.lower()
        player = player.lower()
        if alias != "unvote":
            self.aliases.update([(alias, player)])
            if self.csvName != None:
                self.toCSV(self.csvName)
    
    def addAlignment(self, player, alignment):
        player = player.lower()
        alignment = alignment.lower()
        self.alignments.update([(player, alignment)])
        if self.csvName != None:
                self.toCSV(self.csvName)

    def removeAlias(self, alias):
        alias = alias.lower()
        self.aliases.pop(alias)
        if self.csvName != None:
                self.toCSV(self.csvName)

    def resolveSubstringAlias(self, name):
        matchingNames = []
        for player in self.players:
            if player.lower().find(name.lower()) != -1:
                matchingNames.append(player)
        if len(matchingNames) == 1:
            return matchingNames[0]
        else:
            raise Exception("Multiple players matched this substring!")

    def getPlayerlist(self):
        return self.players
    
    def printAliases(self):
        for alias in self.aliases:
            print(f"Alias: {alias} -- Player: {self.aliases.get(alias)}")

    def printAlignments(self):
        for player in self.alignments:
            print(f"Player: {player} -- Alignment: {self.alignments.get(player)}")
    

    #This method removes posts entirely if they do not contain "#" (since this is the postnumber every real post has this) and removes some "b'"s
    #this must be used while posts are a single string
    #this method is also the one that resolves the escape characters - if there's an escape character not being resolved, it must be added here
    #(yes this is a jank workaround)
    def cleanStringPost(self, post):
        post = sUtil.replaceAll(post, "\\xe2\\x80\\x94", "—")
        post = sUtil.replaceAll(post, "\\xe2\\x80\\x99", "’")
        post = sUtil.replaceAll(post, "\\'", "'")
        if post.find("#") !=  -1:
            startingOffset = 0
            if post[0:2] == "b'":
                startingOffset = 2
            return (post[startingOffset:])
        return None
    
    #given the link of the thread, returns the topic number.
    def getTopicNumber(self, gameLink):
        discard, remainder, discard2 = sUtil.splitOnce(gameLink, "fortressoflies.com/t/")
        discard, remainder, discard2 = sUtil.splitOnce(remainder, "/")
        result, discard, discard2 = sUtil.splitOnce(remainder, "/")
        return result

    #given the link of the thread, returns the link to the first post.
    def getLinkToFirstPost(self, gameLink):
        topicNumber = self.getTopicNumber(gameLink)
        baseLinkMinusTopicNumber, discard, discard2 = sUtil.splitOnce(gameLink, "/" + topicNumber)
        return baseLinkMinusTopicNumber + "/" + topicNumber + "/"

    #given the pagenumber and the base raw link, returns the content on that page.
    def getPage(self, pageNumber, link):
        f = urllib.request.urlopen(link + "?page=" + str(pageNumber))
        myfile = str(f.read())
        if (myfile == "b''"):
            return ""
        return myfile
    
    #returns the starting post array and the topic number
    def initializePosts(self, topicNumber):
        postStrings = []
        link = "https://www.fortressoflies.com/raw/" + topicNumber
        page = 1
        while(True):
            nextPageOfPosts = self.getPage(page, link)
            if nextPageOfPosts == "":
                break
            postStrings = postStrings + nextPageOfPosts.split("\\n\\n-------------------------\\n\\n")
            print(f"Accessed posts {(page * 100) - 99} to {(page * 100) + 1}")
            page += 1
            if (page % 40 == 0):
                print("Pausing for some time to avoid too many requests.")
                time.sleep(5)

        result = []
        for postString in postStrings:
            stringPost = self.cleanStringPost(postString)
            if stringPost == None:
                continue
            toBeAdded, remainder, discard = sUtil.splitOnce(stringPost, " | ")
            poster = toBeAdded
            toBeAdded, remainder, discard = sUtil.splitOnce(remainder, " | #")
            timestamp = toBeAdded
            toBeAdded, remainder, discard = sUtil.splitOnce(remainder, "\\n\\n")
            postNumber = str(sUtil.cleanNumber(toBeAdded))
            content = remainder

            self.players.add(poster.lower())
            self.playersCaseFixer.update([(poster.lower(), poster)])
            result.append(p.Post(poster, timestamp, postNumber, content))
        return result
    
    #returns all posts by input players, displays/outputs if applicable
    def multiISO(self, doDisplay=False, copyQuotes=False, copyLinks=False):
        players = []
        while(True):
            player = input("Individually enter the name of each player you want to ISO. Enter -1 to stop. ").lower()
            if player == "-1":
                break
            players.append(player)
        filteredPosts = []
        for post in self.posts:
            if post.poster.lower() in players:
                filteredPosts.append(post)
        self.outputPosts(filteredPosts, doDisplay, copyQuotes, copyLinks)
        return filteredPosts
    

    #this method should output the posts. if copyQuotes is true, all posts have their
    #quotes copied to the clipboard. if copyLinks is true, all posts have their links copied to the clipboard.
    #if doDisplay is true, posts are also displayed
    def outputPosts(self, posts, doDisplay=True, copyQuotes=False, copyLinks=False):
        if doDisplay:
            for post in posts:
                print(post.displayString() + "\n")
        if copyQuotes:
            toBeCopied = ""
            for post in posts:
                toBeCopied += post.quoteString(self.topicNumber)
            try:
                pyperclip.copy(toBeCopied)
            except:
                print("Clipboard access is not working...")
        if copyLinks:
            toBeCopied = ""
            for post in posts:
                toBeCopied = toBeCopied + self.link + post.postNumber + "\n"
            try:
                pyperclip.copy(toBeCopied)
            except:
                print("Clipboard access is not working...")
    
    #returns all votes, in a list
    #a vote is in the format [votingPlayer, votingPlayerAlignment, votedPlayer, votedPlayerAlignment, postNumber]
    def getAllVotes(self):
        votes = []
        for post in self.posts:
            if post.vote != None:
                votingPlayer = post.poster #always the actual username, so never a need to do aliases
                votingPlayerAlignment = self.alignments.get(votingPlayer.lower(), "q")
                votedPlayer = self.aliases.get(post.vote.lower(), post.vote.lower())
                try:
                    votedPlayer = self.resolveSubstringAlias(votedPlayer)
                except:
                    pass
                votedPlayer = self.playersCaseFixer.get(votedPlayer, votedPlayer)
                votedPlayerAlignment = self.alignments.get(votedPlayer.lower(), "q")
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
            if (votingPlayers == None or vote[0] in votingPlayers) and (votingPlayerAlignments == None or vote[1] in votingPlayerAlignments) and (votedPlayers == None or vote[2] in votedPlayers) and (votedPlayersAlignment == None or vote[3] in votedPlayersAlignment):
                filteredVotes.append(vote)
        return filteredVotes

    def toCSV(self, filename: str):
        csvfile = open(filename, 'w')
        csvwriter = csv.writer(csvfile, delimiter=",")
        csvwriter.writerow([self.link])
        csvwriter.writerow(["---------"])
        for alias in self.aliases:
            csvwriter.writerow([alias, self.aliases.get(alias)])
        csvwriter.writerow(["---------"])
        for player in self.alignments:
            csvwriter.writerow([player, self.alignments.get(player)])
        csvfile.close()
    
    

        

            
        


