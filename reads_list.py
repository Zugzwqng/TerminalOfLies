import read

class ReadsList:
    def __init__(self):
        self.miscthoughts = read.Read('Misc Thoughts', '', []) #note that 'Misc Thoughts' has a space, and therefore can't be a username
        self.reads = [self.miscthoughts]
        self.reads.pop() #type checking fix
    



    

    def changeTier(self, player: str, newTier: str, tiersList: list[str]) -> bool:
        read = self.getRead(player)
        if read == None:
            return False
        read.tier = newTier
        tiersList = list(map(lambda input : input.lower(), tiersList))
        if newTier.lower() not in tiersList:
            return True

        index = self.getPlayerIndex(player)
        self.reads.pop(index)
        newTierIndex = tiersList.index(read.tier.lower())
        for num in range(len(self.reads)):
            currentTierIndex = tiersList.index(self.reads[num].tier.lower())
            if currentTierIndex != -1 and currentTierIndex > newTierIndex:
                self.reads.insert(num, read)
                return True
        self.reads.append(read)
        return True

    def getPlayerIndex(self, playername: str) -> int:
        for num in range(len(self.reads)):
            if self.reads[num].player.lower() == playername.lower():
                return num
        return -1

    def getRead(self, playername: str):
        index = self.getPlayerIndex(playername)
        return (None if index == -1 else self.reads[index])
    
    def getReadIndex(self, index: int):
        return (None if index < 0 or index >= len(self.reads) else self.reads[index])
    
    def removeRead(self, playername: str) -> bool:
        index = self.getPlayerIndex(playername)
        if index == -1:
            return False
        self.reads.pop(index)
        return True

    def addThought(self, player: str, thought: str, index=-1) -> bool:
        readObject = self.getRead(player)
        if readObject == None:
            return False
        readObject.addThought(thought, index)
        return True
    
    def removeThought(self, player: str, index: int) -> bool:
        read = self.getReadIndex(index)
        if read == None:
            return False
        read.deleteThought(index)
        return True

    def mergeReads(self, name1: str, name2: str) -> bool:
        read1 = self.getRead(name1)
        read2 = self.getRead(name2)
        if read1 != None and read2 != None:
            read1.mergeReads(read2)
            self.removeRead(name2)
            return True
        return False
        
    def addPlayer(self, playername: str) -> bool:
        if self.containsPlayer(playername):
            return False
        newRead = read.Read(playername, "null", [])
        self.reads.append(newRead)
        return True

    def containsPlayer(self, playername: str) -> bool:
        return self.getRead(playername) != None

    def swapPlayer(self, playername1: str, playername2: str) -> bool:
        index1 = self.getPlayerIndex(playername1)
        index2 = self.getPlayerIndex(playername2)
        if index1 == -1 or index2 == -1:
            return False
        if index1 > index2:
            temp = index1
            index1 = index2
            index2 = temp
        read2 = self.reads.pop(index2)
        read1 = self.reads.pop(index1)
        self.reads.insert(index1, read2)
        self.reads.insert(index2, read1)
        return True
    
    def renamePlayer(self, originalName: str, newName: str) -> bool:
        read = self.getRead(originalName)
        if read == None:
            return False
        read.player = newName
        return True

    
    def lightCopy(self):
        """Returns a copy of the ReadsList, but with no thoughts."""
        result = ReadsList()
        for readToCopy in self.reads:
            result.reads.append(read.Read(readToCopy.player, readToCopy.tier, []))
        return result
    
    def toString(self, withoutThoughts=False, spoileredThoughts=False, tabbedThoughts=True, showHidden=True) -> str:
        result = ""
        for num in range(len(self.reads)):
            result += self.reads[num].toString(withoutThoughts=withoutThoughts, spoileredThoughts=spoileredThoughts, tabbedThoughts=tabbedThoughts, showHidden=showHidden)
            if num != len(self.reads) - 1 and self.reads[num].tier != self.reads[num + 1].tier: #add spacing between tiers
                result += "\n"
                if spoileredThoughts:
                    result += "<b></b>\n"
        if not withoutThoughts:
            self.miscthoughts.toString(withoutThoughts=False, spoileredThoughts=spoileredThoughts, tabbedThoughts=tabbedThoughts, showHidden=showHidden)
        return result

    def withoutThoughts(self) -> str:
        result = ""
        for read in self.reads:
            result += read.withoutThoughts()
        return result

    def stringToPrintToTerminal(self) -> str:
        result = ""
        for read in self.reads:
            result += read.printToTerminalString() + "\n"
        if len(self.miscthoughts.thoughts) > 0:
            result += "\n" + self.miscthoughts.printToTerminalString()
        return result

    def __str__(self) -> str:
        result = ""
        for read in self.reads:
            result += str(read) + "\n"
        if len(self.miscthoughts.thoughts) > 0:
            result += "\n" + str(self.miscthoughts)
        return result
    
