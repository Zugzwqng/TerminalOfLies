

import reads_list
# import analyze
import game
import games_list
import menu
import view

import os
import csv
import pyperclip
import time
import flet as ft
import flet_core.page #for type checking

exitLayer = False #This says whether to exit the current menu, and go back to the previous one (or exit the program).
overallDirectoryName = "overallGamesDirectory.csv"
readsTiers = "readTiers.csv"

ARCHIVE_GAME = 0
UNARCHIVE_GAME = 1
DELETE_GAME = 2
ENTER_GAME = 3
ALIASES_MODE = 4
ALIGNMENTS_MODE = 5
REMOVE_ALIAS = 6
ADD_ALIAS = 7


def getPlayerForReads(prompt: str, gameObject: game.Game, readsList: reads_list.ReadsList, implicitAliases=True, requireContains=True, allowEmptyString=True) -> str | None:
  """
  Requests a player from the user. 

  Prompts them with the prompt parameter.
  Resolves aliases using gameObject.
  Checks if the player is present in the reads list with readsList.
  implicitAliases being true means substrings will be used as aliases.
  requireContains means the player will have to be in the readsList.
  allowEmptyString only effects the function when requireContains is false. In this case, it allows the empty
    string to be valid, even if it is not within the reads list.

  Returns the string the user entered, or None if it was not valid.
  """
  player = input(prompt)
  player = gameObject.resolveAlias(player, implictAliases=implicitAliases)
  if not requireContains or readsList.containsPlayer(player) or (allowEmptyString and player == ''):
    return player
  return None


#takes a string and a colorama Fore color, and colors it with [color] tags
def doColorTags(toBeColored, color):
  if color == "gray":
    return r'[color="a6a6a6"]' + toBeColored + r'[/color]'
  elif color == "red":
    return r'[color="ff0000"]' + toBeColored + r'[/color]'
  elif color == "green":
    return r'[color="00ff00"]' + toBeColored + r'[/color]'
  return toBeColored

def voteOptionExplanation(gameObject: game.Game, page: flet_core.page.Page):
  """
  Unfinished function meant to explain the options provided by vote compilation.

  TODO: finish
  """
  clearAll(page)
  page.add(ft.Text(""))

def voteOption(gameObject: game.Game, page: flet_core.page.Page):
  clearAll(page)

  def copy_votes_on_click(e):
    toBeCopied = ""
    if (require_both_of_above.value and do_subset_of_voted_players.value and do_subset_of_voting_players.value):
      requiredProperties = 2
    elif (do_subset_of_voting_players.value or do_subset_of_voted_players.value):
      requiredProperties = 1
    else:
      requiredProperties = 0

   
    votes = gameObject.getCertainVotesNew(votingPlayers=current_voting_players_list, votedPlayers=current_voted_players_list, 
                                          requiredSatisfaction=requiredProperties)
    alignmentToColor = {"t": "green", "m": "red", "n": "gray", "u": "gray", "q": "gray", "h": "gray"}
    #t is town, m is mafia, n is neutral, u/q is unknown, h is host
    for vote in votes:
      voter = doColorTags(vote[0], alignmentToColor[vote[1].lower()])
      votedPlayer = gameObject.resolveAlias(vote[2], implictAliases=False)
      #votedPlayer = gameObject.aliases.get(vote[2], vote[2])
      voted = doColorTags(votedPlayer, alignmentToColor[vote[3].lower()])
      toBeCopied += voter + " voted " + voted + " in post " + str(vote[4]) + "\n"
    try:
      pyperclip.copy(toBeCopied)
      print("Votes copied successfully.")
    except:
      print("Clipboard is not accessible...")

  def reset_chosen_players_on_click(e):
    nonlocal current_voting_players_list
    nonlocal current_voted_players_list
    nonlocal current_voting_players
    nonlocal current_voted_players
    current_voting_players_list = []
    current_voted_players_list = []
    current_voting_players = view.createNumberedList(current_voting_players_list, visible=False)
    current_voted_players = view.createNumberedList(current_voted_players_list, visible=False)
    error_text_voted.visible = False
    error_text_voting.visible = False
    reload_page()
    do_subset_of_voted_players_on_change("a")
    do_subset_of_voting_players_on_change("a")

  def go_back_on_click(e):
    accessGameWithGUI(gameObject, page)

  def do_subset_of_voting_players_on_change(e):
    assert do_subset_of_voting_players.value is not None
    current_voting_players.visible = do_subset_of_voting_players.value
    voting_players_entry.visible = do_subset_of_voting_players.value
    voting_players_title.visible = do_subset_of_voting_players.value
    error_text_voting.visible = False
    page.update()

  def do_subset_of_voted_players_on_change(e):
    assert do_subset_of_voted_players.value is not None
    current_voted_players.visible = do_subset_of_voted_players.value
    voted_players_entry.visible = do_subset_of_voted_players.value
    voted_players_title.visible = do_subset_of_voted_players.value
    error_text_voted.visible = False
    page.update()

  def reload_page():
    clearAll(page)
    nonlocal main_button_row
    nonlocal current_selections_row
    nonlocal require_both_of_above
    main_button_row = ft.Row(
    [
      copy_votes, reset_chosen_players, go_back,
    ]
    )

    current_selections_row = ft.Row(
      [
        ft.Column([voting_players_title, current_voting_players, do_subset_of_voting_players, voting_players_entry, error_text_voting]),
        ft.Column([voted_players_title, current_voted_players, do_subset_of_voted_players, voted_players_entry, error_text_voted]),
      ]
    )

    page.add(current_selections_row)
    page.add(main_button_row)
    page.add(require_both_of_above)

  def add_player_to_subset_list(player: str, voter=True):
    nonlocal current_voting_players
    nonlocal current_voted_players
    error = False
    player = gameObject.resolveAlias(player, implictAliases=True)
    assert page.controls is not None
    if voter:
      if player in current_voting_players_list or player == '':
        error = True
      else:
        current_voting_players_list.append(player)
        voting_players_entry.value = ''
        current_voting_players = view.createNumberedList(current_voting_players_list, visible=False)
    else:
      if player in current_voted_players_list or player == '':
        error = True
      else:
        current_voted_players_list.append(player)
        voted_players_entry.value = ''
        current_voted_players = view.createNumberedList(current_voted_players_list, visible=False)
    reload_page()
    do_subset_of_voted_players_on_change("a")
    do_subset_of_voting_players_on_change("a")
    if error:
      if voter:
        error_text_voting.visible = True
      else:
        error_text_voted.visible = True
      page.update()

  


  do_subset_of_voting_players = ft.Checkbox("Filter votes by voter", on_change=do_subset_of_voting_players_on_change)
  do_subset_of_voted_players = ft.Checkbox("Filter votes by target", on_change=do_subset_of_voted_players_on_change)
  require_both_of_above = ft.Checkbox("Require both requirements above to be fulfilled (vs just one)")

  current_voting_players_list = []
  current_voted_players_list = []

  voting_players_title = ft.Text("Voters currently selected: ", visible=False)
  voted_players_title = ft.Text("Voted players currently selected: ", visible=False)
  current_voting_players = view.createNumberedList(current_voting_players_list, visible=False)
  current_voted_players = view.createNumberedList(current_voted_players_list, visible=False)
  voting_players_entry = ft.TextField(
    hint_text="Add voting player (Enter to submit)", 
    visible=False, 
    on_submit=lambda e : add_player_to_subset_list(voting_players_entry.value if voting_players_entry.value is not None else '', True))
  voted_players_entry = ft.TextField(hint_text="Add target player (Enter to submit)", 
    visible=False, 
    on_submit=lambda e : add_player_to_subset_list(voted_players_entry.value if voted_players_entry.value is not None else '', False))
  error_text_voting = ft.Text("This player is already added, or otherwise invalid.", visible=False)
  error_text_voted = ft.Text("This player is already added, or otherwise invalid.", visible=False)

  
  copy_votes = ft.ElevatedButton(text="Copy votes", on_click=copy_votes_on_click)
  reset_chosen_players = ft.ElevatedButton(text="Reset chosen players", on_click=reset_chosen_players_on_click)
  go_back = ft.ElevatedButton(text="Go back", on_click=go_back_on_click)

  main_button_row = ft.Row(
    [
      copy_votes, reset_chosen_players, go_back,
    ]
  )

  current_selections_row = ft.Row(
    [
      ft.Column([voting_players_title, current_voting_players, do_subset_of_voting_players, voting_players_entry, error_text_voting]),
      ft.Column([voted_players_title, current_voted_players, do_subset_of_voted_players, voted_players_entry, error_text_voted]),
    ]
  )

  page.add(current_selections_row)
  page.add(main_button_row)
  page.add(require_both_of_above)

  return
  clearAll(page)
  tellUserToGoToTerminal(page)
  doSubsetOfVotingPlayers = input('If you want to see only the votes made by a subset of players, enter "s". Otherwise, enter anything else: ').lower() == "s"
  doSubsetOfVotedPlayers = input('If you want to see only votes made onto a subset of players, enter "s". Otherwise, enter anything else: ').lower() == "s"
  chosenVotingPlayers = []
  chosenVotedPlayers = []
  while(doSubsetOfVotingPlayers):
    player = input("Enter the name of each player you want to see the votes of. When finished, enter -1: ").lower()
    player = gameObject.resolveAlias(player, implictAliases=True)
    if player == "-1":
      break
    chosenVotingPlayers.append(player)
  
  while (doSubsetOfVotedPlayers):
    player = input("Enter the name of each player you want to see votes on. When finished, enter -1: ").lower()
    player = gameObject.resolveAlias(player, implictAliases=True)
    if player == "-1":
      break
    chosenVotedPlayers.append(player)
  
  toBeCopied = ""
  chosenVotingPlayers = chosenVotingPlayers if doSubsetOfVotingPlayers else None
  chosenVotedPlayers = chosenVotedPlayers if doSubsetOfVotedPlayers else None
  votes = gameObject.getCertainVotes(votingPlayers=chosenVotingPlayers, votedPlayers=chosenVotedPlayers)
  alignmentToColor = {"t": "green", "m": "red", "n": "gray", "u": "gray", "q": "gray", "h": "gray"}
  #t is town, m is mafia, n is neutral, u/q is unknown, h is host
  for vote in votes:
    voter = doColorTags(vote[0], alignmentToColor[vote[1].lower()])
    votedPlayer = gameObject.resolveAlias(vote[2], implictAliases=False)
    #votedPlayer = gameObject.aliases.get(vote[2], vote[2])
    voted = doColorTags(votedPlayer, alignmentToColor[vote[3].lower()])
    toBeCopied += voter + " voted " + voted + " in post " + str(vote[4]) + "\n"
  try:
    pyperclip.copy(toBeCopied)
    print("Votes copied successfully.")
  except:
    print("Clipboard is not accessible...")
  accessGameWithGUI(gameObject, page)
  tellUserToGoToGUI(page)



