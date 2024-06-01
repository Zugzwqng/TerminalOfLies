"""
Terminal of Lies, version 2.0
By Zugzwang (crystqllized on Discord)
Inspired by lilith
"""

# The below import redirects users to GuiOfLies.py, which is the current version.
# While it is marked as 'not accessed' by IDEs, it is still very much needed - do not remove it!
import GuiOfLies
exit()


# import reads_list
# import analyze
# import game
# import games_list
# import menu

# import os
# import csv
# import pyperclip
# import time

# overallDirectoryName = "overallGamesDirectory.csv"
# readsTiers = "readTiers.csv"


# def getPlayerForReads(prompt: str, gameObject: game.Game, readsList: reads_list.ReadsList, implicitAliases=True, requireContains=True, allowEmptyString=True) -> str | None:
#   """
#   Requests a player from the user. 

#   Prompts them with the prompt parameter.
#   Resolves aliases using gameObject.
#   Checks if the player is present in the reads list with readsList.
#   implicitAliases being true means substrings will be used as aliases.
#   requireContains means the player will have to be in the readsList.
#   allowEmptyString only effects the function when requireContains is false. In this case, it allows the empty
#     string to be valid, even if it is not within the reads list.

#   Returns the string the user entered, or None if it was not valid.
#   """
#   player = input(prompt)
#   player = gameObject.resolveAlias(player, implictAliases=implicitAliases)
#   if not requireContains or readsList.containsPlayer(player) or (allowEmptyString and player == ''):
#     return player
#   return None


# #takes a string and a colorama Fore color, and colors it with [color] tags
# def doColorTags(toBeColored, color):
#   if color == "gray":
#     return r'[color="a6a6a6"]' + toBeColored + r'[/color]'
#   elif color == "red":
#     return r'[color="ff0000"]' + toBeColored + r'[/color]'
#   elif color == "green":
#     return r'[color="00ff00"]' + toBeColored + r'[/color]'
#   return toBeColored

# def voteOption(gameObject: game.Game):
#   doSubsetOfVotingPlayers = input('If you want to see only the votes made by a subset of players, enter "s". Otherwise, enter anything else: ').lower() == "s"
#   doSubsetOfVotedPlayers = input('If you want to see only votes made onto a subset of players, enter "s". Otherwise, enter anything else: ').lower() == "s"
#   chosenVotingPlayers = []
#   chosenVotedPlayers = []
#   while(doSubsetOfVotingPlayers):
#     player = input("Enter the name of each player you want to see the votes of. When finished, enter -1: ").lower()
#     player = gameObject.resolveAlias(player, implictAliases=True)
#     if player == "-1":
#       break
#     chosenVotingPlayers.append(player)
  
#   while (doSubsetOfVotedPlayers):
#     player = input("Enter the name of each player you want to see votes on. When finished, enter -1: ").lower()
#     player = gameObject.resolveAlias(player, implictAliases=True)
#     if player == "-1":
#       break
#     chosenVotedPlayers.append(player)
  
#   toBeCopied = ""
#   chosenVotingPlayers = chosenVotingPlayers if doSubsetOfVotingPlayers else None
#   chosenVotedPlayers = chosenVotedPlayers if doSubsetOfVotedPlayers else None
#   votes = gameObject.getCertainVotes(votingPlayers=chosenVotingPlayers, votedPlayers=chosenVotedPlayers)
#   alignmentToColor = {"t": "green", "m": "red", "n": "gray", "u": "gray", "q": "gray", "h": "gray"}
#   #t is town, m is mafia, n is neutral, u/q is unknown, h is host
#   for vote in votes:
#     voter = doColorTags(vote[0], alignmentToColor[vote[1].lower()])
#     votedPlayer = gameObject.resolveAlias(vote[2], implictAliases=False)
#     #votedPlayer = gameObject.aliases.get(vote[2], vote[2])
#     voted = doColorTags(votedPlayer, alignmentToColor[vote[3].lower()])
#     toBeCopied += voter + " voted " + voted + " in post " + str(vote[4]) + "\n"
#   try:
#     pyperclip.copy(toBeCopied)
#     print("Votes copied successfully.")
#   except:
#     print("Clipboard is not accessible...")


