# Terminal of Lies, version 1.0, 10/7/2023
# By Zugzwang (crystqllized on Discord)
# Inspired by TodaysStory

import urllib.request
import pyperclip
import re
import time
import colorama
from colorama import Fore, Style, init
init(convert=True)
from sys import stdout

#post format: Player, Time, PostNum, Content

#given the link of the thread, returns the topic number.
def getTopicNumber(gameLink):
  discard, remainder = splitOnce(gameLink, "fortressoflies.com/t/")
  discard, remainder = splitOnce(remainder, "/")
  result, discard = splitOnce(remainder, "/")
  return result

#given the link of the thread, returns the link to the first post.
def getLinkToFirstPost(gameLink):
  topicNumber = getTopicNumber(gameLink)
  baseLinkMinusTopicNumber, discard = splitOnce(gameLink, "/" + topicNumber)
  return baseLinkMinusTopicNumber + "/" + topicNumber + "/"

#given the pagenumber and the base raw link, returns the content on that page.
def getPage(pageNumber, link):
  f = urllib.request.urlopen(link + "?page=" + str(pageNumber))
  myfile = str(f.read())
  if (myfile == "b''"):
    return ""
  return myfile

#This method removes posts entirely if they do not contain "#" (since this is the postnumber every real post has this) and removes some "b'"s
#this must be used while posts are a single string
#this method is also the one that resolves the escape characters - if there's an escape character not being resolved, it must be added here
#(yes this is a jank workaround)
def cleanPosts(posts):
  newPosts = []
  for post in posts:
    post = replaceAll(post, "\\xe2\\x80\\x94", "—")
    post = replaceAll(post, "\\xe2\\x80\\x99", "’")
    post = replaceAll(post, "\\'", "'")
    if post.find("#") !=  -1:
      startingOffset = 0
      if post[0:2] == "b'":
        startingOffset = 2
      newPosts.append(post[startingOffset:])
  return newPosts

#splits the string, but only into two parts. uses the first instance of delimiter
def splitOnce(mainString, delimiter):
  if mainString.find(delimiter) == -1:
    return mainString, ""
  delimiterIndex = mainString.find(delimiter)
  return mainString[0:delimiterIndex], mainString[delimiterIndex + len(delimiter):]

#returns mainString, but with all occurences of toSearchFor substituted with toReplaceWith
def replaceAll(mainString, toSearchFor, toReplaceWith):
  while(True):
    start, end = splitOnce(mainString, toSearchFor)
    if end == "":
      return mainString
    mainString = start + toReplaceWith + end

#This method takes in a post that is a string with poster, time, postnumber, and content, and splits these parts into 4 elements of an array
def basePostToArray(post):
  splitPost = []
  toBeAdded, remainder = splitOnce(post, " | ")
  splitPost.append(toBeAdded)
  toBeAdded, remainder = splitOnce(remainder, " | #")
  splitPost.append(toBeAdded)
  toBeAdded, remainder = splitOnce(remainder, "\\n\\n")
  splitPost.append(toBeAdded)
  splitPost.append(remainder)
  return splitPost

#Applies basePostToArray to every post
def postsToArray(posts):
  result = []
  for post in posts:
    result.append(basePostToArray(post))
  return result

#returns the starting post array and the topic number
def initializePosts(topicNumber):
  posts = []
  link = "https://www.fortressoflies.com/raw/" + topicNumber
  page = 1
  while(True):
    nextPageOfPosts = getPage(page, link)
    if nextPageOfPosts == "":
      break
    #print(nextPageOfPosts)
    posts = posts + nextPageOfPosts.split("\\n\\n-------------------------\\n\\n")
    print("Completed page: " + str(page))
    page += 1
    if (page % 40 == 0):
      print("Pausing for some time to avoid too many requests.")
      time.sleep(5)

  posts = cleanPosts(posts)
  posts = postsToArray(posts)
  return posts

#--------------------above this line should likely not need to be changed for new features.

