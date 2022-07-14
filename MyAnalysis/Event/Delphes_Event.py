from Functions.Event.EventTemplate import EventTemplate 
from Particles.Particles import Particle
class Event(EventTemplate):
    def __init__(self):
        EventTemplate.__init__(self)
        self.runNumber = "Event.Number"
        self.Weight = "Event.Weight"
        self.Tree = ["Delphes"]
        self.Branches = ["Particle"]
        self.Objects = {
                "Particle" : Particle()
                                        }
        self.DefineObjects()

    def CompileEvent(self, ClearVal):
        def Sort (a,target,Top_Number):
            if isinstance(a, list):
                for i in a:
                    target.Index = Top_Number
                    if i not in target.Decay:
                        target.Decay.append(i)
                    i.Index = Top_Number
                    Sort(i,target,Top_Number)
                return
            else:
                D1_i = a.Daughter1
                D2_i = a.Daughter2
                Stat = a.Status
                if Stat == 1:
                    a.Index = Top_Number
                    if a not in Final_Particles:
                        Final_Particles.append(a)
                elif D1_i == D2_i:
                    if self.Particle[D1_i] not in a.Decay:
                        a.Decay.append(self.Particle[D1_i])
                    a.Index = Top_Number
                    return Sort(self.Particle[D1_i], a, Top_Number)
                elif D1_i != D2_i:
                    Decays = self.Particle[D1_i : (D2_i+1)]
                    a.Index = Top_Number
                    return Sort(Decays,a,Top_Number)
       






        self.CompileParticles(ClearVal)
        
        #print(self.Particle)
        self.Tops = []
        self.Particle = self.DictToList(self.Particle)
        for e in range(len(self.Particle)):
            Target_Top = self.Particle[e]
            if abs(Target_Top.PID) == 6 and Target_Top.Status == 62:
                self.Tops.append(Target_Top)
                print(self.Tops)
        for h in range(len(self.Tops)):
            Final_Particles = []
            Tops_Index = "Top"
            Anti_Tops_Index = "Anti-Top"
            if self.Tops[h].PID == 6:
               Top_Index = Tops_Index
            if self.Tops[h].PID == -6:
               Top_Index = Anti_Tops_Index
            Sort(self.Tops[h],self.Tops[h], Top_Index)
            Exclusion = []
            for t in self.Particle:
                if t.Index != Top_Index:
                    D1 = t.Daughter1
                    D2 = t.Daughter2
                    Daughter = self.Particle[D1:D2+1]
                    for g in Daughter:
                        if g.Index == Top_Index and abs(g.PID) != 6 and t not in Exclusion:
                           Exclusion.append(t)
                   
   
        print(self.Tops) 