def addAlias(gameObject: game.Game):
  player = input("Enter the name of the player you would like to add an alias for: ").lower()
  if (gameObject.playerExists(player)):
    alias = input("Enter the new alias of the player: ").lower()
    if gameObject.aliasExists(alias):
      print("This alias is already used.")
    elif (alias == "-1"):
      print("This alias is not allowed.")
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

def printPlayerlist(gameObject: game.Game, doPrint=True) -> list[str] | None:
  playerlist = gameObject.getPlayerlist()
  paddedPlayers = []
  alignments = []
  aliasStrings = []

  maxPlayerLength = len(max(playerlist, key=(lambda p: len(p))))
  for player in playerlist:
    paddedPlayers.append((player + (" " * 22))[0:maxPlayerLength])
    alignments.append(gameObject.getAlignment(player))
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
  overallList = []
  for num in range(len(paddedPlayers)):
    overallList.append(f"{alignments[num]} | {paddedPlayers[num]} | {aliasStrings[num]}")
  overallList.sort(key=(lambda string : string[0]))
  if doPrint:
    print("\n".join(overallList))
  else:
    return overallList


def changeAlignment(gameObject: game.Game, changeDefault=False, hasPosts=True):
  if not hasPosts and not changeDefault:
    print("You have entered this game without gathering posts. This means aliases will not work, unless you explicitly created them yourself.")
    print("If the player is entered incorrectly, it will fail without an error message.")
  player = input("Enter the name of the player you would like to change the alignment of: ").lower() if not changeDefault else "unused___________________________________________________________"
  player = gameObject.resolveAlias(player, implictAliases=True)
  if (changeDefault or gameObject.playerExists(player) or not hasPosts):
    menu.displayPossibleAlignments()
    possibleAlignments = ["t", "m", "n", "h", "u"]
    alignment = input("Enter the new alignment: ").lower()
    if alignment in possibleAlignments:
      if changeDefault:
        gameObject.changeDefaultAlignment(alignment)
      else:
        gameObject.addAlignment(player, alignment)
    else:
      print("No such alignment exists!")
  else:
    print("No player with such name!")

def resetAlignments(gameObject: game.Game):
  gameObject.clearAlignments()
  print("Alignments reset!")

def createGame(gamesList: games_list.GamesList, page: flet_core.page.Page, toRemove=[]):
    clearAll(page)

    def cancelClicked(e):
        clearAll(page)
        assert page is not None
        restoreHomeScreen(page)

    

    currentErrorText = None
    previousFilenameConflict = False
    def submitClicked(e, do_not_overwrite=True):
        nonlocal currentErrorText
        nonlocal previousFilenameConflict

        gameTitle = inputGame.value
        gameTitle = gameTitle.lower() if gameTitle is not None else None
        gameURL = inputURL.value
        filename = gameTitle + ".csv" if gameTitle is not None else None
        currentFiles = os.listdir()

        errorText = None
        filenameConflict = False
        if gameTitle is None or gameURL is None:
            errorText = ft.Text("No name has been entered.")
        elif gameTitle.find(".") != -1 or gameTitle.find("/") != -1 or gameTitle.find("\\") != -1:
            errorText = ft.Text("The filename cannot include a period, forward slash, or backslash.")
        elif gamesList.gameExists(gameTitle):
            errorText = ft.Text("This name is already taken!")
        elif filename == overallDirectoryName or filename == readsTiers:
            errorText = ft.Text("This name is reserved.")
        else:
            couldExist = False
            for file in currentFiles:
                if file.lower().find(gameTitle + ".") == 0:
                    couldExist = True
            if couldExist and do_not_overwrite:
                errorText = ft.Text("This name is already present in the directory (or, there are files with the same name but a different extension, "
                                    "which this program may eventually want to use). If you've previously created and deleted a game of this name, "
                                    "this is nothing to worry about. Otherwise, you may be overwriting files, which you probably should not do."
                                    "Click the 'Continue Creation' button if you wish to continue.")
                filenameConflict = True
        if errorText is None:
          assert gameTitle is not None and gameURL is not None
          try:
            gamesList.createGame(gameTitle.lower(), gameURL)
            clearAndRemove(page=page, toRemove=(page.controls))
            clearAll(page)
            restoreHomeScreen(page)
            return
          except:
            errorText = ft.Text("This URL is invalid! Or something else has gone wrong while accessing the page.")
        
        if currentErrorText is not None:
            page.remove(currentErrorText)
            currentErrorText = None
        if errorText is not None:
          page.add(errorText)
          currentErrorText = errorText
        if previousFilenameConflict:
          page.remove(continueCreationButton)
        if filenameConflict:
          page.add(continueCreationButton)
        previousFilenameConflict = filenameConflict

    inputGame = ft.TextField(label=f"New name of game to create")
    inputURL = ft.TextField(label=f"URL of new game")
    submitButton = ft.ElevatedButton(text="Create", on_click=submitClicked)
    backButton = ft.ElevatedButton(text="Cancel", on_click=cancelClicked)
    continueCreationButton = ft.ElevatedButton(text="Continue Creation", on_click=lambda e : submitClicked(e, do_not_overwrite=False))
    
    page.add(inputGame)
    page.add(inputURL)
    page.add(submitButton)
    page.add(backButton)
    


    
    # gameTitle = input("Enter the title you would like to use for the file that stores this game: ").lower()
    # filename = gameTitle + ".csv"
    # currentFiles = os.listdir()
    # if gameTitle.find(".") != -1 or gameTitle.find("/") != -1 or gameTitle.find("\\") != -1:
    #     print("The filename cannot include a period, forward slash, or backslash. ")
    # elif gamesList.gameExists(gameTitle):
    #     print("This name is already taken!")
    # elif filename == overallDirectoryName or filename == readsTiers:
    #     print("This name is reserved.")
    # else:
    #   couldExist = False
    #   for file in currentFiles:
    #     if file.lower().find(gameTitle + ".") != -1:
    #       couldExist = True
    #   if couldExist:
    #     print("This name is already present in the directory (or, there are files with the same name but a different extension, which this program may eventually want to use).")
    #     print("If you've previously created and deleted a game of this name, this is nothing to worry about. Otherwise, you may be overwriting files, which you probably should not do.")
    #     continueCreation = input("Enter 'y' (case insensitive) to continue: ").lower() == "y"
    #     if not continueCreation:
    #       return
    #   gameThreadURL = input("Enter the URL of the game thread: ")
    #   try:
    #     gamesList.createGame(gameTitle, gameThreadURL)
    #     print("Game created successfully.")
    #   except:
    #     print("This URL is invalid! Or something else has gone wrong while accessing the page.")
    
    # tellUserToGoToGUI(page)
    # if page is not None:
    #     restoreHomeScreen(page)

