from BaseFunctions.VariableManager import *
from BaseFunctions.Alerting import ErrorAlert, Alerting, Debugging
from BaseFunctions.ParticlesManager import * 
import multiprocessing

class EventCompiler(ErrorAlert, BranchVariable, Debugging):
    def __init__(self, FileDir, Tree, Branches):
        Branches += ["eventNumber"]
        
        ErrorAlert.__init__(self)
        self.expected = str
        self.given = Tree
        self.WrongInputType("GAVE LIST EXPECTED STRING FOR TREE!")

        self.Exclude = ["eventNumber"]
        BranchVariable.__init__(self, FileDir, Tree, Branches)
        self.EventDictionary = {}
        
        Debugging.__init__(self, events = 100)

    def GenerateEvents(self):
        al = Alerting(self.EventNumber)

        al.Notice("ENTERING EVENT GENERATOR")
        for i in range(len(self.EventNumber)):
                
            P = CreateParticleObjects(self.E[i], self.Pt[i], self.Phi[i], self.Eta[i])
            
            try: 
                P.PDGID = self.PDGID[i]
            except AttributeError:
                pass

            try: 
                P.Flavour = self.Flavour[i]
            except AttributeError:
                pass
            
            try: 
                P.Mask = self.Mask[i]
            except AttributeError:
                pass

            try: 
                P.Charge = self.Charge[i]
            except AttributeError:
                pass
            
            self.EventDictionary[self.EventNumber[i]] = P
            al.ProgressAlert()
            
            self.BreakCounter()
            if self.DebugKill:
                break

        al.Notice("FINISHED EVENT GENERATOR")
        self.MultiThreadingCompiler()

    def MultiThreadingCompiler(self):
        def Running(Pieces, Sender):
            out = {}
            for x in Pieces:
                P = Pieces[x].CompileParticles()
                out[x] = P
            Sender.send(out)
        
        batch_s = 4000
        Pipe = []
        Prz = []
        
        bundle = {}
        for ev in self.EventDictionary:
            bundle[ev] = self.EventDictionary[ev]

            if len(bundle) == batch_s:
                recv, send = multiprocessing.Pipe(False)
                P = multiprocessing.Process(target = Running, args = (bundle, send, ))
                Pipe.append(recv)
                Prz.append(P)
                bundle = {}
        
        if len(bundle) != 0:
            recv, send = multiprocessing.Pipe(False)
            P = multiprocessing.Process(target = Running, args = (bundle, send, ))
            Pipe.append(recv)
            Prz.append(P)
       
        al = Alerting(Prz)
        al.Notice("-> COMPILING PARTICLES")
        for i in Prz:
            i.start()
        
        for i, j in zip(Prz, Pipe):
            con = j.recv()
            i.join()
            for t in con:
                self.EventDictionary[t] = con[t]
            al.ProgressAlert()
        al.Notice("-> COMPILING COMPLETE")


class TruthCompiler(EventCompiler):
    def __init__(self, FileDir, Tree, Branches):
        if "top_FromRes" not in Branches:
            Branches += ["top_FromRes"]
        
        EventCompiler.__init__(self, FileDir, Tree, Branches)


    def MatchParticles(self, Incoming):
        self.expected = dict
        self.given = Incoming
        self.WrongInputType("EXPECTED DICTIONARY OF EVENTS")
        p = 0 
        for i in self.EventDictionary:
            self.FindCommonIndex(Incoming[i], self.EventDictionary[i])
            
            if p == 5:
                break
            p += 1
    
    def FindCommonIndex(self, incom, truth):
        for i in range(len(truth)):
            for j in range(len(incom)):
                if truth[i].Index == incom[j].Index:
                    truth[i].AddProduct(incom[j])