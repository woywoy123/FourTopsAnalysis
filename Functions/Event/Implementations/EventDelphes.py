from Functions.Event.EventTemplate import EventTemplate 
from Functions.Particles.ParticleTemplate import ParticleTemplate

# Particle Definitions 
class Particle(ParticleTemplate):
    def __init__(self):
        ParticleTemplate.__init__(self)
        self.Type = "Particle"
        self.PID = self.Type + ".PID"
        self.Status = self.Type + ".Status"
        self.Charge = self.Type + ".Charge"
        self.PT = self.Type + ".PT"
        self.Eta = self.Type + ".Eta"
        self.Phi = self.Type + ".Phi"
        self.E = self.Type + ".E"
        
        self._DefineParticle() 


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
        self.CompileParticles(ClearVal)
        self.Particle = self.DictToList(self.Particle)