# def addAlias(gameObject: game.Game):
#   player = input("Enter the name of the player you would like to add an alias for: ").lower()
#   if (gameObject.playerExists(player)):
#     alias = input("Enter the new alias of the player: ").lower()
#     if gameObject.aliasExists(alias):
#       print("This alias is already used.")
#     elif (alias == "-1"):
#       print("This alias is not allowed.")
#     else:
#       gameObject.addAlias(player, alias)
#   else:
#     print("No player with such name!")

# def removeAlias(gameObject: game.Game):
#   alias = input("Enter the alias you would like to remove: ").lower()
#   if gameObject.aliasExists(alias):
#     gameObject.removeAlias(alias)
#     print("Alias removed.")
#   else:
#     print("This alias does not exist.")

# def printPlayerlist(gameObject: game.Game):
#   playerlist = gameObject.getPlayerlist()
#   paddedPlayers = []
#   alignments = []
#   aliasStrings = []

#   maxPlayerLength = len(max(playerlist, key=(lambda p: len(p))))
#   for player in playerlist:
#     paddedPlayers.append((player + (" " * 22))[0:maxPlayerLength])
#     alignments.append(gameObject.getAlignment(player))
#     relevantAliases = "("
#     hasAlias = False
#     for alias in gameObject.aliases:
#       if gameObject.aliases.get(alias, "this string is never used").lower() == player.lower():
#         relevantAliases = relevantAliases + alias + " / "
#         hasAlias = True
#     relevantAliases = relevantAliases[0:len(relevantAliases) - 3] + ")"
#     if not hasAlias:
#       relevantAliases = ""
#     aliasStrings.append(relevantAliases)
#   overallList = []
#   for num in range(len(paddedPlayers)):
#     overallList.append(f"{alignments[num]} | {paddedPlayers[num]} | {aliasStrings[num]}")
#   overallList.sort(key=(lambda string : string[0]))
#   print("\n".join(overallList))


# def changeAlignment(gameObject: game.Game, changeDefault=False, hasPosts=True):
#   if not hasPosts and not changeDefault:
#     print("You have entered this game without gathering posts. This means aliases will not work, unless you explicitly created them yourself.")
#     print("If the player is entered incorrectly, it will fail without an error message.")
#   player = input("Enter the name of the player you would like to change the alignment of: ").lower() if not changeDefault else "unused___________________________________________________________"
#   player = gameObject.resolveAlias(player, implictAliases=True)
#   if (changeDefault or gameObject.playerExists(player) or not hasPosts):
#     menu.displayPossibleAlignments()
#     possibleAlignments = ["t", "m", "n", "h", "u"]
#     alignment = input("Enter the new alignment: ").lower()
#     if alignment in possibleAlignments:
#       if changeDefault:
#         gameObject.changeDefaultAlignment(alignment)
#       else:
#         gameObject.addAlignment(player, alignment)
#     else:
#       print("No such alignment exists!")
#   else:
#     print("No player with such name!")

# def resetAlignments(gameObject: game.Game):
#   gameObject.clearAlignments()
#   print("Alignments reset!")

# def createGame(gamesList: games_list.GamesList):
#   gameTitle = input("Enter the title you would like to use for the file that stores this game: ").lower()
#   filename = gameTitle + ".csv"
#   currentFiles = os.listdir()
  
