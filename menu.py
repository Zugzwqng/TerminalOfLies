def displayInGameMenu(hasPosts=True):
  print("Available Commands (case insensitive): ")
  if hasPosts:
    print("'MultiISO' - Copies an ISO of player(s) to the clipboard; either quotes or links")
    print("'Vote compilation' - Copies a vote compilation to the clipboard")
    print("'Count' - Count the number of times a phrase has been said")
    print("'Reads' - Keep a reads list, and reads histories")
    print("'Add Link' - Adds a link to a second thread")
    print("'Display links' - Display all current links to threads")
    print("'Remove link' - Remove a link. Note this reloads the game.")
    print("'Alias' - Add an alias for a player. This alias will be resolved to their full name in most cases.")
    print("'Remove alias' - Remove an alias")
  print("'Align' - Modify player alignments")
  print("'Align d' - Change default alignment")
  print("'Align reset' - reset all alignments to unknown")
  if hasPosts:
    print("'Print playerlist' - Prints playerlist in format 'Alignment | Name | Aliases'")
  print("'Menu' - Displays this menu")
  print("'Exit' - Exit this game, returning to the previous menu")

def displayPossibleAlignments():
  print("Possible alignments: ")
  print("'t' - town")
  print("'m' - mafia")
  print("'n' - neutral")
  print("'h' - host")
  print("'u' - unknown")

def displayOverallMenu():
  print("Available Commands (case insensitive): ")
  print("'create' - Create new game ")
  print("'enter' - Enter a game")
  print("'enter n' - Enter a game, but do not load posts. Some functionality is unavailable here.")
  print("'archive' - Archive a game")
  print("'restore' - Unarchive a game")
  print("'delete' - Delete a game (file will still be present, but program will no longer see it)")
  print("'list' - Lists all active games")
  print("'list all' - Lists all games (both current and archived)")
  print("'tiers' - Customize tiers for reads lists")
  print("'analyze' - Get statistics about a player")
  print("'menu' - Displays this menu")
  print("'exit' - Exit Terminal of Lies")

def displayNotesMenu():
  print("Available Commands: ")
  print("'list' - Lists all reads lists for this game")
  print("'enter' - Enter a reads list, allowing modification and full view")
  print("'duplicate' - Duplicate a reads list, inserting it at any position. You can choose whether to keep thoughts.")
  print("'rename' - Rename a reads list")
  print("'create' - Create a new, empty reads list")
  print("'delete' - Delete a reads list (WARNING: cannot be undone!)")
  print("'swap' - Swap the orders of two reads lists")
  print("'copy' - Copy reads lists, ready for posting")
  print("'menu' - Display this menu")
  print("'exit' - Exit")

def modifyReadsMenu():
  print("Available Commands: ")
  print("'Add' - Adds a player to the list")
  print("'Remove' - Removes a player from the list. Cannot be undone.")
  print("'Swap' - Swap the positions of two players in the reads list")
  print("'Merge' - Merge the read entries of two players into one")
  print("'Rename' - Rename a player")

  print("'Tier' - Change a player's tier")
  
  print("'Thought' / 'T' - Add a thought")
  print("'Remove thought' / 'RT' - Remove a thought. Cannot be undone.")
  print("'Move thought' / 'MT' - Move a thought")
  
  print("'Display' - Displays this reads list")
  print("'Display short' / 'ds' - Displays this reads list without thoughts")
  print("'Copy' - Copy this reads list")
  print("'Copy' / 'cs' - Copies this reads list without thoughts")
  print("'Menu' - Displays this menu")
  print("'exit' - Exit")





def readTierCustomizationMenu():
  print("Available Commands: ")
  print("'current' - display current reads tiers")
  print("'add' - add a tier")
  print("'remove' - remove a tier")
  print("'exit' - exit read customization")
  print("'menu' - display this menu")