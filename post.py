import StringUtils as sUtil
import re
import post as p

class Post:
    def __init__(self, poster: str, timestamp: str, postNumber, content: str):
        self.poster = poster
        self.timestamp = timestamp
        self.postNumber = str(postNumber)
        self.content = content
        self.vote = self.findVote()
        self.cleanVotes()

    def quoteString(self, topicNumber):
        openQuote = "[quote=\""
        openQuote += self.poster
        openQuote += ", post:"
        openQuote += str(sUtil.cleanNumber(self.postNumber))
        openQuote += ", topic:"
        openQuote += topicNumber
        openQuote += "\"]"
        totalString = openQuote
        totalString += "\n" + sUtil.replaceAll(sUtil.replaceAll(self.content, "[/vote]", "[vote]"), "[/v]", "[v]")
        totalString += "[/quote]" + "\n"
        return sUtil.replaceAll(totalString, "\\n", "\n")

    def displayString(self):
        return self.poster + ", " + self.timestamp + ", " + self.postNumber + "\n" + sUtil.replaceAll(self.content, "\\n", "\n")
    
    #returns True if the post contains an unvote
    def findUnvote(self):
        unvoteTester = re.compile("\[unvote\].*\[/unvote\]", re.IGNORECASE)
        return unvoteTester.search(self.content)
    
    #given the content of a post, returns the substring that is a valid vote, or returns
    #None if no such substring exists
    #does not remove quotes/spoilers
    def getVoteString(self):
        voteFull = re.compile(r"\[vote\].*?\[/vote\]", re.IGNORECASE)
        voteFullMini = re.compile(r"\[v\].*?\[/v\]", re.IGNORECASE)
        fullMatch = voteFull.search(self.content)
        miniMatch = voteFullMini.search(self.content)
        actualVote = None
        if fullMatch != None:
            actualVote = fullMatch.group(0)
        elif miniMatch != None:
            actualVote = miniMatch.group(0)
        else:
            return None
        actualVote = actualVote[actualVote.find("]") + 1:len(actualVote)]
        actualVote = actualVote[0:actualVote.find("[")]
        return actualVote
    
    #returns the (un)vote in the post (ie the voted player); or None if no such vote exists
    def findVote(self):
        unvote = self.findUnvote()
        vote = self.getVoteString()
        if unvote != None:
            return "unvote"
        return vote

    #removes spaces and newlines from vote
    def cleanVotes(self):
        if self.vote != None:
            self.vote = sUtil.replaceAll(self.vote, " ", "")
            self.vote = sUtil.replaceAll(self.vote, r"\n", "")