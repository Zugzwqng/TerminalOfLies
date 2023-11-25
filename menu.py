def displayInGameMenu():
  print("Available Commands (case insensitive): ")
  print("'MultiISO' - Copies an ISO of player(s) to the clipboard; either quotes or links")
  print("'Vote compilation' - Copies a vote compilation to the clipboard")
  # print("'Notes' - Allows you take take notes and have a reads list")

  print("'Alias' - Add an alias for a player. This alias will be resolved to their full name in most cases.")
  print("'Remove alias' - Remove an alias")
  print("'Align' - Modify player alignments")
  print("'Align u' - Players currently of unknown ('u') alignment are marked as the specified alignment")
  print("'Align reset' - reset all alignments to unknown")
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
  print("'archive' - Archive a game")
  print("'restore' - Unarchive a game")
  print("'delete' - Delete a game (file will still be present, but program will no longer see it)")
  print("'list' - Lists all active games")
  print("'list all' - Lists all games (both current and archived)")

  # print("'tiers' - Customize tiers for reads lists")

  print("'menu' - Displays this menu")
  print("'exit' - Exit Terminal of Lies")

def displayNotesMenu():
  print("Available Commands: ")
  print("'r' - Allows you to update your reads list")
  print("'t' - Customize tiers in reads lists")
  print("'s' - Save a snapshot of your current reads")
  print("'c' - Copy selected information from your reads and thoughts")
  print("'e' - Exit")
  print("'<anything else>' - Begins a thought (a stored piece of text). To end the thought, press enter 3 times in a row.")


def readTierCustomizationMenu():
  print("Available Commands: ")
  print("'current' - display current reads tiers")
  print("'add' - add a tier")
  print("'remove' - remove a tier - Warning: if a read has a tier you delete, it may break.")
  print("'exit' - exit read customization")
  print("'menu' - display this menu")