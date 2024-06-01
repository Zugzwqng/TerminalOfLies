import reads_list

import copy
import json

# @staticmethod
# def fromList(list: list[reads_list.ReadsList]):
#     result = ReadsListList()
#     result.reads_lists = list
#     return result

class ReadsListList:
    """
    Represents a list of reads lists.
    The internal list has elements of the form [ReadsList, name]. name is a string.
    """
    def __init__(self):
        self.reads_lists = []
    

    def getReadsList(self, name: str) -> reads_list.ReadsList | None:
        for list in self.reads_lists:
            if list[1].lower() == name.lower():
                return list[0]
        return None


    def swap(self, name1: str, name2: str) -> bool:
        index1 = self.getIndex(name1)
        index2 = self.getIndex(name2)
        if index1 == -1 or index2 == -1:
            return False
        if index1 > index2:
            temp = index1
            index1 = index2
            index2 = temp
        read2 = self.reads_lists.pop(index2)
        read1 = self.reads_lists.pop(index1)
        self.reads_lists.insert(index1, read2)
        self.reads_lists.insert(index2, read1)
        return True
    
    def create(self, name: str) -> bool:
        if self.contains(name):
            return False
        self.reads_lists.append([reads_list.ReadsList(), name])
        return True

    def contains(self, name: str) -> bool:
        return self.getIndex(name) != -1

    def rename(self, oldName: str, newName: str) -> bool:
        if self.contains(newName) or (not self.contains(oldName)):
            return False
        self.reads_lists[self.getIndex(oldName)][1] = newName
        return True

    def getIndex(self, name: str) -> int:
        names = self.listReadsLists()
        for num in range(len(names)):
            if names[num].lower() == name.lower():
                return num
        return -1

    def listReadsLists(self) -> list[str]:
        names = []
        for read_and_name in self.reads_lists:
            names.append(read_and_name[1])
        return names

    def delete_list(self, name: str) -> bool:
        try:
            self.reads_lists.pop(self.getIndex(name))
            return True
        except:
            return False
    
    def getNextDefaultName(self) -> str:
        takenNumbers = []
        for read_and_name in self.reads_lists:
            name = read_and_name[1]
            if name[0:7].lower() == "unnamed":
                try:
                    newNum = int(name[7:])
                    takenNumbers.append(newNum)
                except:
                    pass
        takenNumbers.sort()
        currentNum = 1
        while len(takenNumbers) > 0:
            if takenNumbers[0] != currentNum:
                break
            takenNumbers.pop(0)
            currentNum += 1
        return "unnamed" + str(currentNum)


    # def newEmptyList(self):
    #     self.reads_lists.append([reads_list.ReadsList(), self.getNextDefaultName()])
    
    def duplicateAndAddAtEnd(self, name: str, fullDuplicate=True) -> bool:
        index = self.getIndex(name)
        if index == -1:
            return False
        if fullDuplicate:
            self.newCopy(indexToClone=index)
        else:
            newList = self.reads_lists[index][0].lightCopy()
            self.reads_lists.append([newList, self.getNextDefaultName()])
        return True

    def newCopy(self, indexToClone=-1, indexToInsertAt=-1):
        indexToClone = indexToClone if indexToClone >=0 and indexToClone < len(self.reads_lists) else len(self.reads_lists) - 1
        indexToInsertAt = indexToInsertAt if indexToInsertAt >=0 and indexToInsertAt <= len(self.reads_lists) else len(self.reads_lists)
        newList = copy.deepcopy(self.reads_lists[indexToClone][0])
        self.reads_lists.append([newList, self.getNextDefaultName()])

    def getNumLists(self) -> int:
        return len(self.reads_lists)
    
    def toJSON(self):
        return json.dumps(self, default = lambda o : o.__dict__)
        