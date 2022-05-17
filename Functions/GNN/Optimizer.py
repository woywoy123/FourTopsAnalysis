import torch
from torch.utils.data import SubsetRandomSampler
from torch_geometric.loader import DataLoader
from torch_geometric.utils import accuracy

from sklearn.model_selection import KFold
import numpy as np

import time
from Functions.Tools.Alerting import Notification
from Functions.IO.Files import WriteDirectory, Directories
from Functions.IO.IO import PickleObject

class Optimizer(Notification):

    def __init__(self, DataLoaderInstance = None):
        self.Verbose = True
        Notification.__init__(self, self.Verbose)

        self.Caller = "OPTIMIZER"
        ### DataLoader Inheritence 
        if DataLoaderInstance != None:
            self.ReadInDataLoader(DataLoaderInstance)

        ### User defined ML parameters
        self.LearningRate = 0.001
        self.WeightDecay = 0.001
        self.kFold = 10
        self.Epochs = 10
        self.BatchSize = 10
        self.Model = None
        self.RunName = "UNTITLED"
        self.RunDir = "_Models"
        self.ONNX_Export = False
        self.TorchScript_Export = True

        ### Internal Stuff 
        self.Training = True
        self.Sample = None
        self.T_Features = {}
      
    def ReadInDataLoader(self, DataLoaderInstance):
        self.TrainingSample = DataLoaderInstance.TrainingSample

        self.EdgeFeatures = DataLoaderInstance.EdgeAttribute
        self.NodeFeatures = DataLoaderInstance.NodeAttribute
        self.GraphFeatures = DataLoaderInstance.GraphAttribute

        self.Device_S = DataLoaderInstance.Device_S
        self.Device = DataLoaderInstance.Device
        self.DataLoader = DataLoaderInstance

    def DumpStatistics(self):
        WriteDirectory().MakeDir(self.RunDir + "/" + self.RunName + "/Statistics")
        if self.epoch == "Done":
            PickleObject(self.Stats, "Stats_" + self.epoch, self.RunDir + "/" + self.RunName + "/Statistics")
        else:
            PickleObject(self.Stats, "Stats_" + str(self.epoch+1), self.RunDir + "/" + self.RunName + "/Statistics")
        self.MakeStats()

    def MakeStats(self):

        ### Output Information
        self.Stats = {}
        self.Stats["EpochTime"] = []
        self.Stats["BatchRate"] = []
        self.Stats["kFold"] = []
        self.Stats["FoldTime"] = []
        self.Stats["Nodes"] = []

        self.Stats["Training_Accuracy"] = {}
        self.Stats["Validation_Accuracy"] = {}
        self.Stats["Training_Loss"] = {}
        self.Stats["Validation_Loss"] = {}

        for i in self.T_Features:
            self.Stats["Training_Accuracy"][i] = []
            self.Stats["Validation_Accuracy"][i] = []
            self.Stats["Training_Loss"][i] = []
            self.Stats["Validation_Loss"][i] = []

    def __GetFlags(self, inp, FEAT):
        if FEAT == "M":
            self.ModelInputs = list(self.Model.forward.__code__.co_varnames[:self.Model.forward.__code__.co_argcount])
            self.ModelInputs.remove("self")
            if len(list(set(list(inp.__dict__["_store"])).intersection(set(self.ModelInputs)))) < len(self.ModelInputs):
                
                self.Warning("---> ! Features Expected in Model Input ! <---")
                for i in self.ModelInputs:
                    self.Warning("+-> " + i)
                
                self.Warning("---> ! Features Found in Sample Input ! <---")
                for i in list(inp.__dict__["_store"]):
                    self.Warning("+-> " + i)
                
                self.Fail("MISSING VARIABLES IN GIVEN DATA SAMPLE")

            self.Notify("FOUND ALL MODEL INPUT PARAMETERS IN SAMPLE")
            for i in self.ModelInputs:
                self.Notify("---> " + i)

            Setting = [i for i in self.Model.__dict__ if i.startswith("C_") or i.startswith("L_") or i.startswith("O_") or i.startswith("N_")]
            self.ModelOutputs = {}
            for i in Setting:
                self.ModelOutputs[i] = self.Model.__dict__[i]
            return
            
        for i in inp:
            if i.startswith("T_"):
                self.T_Features[i[2:]] = [FEAT + "_" +i, FEAT + "_" +i[2:]]

    def __ExportONNX(self, DummySample, Name):
        import onnx
        
        DummySample = tuple([DummySample[i] for i in self.ModelInputs])
        torch.onnx.export(
                self.Model, DummySample, Name,
                export_params = True, 
                input_names = self.ModelInputs, 
                output_names = [i for i in self.ModelOutputs if i.startswith("O_")])

   
    def __ExportTorchScript(self, DummySample, Name):
        DummySample = tuple([DummySample[i] for i in self.ModelInputs])
      
        Compact = {}
        for i in self.ModelInputs:
            Compact[i] = str(self.ModelInputs.index(i))

        p = 0
        for i in self.ModelOutputs:
            if i.startswith("O_"):
                Compact[i] = str(p)
                p+=1
            else:
                Compact[i] = str(self.ModelOutputs[i])

        model = torch.jit.trace(self.Model, DummySample)
        torch.jit.save(model, Name, _extra_files = Compact)

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
    
    def __SaveModel(self, DummySample):
        self.Model.eval()
        DummySample = [i for i in DummySample][0]
        DummySample = DummySample.to_data_list()[0].detach().to_dict()
        DirOut = self.RunDir + "/" + self.RunName + "/"
        if self.ONNX_Export:
            WriteDirectory().MakeDir(DirOut + "ModelONNX")
            Name = DirOut + "ModelONNX/Epoch_" + str(self.epoch+1) + "_" + str(self.Epochs) + ".onnx"
            self.__ExportONNX(DummySample, Name)
        
        if self.TorchScript_Export:
            WriteDirectory().MakeDir(DirOut + "ModelTorchScript")
            Name = DirOut + "ModelTorchScript/Epoch_" + str(self.epoch+1) + "_" + str(self.Epochs) + ".pt"
            self.__ExportTorchScript(DummySample, Name)

    def DefineOptimizer(self):
        self.Model.to(self.Device)
        #self.Optimizer = torch.optim.Adam(self.Model.parameters(), lr = self.LearningRate, weight_decay = self.WeightDecay)
        self.Optimizer = torch.optim.SGD(self.Model.parameters(), lr = self.LearningRate)

    def DefineLossFunction(self, LossFunction):
        if LossFunction == "CEL":
            self.LF = torch.nn.CrossEntropyLoss()
        elif LossFunction == "MSEL":
            self.LF = torch.nn.MSELoss()
   
    def MakePrediction(self, sample, TargetAttribute, Classification, Topology):
        
        dr = {}
        for i in self.ModelInputs:
            dr[i] = sample[i]
        self.Model(**dr)
        pred  = self.Model.__dict__[TargetAttribute]

        if Topology:
            pred = pred[sample.edge_index[0]]

        if Classification:
            _, p = pred.max(1)
            p = p.view(1, -1)[0]
        else:
            pred = pred.view(1, -1)[0]
            p = torch.round(pred, decimals=3)
        
        return pred, p

    def Train(self, sample):
        for key in self.T_Features:
            if self.Training:
                self.Model.train()
                self.Optimizer.zero_grad()
            else:
                self.Model.eval()

            key_t = self.T_Features[key][0]
            key_o = "O_" + key
            key_l = self.Model.__dict__["L_" + key]
            key_c = self.Model.__dict__["C_" + key]

            if "N_" + key in self.Model.__dict__:
                key_n = self.Model.__dict__["N_" + key]
            else:
                key_n = False

            self.DefineLossFunction(key_l)
            
            pred, p = self.MakePrediction(sample, key_o, key_c, key_n) 

            if key_l == "CEL":
                truth = sample[key_t].type(torch.LongTensor).to(self.Device).view(1, -1)[0]

            elif key_l == "MSEL":
                truth = sample[key_t].type(torch.float).to(self.Device).view(1, -1)[0]
            
            self.L = self.LF(pred, truth)
            acc = accuracy(p, truth)
            
            if self.Training:
                self.Stats["Training_Accuracy"][key][-1].append(acc)
                self.Stats["Training_Loss"][key][-1].append(self.L)
            else:
                self.Stats["Validation_Accuracy"][key][-1].append(acc)
                self.Stats["Validation_Loss"][key][-1].append(self.L)
            
            if self.Training:
                self.L.backward()
                self.Optimizer.step()



    def SampleLoop(self, samples):
        self.ResetAll() 
        self.len = len(samples.dataset)
        R = []
        for i in samples:
            if self.Training:
                self.ProgressInformation("TRAINING")
            else:
                self.ProgressInformation("VALIDATING")
            self.Train(i) 
            R.append(self.Rate)
        if self.AllReset:
            self.Stats["BatchRate"].append(R)

    def KFoldTraining(self):
        def CalcAverage(Mode, k):
            for f_k in self.Stats[Mode]:
                v = round(float(sum(self.Stats[Mode][f_k][k])/len(self.Stats[Mode][f_k][k])), 3)
                self.Notify("-- (" + f_k + ") -> " + Mode.split("_")[1] + ": " + str(v))

        self.DefineOptimizer()
        Splits = KFold(n_splits = self.kFold, shuffle = True, random_state= 42)
        N_Nodes = list(self.TrainingSample)
        N_Nodes.sort(reverse = True)
        self.__GetFlags(self.EdgeFeatures, "E")
        self.__GetFlags(self.NodeFeatures, "N")
        self.__GetFlags(self.GraphFeatures, "G")
        self.__GetFlags(self.TrainingSample[N_Nodes[0]][0], "M")

        self.MakeStats()
        self.Model.Device = self.Device_S
        
        TimeStart = time.time()
        for self.epoch in range(self.Epochs):
            self.Notify(" >============== [ EPOCH (" + str(self.epoch+1) + "/" + str(self.Epochs) + ") ] ==============< ")
            
            TimeStartEpoch = time.time()
            k = 0
            for n_node in N_Nodes:
                Curr = self.TrainingSample[n_node]
                Curr_l = len(Curr)
                self.Notify("+++++++++++++++++++++++")
                self.Notify("NUMBER OF NODES -----> " + str(n_node) + " NUMBER OF ENTRIES: " + str(Curr_l))

                if Curr_l < self.kFold:
                    self.Warning("NOT ENOUGH SAMPLES FOR EVENTS WITH " + str(n_node) + " PARTICLES :: SKIPPING")
                    continue

                self.Stats["FoldTime"].append([])
                self.Stats["kFold"].append([])
                for fold, (train_idx, val_idx) in enumerate(Splits.split(np.arange(Curr_l))):

                    for f in self.T_Features:
                        self.Stats["Training_Accuracy"][f].append([])
                        self.Stats["Validation_Accuracy"][f].append([])
                        self.Stats["Training_Loss"][f].append([])
                        self.Stats["Validation_Loss"][f].append([])

                    TimeStartFold = time.time()
                    self.Notify("CURRENT k-Fold: " + str(fold+1))

                    train_loader = DataLoader(Curr, batch_size = self.BatchSize, sampler = SubsetRandomSampler(train_idx))
                    valid_loader = DataLoader(Curr, batch_size = self.BatchSize, sampler = SubsetRandomSampler(val_idx)) 
                    self.Notify("-------> Training <-------")
                    self.Training = True
                    self.SampleLoop(train_loader)
                    CalcAverage("Training_Accuracy", k)
                    CalcAverage("Training_Loss", k)


                    self.Notify("-------> Validation <-------")
                    self.Training = False
                    self.SampleLoop(valid_loader)
                    CalcAverage("Validation_Accuracy", k)
                    CalcAverage("Validation_Loss", k)

                    self.Stats["FoldTime"][-1].append(time.time() - TimeStartFold)
                    self.Stats["kFold"][-1].append(fold+1)

                    k += 1



                self.Stats["Nodes"].append(n_node)

            self.Stats["EpochTime"].append(time.time() - TimeStartEpoch)
            self.DumpStatistics()
            self.__SaveModel(train_loader)

        self.Stats["TrainingTime"] = time.time() - TimeStart
        self.Stats.update(self.DataLoader.FileTraces)
        
        ix = 0
        self.Stats["n_Node_Files"] = [[]]
        self.Stats["n_Node_Count"] = [[]]
        for i in self.TrainingSample:
            for j in self.TrainingSample[i]:
                indx, n_nodes = j.i, j.num_nodes
                start, end = self.Stats["Start"][ix], self.Stats["End"][ix]
                if start <= indx and indx <= end:
                    pass
                else:
                    self.Stats["n_Node_Files"].append([])
                    self.Stats["n_Node_Count"].append([])
                    ix += 1

                if n_nodes not in self.Stats["n_Node_Files"][ix]:
                    self.Stats["n_Node_Files"][ix].append(n_nodes)
                    self.Stats["n_Node_Count"][ix].append(0)
                
                n_i = self.Stats["n_Node_Files"][ix].index(n_nodes)
                self.Stats["n_Node_Count"][ix][n_i] += 1
        self.Stats["BatchSize"] = self.BatchSize
        self.Stats["Model"] = {}
        self.Stats["Model"]["LearningRate"] = self.LearningRate
        self.Stats["Model"]["WeightDecay"] = self.WeightDecay
        self.Stats["Model"]["ModelFunctionName"] = str(type(self.Model))
        self.epoch = "Done"
        self.DumpStatistics()

