class Read:
    def __init__(self, player: str, tier: str, thoughts: list[str]):
        self.player = player
        self.tier = tier
        self.thoughts = thoughts

    def deleteThought(self, index: int) -> bool:
        """
        Removes a thought by index. If the index is invalid, nothing happens.
        Returns True iff the thought was succesfully removed.
        """
        try:
            self.thoughts.pop(index)
            return True
        except:
            return False
            
    def addThought(self, thought: str, index=-1) -> bool:
        """
        Adds a thought at the specified index, or at the end if no index is provided.
        If the index is invalid, the thought is not added.
        Returns True iff the thought was successfully added.
        """
        if index == -1:
            self.thoughts.append(thought)
            return True
        try:
            self.thoughts.insert(index, thought)
            return True
        except:
            return False
            
    def changeTier(self, newTier: str):
        self.tier = newTier

    def withoutThoughts(self) -> str:
        return f"{self.player} - {self.tier}" + "\n"

    def __str__(self) -> str:
        result = f"{self.player} - {self.tier}"
        for num in range(len(self.thoughts)):
            result += f"\n{num}. " + self.thoughts[num]
        return result + "\n"
    
    def mergeReads(self, other):
        if type(other) != Read:
            raise Exception
        for thought in other.thoughts:
            self.thoughts.append(thought)

    def printToTerminalString(self):
        result = f"{self.player} - {self.tier}"
        for num in range(len(self.thoughts)):
            result += f"\n{num}. " + self.thoughts[num].replace("\n", "\n\t")
        return result + "\n"
    
    def toString(self, withoutThoughts=False, spoileredThoughts=False, tabbedThoughts=False, showHidden=True) -> str:
        result = f"{self.player} - {self.tier}\n"
        newline = "\n" #escape sequences are not allowed in f-string expressions before python 3.12
        if not withoutThoughts:
            if spoileredThoughts:
                result = f'[details="{result.replace(newline, "")}"]\n'
            for num in range(len(self.thoughts)):
                thought = self.thoughts[num]
                if not showHidden and len(thought) >= 8 and thought.lower().find(r"{hidden}") != -1:
                    continue
                while len(thought) > 0 and thought[0] == "\n":
                    thought = thought[1:]
                thought = thought if not tabbedThoughts else thought.replace("\n", "\n\t")
                result += f"\n{num}. " + thought + "\n"
            if spoileredThoughts:
                result += '[/details]\n'
            result += "\n"
            
        return result