#   if gameTitle.find(".") != -1 or gameTitle.find("/") != -1 or gameTitle.find("\\") != -1:
#       print("The filename cannot include a period, forward slash, or backslash. ")
#   elif gamesList.gameExists(gameTitle):
#       print("This name is already taken!")
#   elif filename == overallDirectoryName or filename == readsTiers:
#       print("This name is reserved.")
#   else:
#       couldExist = False
#       for file in currentFiles:
#         if file.lower().find(gameTitle + ".") != -1:
#           couldExist = True
#       if couldExist:
#         print("This name is already present in the directory (or, there are files with the same name but a different extension, which this program may eventually want to use).")
#         print("If you've previously created and deleted a game of this name, this is nothing to worry about. Otherwise, you may be overwriting files, which you probably should not do.")
#         continueCreation = input("Enter 'y' (case insensitive) to continue: ").lower() == "y"
#         if not continueCreation:
#           return
#       gameThreadURL = input("Enter the URL of the game thread: ")
#       try:
#         gamesList.createGame(gameTitle, gameThreadURL)
#         print("Game created successfully.")
#       except:
#         print("This URL is invalid! Or something else has gone wrong while accessing the page.")





# def archiveGame(gamesList: games_list.GamesList):
#   gameTitle = input("Enter the title of the game you want to archive: ").lower()
#   if not gamesList.gameIsActive(gameTitle):
#       print("This game either does not exist, or is archived.")
#   else:
#       gamesList.archiveGame(gameTitle)
#       print("Game archived successfully.")

# def restoreGame(gamesList: games_list.GamesList):
#   gameTitle = input("Enter the title of the game you want to restore: ").lower()
#   if not gamesList.gameIsArchived(gameTitle):
#       print("This game either does not exist, or is not archived.")
#   else:
#       gamesList.restoreGame(gameTitle)
#       print("Game restored successfully.")

# def deleteGame(gamesList: games_list.GamesList):
#   gameTitle = input("Enter the title of the game you want to delete: ").lower()
#   if not gamesList.gameExists(gameTitle):
#       print("This game does not exist! ")
#   else:
#       gamesList.deleteGame(gameTitle)
#       print("Game deleted successfully.")


# def enterGame(gamesList: games_list.GamesList, getPosts=True):
#   gameTitle = input("Enter the title of the game you want to enter: ").lower()
#   if not gamesList.gameExists(gameTitle):
#       print("This game does not exist! ")
#   else:
#       reenter = True
#       while (reenter):
#         gameObject = gamesList.recreateGame(gameTitle, getPosts=getPosts)
#         exitCode = accessGame(gameObject, hasPosts=getPosts)
#         reenter = exitCode == 'reenter'

# def listGames(gamesList: games_list.GamesList, showArchived=True):
#   createdGames, archivedGames = gamesList.getCreatedAndArchivedGames()
#   print("Current games: \n" + "\n".join(createdGames)) if len(createdGames) > 0 else print("No current games.")
#   if showArchived:
#     print("Archived games: \n" + "\n".join(archivedGames)) if len(archivedGames) > 0 else print("No archived games.")

# def customizeTiers():
#   allTiers = []
#   readsFile = open(readsTiers, "r")
#   csvfile = csv.reader(readsFile, delimiter=",")
#   for tierList in csvfile:
#     allTiers = tierList
#     break
#   readsFile.close()
#   menu.readTierCustomizationMenu()

#   while(True):
#     command = input("Enter the command you want to do: ").lower()
#     if (command == "current"):
#       print("\n".join(allTiers))
#     if (command == "add"):
#       newTier = input("Enter the name of the new tier: ").lower()
#       location = input("Enter the tier you would like to put this new tier above, or 'bottom' if you want to put it at the bottom: ").lower()
#       if location == "bottom":
#         allTiers.append(newTier)
#       else:
#         try:
#           allTiers.insert(allTiers.index(location), newTier)
#           print("Tier added.")
#         except:
#           print("That tier does not exist!")
#     if (command == "remove"):
#       toRemove = input("Enter the name of the tier to remove: ").lower()
#       try:
#         allTiers.remove(toRemove)
#         print("Tier removed.")
#       except:
#         print("That tier does not exist.")
#     if (command == "menu"):
#       menu.readTierCustomizationMenu()
#     if (command == "exit"):
#       csvfile = open(readsTiers, "w")
#       csvwriter = csv.writer(csvfile, delimiter=",")
#       csvwriter.writerow(allTiers)
#       csvfile.close()
#       break
    