def accessGameIntermediate(gameTitle: str, page: flet_core.page.Page):
  """
  This is a method that calls accessGame with just the game name. It exists so that
  archiveUnarchiveDeleteEnterGame can use it without special cases.
  """
  clearAll(page)
  page.add(ft.Text("Please wait as posts are collected. Progress is displayed in the terminal."))
  gameObject = gamesList.recreateGame(gameTitle, getPosts=True)
  accessGameWithGUI(gameObject, page)


def archiveUnarchiveDeleteEnterGame(gamesList: games_list.GamesList, mode: int, page: flet_core.page.Page, toRemove=[]):
  if mode != ARCHIVE_GAME and mode != UNARCHIVE_GAME and mode != DELETE_GAME and mode != ENTER_GAME:
    raise Exception("Invalid mode for archiving/unarchiving/deleting games.")
  if mode == ARCHIVE_GAME:
    action = "Archive"
    verifier = gamesList.gameIsActive
    actor = gamesList.archiveGame
  elif mode == UNARCHIVE_GAME:
    action = "Unarchive"
    verifier = gamesList.gameIsArchived
    actor = gamesList.restoreGame
  elif mode == DELETE_GAME:
    action = "Delete"
    verifier = gamesList.gameExists
    actor = gamesList.deleteGame
  else:
    action = "Enter"
    verifier = gamesList.gameExists
    actor = lambda gameTitle : accessGameIntermediate(gameTitle, page)

  errorTextAdded = False
  def submitClicked(e):
    nonlocal errorTextAdded
    gameTitle = inputGame.value
    if gameTitle is None or not verifier(gameTitle):
        if not errorTextAdded:
            page.add(errorText)
            errorTextAdded = True
    else:
      actor(gameTitle.lower())
      if mode != ENTER_GAME:
        clearAndRemove(page=page, toRemove=(page.controls))
        clearAll(page)
        restoreHomeScreen(page)

  def cancelClicked(e):
    clearAll(page)
    assert page is not None
    restoreHomeScreen(page)

  clearAndRemove(page=page, toRemove=toRemove)
  page.add(createGamesList())
  inputGame = ft.TextField(label=f"Game to {action}")
  submitButton = ft.ElevatedButton(text=action, on_click=submitClicked)
  backButton = ft.ElevatedButton(text="Cancel", on_click=cancelClicked)
  if mode != ENTER_GAME:
    errorText = ft.Text(f"This game is not valid (it may have been spelled incorrectly, or may already be {action.lower()}d).")
  else:
    errorText = ft.Text(f"This game is not valid (it may have been spelled incorrectly).")
  page.add(inputGame)
  page.add(submitButton)
  page.add(backButton)


# def archiveGame(gamesList: games_list.GamesList, page: flet_core.page.Page, toRemove=[]):
#   errorTextAdded = False
#   def submitClicked(e):
#     nonlocal errorTextAdded
#     gameTitle = inputGame.value
#     if gameTitle is None or not gamesList.gameIsActive(gameTitle):
#         if not errorTextAdded:
#             page.add(errorText)
#             errorTextAdded = True
#     else:
#       gamesList.archiveGame(gameTitle.lower())
#       clearAndRemove(page=page, toRemove=(page.controls))
#       clearAll(page)
#       restoreHomeScreen(page)

#   def cancelClicked(e):
#     clearAll(page)
#     assert page is not None
#     restoreHomeScreen(page)

#   clearAndRemove(page=page, toRemove=toRemove)
#   page.add(createGamesList())
#   inputGame = ft.TextField(label="Game to Archive")
#   submitButton = ft.ElevatedButton(text="Archive", on_click=submitClicked)
#   backButton = ft.ElevatedButton(text="Cancel", on_click=cancelClicked)
#   errorText = ft.Text("This game is not valid (it may have been spelled incorrectly, or may already be archived).")
#   page.add(inputGame)
#   page.add(submitButton)
#   page.add(backButton)



  
# #   text = ft.Text("Enter the name of the game you'd like to archive:")

# #   gameTitle = input("Enter the title of the game you want to archive: ").lower()
# #   if not gamesList.gameIsActive(gameTitle):
# #       print("This game either does not exist, or is archived.")
# #   else:
# #       gamesList.archiveGame(gameTitle)
# #       print("Game archived successfully.")
# #   tellUserToGoToGUI(page)
# #   if page is not None:
# #     clearAndRemove(page=page, toRemove=(page.controls))
# #     restoreHomeScreen(page)

# def restoreGame(gamesList: games_list.GamesList, page=None, toRemove=[]):
#   clearAndRemove(page=page, toRemove=toRemove)
#   text = tellUserToGoToTerminal(page)

#   gameTitle = input("Enter the title of the game you want to restore: ").lower()
#   if not gamesList.gameIsArchived(gameTitle):
#       print("This game either does not exist, or is not archived.")
#   else:
#       gamesList.restoreGame(gameTitle)
#       print("Game restored successfully.")
#   tellUserToGoToGUI(page)
#   if page is not None:
#     clearAndRemove(page=page, toRemove=(page.controls))
#     restoreHomeScreen(page)


# def deleteGame(gamesList: games_list.GamesList, page=None, toRemove=[]):
#   clearAndRemove(page=page, toRemove=toRemove)
#   text = tellUserToGoToTerminal(page)

#   gameTitle = input("Enter the title of the game you want to delete: ").lower()
#   if not gamesList.gameExists(gameTitle):
#       print("This game does not exist! ")
#   else:
#       gamesList.deleteGame(gameTitle)
#       print("Game deleted successfully.")
#   tellUserToGoToGUI(page)
#   if page is not None:
#     clearAndRemove(page=page, toRemove=(page.controls))
#     restoreHomeScreen(page)



