# Terminal of Lies, version 1.1.1, 11/17/2023
# By Zugzwang (crystqllized on Discord)
# Inspired by TodaysStory

import post as p
import StringUtils as sUtil
import game
import games_list
import os

import urllib.request
import pyperclip
import re
import time
import colorama
from colorama import Fore, Style, init
init(convert=True)
from sys import stdout

overallDirectoryName = "overallGamesDirectory.csv"



def displayMenu():
  print("Available Commands: ")
  
  print("'MultiISO' - Copies an ISO of player(s) to the clipboard; either quotes or links")
  print("'Vote compilation' - Copies a vote compilation to the clipboard")

  print("'Add alias'")
  print("'Remove alias'")
  print("'Align' - Modify player alignments")
  print("'Print playerlist'")
  print("'Menu'")
  print("'Exit'")

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
  doSubsetOfPlayers = input('If you want to see only the votes made by a subset of players, enter "s". Otherwise, enter anything else: ').lower() == "s"
  chosenPlayers = [] if doSubsetOfPlayers else None
  while(doSubsetOfPlayers):
    player = input("Enter the name of each player you want to see the votes of. When finished, enter -1: ").lower()
    if player == "-1":
      break
    chosenPlayers.append(player)
  toBeCopied = ""
  votes = gameObject.getCertainVotes(votingPlayers=chosenPlayers)
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

def displayOverallMenu():
  print("Available Commands: ")
  print("'create' - Create new game ")
  print("'enter' - Enter a game")
  print("'archive' - Archive a game")
  print("'delete' - Delete a game (file will still be present, but program will no longer see it)")
  print("'list' - Lists all active games")
  print("'list all' - Lists all games (both current and archived)")
  print("'menu' - Displays this menu")
  print("'exit' - Exit")

# def listCurrentGames():
#   print("to be implemented")


# displayOverallMenu()
# listCurrentGames()
# command = input("Enter the command you want to do: ").lower()
# while(True):
#   if(command == "create"):
#     createGame()
#   if(command == "enter"):
#     enterGame()
#   if(command == "archive"):
#     archiveGame()
#   if(command == "exit"):
#     break


def addAlias(gameObject):
  player = input("Enter the name of the player you would like to add an alias for: ").lower()
  if (gameObject.playerExists(player)):
    alias = input("Enter the new alias of the player: ").lower()
    if gameObject.aliasExists(alias):
      print("This alias is already used.")
    else:
      gameObject.addAlias(player, alias)
  else:
    print("No player with such name!")

def removeAlias(gameObject):
  alias = input("Enter the alias you would like to remove: ").lower()
  if gameObject.aliasExists(alias):
    gameObject.removeAlias(alias)
    print("Alias removed.")
  else:
    print("This alias does not exist.")

def printPlayerlist(gameObject: game.Game):
  playerlist = gameObject.getPlayerlist()
  for player in playerlist:
    print(player)

def changeAlignment(gameObject: game.Game):
  player = input("Enter the name of the player you would like to change the alignment of: ").lower()
  if (gameObject.playerExists(player)):
    print("Possible alignments: ")
    print("'t' - town")
    print("'m' - mafia")
    print("'n' - neutral")
    print("'h' - host")
    print("'u' - unknown")
    possibleAlignments = ["t", "m", "n", "h", "u"]
    alignment = input("Enter the new alignment of the player: ").lower()
    if alignment in possibleAlignments:
      gameObject.addAlignment(player, alignment)
    else:
      print("No such alignment exists!")
  else:
    print("No player with such name!")



def createGame(gamesList: games_list.GamesList):
  gameTitle = input("Enter the title you would like to use for the file that stores this game: ").lower()
  if gameTitle.find(".") != -1:
      print("The filename cannot include a period. ")
  elif gamesList.gameExists(gameTitle):
      print("This name is already taken! ")
  elif gameTitle == overallDirectoryName[0:overallDirectoryName.find(".")]:
      print("This name is reserved.")
  else:
      gameThreadURL = input("Enter the URL of the game thread: ")
      gamesList.createGame(gameTitle, gameThreadURL)
      print("Game created successfully.")

def archiveGame(gamesList: games_list.GamesList):
  gameTitle = input("Enter the title of the game you want to archive: ").lower()
  if not gamesList.gameIsActive(gameTitle):
      print("This game either does exist, or is not archived. ")
  else:
      gamesList.archiveGame(gameTitle)
      print("Game archived successfully.")

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
  print("Current games: ")
  for game in createdGames:
    print(game)
  if showArchived:
    print("Archived games: ")
    for game in archivedGames:
      print(game)


def accessGame(gameObject: game.Game):
  displayMenu()
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
    if (command == "menu"):
      displayMenu()
    if (command == "add alias"):
      addAlias(gameObject)
    if (command == "remove alias"):
      removeAlias(gameObject)
    if (command == "align"):
      changeAlignment(gameObject)
    if (command == "print playerlist"):
      printPlayerlist(gameObject)
    if (command == "exit"):
      return

print(os.getcwd())
if overallDirectoryName not in os.listdir():
  f = open(overallDirectoryName, "w")
  time.sleep(1)
  f.close()

gamesList = games_list.GamesList(overallDirectoryName)
gamesList.compressCSV()
displayOverallMenu()
while(True):
    command = input("Enter the command you want to do: ").lower()
    if (command == "create"):
      createGame(gamesList)
    if (command == "enter"):
      enterGame(gamesList)
      displayOverallMenu()
    if (command == "archive"):
      archiveGame(gamesList)
    if (command == "delete"):
      deleteGame(gamesList)
    if (command == "list"):
      listGames(gamesList, showArchived=False)
    if (command == "list all"):
      listGames(gamesList)
    if (command == "menu"):
      displayOverallMenu()
    if (command == "exit"):
      break