# def addPlayerToReadsList(gameObject: game.Game, readsList: reads_list.ReadsList):
#   player = input("Enter the name of the player you would like to add: ")
#   player = gameObject.resolveAlias(player, implictAliases=True)
#   if readsList.containsPlayer(player):
#     print("This reads list already has this player.")
#   else:
#     readsList.addPlayer(player)
#     print(f"Player {player} added.")

# def removePlayerFromReadsList(gameObject: game.Game, readsList: reads_list.ReadsList):
#   print("Reminder: This removes a PLAYER. Not a single thought.")
#   print("Note that removals cannot be undone. If you wish to cancel, enter an invalid name.")
#   player = input("Enter the name of the player you would like to remove: ")
#   player = gameObject.resolveAlias(player, implictAliases=False) #False to prevent accidental deletion
#   if readsList.removeRead(player):
#     print(f"Player {player} removed successfully.")
#   else:
#     print("This player does not exist.")

# def swapPlayersInReadsList(gameObject: game.Game, readsList: reads_list.ReadsList):
#   player1 = input("Enter the name of one of the players you would like to swap: ")
#   player1 = gameObject.resolveAlias(player1, implictAliases=True)
#   if not readsList.containsPlayer(player1):
#     print("This player is not in the reads list.")
#     return
#   player2 = input("Enter the name of the other player you would like to swap: ")
#   player2 = gameObject.resolveAlias(player2, implictAliases=True)
#   if not readsList.containsPlayer(player2):
#     print("This player is not in the reads list.")
#     return
#   if readsList.swapPlayer(player1, player2):
#     print(f"Successfully swapped {player1} and {player2}.")
#   else:
#     print("Players not swapped successfully. This should never happen.")

# def mergeReads(gameObject: game.Game, readsList: reads_list.ReadsList):
#   print("The read associated with the first name you enter will continue to exist, with it's original tier and position, but with all the thoughts of the second read.")
#   print("The read associated with the second name will be destroyed.")
#   player1 = input("Enter the first name: ")
#   player1 = gameObject.resolveAlias(player1, implictAliases=True)
#   if not readsList.containsPlayer(player1):
#     print("This player does not exist.")
#     return
#   player2 = input("Enter the second name: ")
#   player2 = gameObject.resolveAlias(player2, implictAliases=True)
#   if not readsList.containsPlayer(player2):
#     print("This player does not exist.")
#     return
#   readsList.mergeReads(player1, player2)
#   print("Reads merged successfully.")

# def renamePlayerInReadsList(gameObject: game.Game, readsList: reads_list.ReadsList):
#   currentName = input("Enter the current name of the player: ") #intentionally no alias resolution
#   if not readsList.containsPlayer(currentName):
#     print("This player does not exist.")
#     return
#   newName = input("Enter the new name of the player: ")
#   newName = gameObject.resolveAlias(newName, implictAliases=True)
#   readsList.renamePlayer(currentName, newName)
#   print(f"Player with name '{currentName}' renamed to '{newName}'")

# def changeTierInReads(gameObject: game.Game, readsList: reads_list.ReadsList):
#   player = input("Enter the name of the player you would like to change the tier of: ")
#   player = gameObject.resolveAlias(player, implictAliases=True)
#   if (not readsList.containsPlayer(player)):
#     print("This player does not exist.")
#     return
#   newTier = input("Enter the new tier of the player: ")


#   tiersFile = open(readsTiers)
#   csvreader = csv.reader(tiersFile)
#   tiers = next(csvreader)
#   tiersFile.close()
#   #print(tiers)
#   readsList.changeTier(player, newTier, tiers)
#   print(f"Player {player} has tier changed to {newTier}.")

  



# def displayReadsList(gameObject: game.Game, readsList: reads_list.ReadsList, withoutThoughts=False):
#   toPrint = readsList.withoutThoughts() if withoutThoughts else readsList.stringToPrintToTerminal()
#   print(toPrint)