# def enterGame(gamesList: games_list.GamesList, page: flet_core.page.Page, getPosts=True, toRemove=[]):
#   clearAll(page)
#   page.title = "Enter Game"
  




#   text=tellUserToGoToTerminal(page)
  


#   gameTitle = input("Enter the title of the game you want to enter: ").lower()
#   if not gamesList.gameExists(gameTitle):
#       print("This game does not exist! ")
#   else:
#       reenter = True
#       while (reenter):
#         gameObject = gamesList.recreateGame(gameTitle, getPosts=getPosts)
#         exitCode = accessGame(gameObject, hasPosts=getPosts)
#         reenter = exitCode == 'reenter'
#   tellUserToGoToGUI(page)
#   if page is not None:
#     clearAndRemove(page=page, toRemove=(page.controls))
#     restoreHomeScreen(page)



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
    


def addPlayerToReadsList(gameObject: game.Game, readsList: reads_list.ReadsList):
  player = input("Enter the name of the player you would like to add: ")
  player = gameObject.resolveAlias(player, implictAliases=True)
  if readsList.containsPlayer(player):
    print("This reads list already has this player.")
  else:
    readsList.addPlayer(player)
    print(f"Player {player} added.")

def removePlayerFromReadsList(gameObject: game.Game, readsList: reads_list.ReadsList):
  print("Reminder: This removes a PLAYER. Not a single thought.")
  print("Note that removals cannot be undone. If you wish to cancel, enter an invalid name.")
  player = input("Enter the name of the player you would like to remove: ")
  player = gameObject.resolveAlias(player, implictAliases=False) #False to prevent accidental deletion
  if readsList.removeRead(player):
    print(f"Player {player} removed successfully.")
  else:
    print("This player does not exist.")

def swapPlayersInReadsList(gameObject: game.Game, readsList: reads_list.ReadsList):
  player1 = input("Enter the name of one of the players you would like to swap: ")
  player1 = gameObject.resolveAlias(player1, implictAliases=True)
  if not readsList.containsPlayer(player1):
    print("This player is not in the reads list.")
    return
  player2 = input("Enter the name of the other player you would like to swap: ")
  player2 = gameObject.resolveAlias(player2, implictAliases=True)
  if not readsList.containsPlayer(player2):
    print("This player is not in the reads list.")
    return
  if readsList.swapPlayer(player1, player2):
    print(f"Successfully swapped {player1} and {player2}.")
  else:
    print("Players not swapped successfully. This should never happen.")

def mergeReads(gameObject: game.Game, readsList: reads_list.ReadsList):
  print("The read associated with the first name you enter will continue to exist, with it's original tier and position, but with all the thoughts of the second read.")
  print("The read associated with the second name will be destroyed.")
  player1 = input("Enter the first name: ")
  player1 = gameObject.resolveAlias(player1, implictAliases=True)
  if not readsList.containsPlayer(player1):
    print("This player does not exist.")
    return
  player2 = input("Enter the second name: ")
  player2 = gameObject.resolveAlias(player2, implictAliases=True)
  if not readsList.containsPlayer(player2):
    print("This player does not exist.")
    return
  readsList.mergeReads(player1, player2)
  print("Reads merged successfully.")

def renamePlayerInReadsList(gameObject: game.Game, readsList: reads_list.ReadsList):
  currentName = input("Enter the current name of the player: ") #intentionally no alias resolution
  if not readsList.containsPlayer(currentName):
    print("This player does not exist.")
    return
  newName = input("Enter the new name of the player: ")
  newName = gameObject.resolveAlias(newName, implictAliases=True)
  readsList.renamePlayer(currentName, newName)
  print(f"Player with name '{currentName}' renamed to '{newName}'")

def changeTierInReads(gameObject: game.Game, readsList: reads_list.ReadsList):
  player = input("Enter the name of the player you would like to change the tier of: ")
  player = gameObject.resolveAlias(player, implictAliases=True)
  if (not readsList.containsPlayer(player)):
    print("This player does not exist.")
    return
  newTier = input("Enter the new tier of the player: ")


  tiersFile = open(readsTiers)
  csvreader = csv.reader(tiersFile)
  tiers = next(csvreader)
  tiersFile.close()
  #print(tiers)
  readsList.changeTier(player, newTier, tiers)
  print(f"Player {player} has tier changed to {newTier}.")

  



def displayReadsList(gameObject: game.Game, readsList: reads_list.ReadsList, withoutThoughts=False):
  toPrint = readsList.withoutThoughts() if withoutThoughts else readsList.stringToPrintToTerminal()
  print(toPrint)

def copyReadsList(gameObject: game.Game, readsList: reads_list.ReadsList, withoutThoughts=False):
  toCopy = readsList.toString(withoutThoughts=withoutThoughts, spoileredThoughts=not withoutThoughts, tabbedThoughts=False, showHidden=False)
  try:
    pyperclip.copy(toCopy)
    print("Reads list copied to clipboard.")
  except:
    print("Clipboard could not be accessed.")

def addThoughtToReads(gameObject: game.Game, readsList: reads_list.ReadsList):
  player = input("Enter the player you wish to add a thought for. \nPressing enter without any text will allow you to create a miscellaneous thought, not linked to any player: ")
  player = gameObject.resolveAlias(player, implictAliases=True)
  if player != '' and not readsList.containsPlayer(player):
    print("This player does not exist.")
    return

  print("Thoughts can have newlines in them. So, to finish entering a thought, press Enter thrice in a row. Enter your thought now.")
  fullThought = ""
  consecutiveNewlines = 0
  while(consecutiveNewlines < 2):
    thoughtPiece = input()
    consecutiveNewlines = 0 if thoughtPiece != '' else consecutiveNewlines + 1
    fullThought += "\n" + thoughtPiece
  
  while(fullThought[len(fullThought) - 1:] == "\n"): #trim trailing newlines
    fullThought = fullThought[0:len(fullThought) - 1]
  
  if player == '':
    readsList.miscthoughts.addThought(fullThought)
  else:
    readsList.addThought(player, fullThought)

def removeThoughtFromReads(gameObject: game.Game, readsList: reads_list.ReadsList):
  print("Note: At the end, you will confirm or deny whether you would like to remove the thought in question.")
  player = input("Enter the name of the player who you would like to remove a thought about. If you would like "
                 "to remove a miscellaneous thought, press Enter without any text.")
  player = gameObject.resolveAlias(player, implictAliases=True)
  if player != '' and not readsList.containsPlayer(player):
    print("This player is not in the reads list.")
    return
  
  if player == '':
    relevantRead = readsList.miscthoughts
  else:
    relevantRead = readsList.getRead(player)
  assert relevantRead != None
  print("This is the read in question: ")
  print(relevantRead)
  index = input("Enter the index of the thought you would like to remove: ")
  try:
    index = int(index)
  except:
    print("This index is not valid.")
    return
  if not (index >= 0 and index < len(relevantRead.thoughts)):
    print("This index is not valid.")
    return
  toRemove = relevantRead.thoughts[index]
  print("You are about to remove the following thought: ")
  print(toRemove)
  delete = input("Enter 'y' (case-insensitive) to continue. Enter anything else to cancel: ").lower() == 'y'
  if delete:
    relevantRead.thoughts.pop(index)
    print("Thought deleted.")
  else:
    print("Deletion cancelled.")

