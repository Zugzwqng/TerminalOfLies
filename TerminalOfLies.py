# Terminal of Lies, version 1.2, 11/20/2023
# By Zugzwang (crystqllized on Discord)
# Inspired by TodaysStory

import post as p
import StringUtils as sUtil
import game
import games_list
import os
import menu
import csv

import pyperclip
import time
from colorama import Fore

overallDirectoryName = "overallGamesDirectory.csv"
readsTiers = "readTiers.csv"


#takes a string and a colorama Fore color, and colors it with [color] tags
def doColorTags(toBeColored, color):
  if color == Fore.RESET:
    return r'[color="a6a6a6"]' + toBeColored + r'[/color]'
  elif color == Fore.RED:
    return r'[color="ff0000"]' + toBeColored + r'[/color]'
  elif color == Fore.GREEN:
    return r'[color="00ff00"]' + toBeColored + r'[/color]'
  return toBeColored

def voteOption(gameObject: game.Game):
  doSubsetOfVotingPlayers = input('If you want to see only the votes made by a subset of players, enter "s". Otherwise, enter anything else: ').lower() == "s"
  doSubsetOfVotedPlayers = input('If you want to see only votes made onto a subset of players, enter "s". Otherwise, enter anything else: ').lower() == "s"
  chosenVotingPlayers = []
  chosenVotedPlayers = []
  while(doSubsetOfVotingPlayers):
    player = input("Enter the name of each player you want to see the votes of. When finished, enter -1: ").lower()
    player = gameObject.aliases.get(player, player)
    if player == "-1":
      break
    chosenVotingPlayers.append(player)
  
  while (doSubsetOfVotedPlayers):
    player = input("Enter the name of each player you want to see votes on. When finished, enter -1: ").lower()
    player = gameObject.aliases.get(player, player)
    if player == "-1":
      break
    chosenVotedPlayers.append(player)
  
  toBeCopied = ""
  chosenVotingPlayers = chosenVotingPlayers if doSubsetOfVotingPlayers else None
  chosenVotedPlayers = chosenVotedPlayers if doSubsetOfVotedPlayers else None
  votes = gameObject.getCertainVotes(votingPlayers=chosenVotingPlayers, votedPlayers=chosenVotedPlayers)
  alignmentToColor = {"t": Fore.GREEN, "m": Fore.RED, "n": Fore.RESET, "u": Fore.RESET, "q": Fore.RESET, "h": Fore.RESET}
  #t is town, m is mafia, n is neutral, u/q is unknown, h is host
  for vote in votes:
    voter = doColorTags(vote[0], alignmentToColor[vote[1]])
    votedPlayer = gameObject.aliases.get(vote[2], vote[2])
    voted = doColorTags(votedPlayer, alignmentToColor[vote[3]])
    toBeCopied += voter + " voted " + voted + " in post " + str(vote[4]) + "\n"
  try:
    pyperclip.copy(toBeCopied)
    print("Votes copied successfully.")
  except:
    print("Clipboard is not accessible...")


def addAlias(gameObject: game.Game):
  player = input("Enter the name of the player you would like to add an alias for: ").lower()
  if (gameObject.playerExists(player)):
    alias = input("Enter the new alias of the player: ").lower()
    if gameObject.aliasExists(alias):
      print("This alias is already used.")
    else:
      gameObject.addAlias(player, alias)
  else:
    print("No player with such name!")

def removeAlias(gameObject: game.Game):
  alias = input("Enter the alias you would like to remove: ").lower()
  if gameObject.aliasExists(alias):
    gameObject.removeAlias(alias)
    print("Alias removed.")
  else:
    print("This alias does not exist.")

def printPlayerlist(gameObject: game.Game):
  playerlist = gameObject.getPlayerlist()
  paddedPlayers = []
  alignments = []
  aliasStrings = []

  maxPlayerLength = len(max(playerlist, key=(lambda p: len(p))))
  for player in playerlist:
    paddedPlayers.append((player + (" " * 22))[0:maxPlayerLength])
    alignments.append(gameObject.alignments.get(player.lower(), "u"))
    relevantAliases = "("
    hasAlias = False
    for alias in gameObject.aliases:
      if gameObject.aliases.get(alias, "this string is never used").lower() == player.lower():
        relevantAliases = relevantAliases + alias + " / "
        hasAlias = True
    relevantAliases = relevantAliases[0:len(relevantAliases) - 3] + ")"
    if not hasAlias:
      relevantAliases = ""
    aliasStrings.append(relevantAliases)
  for num in range(len(paddedPlayers)):
    print(f"{alignments[num]} | {paddedPlayers[num]} | {aliasStrings[num]}")

