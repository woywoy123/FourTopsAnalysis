import torch

class VariableManager:

    def __init__(self):
        pass

    def ListAttributes(self):
        self.Leaves = []
        for i in list(self.__dict__.values()):
            if isinstance(i, str) and i != "" and i != self.Type:
                self.Leaves.append(i)

    def SetAttribute(self, key, val):
        setattr(self, key, val)

    def CompileKeyMap(self):
        self.KeyMap = {}
        for i in self.__dict__.keys():
            val = self.__dict__[i]
            if isinstance(val, str) and self.Type != val:
                self.KeyMap[val] = i

    def GetAttributeFromKeyMap(self, key):
        obj = getattr(self, self.KeyMap[key])
        return obj
    
    def ClearVariable(self):
        del self.Leaves 
        del self.KeyMap

    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if self.__dict__.items() != other.__dict__.items():
            return False

        for k, j in zip(self.__dict__.keys(), other.__dict__.keys()):
            if k != j:
                return False
            
            if type(self.__dict__[k]) != type(other.__dict__[j]):
                return False
            
            if isinstance(self.__dict__[k], torch.Tensor):
                if torch.equal(self.__dict__[k], other.__dict__[j]):
                    continue
            
            if self.__dict__[k] != other.__dict__[j]:
                return False
        return True


def RecallObjectFromString(string):
    import importlib
    mod = importlib.import_module(".".join(string.split(".")[:-1]))
    Reco = getattr(mod, string.split(".")[-1])
    
    if Reco.__init__.__defaults__ == None:
        return Reco()

    def_inp = list(Reco.__init__.__defaults__)
    inp = list(Reco.__init__.__code__.co_varnames)
    inp.remove("self")
    
    l = {i : None for i in inp}
    
    inp.reverse()
    def_inp.reverse()

    for i, j in zip(inp, def_inp):
        l[i] = j
    
    return Reco(**l)