#given a string, returns the section of the string that ^[0-9]* matches
#ie if there's a number at the start followed by non-numeric characters, returns the number
def cleanNumber(numString):
  for num in range(1, len(numString) + 1):
    try:
      test = int(numString[0:num])
    except:
      return int(numString[0:num - 1])
  return int(numString)

#returns all posts by input players, and an array of post numbers
def multiISO(posts):
  players = []
  while(True):
    player = input("Individually enter the name of each player you want to ISO. Enter -1 to stop. ").lower()
    if player == "-1":
      break
    players.append(player)
  filteredPosts = []
  postNums = []
  for post in posts:
    if post[0].lower() in players:
      filteredPosts.append(post)
      postNums.append(int(cleanNumber(post[2])))
  return filteredPosts, postNums


#returns the post in a string format, and displays the post if doDisplay is True
def outputPost(post, doDisplay):
  result = ""
  toDisplay = post[0] + ", " + post[1] + ", " + post[2] + "\n"
  content = post[3]
  lines = content.split("\\n")
  for line in lines:
    toDisplay = toDisplay + line + "\n"
    result = result + line + "\n"
  if doDisplay:
    print(toDisplay)
  return result

#this method should output the posts. if copyQuotes is true, all posts have their
#quotes copied to the clipboard. if copyLinks is true, all posts have their links copied to the clipboard.
#if doDisplay is true, posts are also displayed
def outputPosts(posts, topicNumber, gameThreadURL, doDisplay, copyQuotes, copyLinks):
  if doDisplay:
    for post in posts:
      outputPost(post, True)
  if copyQuotes:
    toBeCopied = ""
    for post in posts:
      quoteString = "[quote=\""
      quoteString = quoteString + post[0]
      quoteString = quoteString + ", post:"
      quoteString = quoteString + str(cleanNumber(post[2]))
      quoteString = quoteString + ", topic:"
      quoteString = quoteString + topicNumber
      quoteString = quoteString + "\"]"
      toBeCopied = toBeCopied + quoteString
      #toBeCopied = toBeCopied + str( +  + ", post:" + str(cleanNumber(post[2])), ", topic:" + topicNumber + "\"]")
      toBeCopied += "\n" + outputPost(post, False)
      toBeCopied += "[/quote]" + "\n"
    try:
      pyperclip.copy(toBeCopied)
    except:
      print("Clipboard access is not working...")
  if copyLinks:
    toBeCopied = ""
    link = getLinkToFirstPost(gameThreadURL)
    print(link)
    for post in posts:
      toBeCopied = toBeCopied + link + post[2] + "\n"
    try:
      pyperclip.copy(toBeCopied)
    except:
      print("Clipboard access is not working...")


def displayLinks(postNums, gameThreadURL):
  for num in postNums:
    print(gameThreadURL + "/" + str(num))

#returns an array with each player name in it
def getPlayerlist(posts):
  result = []
  for post in posts:
    if post[0] not in result:
      result.append(post[0])
  return result

def duplicateNewlines(string):
  newString = ""
  for char in string:
    if char == "\n":
      newString += char
    newString += char
  return newString

def removeQuotes(content):
  #quoteRegex = re.compile(r"\n ? ? ?\[quote[^\n\]]*\] *\n.*\n ? ? ?\[/quote\] *\n", re.IGNORECASE or re.DOTALL) #if using multiple flags worked like this then this would work
  #however it does not seem to work, so I am using a janky workaround where I manually make it ignore case
  quoteRegex = re.compile(r"\n ? ? ?\[[Qq][Uu][Oo][Tt][Ee][^\n\]]*\] *\n.*\n ? ? ?\[/[Qq][Uu][Oo][Tt][Ee]\] *\n", re.DOTALL)
  quoteEnd = re.compile(r"\n ? ? ?\[/quote\] *\n", re.IGNORECASE)
  if(quoteRegex.search(content) == None):
    return content
  contentBeforeQuoteEnd = content[0:quoteEnd.search(content).span()[1]]

  previousBeginIndex = 0
  beginIndex = 0
  previousQuote = None
  while(True):
    newQuote = quoteRegex.search(contentBeforeQuoteEnd[beginIndex:])
    if newQuote == None:
      break
    previousQuote = newQuote
    previousBeginIndex = beginIndex
    beginIndex = beginIndex + newQuote.span()[0] + 1

  before = content[0:previousBeginIndex + previousQuote.span()[0]]
  after = content[previousBeginIndex + previousQuote.span()[1]:]
  return removeQuotes(before + after)