def changeAlignment(gameObject: game.Game, allUnaligned=False):
  player = input("Enter the name of the player you would like to change the alignment of: ").lower() if not allUnaligned else "unused___________________________________________________________"
  player = gameObject.aliases.get(player, player)
  if (allUnaligned or gameObject.playerExists(player)):
    menu.displayPossibleAlignments()
    possibleAlignments = ["t", "m", "n", "h", "u"]
    alignment = input("Enter the new alignment: ").lower()
    if alignment in possibleAlignments:
      if allUnaligned:
        for player in gameObject.players:
          gameObject.addAlignment(player.lower(), alignment)
      else:
        gameObject.addAlignment(player, alignment)
    else:
      print("No such alignment exists!")
  else:
    print("No player with such name!")

def resetAlignments(gameObject: game.Game):
  for player in gameObject.players:
    gameObject.addAlignment(player, "u")
  print("Alignments reset!")

def createGame(gamesList: games_list.GamesList):
  gameTitle = input("Enter the title you would like to use for the file that stores this game: ").lower()
  filename = gameTitle + ".csv"
  if gameTitle.find(".") != -1:
      print("The filename cannot include a period. ")
  elif gamesList.gameExists(gameTitle):
      print("This name is already taken! ")
  elif filename == overallDirectoryName or filename == readsTiers:
      print("This name is reserved.")
  else:
      gameThreadURL = input("Enter the URL of the game thread: ")
      try:
        gamesList.createGame(gameTitle, gameThreadURL)
        print("Game created successfully.")
      except:
        print("This URL is invalid! Or something else has gone wrong while accessing the page.")

def archiveGame(gamesList: games_list.GamesList):
  gameTitle = input("Enter the title of the game you want to archive: ").lower()
  if not gamesList.gameIsActive(gameTitle):
      print("This game either does not exist, or is archived.")
  else:
      gamesList.archiveGame(gameTitle)
      print("Game archived successfully.")

def restoreGame(gamesList: games_list.GamesList):
  gameTitle = input("Enter the title of the game you want to restore: ").lower()
  if not gamesList.gameIsArchived(gameTitle):
      print("This game either does not exist, or is not archived.")
  else:
      gamesList.restoreGame(gameTitle)
      print("Game restored successfully.")

def deleteGame(gamesList: games_list.GamesList):
  gameTitle = input("Enter the title of the game you want to delete: ").lower()
  if not gamesList.gameExists(gameTitle):
      print("This game does not exist! ")
  else:
      gamesList.deleteGame(gameTitle)
      print("Game deleted successfully.")

def enterGame(gamesList: games_list.GamesList):
  gameTitle = input("Enter the title of the game you want to enter: ").lower()
  if not gamesList.gameExists(gameTitle):
      print("This game does not exist! ")
  else:
      gameObject = gamesList.recreateGame(gameTitle)
      accessGame(gameObject)

def listGames(gamesList: games_list.GamesList, showArchived=True):
  createdGames, archivedGames = gamesList.getCreatedAndArchivedGames()
  print("Current games: \n" + "\n".join(createdGames)) if len(createdGames) > 0 else print("No current games.")
  if showArchived:
    print("Archived games: \n" + "\n".join(archivedGames)) if len(archivedGames) > 0 else print("No archived games.")