def moveThoughtInReads(gameObject: game.Game, readsList: reads_list.ReadsList):
  prompt = "Presumably, you'd like to move a thought. Enter the player the thought is currently associated with, or press Enter with no text to indicate it is a miscellaneous thought: "
  player1 = getPlayerForReads(prompt, gameObject, readsList)
  if player1 == None:
    print("This player does not exist in the reads list.")
    return
  print("Here are the thoughts of this player:")
  read = readsList.getRead(player1) if player1 != '' else readsList.miscthoughts
  assert read != None
  print(read.toString())
  try:
    index = int(input("Enter the index of the thought you would like to move: "))
    if index < 0 or index >= len(read.thoughts):
      raise Exception
  except:
    print("This index is invalid or out of range.")
    return
  
  thought = read.thoughts[index]
  player2 = getPlayerForReads("Enter the name of the player you would like to move the thought to: ", gameObject, readsList)
  if player2 == None:
    print("This player does not exist in the reads list. Move cancelled. ")
    return
  print("Here are the thoughts of this player:")
  read2 = readsList.getRead(player2) if player2 != '' else readsList.miscthoughts
  assert read2 != None
  print(read2.toString())
  try:
    index2 = int(input("Enter the index you would like the thought to end at: "))
    if index2 < 0 or index2 > len(read2.thoughts) - (1 if player1 == player2 else 0):
      raise Exception
  except:
    print("This index is invalid or out of range.")
    return
  thoughtToMove = read.thoughts.pop(index)
  read2.thoughts.insert(index2, thoughtToMove)
  print("Thought moved successfully.")



def enterReadsList(gameObject: game.Game):
  name = input("Input the name of the reads list you wish to enter: ")
  readsList = gameObject.readslistlist.getReadsList(name)
  if readsList == None:
    print("There is no reads list with this name.")
    return  
  menu.modifyReadsMenu()
  while(True):
    command = input("Enter the command you want to do: ").lower()
    if (command == "add"):
      addPlayerToReadsList(gameObject, readsList)
      gameObject.saveJSON()
    elif (command == "remove"):
      removePlayerFromReadsList(gameObject, readsList)
      gameObject.saveJSON()
    elif (command == "swap"):
      swapPlayersInReadsList(gameObject, readsList)
      gameObject.saveJSON()
    elif (command == "merge"):
      mergeReads(gameObject, readsList)
      gameObject.saveJSON()
    elif (command == "rename"):
      renamePlayerInReadsList(gameObject, readsList)
      gameObject.saveJSON()
    elif (command == "tier"):
      changeTierInReads(gameObject, readsList)
      gameObject.saveJSON()
    elif (command == "thought" or command == "t"):
      addThoughtToReads(gameObject, readsList)
      gameObject.saveJSON()
    elif (command == "remove thought" or command == "rt"):
      removeThoughtFromReads(gameObject, readsList)
      gameObject.saveJSON()
    elif (command == "move thought" or command == "mt"):
      moveThoughtInReads(gameObject, readsList)
      gameObject.saveJSON()
    elif (command == "display"):
      displayReadsList(gameObject, readsList)
    elif (command == "display short" or command == "ds"):
      displayReadsList(gameObject, readsList, withoutThoughts=True)
    elif (command == "copy"):
      copyReadsList(gameObject, readsList)
    elif (command == "copy short" or command == "cs"):
      copyReadsList(gameObject, readsList, withoutThoughts=True)
    elif (command == "menu"):
      menu.modifyReadsMenu()
    elif (command == "exit"):
      break
  

def listReadsLists(gameObject: game.Game):
  readsLists = gameObject.readslistlist.listReadsLists()
  print("No reads lists." if len(readsLists) == 0 else "\n".join(readsLists))

def duplicateReadsList(gameObject: game.Game):
  fullDuplicate = input("Enter 'y' if you want to keep thoughts in the duplicate. Enter anything else otherwise: ").lower() == "y"
  toDuplicate = input("Enter the name of the reads list you would like to duplicate: ")
  if gameObject.readslistlist.duplicateAndAddAtEnd(toDuplicate, fullDuplicate=fullDuplicate):
    print(f"List {toDuplicate} duplicated.")
  else:
    print("No list with this name.")
    

def renameReadsList(gameObject: game.Game):
  toRename = input("Enter the current name of the reads list you would like to change: ")
  if not gameObject.readslistlist.contains(toRename):
    print("This list does not exist.")
    return
  newName = input("Enter the new name of the reads list: ")
  if gameObject.readslistlist.rename(toRename, newName):
    print("Renamed successfully.")
  else:
    print("This new name is already taken.")

def swapReadsList(gameObject: game.Game):
  name1 = input("Enter the name of one list you would like to swap: ")
  if not gameObject.readslistlist.contains(name1):
    print("This list does not exist.")
    return
  name2 = input("Enter the name of the other list you would like to swap: ")
  if not gameObject.readslistlist.contains(name2):
    print("This list does not exist.")
    return
  if gameObject.readslistlist.swap(name1, name2):
    print("Reads lists swapped successfully.")
  else:
    print("A bug has occured somewhere! Reads lists not swapped.")

def createReadsList(gameObject: game.Game):
  name = input("Enter the name of the new reads list: ")
  if gameObject.readslistlist.create(name):
    print("New reads list created.")
  else:
    print("Name already taken.")

def deleteReadsList(gameObject: game.Game):
  name = input("Enter the name of the reads list you wish to delete: ")
  if not gameObject.readslistlist.contains(name):
    print("This list does not exist.")
  if input(f"Are you sure you want to Permanently Delete list {name}? This cannot be undone. Enter 'yes' to continue: ") == "yes":
    gameObject.readslistlist.delete_list(name)
  

def exportReadsLists(gameObject: game.Game):
  includeThoughts = input("Enter 'y' if you would like to include thoughts. Enter anything else to exclude them: ").lower() == 'y'
  result = ""
  for readsList_and_name in gameObject.readslistlist.reads_lists:
    result += f'[details="{readsList_and_name[1]}"]\n'
    readsList = readsList_and_name[0]
    assert type(readsList) == reads_list.ReadsList
    result += readsList.toString(withoutThoughts=(not includeThoughts), spoileredThoughts=True, tabbedThoughts=False)
    result += "[/details] \n"
  try:
    pyperclip.copy(result)
    print("Reads lists successfully copied.")
  except:
    print("Clipboard cannot be accessed.")


def notes(gameObject: game.Game):
  menu.displayNotesMenu()
  command = None
  while(True):
    command = input("Enter the command you want to do: ").lower()
    if (command == "list"):
      listReadsLists(gameObject)
    elif (command == "enter"):
      enterReadsList(gameObject)
      menu.displayNotesMenu()
    elif (command == "duplicate"):
      duplicateReadsList(gameObject)
      gameObject.saveJSON()
    elif (command == "rename"):
      renameReadsList(gameObject)
      gameObject.saveJSON()
    elif (command == "create"):
      createReadsList(gameObject)
      gameObject.saveJSON()
    elif (command == "delete"):
      deleteReadsList(gameObject)
      gameObject.saveJSON()
    elif (command == "swap"):
      swapReadsList(gameObject)
      gameObject.saveJSON()
    elif (command == "copy"):
      exportReadsLists(gameObject)
    elif (command == "menu"):
      menu.displayNotesMenu()
    elif (command == "exit"):
      break
  
def getCount(gameObject: game.Game, page: flet_core.page.Page) -> None:
  clearAll(page)
  def search_on_click(e):
    if string_to_search_for.value is not None:
      output.value = (f"The string '{string_to_search_for.value}' occured in the game "
                      f"{gameObject.countOccurances(string_to_search_for.value, ignoreCase=(not case_sensitive_checkbox.value))}" 
                      " times. This counts quotes.")
      page.update()

  def go_back_on_click(e):
    accessGameWithGUI(gameObject, page)

  string_to_search_for = ft.TextField(hint_text="String to search for")
  case_sensitive_checkbox = ft.Checkbox(label="Case sensitive", value=False)
  go_back = ft.ElevatedButton(text="Go back", on_click=go_back_on_click)
  search_button = ft.ElevatedButton(text="Search", on_click=search_on_click)
  output = ft.Text()

  page.add(string_to_search_for)
  page.add(case_sensitive_checkbox)
  page.add(ft.Row(
    [
      search_button,
      go_back
    ]
  ))
  page.add(output)



  # clearAll(page)
  # tellUserToGoToTerminal(page)
  # string = input("Enter the string you wish to search for: ")
  # caseSensitive = input("If you wish to do a case-sensitive search, enter 'y'. Enter anything else otherwise.").lower() == "y"
  # occurances = gameObject.countOccurances(string, ignoreCase=(not caseSensitive))
  # print(f"The string '{string}' occured in the game {occurances} times.")
  # accessGameWithGUI(gameObject, page)
  # tellUserToGoToGUI(page)

