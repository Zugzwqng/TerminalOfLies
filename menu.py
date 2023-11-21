def displayInGameMenu():
  print("Available Commands: ")
  print("'MultiISO' - Copies an ISO of player(s) to the clipboard; either quotes or links")
  print("'Vote compilation' - Copies a vote compilation to the clipboard")
  # print("'Notes' - Allows you take take notes and have a reads list")

  print("'Add alias'")
  print("'Remove alias'")
  print("'Align' - Modify player alignments")
  print("'Print playerlist' - Prints playerlist in format 'Alignment | Name | Aliases'")
  print("'Menu'")
  print("'Exit'")

def displayOverallMenu():
  print("Available Commands: ")
  print("'create' - Create new game ")
  print("'enter' - Enter a game")
  print("'archive' - Archive a game")
  print("'restore' - Unarchive a game")
  print("'delete' - Delete a game (file will still be present, but program will no longer see it)")
  print("'list' - Lists all active games")
  print("'list all' - Lists all games (both current and archived)")

  # print("'tiers' - Customize tiers for reads lists")

  print("'menu' - Displays this menu")
  print("'exit' - Exit")

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