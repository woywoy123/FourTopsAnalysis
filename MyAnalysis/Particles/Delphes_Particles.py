
from Functions.Event.EventTemplate import EventTemplate 
from Functions.Particles.ParticleTemplate import Particle as Part

# Particle Definitions 
class Particle(Part):
    def __init__(self):
        Part.__init__(self)
        self.Type = "Particle"
        self.PID = self.Type + ".PID"
        self.Status = self.Type + ".Status"
        self.Charge = self.Type + ".Charge"
        self.PT = self.Type + ".PT"
        self.Eta = self.Type + ".Eta"
        self.Phi = self.Type + ".Phi"
        self.E = self.Type + ".E"
        self.Mass = self.Type + ".Mass"
        self.Daughter1 = self.Type + ".D1"
        self.Daughter2 = self.Type + ".D2"
        self.Mother1 = self.Type + ".M1"
        self.Mother2 = self.Type + ".M2"
        
        self.__DefineParticle()
        self.Decay_init = []
        self.Decay = []
        self.Index = -1

      

 