def addLink(gameObject: game.Game):
  newLink = input("Enter the link to the next thread: ")
  if gameObject.linkValid(newLink):
    gameObject.addLink(newLink)
    print("Link sucessfully added.")
  else:
    print("This link is not valid, or something else has gone wrong (perhaps your internet is not working).")

def displayLinks(gameObject: game.Game):
  if len(gameObject.links) > 0:
    print("\n".join(gameObject.links))
  else:
    print("No links? This should not happen...")

def removeLink(gameObject: game.Game) -> bool:
  if (len(gameObject.links) == 1):
    print("There is only one link, so you cannot remove any.")
    return False
  print("Current links: ")
  for num in range(1, len(gameObject.links) + 1):
    print(f"{num}: {gameObject.links[num - 1]}")
  try:
    index = int(input("Enter the index of the link you wish to remove: "))
    successful = gameObject.removeLink(index - 1)
  except:
    successful = False
  if (successful):
    print("Link successfully removed.")
    return True
  else:
    print("This index is invalid, or entered incorrectly.")
    return False
  

def createInGameMenu(page: flet_core.page.Page, gameObject: game.Game) -> ft.Card:
    inGameMenu = ft.Card(
    content=ft.Container(
        width=500,
        
        content=ft.Column(
            [
                ft.ListTile(
                    title=ft.TextButton(
                        text="Multi-ISO",
                        on_click=(lambda e : multiISO(gameObject, page))
                    )
                ),
                ft.ListTile(
                    title=ft.TextButton(
                        text="Vote Compilation",
                        on_click=(lambda e : voteOption(gameObject, page))
                    )
                ),
                ft.ListTile(
                    title=ft.TextButton(
                        text="Count words in this game",
                        on_click=(lambda e : getCount(gameObject, page))
                    )
                ),
                # ft.ListTile( #TODO: implement!
                #     title=ft.TextButton(
                #         text="Modify this game's reads",
                #         on_click=(lambda e : print("reads soon tm"))
                #     )
                # ),
                ft.ListTile(
                    title=ft.TextButton(
                        text="Change aliases of players in this game",
                        on_click=(lambda e : aliases_and_alignments(gameObject, page, ALIASES_MODE))
                    )
                ),
                ft.ListTile(
                    title=ft.TextButton(
                        text="Change alignments of players in this game",
                        on_click=(lambda e : aliases_and_alignments(gameObject, page, ALIGNMENTS_MODE))
                    )
                ),
                ft.ListTile(
                    title=ft.TextButton(
                        text="Change the URLs stored for this game",
                        on_click=(lambda e : modifyLinks(gameObject, page))
                    )
                ),
                ft.ListTile(
                    title=ft.TextButton(
                        text="Exit",
                        on_click=(lambda e : restoreHomeScreen(page))
                    )
                ),
            ],
            spacing=0,
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

        ),
        padding=ft.padding.symmetric(vertical=10),
        alignment=ft.alignment.center
        )
    )
    return inGameMenu

def aliases_and_alignments(gameObject: game.Game, page: flet_core.page.Page, mode: int):
    alignmentsToAbbreviations = {
      "Town" : "t",
        "Mafia" : "m",
        "Neutral" : "n",
        "Host" : "h",
        "Unknown" : "u",
    }
    if mode != ALIASES_MODE and mode != ALIGNMENTS_MODE:
        raise Exception("aliases_and_alignments called with invalid mode.")
    clearAll(page)

    def resetAllAliases(gameObject: game.Game, page: flet_core.page.Page):
        while (len(gameObject.aliases) > 0):
            gameObject.removeAlias(next(iter(gameObject.aliases)))
        aliases_and_alignments(gameObject, page, ALIASES_MODE)
    
    def resetAllAlignments(gameObject: game.Game, page: flet_core.page.Page):
        gameObject.clearAlignments()
        aliases_and_alignments(gameObject, page, ALIGNMENTS_MODE)

    def changeDefaultAlignment(gameObject: game.Game, page: flet_core.page.Page):
        alignmentsDropdown.visible = True
        alignmentSubmit.visible = True
        alignmentSubmit.on_click = changeDefaultAlignment_on_click
        page.update()
    
    def changePlayerAlignment(gameObject: game.Game, page: flet_core.page.Page):
        alignmentsDropdown.visible = True
        alignmentSubmit.visible = True
        enterPlayer.visible = True
        alignmentSubmit.on_click = changePlayerAlignment_on_click
        page.update()

    def changePlayerAlignment_on_click(e):
        if alignmentsDropdown.value is not None and enterPlayer.value is not None:
            player = gameObject.resolveAlias(enterPlayer.value, implictAliases=True)
            if gameObject.playerExists(player):
                gameObject.addAlignment(player, alignmentsToAbbreviations[alignmentsDropdown.value])
                aliases_and_alignments(gameObject, page, ALIGNMENTS_MODE)
            else:
                alignmentErrorText.visible = True
                page.update()
        
    

    def changeDefaultAlignment_on_click(e):
        if alignmentsDropdown.value is not None:
            gameObject.changeDefaultAlignment(alignmentsToAbbreviations[alignmentsDropdown.value])
            aliases_and_alignments(gameObject, page, ALIGNMENTS_MODE)



    def add_or_remove_alias(gameObject: game.Game, page: flet_core.page.Page, mode: int):
        def addAlias(e):
            if relevantPlayer.value is not None and relevantAlias.value is not None and gameObject.playerExists(relevantPlayer.value) and not gameObject.aliasExists(relevantAlias.value):
                gameObject.addAlias(relevantPlayer.value, relevantAlias.value)
                aliases_and_alignments(gameObject, page, ALIASES_MODE)
            else:
                if page.controls is not None and removeErrorText in page.controls:
                    page.remove(removeErrorText)
                if page.controls is None or addErrorText not in page.controls:
                    page.add(addErrorText)
        def removeAlias(e):
            if relevantAlias.value is not None and gameObject.aliasExists(relevantAlias.value):
                gameObject.removeAlias(relevantAlias.value)
                aliases_and_alignments(gameObject, page, ALIASES_MODE)
            else:
                if page.controls is not None and addErrorText in page.controls:
                    page.remove(addErrorText)
                if page.controls is None or removeErrorText not in page.controls:
                    page.add(removeErrorText)

        clearAll(page)
        page.add(playerlist_gui)
        page.add(actionDropdown)
        page.add(submitAction)


        on_click = addAlias if mode == ADD_ALIAS else removeAlias
        relevantPlayer = ft.TextField(label="Player")
        relevantAlias = ft.TextField(label="Alias")
        submit = ft.ElevatedButton("Submit", on_click=on_click)

        removeErrorText = ft.Text("This alias is not recognized.")
        addErrorText = ft.Text("Either the player does not exist, or this alias is already taken.")

        if mode == ADD_ALIAS:
            page.add(relevantPlayer)
        page.add(relevantAlias)
        page.add(submit)
        
    def submitClicked(e):
        actionDropdown.value
        toAdd = []
        if actionDropdown.value == "Add alias":
          add_or_remove_alias(gameObject, page, ADD_ALIAS)
        elif actionDropdown.value == "Remove alias":
          add_or_remove_alias(gameObject, page, REMOVE_ALIAS)
        elif actionDropdown.value == "Reset all aliases":
          toAdd.append(ft.Text("You are about to reset all aliases for this game. If you really want to do this, confirm below."))
          toAdd.append(ft.ElevatedButton(text="Confirm", on_click=lambda x : resetAllAliases(gameObject, page)))
        elif actionDropdown.value == "Change player's alignment":
          changePlayerAlignment(gameObject, page)
        elif actionDropdown.value == "Change default alignment":
          changeDefaultAlignment(gameObject, page)
        elif actionDropdown.value == "Reset all alignments":
          toAdd.append(ft.Text("You are about to reset all alignments for this game. If you really want to do this, confirm below."))
          toAdd.append(ft.ElevatedButton(text="Confirm", on_click=lambda x : resetAllAlignments(gameObject, page)))
        elif actionDropdown.value == "Return to previous menu":
          clearAll(page)
          accessGameWithGUI(gameObject, page)
   
        for item in toAdd:
          page.add(item)

    if mode == ALIASES_MODE:
      action = "alias"
      dropdown_options = [
        ft.dropdown.Option("Add alias"),
        ft.dropdown.Option("Remove alias"),
        ft.dropdown.Option("Reset all aliases"),
        ft.dropdown.Option("Return to previous menu")
      ]
    elif mode == ALIGNMENTS_MODE:
      action = "alignment"
      dropdown_options = [
        ft.dropdown.Option("Change player's alignment"),
        ft.dropdown.Option("Change default alignment"),
        ft.dropdown.Option("Reset all alignments"),
        ft.dropdown.Option("Return to previous menu")
      ]

    def hide_below_inputs(e):
      alignmentSubmit.visible = False
      enterPlayer.visible = False
      alignmentsDropdown.visible = False
      alignmentErrorText.visible = False
      page.update()
    
    actionDropdown = ft.Dropdown(
        label="Action",
        hint_text="Action to take",
        options = dropdown_options,
        on_change=hide_below_inputs,
    )


    submitAction = ft.ElevatedButton(text=f"Continue", on_click=submitClicked)

    playerlist_gui = get_playerlist_gui(gameObject, page)

    

    alignmentsDropdown = ft.Dropdown(
        label="Alignment",
        hint_text="Alignment",
        options = [
        ft.dropdown.Option("Town"),
        ft.dropdown.Option("Mafia"),
        ft.dropdown.Option("Neutral"),
        ft.dropdown.Option("Host"),
        ft.dropdown.Option("Unknown"),
      ],
      visible=False,
      
    )
    alignmentSubmit = ft.ElevatedButton(text=f"Submit", on_click=changeDefaultAlignment_on_click, visible=False)

    enterPlayer = ft.TextField(hint_text="Player", visible=False)
    alignmentErrorText = ft.Text("This player does not exist, and it is not an alias of any player.", visible=False)

    page.add(playerlist_gui)
    page.add(actionDropdown)
    page.add(submitAction)
    page.add(alignmentsDropdown)
    page.add(enterPlayer)
    page.add(alignmentSubmit)
    page.add(alignmentErrorText)



