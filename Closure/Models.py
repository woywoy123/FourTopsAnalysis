from Functions.GNN.Graphs import GenerateDataLoader
from Functions.GNN.Optimizer import Optimizer
from Functions.GNN.Metrics import EvaluationMetrics
from Functions.IO.IO import UnpickleObject, PickleObject
from Functions.GNN.Models import EdgeConv, GCN, InvMassGNN

def GenerateTemplate():
    def eta(a):
        return float(a.eta)
    def energy(a):
        return float(a.e)
    def pt(a):
        return float(a.pt)
    def phi(a):
        return float(a.phi)
    def Signal(a):
        return int(a.Signal)

    ev = UnpickleObject("SignalSample.pkl")
    Loader = GenerateDataLoader()
    Loader.AddNodeFeature("e", energy)
    Loader.AddNodeFeature("eta", eta)
    Loader.AddNodeFeature("pt", pt)
    Loader.AddNodeFeature("phi", phi)
    Loader.AddNodeTruth("y", Signal)

    Loader.AddSample(ev, "nominal", "TruthChildren_init")
    Loader.ToDataLoader()
    
    for i in Loader.EventData:
        ev = Loader.EventData[i]
        for k in ev:
            PickleObject(k, "Nodes_" + str(i) + ".pkl")
            break


def ExampleEventGraph():
    # Different features to include as node and edges
    def eta(a):
        return float(a.eta)
    def energy(a):
        return float(a.e)
    def pt(a):
        return float(a.pt)
    def phi(a):
        return float(a.phi)
    def d_r(a, b):
        return float(a.DeltaR(b))
    def Signal(a):
        return int(a.Index)
    
    #GenerateTemplate()
    event = UnpickleObject("Nodes_10.pkl")

    event.SetNodeAttribute("e", energy)
    event.SetNodeAttribute("eta", eta)
    event.SetNodeAttribute("pt", pt)
    event.SetNodeAttribute("phi", phi)
    event.SetNodeAttribute("y", Signal)
    event.SetEdgeAttribute("d_r", d_r)
    event.ConvertToData()


    print("Number of Nodes: ", len(event.Nodes), "Number of Edges: ", len(event.Edges))
    return event


def TestEdgeConvModel():
    
    event1 = ExampleEventGraph()

    Data1 = event1.Data
    Map1 = event1.NodeParticleMap

    Op = Optimizer({}, Debug = True)
    Op.Model = EdgeConv(4, 2)
    Op.DefineOptimizer()
    Op.sample = Data1
    
    for i in range(10):
        Op.TrainClassification()
        print(Op.L)

    return True

def TestGCNModel():
    
    event1 = ExampleEventGraph()
    print("Number of Nodes: ", len(event1.Nodes), "Number of Edges: ", len(event1.Edges))

    Data1 = event1.Data
    Map1 = event1.NodeParticleMap

    Op = Optimizer({}, Debug = True)
    Op.Model = GCN(4, 2)
    Op.DefineOptimizer()
    Op.sample = Data1
    
    for i in range(10):
        Op.TrainClassification()
        print(Op.Model(Data1).max(1))

    return True

def TestInvMassGNN():
    
    event1 = ExampleEventGraph()
    #Model = InvMassGNN(4)
    #Model.forward(event1.Data)

    Op = Optimizer({}, Debug = True)
    Op.Model = InvMassGNN(4)
    Op.LearningRate = 1e-5
    Op.WeightDecay = 1e-3
    Op.DefineOptimizer()
    Op.sample = event1.Data

    P = [event1.NodeParticleMap[i].Index for i in event1.NodeParticleMap]
        
    print("==========")
    for i in range(100000):
        Op.TrainClassification()
        _, p = Op.Model(Op.sample).max(1)
        print(p, P, Op.L)



    return True
