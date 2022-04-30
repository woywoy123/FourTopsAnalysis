from Functions.Tools.Alerting import Debugging
from Functions.Particles.Particles import *
from Functions.Tools.Variables import VariableManager

class EventVariables:
    def __init__(self):
        self.MinimalTrees = ["tree", "nominal"]
        self.MinimalLeaves = []
        self.MinimalLeaves += Event().Leaves
        self.MinimalLeaves += Jet().Leaves
        self.MinimalLeaves += Electron().Leaves
        self.MinimalLeaves += Muon().Leaves

        self.MinimalLeaves += TruthJet().Leaves
        self.MinimalLeaves += TruthTopChildren().Leaves
        self.MinimalLeaves += TopPostFSRChildren().Leaves
        
        self.MinimalLeaves += TruthTop().Leaves
        self.MinimalLeaves += TopPreFSR().Leaves
        self.MinimalLeaves += TopPostFSR().Leaves

class EventTemplate(VariableManager):
    def __init__(self):
        VariableManager.__init__(self)
        self.runNumber = "runNumber"
        self.eventNumber = "eventNumber"
        self.mu = "mu"

        self.met = "met_met"
        self.met_phi = "met_phi" 
        self.mu_actual = "mu_actual"
        
        self.Type = "Event"
        self.ListAttributes()
        self.CompileKeyMap()
        self.iter = -1
        self.Tree = ""
        self.BrokenEvent = False

    def DefineObjects(self):
        for i in self.Objects:
           self.SetAttribute(i, {})

    def ParticleProxy(self, File):
        
        def Attributor(variable, value):
            for i in self.Objects:
                obj = self.Objects[i]
                if variable in obj.KeyMap:
                    o = getattr(self, i)
                    o[variable] = value
                    self.SetAttribute(i, o)
                    return True
            return False

        self.ListAttributes()
        for i in File.ArrayLeaves:
            if self.Tree in i:
                var = i.replace(self.Tree + "/", "")
                try: 
                    val = File.ArrayLeaves[i][self.iter]
                except:
                    self.BrokenEvent = True
                    continue
                
                if Attributor(var, val):
                    continue

                if var in self.KeyMap:
                    self.SetAttribute(self.KeyMap[var], val)

    def CompileEvent(self, ClearVal = True):
        pass

    def DictToList(self, inp): 
        out = []
        for i in inp:
            out += inp[i]
        return out



class Event(EventTemplate):
    def __init__(self):
        EventTemplate.__init__(self)
        self.Objects = {
                            "Electrons" : Electron(), 
                            "Muons" : Muon(), 
                            "Jets" : Jet(), 
                            "TruthJets": TruthJet(), 
                            "TruthTops" : TruthTop(), 
                            "TruthTopChildren": TruthTopChildren(), 
                            "TopPreFSR" : TopPreFSR(),
                            "TopPostFSR" : TopPostFSR(),
                            "TopPostFSRChildren" : TopPostFSRChildren()
                        }
        self.DefineObjects()


    def CompileEvent(self, ClearVal = True):
        def FixList(Input):
            try:
                return [int(Input)]
            except:
                return list(Input)


        for i in self.Objects:
            l = getattr(self, i)
            l = CompileParticles(l, self.Objects[i]).Compile(ClearVal)
            self.SetAttribute(i, l)
        
        for i in self.TruthTops:
            self.TruthTops[i][0].Decay_init += self.TruthTopChildren[i]

        for i in self.TopPostFSR:
            self.TopPostFSR[i][0].Decay_init += self.TopPostFSRChildren[i]

        for i in self.TruthJets:
            self.TruthJets[i][0].GhostTruthJetMap = FixList(self.TruthJets[i][0].GhostTruthJetMap)

        for i in self.Jets:
            self.Jets[i][0].JetMapGhost = FixList(self.Jets[i][0].JetMapGhost)
            self.Jets[i][0].JetMapTops = FixList(self.Jets[i][0].JetMapTops)

        for i in self.TruthJets:
            for t in self.TruthJets[i][0].GhostTruthJetMap:
                if t == -1:
                    continue
                self.TopPostFSR[t][0].Decay += self.TruthJets[i]

        for i in self.Jets:
            for tj in self.Jets[i][0].JetMapGhost:
                if tj == -1:
                    continue
                self.TruthJets[tj][0].Decay += self.Jets[i]

        self.Electrons = self.DictToList(self.Electrons)
        self.Muons = self.DictToList(self.Muons)
        self.Jets = self.DictToList(self.Jets)
        
        Leptons = []
        Leptons += self.Electrons
        Leptons += self.Muons
        
        All = [y for i in self.TopPostFSRChildren for y in self.TopPostFSRChildren[i] if abs(y.pdgid) in [11, 13, 15]]
        for j in Leptons:
            dr = 99
            low = ""
            for i in All:
                d = i.DeltaR(j) 
                if dr < d:
                    continue
                dr = d
                low = i
            if low == "":
                continue
            j.Index = low.Index
            self.TopPostFSR[low.Index][0].Decay.append(j)

        self.DetectorParticles = []
        self.DetectorParticles += self.Electrons
        self.DetectorParticles += self.Muons
        self.DetectorParticles += self.Jets

        self.TruthJets = self.DictToList(self.TruthJets)
        self.TruthTops = self.DictToList(self.TruthTops)
        self.TruthTopChildren = self.DictToList(self.TruthTopChildren)

        self.TopPreFSR = self.DictToList(self.TopPreFSR)
        self.TopPostFSR = self.DictToList(self.TopPostFSR)
        self.TopPostFSRChildren = self.DictToList(self.TopPostFSRChildren)

        if ClearVal: 
            del self.Objects
            del self.Leaves
            del self.KeyMap