def modifyLinks(gameObject: game.Game, page: flet_core.page.Page):
    linkRemoved = False
    def goBack_on_click(e):
      if linkRemoved:
        overallFletMenu(page)
      else:
        accessGameWithGUI(gameObject, page)

    def addLink(e):
      enterIndexToRemove.visible = False
      submitRemove.visible = False
      enterLinkToAdd.visible = True
      submitAdd.visible = True
      addError.visible = False
      removeErrorParse.visible = False
      removeErrorRange.visible = False
      removeErrorSingleLink.visible = False
      page.update()
    def removeLink(e):
      enterIndexToRemove.visible = True
      submitRemove.visible = True
      enterLinkToAdd.visible = False
      submitAdd.visible = False
      addError.visible = False
      removeErrorParse.visible = False
      removeErrorRange.visible = False
      removeErrorSingleLink.visible = False
      page.update()

    def addLink_on_click(e):
        storedControls = page.controls
        page.controls = [ft.Text("Please wait as the new link is accessed.")]
        page.update()
        nonlocal links_list
        link = enterLinkToAdd.value
        if link is not None:
          if gameObject.linkValid(link):
            addError.visible = False
            enterLinkToAdd.visible = False
            submitAdd.visible = False
            gameObject.addLink(link)
          else:
            addError.visible = True            
        page.controls = storedControls
        assert page.controls is not None
        for num in range(len(page.controls)):
            if page.controls[num] == links_list:
                links_list = view.createNumberedList(gameObject.links, one_index=True)
                page.controls[num] = links_list
                break
        page.update()


    def removeLink_on_click(e):
        nonlocal linkRemoved
        nonlocal links_list
        index = enterIndexToRemove.value
        removeErrorParse.visible = False
        removeErrorRange.visible = False
        removeErrorSingleLink.visible = False
        if index is not None:
          try:
            index = int(index)
            if index < 1 or index > len(gameObject.links):
              removeErrorRange.visible = True
            elif len(gameObject.links) == 1:
              removeErrorSingleLink.visible = True
            else:
              gameObject.removeLink(index - 1)
              linkRemoved = True
              submitRemove.visible = False
              enterIndexToRemove.visible = False
              assert page.controls is not None
              for num in range(len(page.controls)):
                if page.controls[num] == links_list:
                    links_list = view.createNumberedList(gameObject.links, one_index=True)
                    page.controls[num] = links_list
                    break
          except:
            removeErrorParse.visible = True
        page.update()
            
            
    clearAll(page)
    links_list = view.createNumberedList(gameObject.links, one_index=True)
    page.add(links_list)
    page.add(ft.Row(
      [
        ft.ElevatedButton(text="Add Link", on_click=addLink),
        ft.ElevatedButton(text="Remove Link", on_click=removeLink),
        ft.ElevatedButton(text="Go back", on_click=goBack_on_click)
      ],
      alignment = ft.MainAxisAlignment.CENTER
    ))
    page.add(ft.Text("If you remove a link, 'Go back' will bring you to the main menu, so that the game can be reloaded."))
    enterIndexToRemove = ft.TextField(hint_text="Index (number)", visible=False)
    enterLinkToAdd = ft.TextField(hint_text="Link", visible=False)
    submitRemove = ft.ElevatedButton(text="Go", on_click=removeLink_on_click, visible=False)
    submitAdd = ft.ElevatedButton(text="Go", on_click=addLink_on_click, visible=False)
    addError = ft.Text("This link is not valid, or something else has gone wrong (perhaps your internet is out).", visible=False)
    removeErrorParse = ft.Text("This index is not a valid integer.", visible=False)
    removeErrorRange = ft.Text("This index is not between 1 and the number of links that currently exist, inclusive.", visible=False)
    removeErrorSingleLink = ft.Text("There is only one link, so you cannot remove it.", visible=False)
    page.add(enterIndexToRemove)
    page.add(enterLinkToAdd)
    page.add(submitRemove)
    page.add(submitAdd)
    page.add(addError)
    page.add(removeErrorParse)
    page.add(removeErrorRange)
    page.add(removeErrorSingleLink)



def get_playerlist_gui(gameObject: game.Game, page: flet_core.page.Page) -> ft.SafeArea:
  playerlist = printPlayerlist(gameObject, doPrint=False)
  assert playerlist is not None
  return view.createPlayerlist(playerlist)

def accessGameWithGUI(gameObject: game.Game, page: flet_core.page.Page, hasPosts=True):
  clearAll(page)
  page.add(createInGameMenu(page, gameObject))
  page.add(get_playerlist_gui(gameObject, page))
  return ''