def customizeTiers():
  allTiers = []
  readsFile = open(readsTiers, "r")
  csvfile = csv.reader(readsFile, delimiter=",")
  for tierList in csvfile:
    allTiers = tierList
    break
  readsFile.close()
  menu.readTierCustomizationMenu()

  while(True):
    command = input("Enter the command you want to do: ").lower()
    if (command == "current"):
      print("\n".join(allTiers))
    if (command == "add"):
      newTier = input("Enter the name of the new tier: ").lower()
      location = input("Enter the tier you would like to put this new tier above, or 'bottom' if you want to put it at the bottom: ").lower()
      if location == "bottom":
        allTiers.append(newTier)
      else:
        try:
          allTiers.insert(allTiers.index(location), newTier)
          print("Tier added.")
        except:
          print("That tier does not exist!")
    if (command == "remove"):
      toRemove = input("Enter the name of the tier to remove: ").lower()
      try:
        allTiers.remove(toRemove)
        print("Tier removed.")
      except:
        print("That tier does not exist.")
    if (command == "menu"):
      menu.readTierCustomizationMenu()
    if (command == "exit"):
      csvfile = open(readsTiers, "w")
      csvwriter = csv.writer(csvfile, delimiter=",")
      csvwriter.writerow(allTiers)
      csvfile.close()
      break
    



def updateRead(gameObject: game.Game):
  print("not implemented yet")

def snapshotReads():
  print("not implemented yet")

def copyInfo():
  print("not implemented yet")

def enterThought(gameObject: game.Game, thought: str):
  pass

def notes(gameObject: game.Game):
  menu.displayNotesMenu()
  command = None
  while(True):
    command = input("Enter the command you want to do: ").lower()
    if (command == "r"):
      updateRead(gameObject)
    elif (command == "t"):
      customizeTiers()
    elif (command == "s"):
      snapshotReads()
    elif (command == "c"):
      copyInfo()
    elif (command == "e"):
      break
    else:
      enterThought(gameObject, command)


def accessGame(gameObject: game.Game):
  menu.displayInGameMenu()
  while(True):
    command = input("Enter the command you want to do: ").lower()
    if (command == "multiiso"):
      clipboardChoice = input("Enter 'quote' to copy quotes to your clipboard, enter 'link' to copy links to your clipboard, or enter anything else to do neither: ").lower()
      display = input("Enter 'n' to not display posts to the terminal. Enter anything else to display them: ").lower() != "n"
      quotes = clipboardChoice == "quote"
      links = clipboardChoice == "link"
      gameObject.multiISO(doDisplay=display, copyQuotes=quotes, copyLinks=links)
    if (command == "vote compilation"):
      voteOption(gameObject)
    # if (command == "notes"):
    #   notes(gameObject)
    if (command == "menu"):
      menu.displayInGameMenu()
    if (command == "alias"):
      addAlias(gameObject)
    if (command == "remove alias"):
      removeAlias(gameObject)
    if (command == "align"):
      changeAlignment(gameObject, allUnaligned=False)
    if (command == "align u"):
      changeAlignment(gameObject, allUnaligned=True)
    if (command == "align reset"):
      resetAlignments(gameObject)
    if (command == "print playerlist"):
      printPlayerlist(gameObject)
    if (command == "exit"):
      return

if overallDirectoryName not in os.listdir():
  f = open(overallDirectoryName, "w")
  time.sleep(1)
  f.close()

if readsTiers not in os.listdir():
  csvfile = open(readsTiers, "w")
  time.sleep(1)
  csvwriter = csv.writer(csvfile, delimiter=",")
  csvwriter.writerow(["lock town", "medium town", "lean town", "light town", "null", "light wolf", "lean wolf", "medium wolf", "lock wolf"])
  csvfile.close()



gamesList = games_list.GamesList(overallDirectoryName)
gamesList.compressCSV()
menu.displayOverallMenu()
while(True):
    command = input("Enter the command you want to do: ").lower()
    if (command == "create"):
      createGame(gamesList)
    if (command == "enter"):
      enterGame(gamesList)
      menu.displayOverallMenu()
    if (command == "archive"):
      archiveGame(gamesList)
    if (command == "restore"):
      restoreGame(gamesList)
    if (command == "delete"):
      deleteGame(gamesList)
    # if (command == "tiers"):
    #   customizeTiers()
    #   menu.displayOverallMenu()
    if (command == "list"):
      listGames(gamesList, showArchived=False)
    if (command == "list all"):
      listGames(gamesList)
    if (command == "menu"):
      menu.displayOverallMenu()
    if (command == "exit"):
      break