# def copyReadsList(gameObject: game.Game, readsList: reads_list.ReadsList, withoutThoughts=False):
#   toCopy = readsList.toString(withoutThoughts=withoutThoughts, spoileredThoughts=not withoutThoughts, tabbedThoughts=False, showHidden=False)
#   try:
#     pyperclip.copy(toCopy)
#     print("Reads list copied to clipboard.")
#   except:
#     print("Clipboard could not be accessed.")

# def addThoughtToReads(gameObject: game.Game, readsList: reads_list.ReadsList):
#   player = input("Enter the player you wish to add a thought for. \nPressing enter without any text will allow you to create a miscellaneous thought, not linked to any player: ")
#   player = gameObject.resolveAlias(player, implictAliases=True)
#   if player != '' and not readsList.containsPlayer(player):
#     print("This player does not exist.")
#     return

#   print("Thoughts can have newlines in them. So, to finish entering a thought, press Enter thrice in a row. Enter your thought now.")
#   fullThought = ""
#   consecutiveNewlines = 0
#   while(consecutiveNewlines < 2):
#     thoughtPiece = input()
#     consecutiveNewlines = 0 if thoughtPiece != '' else consecutiveNewlines + 1
#     fullThought += "\n" + thoughtPiece
  
#   while(fullThought[len(fullThought) - 1:] == "\n"): #trim trailing newlines
#     fullThought = fullThought[0:len(fullThought) - 1]
  
#   if player == '':
#     readsList.miscthoughts.addThought(fullThought)
#   else:
#     readsList.addThought(player, fullThought)

# def removeThoughtFromReads(gameObject: game.Game, readsList: reads_list.ReadsList):
#   print("Note: At the end, you will confirm or deny whether you would like to remove the thought in question.")
#   player = input("Enter the name of the player who you would like to remove a thought about. If you would like "
#                  "to remove a miscellaneous thought, press Enter without any text.")
#   player = gameObject.resolveAlias(player, implictAliases=True)
#   if player != '' and not readsList.containsPlayer(player):
#     print("This player is not in the reads list.")
#     return
  
#   if player == '':
#     relevantRead = readsList.miscthoughts
#   else:
#     relevantRead = readsList.getRead(player)
#   assert relevantRead != None
#   print("This is the read in question: ")
#   print(relevantRead)
#   index = input("Enter the index of the thought you would like to remove: ")
#   try:
#     index = int(index)
#   except:
#     print("This index is not valid.")
#     return
#   if not (index >= 0 and index < len(relevantRead.thoughts)):
#     print("This index is not valid.")
#     return
#   toRemove = relevantRead.thoughts[index]
#   print("You are about to remove the following thought: ")
#   print(toRemove)
#   delete = input("Enter 'y' (case-insensitive) to continue. Enter anything else to cancel: ").lower() == 'y'
#   if delete:
#     relevantRead.thoughts.pop(index)
#     print("Thought deleted.")
#   else:
#     print("Deletion cancelled.")

# def moveThoughtInReads(gameObject: game.Game, readsList: reads_list.ReadsList):
#   prompt = "Presumably, you'd like to move a thought. Enter the player the thought is currently associated with, or press Enter with no text to indicate it is a miscellaneous thought: "
#   player1 = getPlayerForReads(prompt, gameObject, readsList)
#   if player1 == None:
#     print("This player does not exist in the reads list.")
#     return
#   print("Here are the thoughts of this player:")
#   read = readsList.getRead(player1) if player1 != '' else readsList.miscthoughts
#   assert read != None
#   print(read.toString())
#   try:
#     index = int(input("Enter the index of the thought you would like to move: "))
#     if index < 0 or index >= len(read.thoughts):
#       raise Exception
#   except:
#     print("This index is invalid or out of range.")
#     return
  