def multiISO(gameObject: game.Game, page: flet_core.page.Page):
    clearAll(page)
    def copyQuotes(e):
        errorText.visible = False
        errorText_copy_error.visible = not gameObject.multiISO_good_oop(names, copyQuotes=True)
        page.update()

    def copyLinks(e):
        errorText.visible = False
        errorText_copy_error.visible = not gameObject.multiISO_good_oop(names, copyQuotes=False)
        page.update()
        
    def goBackButton_on_click(e):
      accessGameWithGUI(gameObject, page)
    def submitName_on_click(e):
      nonlocal current_selected_players
      if enterName.value is not None:
        player = gameObject.resolveAlias(enterName.value, implictAliases=True)
        if gameObject.playerExists(player):
            names.append(player)
            errorText.visible = False
            enterName.value = ''
            assert page.controls is not None
            new_selected_players = view.createNumberedList(names, one_index=True, height=(50 * (len(names) + 1)))
            page.controls[page.controls.index(current_selected_players)] = new_selected_players
            current_selected_players = new_selected_players
        else:
            errorText.visible = True
        errorText_copy_error.visible = False
        page.update()
        
    names = []
    copyQuotesButton = ft.ElevatedButton(text="Copy quotes", on_click=copyQuotes)
    copyLinksButton = ft.ElevatedButton(text="Copy links", on_click=copyLinks)
    goBackButton = ft.ElevatedButton(text="Go back", on_click=goBackButton_on_click)
    enterName = ft.TextField(hint_text="Enter name")
    submitNameButton = ft.ElevatedButton(text="Add name", on_click=submitName_on_click)
    current_selected_players_title_text = ft.Text("Currently selected players:")
    current_selected_players = view.createNumberedList(names, one_index=True, height=(50 * (len(names) + 1)))
    errorText = ft.Text("This player is not in the game, and this is not a valid alias.", visible=False)
    errorText_copy_error = ft.Text("The clipboard could not be accessed.", visible = False)

    page.add(current_selected_players_title_text)
    page.add(current_selected_players)
    page.add(ft.Row(
      [
        copyQuotesButton,
        copyLinksButton,
        goBackButton,
      ],
      alignment=ft.MainAxisAlignment.CENTER,
    ))
    page.add(enterName)
    page.add(submitNameButton)
    page.add(errorText)
    page.add(errorText_copy_error)
    # clearAll(page)
    # tellUserToGoToTerminal(page)
    # clipboardChoice = input("Enter 'quote' to copy quotes to your clipboard, enter 'link' to copy links to your clipboard, or enter anything else to do neither: ").lower()
    # display = input("Enter 'n' to not display posts to the terminal. Enter anything else to display them: ").lower() != "n"
    # quotes = clipboardChoice == "quote"
    # links = clipboardChoice == "link"
    # gameObject.multiISO(doDisplay=display, copyQuotes=quotes, copyLinks=links)
    # tellUserToGoToGUI(page)
    # accessGameWithGUI(gameObject, page)

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

if overallDirectoryName not in os.listdir():
  f = open(overallDirectoryName, "w")
  time.sleep(1)
  f.close()

if readsTiers not in os.listdir():
  csvfile = open(readsTiers, "w")
  time.sleep(1)
  csvwriter = csv.writer(csvfile, delimiter=",")
  csvwriter.writerow(["lock town", "town", "medium town", "lean town", "light town", "null", "light wolf", "lean wolf", "medium wolf", "wolf", "lock wolf"])
  csvfile.close()


def clearAndRemove(page=None, toRemove=[]):
    """
    Given a page of type flet_core.page.Page, removes all controls in toRemove.

    If page is not specified, or set to None, does nothing.
    """
    if page is not None:
        assert type(page) == flet_core.page.Page
        for item in toRemove:
            page.remove(item)

def clearAll(page=None):
  """
  Given a page of type flet_core.page.Page, removes all controls in toRemove.

  If page is not specified, or set to None, does nothing.
  """
  if page is not None:
    assert type(page) == flet_core.page.Page
    if page.controls is not None:
      while (len(page.controls) > 0):
        page.remove(page.controls[0])

def restore(page=None, toRestore=[]):
    """
    Given a page of type flet_core.page.Page, restores all controls in toRestore.

    If page is not specified, or set to None, does nothing.
    """
    if page is not None:
        assert type(page) == flet_core.page.Page
        for item in toRestore:
            page.add(item)

def tellUserToGoToGUI(page: flet_core.page.Page | None = None):
  if page is not None:
    print("You can now return to the GUI.")

def tellUserToGoToTerminal(page: flet_core.page.Page | None = None):
  text = ft.Text(value = "This functionality does not yet have a GUI. Return to the terminal for now.")
  if page is not None:
    page.add(
        text
    )
    return text
  else:
    return None

def createGamesList() -> ft.Card:
  global gamesList
  createdGames, archivedGames = gamesList.getCreatedAndArchivedGames() 
  lists_of_games = view.createGamesList(createdGames, archivedGames)
  return lists_of_games

def createMainMenu(lists_of_games: ft.Card, page: flet_core.page.Page) -> ft.Card:
    mainMenu = ft.Card(
    content=ft.Container(
        width=500,
        
        content=ft.Column(
            [
                ft.ListTile(
                    title=ft.TextButton(
                        text="Create a new game",
                        on_click=(lambda e : createGame(gamesList, page=page, toRemove=[mainMenu, lists_of_games]))
                    )
                ),
                ft.ListTile(
                    title=ft.TextButton(
                        text="Enter a game",
                        on_click=(lambda e : archiveUnarchiveDeleteEnterGame(gamesList, ENTER_GAME, page=page, toRemove=[mainMenu, lists_of_games]))
                    )
                ),
                # ft.ListTile(
                #     title=ft.TextButton(
                #         text="Enter a game, without loading posts. Most functionality unavailable.",
                #         on_click=(lambda e : enterGame(gamesList, getPosts=False, page=page, toRemove=[mainMenu, lists_of_games]))
                #     )
                # ),
                ft.ListTile(
                    title=ft.TextButton(
                        text="Archive a game",
                        on_click=(lambda e : archiveUnarchiveDeleteEnterGame(gamesList, ARCHIVE_GAME, page=page, toRemove=[mainMenu, lists_of_games]))
                    )
                ),
                ft.ListTile(
                    title=ft.TextButton(
                        text="Unarchive a game",
                        on_click=(lambda e : archiveUnarchiveDeleteEnterGame(gamesList, UNARCHIVE_GAME, page=page, toRemove=[mainMenu, lists_of_games]))
                    )
                ),
                ft.ListTile(
                    title=ft.TextButton(
                        text="Delete a game",
                        on_click=(lambda e : archiveUnarchiveDeleteEnterGame(gamesList, DELETE_GAME, page=page, toRemove=[mainMenu, lists_of_games]))
                    )
                ),
                ft.ListTile(
                    title=ft.TextButton(
                        text="Exit",
                        on_click=(lambda e : page.window_close())
                    )
                ),
            ],
            spacing=0,
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

        ),
        padding=ft.padding.symmetric(vertical=10),
        alignment=ft.alignment.center
        )
    )
    return mainMenu

def restoreHomeScreen(page: flet_core.page.Page) -> None:
    global gamesList
    page.title = "Overall Menu"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    lists_of_games = createGamesList()
    mainMenu = createMainMenu(lists_of_games, page)
    if page.controls is not None:
        while len(page.controls) > 0:
            page.remove(page.controls[0])
    page.add(mainMenu)
    page.add(lists_of_games)

def doExit():
  global exitLayer
  exitLayer = True

def overallFletMenu(page: flet_core.page.Page):
    clearAll(page)
    global gamesList
    page.title = "Terminal of Lies"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    lists_of_games = createGamesList()
    
    mainMenu = createMainMenu(lists_of_games, page)
    page.add(mainMenu)
    page.add(lists_of_games)
    

gamesList = games_list.GamesList(overallDirectoryName)
gamesList.compressCSV()
#menu.displayOverallMenu()

ft.app(target=overallFletMenu)



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

