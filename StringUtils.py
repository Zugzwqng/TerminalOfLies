#splits the string, but only into two parts. uses the first instance of delimiter
#returns True if the delimiter was found in the string
def splitOnce(mainString, delimiter, ignoreCase=False):
  mainStringLoweredIfApplicable = mainString
  if (ignoreCase):
    delimiter = delimiter.lower()
    mainStringLoweredIfApplicable = mainStringLoweredIfApplicable.lower()
  if mainStringLoweredIfApplicable.find(delimiter) == -1:
    return mainString, "", False
  delimiterIndex = mainStringLoweredIfApplicable.find(delimiter)
  return mainString[0:delimiterIndex], mainString[delimiterIndex + len(delimiter):], True

#returns mainString, but with all occurences of toSearchFor substituted with toReplaceWith
def replaceAll(mainString, toSearchFor, toReplaceWith, ignoreCase=False):
  splitString = mainString.split(toSearchFor)
  result = ""
  for piece in splitString:
    result = result + piece + toReplaceWith
  result = result[0:len(result) - len(toReplaceWith)]
  return result

#given a string, returns the section of the string that ^[0-9]* matches
#ie if there's a number at the start followed by non-numeric characters, returns the number
def cleanNumber(numString):
  numString = str(numString)
  for num in range(1, len(numString) + 1):
    try:
      test = int(numString[0:num])
    except:
      return int(numString[0:num - 1])
  return int(numString)