#   thought = read.thoughts[index]
#   player2 = getPlayerForReads("Enter the name of the player you would like to move the thought to: ", gameObject, readsList)
#   if player2 == None:
#     print("This player does not exist in the reads list. Move cancelled. ")
#     return
#   print("Here are the thoughts of this player:")
#   read2 = readsList.getRead(player2) if player2 != '' else readsList.miscthoughts
#   assert read2 != None
#   print(read2.toString())
#   try:
#     index2 = int(input("Enter the index you would like the thought to end at: "))
#     if index2 < 0 or index2 > len(read2.thoughts) - (1 if player1 == player2 else 0):
#       raise Exception
#   except:
#     print("This index is invalid or out of range.")
#     return
#   thoughtToMove = read.thoughts.pop(index)
#   read2.thoughts.insert(index2, thoughtToMove)
#   print("Thought moved successfully.")



# def enterReadsList(gameObject: game.Game):
#   name = input("Input the name of the reads list you wish to enter: ")
#   readsList = gameObject.readslistlist.getReadsList(name)
#   if readsList == None:
#     print("There is no reads list with this name.")
#     return  
#   menu.modifyReadsMenu()
#   while(True):
#     command = input("Enter the command you want to do: ").lower()
#     if (command == "add"):
#       addPlayerToReadsList(gameObject, readsList)
#       gameObject.saveJSON()
#     elif (command == "remove"):
#       removePlayerFromReadsList(gameObject, readsList)
#       gameObject.saveJSON()
#     elif (command == "swap"):
#       swapPlayersInReadsList(gameObject, readsList)
#       gameObject.saveJSON()
#     elif (command == "merge"):
#       mergeReads(gameObject, readsList)
#       gameObject.saveJSON()
#     elif (command == "rename"):
#       renamePlayerInReadsList(gameObject, readsList)
#       gameObject.saveJSON()
#     elif (command == "tier"):
#       changeTierInReads(gameObject, readsList)
#       gameObject.saveJSON()
#     elif (command == "thought" or command == "t"):
#       addThoughtToReads(gameObject, readsList)
#       gameObject.saveJSON()
#     elif (command == "remove thought" or command == "rt"):
#       removeThoughtFromReads(gameObject, readsList)
#       gameObject.saveJSON()
#     elif (command == "move thought" or command == "mt"):
#       moveThoughtInReads(gameObject, readsList)
#       gameObject.saveJSON()
#     elif (command == "display"):
#       displayReadsList(gameObject, readsList)
#     elif (command == "display short" or command == "ds"):
#       displayReadsList(gameObject, readsList, withoutThoughts=True)
#     elif (command == "copy"):
#       copyReadsList(gameObject, readsList)
#     elif (command == "copy short" or command == "cs"):
#       copyReadsList(gameObject, readsList, withoutThoughts=True)
#     elif (command == "menu"):
#       menu.modifyReadsMenu()
#     elif (command == "exit"):
#       break
  

# def listReadsLists(gameObject: game.Game):
#   readsLists = gameObject.readslistlist.listReadsLists()
#   print("No reads lists." if len(readsLists) == 0 else "\n".join(readsLists))

# def duplicateReadsList(gameObject: game.Game):
#   fullDuplicate = input("Enter 'y' if you want to keep thoughts in the duplicate. Enter anything else otherwise: ").lower() == "y"
#   toDuplicate = input("Enter the name of the reads list you would like to duplicate: ")
#   if gameObject.readslistlist.duplicateAndAddAtEnd(toDuplicate, fullDuplicate=fullDuplicate):
#     print(f"List {toDuplicate} duplicated.")
#   else:
#     print("No list with this name.")
    

# def renameReadsList(gameObject: game.Game):
#   toRename = input("Enter the current name of the reads list you would like to change: ")
#   if not gameObject.readslistlist.contains(toRename):
#     print("This list does not exist.")
#     return
#   newName = input("Enter the new name of the reads list: ")
#   if gameObject.readslistlist.rename(toRename, newName):
#     print("Renamed successfully.")
#   else:
#     print("This new name is already taken.")