#given the content of a post, returns the substring that is a valid vote, or returns
#None if no such substring exists
#does not remove quotes/spoilers
def getVoteString(content):
  voteFull = re.compile(r"\[vote\].*?\[/vote\]", re.IGNORECASE)
  voteFullMini = re.compile(r"\[v\].*?\[/v\]", re.IGNORECASE)
  if voteFull.search(content) == None and voteFullMini.search(content) == None:
    return None
  allVotes = []
  while(True):
    normalVote = voteFull.search(content)
    miniVote = voteFullMini.search(content)
    if normalVote == None and miniVote == None:
      return allVotes[len(allVotes) - 1]
    elif normalVote == None: #and miniVote exists
      miniVoteString = miniVote.group()
      allVotes.append(miniVoteString[3:len(miniVoteString) - 4])
      content = content[miniVote.end():]
    elif miniVote == None: #and normalVote exists:
      normalVoteString = normalVote.group()
      allVotes.append(normalVoteString[6:len(normalVoteString) - 7])
      content = content[normalVote.end():]
    else: #both votes exist!
      if normalVote.start() < miniVote.start():
        allVotes.append(normalVote.group())
        content = content[normalVote.end():]
      else:
        miniVoteString = miniVote.group()
        allVotes.append(miniVoteString[3:len(miniVoteString) - 4])
        content = content[miniVote.end():]

#given a post array and the playerlist, finds the vote in it, if it contains one.
#if there is no vote, returns None
#if there is a vote, returns an array of the form [poster, time, postnum, votedPlayer]
def findVote(post, playerlist):
  result = [post[0], post[1], post[2]]
  content = removeQuotes(post[3])
  vote = getVoteString(content)
  if vote == None:
    return None
  if vote[0:2] == r"\n": #remove starting newline
    vote = vote[2:]
  if vote[len(vote) - 2:] == r"\n": #remove ending newline
    vote = vote[:len(vote) - 2]
  spacelessVote = ""
  for char in vote:
    if char != " ":
      spacelessVote = spacelessVote + char
  vote = spacelessVote.lower()
  for player in playerlist: #check if vote exactly matches any players
    if vote == player.lower():
      result.append(player)
      return result
  for player in playerlist: #check if vote is substring of any players
    if player.lower().find(vote) != -1:
      result.append(player)
      return result
  result.append(vote)
  return result

#given a post, finds the unvote in it, if it contains one.
#if there is no unvote, returns None
#if there is an unvote, returns an array of the form [poster, time, postnum, "Unvote"]
def findUnvote(post):
  result = [post[0], post[1], post[2], "Unvote"]
  content = removeQuotes(post[3])
  unvoteTester = re.compile("\[unvote\].*\[/unvote\]", re.IGNORECASE)
  hasUnvote = unvoteTester.search(content)
  if hasUnvote:
    return [post[0], post[1], post[2], "Unvote"]
  else:
    return None

#compiles all votes into an array of the format [poster, time, postnum, votedPlayer]
def compileVotes(posts, playerlist):
  result = []
  for post in posts:
    vote = findVote(post, playerlist)
    unvote = findUnvote(post)
    if vote != None:
      result.append(vote)
    if unvote != None:
      result.append(unvote)
  return result

def displayMenu():
  print("Available Commands: ")
  print("MultiISO")
  print("Vote compilation")
  print("Menu")
  print("Exit")

