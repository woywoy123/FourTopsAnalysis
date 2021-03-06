import torch
import onnx
import numpy as np
import string
from Functions.IO.Files import WriteDirectory
from Functions.IO.IO import HDF5
from Functions.Tools.Alerting import Notification
import Functions


class ExportToDataScience(WriteDirectory):
    def __init__(self):
        Notification.__init__(self)

    def ExportModel(self, Sample):
        WriteDirectory.__init__(self)
        self.__EpochDir = "/Epoch_" + str(self.epoch+1) + "_" + str(self.Epochs)
        if self.RunDir == None:
            self.__OutputDir = self.RunName + "/"
        else:
            self.__OutputDir = self.RunDir + "/" + self.RunName + "/"       
        self.__Sample = Sample 
       
        self.__InputMap = {}
        for i in self.ModelInputs:
            self.__InputMap[i] = str(self.ModelInputs.index(i))

        self.__OutputMap = {}
        for i in self.ModelOutputs:
            self.__OutputMap[i] = str(self.ModelOutputs[i]) + "->" + str(type(self.ModelOutputs[i])).split("'")[1]
        
        try:
            self.__Sample = [i for i in self.__Sample][0].to_data_list()[0].detach().to_dict()
        except AttributeError:
            self.__Sample.detach().to_dict()

        self.__Sample = [self.__Sample[i] for i in self.__InputMap]
        self.Model.eval()
        self.Model.requires_grad_(False)
        if self.ONNX_Export:
            try:
                self.__ExportONNX( self.__OutputDir + "ONNX" + self.__EpochDir + ".onnx")
            except:
                self.Warning("FAILED TO EXPORT AS ONNX.")

        if self.TorchScript_Export:
            try:
                self.__ExportTorchScript( self.__OutputDir + "TorchScript" + self.__EpochDir + ".pt")
            except:
                self.Warning("FAILED TO EXPORT AS TORCH SCRIPT")

        self.Model.requires_grad_(True)

    def __ExportONNX(self, Dir):
        self.MakeDir("/".join(Dir.split("/")[:-1]))
        
        torch.onnx.export(
                self.Model, 
                tuple(self.__Sample), 
                Dir, 
                verbose = False,
                export_params = True, 
                opset_version = 14,
                input_names = list(self.__InputMap), 
                output_names = [i for i in self.__OutputMap if i.startswith("O_")])

    def __ExportTorchScript(self, Dir):
        self.MakeDir("/".join(Dir.split("/")[:-1]))
        model = torch.jit.trace(self.Model, self.__Sample)
        torch.jit.save(model, Dir, _extra_files = self.__OutputMap)

    def __Routing(self, inp, MemoryLink):
        if "Functions." in type(inp).__module__ and MemoryLink != True:
            out = str(hex(id(inp)))
            MemoryLink[out] = inp
            self.__SearchObject(inp, MemoryLink)
            return out

        elif "torch_geometric." in type(inp).__module__ and MemoryLink != True:
            out = str(hex(id(inp)))
            MemoryLink[out] = inp
            self.__SearchObject(inp, MemoryLink)
            return out

        elif isinstance(inp, str) and MemoryLink == True:
            if inp.startswith("0x"):
                return self._MemoryLink[inp]

        x = self.__RecursiveDict(inp, MemoryLink)
        if x != None:
            return x

        x = self.__RecursiveList(inp, MemoryLink)           
        if x != None:
            return x
 
    def __RecursiveList(self, lst, MemoryLink):
        if isinstance(lst, list) == False: 
            return None 
        val = [self.__Routing(i, MemoryLink) for i in lst]
        val = [i for i in val if i != None]
        if len(val) != 0:
            return val

    def __RecursiveDict(self, dct, MemoryLink):
        if isinstance(dct, dict) == False:
            return None
        val = {i : self.__Routing(j, MemoryLink) for i, j in dct.items()}
        val = {i : j for i, j in val.items() if j != None}
        if len(val) != 0:
            return val

    def __SearchObject(self, SourceObject, MemoryLink):
        for key, val in SourceObject.__dict__.items():
            l = self.__RecursiveDict(val, MemoryLink)
            if l != None:
                SourceObject.__dict__[key] = l
                continue
            p = self.__RecursiveList(val, MemoryLink)
            if p != None:
                SourceObject.__dict__[key] = p

    def ExportEventGenerator(self, EventGenerator, Name = "UNTITLED", OutDirectory = "_Pickle"):
        self.__ResetAll() 

        self.__SearchObject(EventGenerator, self._MemoryLink)      
        self.__Dump = HDF5(OutDirectory, Name, Chained = True)
        self.__Dump.StartFile()
        ev = 0
        for i in self._MemoryLink:
            obj = self._MemoryLink[i]
            if "Event" in type(obj).__name__:
                self.Notify("!!!Dumped Event " + str(ev +1) + "/" + str(len(EventGenerator.Events)))
                self.__Dump.SwitchFile()
                ev+=1
            self.__Dump.DumpObject(obj)
        self.__Dump.DumpObject(EventGenerator)
        self.__Dump.EndFile()

    def ImportEventGenerator(self, Name = "UNTITLED", InputDirectory = "_Pickle"):
        self.__ResetAll() 

        self.__Collect = HDF5(Chained = True)
        self._MemoryLink = self.__Collect.OpenFile(InputDirectory, Name) 
        
        ObjectDict = {}
        for addr in self._MemoryLink:
            i = self._MemoryLink[addr]
            self.__SearchObject(i, True)
            x = str(type(i).__name__)
            if x not in ObjectDict:
                ObjectDict[x] = []
            ObjectDict[x].append(i)

        Events = ObjectDict["EventGenerator"][0].Events
        ObjectDict["EventGenerator"][0].Events = {ev : Events[ev] for ev in sorted(Events)}
        return ObjectDict["EventGenerator"][0]

    def ExportDataGenerator(self, DataGenerator, Name = "UNTITLED", OutDirectory = "_Pickle"):
        self.__ResetAll() 
        
        for i in DataGenerator.EdgeAttribute:
            DataGenerator.EdgeAttribute[i] = str(DataGenerator.EdgeAttribute[i]).split(" ")[1]

        for i in DataGenerator.NodeAttribute:
            DataGenerator.NodeAttribute[i] = str(DataGenerator.NodeAttribute[i]).split(" ")[1]

        for i in DataGenerator.GraphAttribute:
            DataGenerator.GraphAttribute[i] = str(DataGenerator.GraphAttribute[i]).split(" ")[1]

        DataGenerator.SetDevice("cpu")
        DataGenerator.EventGraph = ""
        self.__SearchObject(DataGenerator, self._MemoryLink)
        
        self.__Dump = HDF5(OutDirectory, Name, Chained = True)
        self.__Dump.StartFile()
        for i in self._MemoryLink:
            obj = self._MemoryLink[i]
            self.__Dump.DumpObject(obj)
            self.Notify("!!!Dumped Event " +  str(int(obj.i)+1) + "/" + str(len(self._MemoryLink)))
            self.__Dump.SwitchFile()
        self.__Dump.DumpObject(DataGenerator)
        self.__Dump.EndFile()
    

    def ImportDataGenerator(self, Name = "UNTITLED", InputDirectory = "_Pickle"):
        self.__ResetAll() 
        self.__Collect = HDF5(Chained = True)
        self._MemoryLink = self.__Collect.OpenFile(SourceDir = InputDirectory, Name = Name)
        
        Obj = {}
        for i, j in self._MemoryLink.items():
            self.__SearchObject(j, True)
            name = type(j).__name__
            if name not in Obj:
                Obj[name] = []
            Obj[name].append(j)

        con = Obj["GenerateDataLoader"][0].DataContainer
        Obj["GenerateDataLoader"][0].DataContainer = {i : con[i] for i in sorted(con)}
        Obj["GenerateDataLoader"][0].SetDevice("cuda")

        return Obj["GenerateDataLoader"][0]

    def ExportEventGraph(self, EventGraph, Name, OutDirectory):
        self.__ResetAll()
        self.__Dump = HDF5(OutDirectory, Name)
        self.__Dump.VerboseLevel = self.VerboseLevel
        self.__Dump.StartFile()
        self.__Dump.DumpObject(EventGraph)
        self.__Dump.EndFile()
    
    def ImportEventGraph(self, Name, InputDirectory):
        self.__ResetAll()
        self.__Collect = HDF5()
        self.__Collect.VerboseLevel = self.VerboseLevel
        self.__Collect.OpenFile(InputDirectory, Name)
        return self.__Collect.RebuildObject()

    def __ResetAll(self):
        self._MemoryLink = {}
        self.__Collect = None
        self.__Dump = None