# def swapReadsList(gameObject: game.Game):
#   name1 = input("Enter the name of one list you would like to swap: ")
#   if not gameObject.readslistlist.contains(name1):
#     print("This list does not exist.")
#     return
#   name2 = input("Enter the name of the other list you would like to swap: ")
#   if not gameObject.readslistlist.contains(name2):
#     print("This list does not exist.")
#     return
#   if gameObject.readslistlist.swap(name1, name2):
#     print("Reads lists swapped successfully.")
#   else:
#     print("A bug has occured somewhere! Reads lists not swapped.")

# def createReadsList(gameObject: game.Game):
#   name = input("Enter the name of the new reads list: ")
#   if gameObject.readslistlist.create(name):
#     print("New reads list created.")
#   else:
#     print("Name already taken.")

# def deleteReadsList(gameObject: game.Game):
#   name = input("Enter the name of the reads list you wish to delete: ")
#   if not gameObject.readslistlist.contains(name):
#     print("This list does not exist.")
#   if input(f"Are you sure you want to Permanently Delete list {name}? This cannot be undone. Enter 'yes' to continue: ") == "yes":
#     gameObject.readslistlist.delete_list(name)
  

# def exportReadsLists(gameObject: game.Game):
#   includeThoughts = input("Enter 'y' if you would like to include thoughts. Enter anything else to exclude them: ").lower() == 'y'
#   result = ""
#   for readsList_and_name in gameObject.readslistlist.reads_lists:
#     result += f'[details="{readsList_and_name[1]}"]\n'
#     readsList = readsList_and_name[0]
#     assert type(readsList) == reads_list.ReadsList
#     result += readsList.toString(withoutThoughts=(not includeThoughts), spoileredThoughts=True, tabbedThoughts=False)
#     result += "[/details] \n"
#   try:
#     pyperclip.copy(result)
#     print("Reads lists successfully copied.")
#   except:
#     print("Clipboard cannot be accessed.")


# def notes(gameObject: game.Game):
#   menu.displayNotesMenu()
#   command = None
#   while(True):
#     command = input("Enter the command you want to do: ").lower()
#     if (command == "list"):
#       listReadsLists(gameObject)
#     elif (command == "enter"):
#       enterReadsList(gameObject)
#       menu.displayNotesMenu()
#     elif (command == "duplicate"):
#       duplicateReadsList(gameObject)
#       gameObject.saveJSON()
#     elif (command == "rename"):
#       renameReadsList(gameObject)
#       gameObject.saveJSON()
#     elif (command == "create"):
#       createReadsList(gameObject)
#       gameObject.saveJSON()
#     elif (command == "delete"):
#       deleteReadsList(gameObject)
#       gameObject.saveJSON()
#     elif (command == "swap"):
#       swapReadsList(gameObject)
#       gameObject.saveJSON()
#     elif (command == "copy"):
#       exportReadsLists(gameObject)
#     elif (command == "menu"):
#       menu.displayNotesMenu()
#     elif (command == "exit"):
#       break
  

# def getCount(gameObject: game.Game) -> None:
#   string = input("Enter the string you wish to search for: ")
#   caseSensitive = input("If you wish to do a case-sensitive search, enter 'y'. Enter anything else otherwise.").lower() == "y"
#   occurances = gameObject.countOccurances(string, ignoreCase=(not caseSensitive))
#   print(f"The string '{string}' occured in the game {occurances} times.")

# def addLink(gameObject: game.Game):
#   newLink = input("Enter the link to the next thread: ")
#   if gameObject.linkValid(newLink):
#     gameObject.addLink(newLink)
#     print("Link sucessfully added.")
#   else:
#     print("This link is not valid, or something else has gone wrong (perhaps your internet is not working).")

# def displayLinks(gameObject: game.Game):
#   if len(gameObject.links) > 0:
#     print("\n".join(gameObject.links))
#   else:
#     print("No links? This should not happen...")