#takes a string and a colorama Fore color, and colors it with [color] tags
def doColorTags(toBeColored, color):
  if color == Fore.RESET:
    return r'[color="a6a6a6"]' + toBeColored + r'[/color]'
  elif color == Fore.RED:
    return r'[color="ff0000"]' + toBeColored + r'[/color]'
  elif color == Fore.GREEN:
    return r'[color="00ff00"]' + toBeColored + r'[/color]'
  return toBeColored

def voteOption(posts):
  doSubsetOfPlayers = input('If you want to see only the votes made by a subset of players, enter "s". Otherwise, enter anything else: ').lower() == "s"
  chosenPlayers = []
  while(doSubsetOfPlayers):
    player = input("Enter the name of each player you want to see the votes of. When finished, enter -1: ").lower()
    if player == "-1":
      break
    chosenPlayers.append(player)

  copyToClipboard = input('Enter "c" to copy a colored vote compilation to your clipboard. Enter anything else to not do this: ').lower() == "c"
  doDisplay = input("Enter 'n' to not display votes to the terminal. Enter anything else to display them: ").lower() != "n"
  if doDisplay:
    print(Fore.RED + "Hello there." + Fore.RESET)
    usePrint = input('If the above text appears colored, enter "p". Enter anything else otherwise: ').lower() == "p"
  toBeCopied = ""
  playerlist = getPlayerlist(posts)
  votes = compileVotes(posts, playerlist)

  playerlist = set()
  for vote in votes:
    playerlist.add(vote[0])
    if vote[3].lower() != "unvote":
      playerlist.add(vote[3])

  playerColorDict = {"Unvote": Fore.RESET, "unvote": Fore.RESET}
  print('Each name will be displayed to you. Enter "t" to mark them as town, "m" to mark them as mafia, or anything else to leave them undecided.')
  print('The names have been taken from players who voted or been voted for. This means there may be mispelled names or other errors.')
  for player in playerlist:
    coloringString = input(player + ": ").lower()
    color = Fore.RESET
    if coloringString == "t":
      color = Fore.GREEN
    if coloringString == "m":
      color = Fore.RED
    playerColorDict[player] = color
  for vote in votes:
    if doSubsetOfPlayers and vote[0].lower() not in chosenPlayers:
      continue
    if doDisplay:
      displayString = playerColorDict[vote[0]] + vote[0] + Fore.RESET + " voted " + playerColorDict[vote[3]] + vote[3] + Fore.RESET + " in post " + str(vote[2])
      if usePrint:
        print(displayString)
      else:
        stdout.write(displayString + "\n")
    voter = doColorTags(vote[0], playerColorDict[vote[0]])
    voted = doColorTags(vote[3], playerColorDict[vote[3]])
    toBeCopied += voter + " voted " + voted + " in post " + str(vote[2]) + "\n"
  try:
    if(copyToClipboard):
      pyperclip.copy(toBeCopied)
  except:
    print("Clipboard is not accessible...")
  return votes, playerColorDict

gameThreadURL = input("Enter the URL of the game thread: ")
topicNumber = str(getTopicNumber(gameThreadURL))
posts = initializePosts(topicNumber)
displayMenu()
while(True):
  command = input("Enter the command you want to do: ").lower()
  if (command == "multiiso"):
    clipboardChoice = input("Enter 'quote' to copy quotes to your clipboard, enter 'link' to copy links to your clipboard, or enter anything else to do neither: ").lower()
    doDisplay = input("Enter 'n' to not display posts to the terminal. Enter anything else to display them: ").lower() != "n"
    copyQuotes = clipboardChoice == "quote"
    copyLinks = clipboardChoice == "link"
    multiISOPosts, postNums = multiISO(posts)
    outputPosts(multiISOPosts, topicNumber, gameThreadURL, doDisplay, copyQuotes, copyLinks)
  if (command == "vote compilation"):
    voteOption(posts)
  if (command == "menu"):
    displayMenu()
  if (command == "exit"):
    break