"""

class Model:
    def __init__(self, dict_in, model):
        self.__Model = model
        self.__router = {}
        for i in dict_in:
            setattr(self, i, dict_in[i])
            if i.startswith("O_"):
                self.__router[dict_in[i]] = i         
    
    def __call__(self, **kargs):
        pred = list(self.__Model(**kargs))
        for i in range(len(pred)):
            setattr(self, self.__router[i], pred[i])

    def train(self):
        self.__Model.train(True)

    def eval(self):
        self.__Model.train(False)


    def __ImportTorchScript(self, Name):
        class Model:
            def __init__(self, dict_in, model):
                self.__Model = model
                self.__router = {}
                for i in dict_in:
                    setattr(self, i, dict_in[i])
                    if i.startswith("O_"):
                        self.__router[dict_in[i]] = i         
            
            def __call__(self, **kargs):
                pred = list(self.__Model(**kargs))
                for i in range(len(pred)):
                    setattr(self, self.__router[i], pred[i])

            def train(self):
                self.__Model.train(True)

            def eval(self):
                self.__Model.train(False)
        
        extra_files = {}
        for i in list(self.ModelOutputs):
            extra_files[i] = ""
        for i in list(self.ModelInputs):
            extra_files[i] = ""
        
        M = torch.jit.load(Name, _extra_files = extra_files)
        for i in extra_files:
            conv = str(extra_files[i].decode())
            if conv.isnumeric():
                conv = int(conv)
            if conv == "True":
                conv = True
            if conv == "False":
                conv = False
            extra_files[i] = conv
         
        self.Model = Model(extra_files, M)

"""