# def removeLink(gameObject: game.Game) -> bool:
#   if (len(gameObject.links) == 1):
#     print("There is only one link, so you cannot remove any.")
#     return False
#   print("Current links: ")
#   for num in range(1, len(gameObject.links) + 1):
#     print(f"{num}: {gameObject.links[num - 1]}")
#   try:
#     index = int(input("Enter the index of the link you wish to remove: "))
#     successful = gameObject.removeLink(index - 1)
#   except:
#     successful = False
#   if (successful):
#     print("Link successfully removed.")
#     return True
#   else:
#     print("This index is invalid, or entered incorrectly.")
#     return False

# def accessGame(gameObject: game.Game, hasPosts=True):
#   menu.displayInGameMenu(hasPosts=hasPosts)
#   while(True):
#     command = input("Enter the command you want to do: ").lower()
#     if (command == "multiiso" and hasPosts):
#       clipboardChoice = input("Enter 'quote' to copy quotes to your clipboard, enter 'link' to copy links to your clipboard, or enter anything else to do neither: ").lower()
#       display = input("Enter 'n' to not display posts to the terminal. Enter anything else to display them: ").lower() != "n"
#       quotes = clipboardChoice == "quote"
#       links = clipboardChoice == "link"
#       gameObject.multiISO(doDisplay=display, copyQuotes=quotes, copyLinks=links)
#     elif (command == "vote compilation" and hasPosts):
#       voteOption(gameObject)
#     elif (command == "count" and hasPosts):
#       getCount(gameObject)
#     elif (command == "reads" and hasPosts):
#       notes(gameObject)
#       menu.displayInGameMenu()
#     elif (command == "menu"):
#       menu.displayInGameMenu(hasPosts=hasPosts)
#     elif (command == "alias" and hasPosts):
#       addAlias(gameObject)
#     elif (command == "remove alias" and hasPosts):
#       removeAlias(gameObject)
#     elif (command == "align"):
#       changeAlignment(gameObject, changeDefault=False, hasPosts=hasPosts)
#     elif (command == "align d"):
#       changeAlignment(gameObject, changeDefault=True, hasPosts=hasPosts)
#     elif (command == "align reset"):
#       resetAlignments(gameObject)
#     elif (command == "print playerlist" and hasPosts):
#       printPlayerlist(gameObject)
#     elif (command == "add link" and hasPosts):
#       addLink(gameObject)
#     elif (command == "display links" and hasPosts):
#       displayLinks(gameObject)
#     elif (command == "remove link" and hasPosts):
#       if removeLink(gameObject):
#         return 'reenter'
#     elif (command == "exit"):
#       return ''

# if overallDirectoryName not in os.listdir():
#   f = open(overallDirectoryName, "w")
#   time.sleep(1)
#   f.close()

# if readsTiers not in os.listdir():
#   csvfile = open(readsTiers, "w")
#   time.sleep(1)
#   csvwriter = csv.writer(csvfile, delimiter=",")
#   csvwriter.writerow(["lock town", "town", "medium town", "lean town", "light town", "null", "light wolf", "lean wolf", "medium wolf", "wolf", "lock wolf"])
#   csvfile.close()



# gamesList = games_list.GamesList(overallDirectoryName)
# gamesList.compressCSV()
# menu.displayOverallMenu()
# while(True):
#     command = input("Enter the command you want to do: ").lower()
#     if (command == "create"):
#       createGame(gamesList)
#     if (command == "enter"):
#       enterGame(gamesList, getPosts=True)
#       menu.displayOverallMenu()
#     if (command == "enter n"):
#       enterGame(gamesList, getPosts=False)
#       menu.displayOverallMenu()
#     if (command == "archive"):
#       archiveGame(gamesList)
#     if (command == "restore"):
#       restoreGame(gamesList)
#     if (command == "delete"):
#       deleteGame(gamesList)
#     if (command == "tiers"):
#       customizeTiers()
#       menu.displayOverallMenu()
#     if (command == "list"):
#       listGames(gamesList, showArchived=False)
#     if (command == "list all"):
#       listGames(gamesList)
#     if (command == "menu"):
#       menu.displayOverallMenu()
#     if (command == "analyze"):
#       analyze.start(gamesList)
#       menu.displayOverallMenu()
#     if (command == "exit"):
#       break

