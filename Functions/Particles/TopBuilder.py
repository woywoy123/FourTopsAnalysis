from Functions.GNN.Optimizer import ModelImporter
from Functions.Tools.Alerting import Notification
from torch_geometric.data import Batch
from torch_geometric.utils import get_laplacian, subgraph, to_dense_adj, dense_to_sparse
import torch 
import LorentzVector as LV

class ParticleReconstructor(ModelImporter, Notification):
    def __init__(self, Model, Sample):
        Notification.__init__(self)
        self.VerboseLevel = 0
        self.Caller = "ParticleReconstructor"
        self.TruthMode = False
        
        if Sample.is_cuda:
            self.Device = "cuda"
        else:
            self.Device = "cpu"
        self.Model = Model
        self.Sample = Sample
        self.InitializeModel()
    
    def Prediction(self):
        if self.TruthMode:
            self.__Results = self.Sample
            self.Warning("USING THE TRUTH SETTING!")
        else:
            self.Model.eval()
            self.MakePrediction(Batch.from_data_list([self.Sample]))
            self.__Results = self.Output(self.ModelOutputs, self.Sample) 
            self.__Results = { i : self.__Results[i][0] for i in self.__Results}

    def MassFromNodeFeature(self, TargetFeature, pt = "N_pt", eta = "N_eta", phi = "N_phi", e = "N_energy"):
        edge_index = self.Sample.edge_index

        # Get the prediction of the sample 
        pred = self.__Results[TargetFeature].to(dtype = int).view(1, -1)[0]
        
        # Filter out the nodes which are not equally valued and apply masking
        mask = pred[edge_index[0]] == pred[edge_index[1]]

        # Only keep nodes of the same classification 
        edge_index_s = edge_index[0][mask == True]
        edge_index_r = edge_index[1][mask == True]
        edge_index = torch.cat([edge_index_s, edge_index_r]).view(2, -1)
        
        # Create a classification matrix nclass x nodes 
        clf = torch.zeros((len(torch.unique(pred)), len(pred)), device = edge_index.device)
        idx = torch.cat([pred[edge_index[0]], edge_index[0]], dim = 0).view(2, -1)
        clf[idx[0], idx[1]] += 1

        # Convert the sample kinematics into cartesian and perform a vector aggregation 
        FV = torch.cat([self.Sample[pt], self.Sample[eta], self.Sample[phi], self.Sample[e]], dim = 1)
        FV = LV.TensorToPxPyPzE(FV)        
        pt_ = torch.mm(clf, FV[:, 0].view(-1, 1))
        eta_ = torch.mm(clf, FV[:, 1].view(-1, 1))
        phi_ = torch.mm(clf, FV[:, 2].view(-1, 1))
        e_ = torch.mm(clf, FV[:, 3].view(-1, 1))
        FourVec = torch.cat([pt_, eta_, phi_, e_], dim = 1)
        return LV.MassFromPxPyPzE(FourVec)/1000
 
    def MassFromFeatureEdges(self, TargetFeature, pt = "N_pt", eta = "N_eta", phi = "N_phi", e = "N_energy"):
        edge_index = self.Sample.edge_index

        # Get the prediction of the sample and extract from the topology the number of unique classes
        adj = self.__Results[TargetFeature].to(dtype = int).view(1, -1)[0].view(-1, self.Sample.num_nodes)
        edge_index, weights = dense_to_sparse(adj)
        nodes = edge_index[0].unique().view(-1, 1).to(dtype = torch.float)
        
        #Apply the mapping between clusters and index of class
        mapping = torch.mm(adj.to(dtype = torch.float), nodes.to(dtype = torch.float))
        classes = mapping.unique().sort()
        mapping = classes[1][(mapping[:, :] == classes[0]).nonzero(as_tuple = True)[1]]

        # Create a classification matrix nclass x nodes 
        clf = torch.zeros((len(classes[1]), len(nodes.t()[0])), device = edge_index.device)
        idx = torch.cat([mapping[edge_index[0]], edge_index[0]], dim = 0).view(2, -1)
        clf[idx[0], idx[1]] += 1

        # Convert the sample kinematics into cartesian and perform a vector aggregation 
        FV = torch.cat([self.Sample[pt], self.Sample[eta], self.Sample[phi], self.Sample[e]], dim = 1)
        FV = LV.TensorToPxPyPzE(FV)        
        pt_ = torch.mm(clf, FV[:, 0].view(-1, 1))
        eta_ = torch.mm(clf, FV[:, 1].view(-1, 1))
        phi_ = torch.mm(clf, FV[:, 2].view(-1, 1))
        e_ = torch.mm(clf, FV[:, 3].view(-1, 1))
        FourVec = torch.cat([pt_, eta_, phi_, e_], dim = 1)
        return LV.MassFromPxPyPzE(FourVec)/1000
        
       

