# Produce the plotting of the events in the analysis (basically a sanity check) 
from Functions.Event.EventGenerator import EventGenerator
from Functions.Particles.Particles import Particle
from Functions.IO.IO import UnpickleObject, PickleObject
from Functions.Plotting.Histograms import TH2F, TH1F, SubfigureCanvas, CombineHistograms
from Functions.GNN.Graphs import GenerateDataLoader
from Functions.GNN.Optimizer import Optimizer
from Functions.GNN.Metrics import EvaluationMetrics
from Closure.GNN import GenerateTemplate

def TestTops():
   
    x = UnpickleObject("SignalSample.pkl")
    x = x.Events 







    # Top mass containers 
    Top_Mass = []
    Top_Mass_Lep = []
    Top_Mass_NoLep = []
    
    Top_Mass_From_Children = []
    Top_Mass_From_Children_Lep = []
    Top_Mass_From_Children_NoLep = []
    
    Top_Mass_From_Children_init = []
    Top_Mass_From_Children_init_Lep = []
    Top_Mass_From_Children_init_NoLep = []
    for i in x:
        ev = x[i]["nominal"]
        
        tops = ev.TruthTops
        for k in tops:
            k.CalculateMass()
            m = k.Mass_GeV
            Top_Mass.append(m)
            
            k.CalculateMassFromChildren()
            Top_Mass_From_Children.append(k.Mass_GeV)
            Top_Mass_From_Children_init.append(k.Mass_init_GeV)
   
            # Now check if the top children contains a leptonic decay, if yes skip
            skip = False
            for l in k.Decay:
                if abs(l.pdgid) in [11, 13, 15]:
                    skip = True
                    break
            if skip: 
                Top_Mass_NoLep.append(m)
                Top_Mass_From_Children_NoLep.append(k.Mass_GeV)
                Top_Mass_From_Children_init_NoLep.append(k.Mass_init_GeV)
            else:
                Top_Mass_Lep.append(m)
                Top_Mass_From_Children_Lep.append(k.Mass_GeV)
                Top_Mass_From_Children_init_Lep.append(k.Mass_init_GeV)
 
    # ALL TOPS
    T = CombineHistograms()
    T.DefaultDPI = 500
    T.DefaultScaling = 7
    T.LabelSize = 15
    T.FontSize = 10
    T.LegendSize = 10
    T.Title = "Invariant Top Mass Derived from Different Branches"
    T.Log = True

    t = TH1F() 
    t.Title = "'truth_top_*'"
    t.xTitle = "Mass (GeV)"
    t.yTitle = "Entries"
    t.Color = "black"
    t.xBins = 250
    t.xMin = 0
    t.xMax = 200
    t.xData = Top_Mass
    t.Filename = "TruthTops.png"
    t.SaveFigure("Plots/TestTops")
    
    tc = TH1F()
    tc.Title = "'truth_top_child_*'"
    tc.xTitle = "Mass (GeV)"
    tc.yTitle = "Entries"
    tc.xBins = 250
    tc.xMin = 0
    tc.xMax = 200
    tc.xData = Top_Mass_From_Children
    tc.Filename = "TopChildren.png"
    tc.SaveFigure("Plots/TestTops")

    tc_in = TH1F()
    tc_in.Title = "'truth_top_child_init_*'"
    tc_in.xTitle = "Mass (GeV)"
    tc_in.yTitle = "Entries"
    tc_in.xBins = 250
    tc_in.xMin = 0
    tc_in.xMax = 200
    tc_in.xData = Top_Mass_From_Children_init
    tc_in.Filename = "TopChildren_init.png"
    tc_in.SaveFigure("Plots/TestTops")

    T.Histograms = [t, tc, tc_in]
    T.CompileHistogram()
    T.Filename = "Combined.png"
    T.Save("Plots/TestTops/")
    

    # NON LEPTONIC TOPS
    T = CombineHistograms()
    T.DefaultDPI = 500
    T.DefaultScaling = 7
    T.LabelSize = 15
    T.FontSize = 10
    T.LegendSize = 10
    T.Title = "Invariant Top Mass Derived from Different Branches (Non Leptonic Decay)"
    T.Log = True

    t = TH1F() 
    t.Title = "'truth_top_*'"
    t.xTitle = "Mass (GeV)"
    t.yTitle = "Entries"
    t.Color = "black"
    t.xBins = 250
    t.xMin = 0
    t.xMax = 200
    t.xData = Top_Mass_NoLep
    t.Filename = "TruthTops_NoLep.png"
    t.SaveFigure("Plots/TestTops")
    
    tc = TH1F()
    tc.Title = "'truth_top_child_*'"
    tc.xTitle = "Mass (GeV)"
    tc.yTitle = "Entries"
    tc.xBins = 250
    tc.xMin = 0
    tc.xMax = 200
    tc.xData = Top_Mass_From_Children_NoLep
    tc.Filename = "TopChildren_NoLep.png"
    tc.SaveFigure("Plots/TestTops")

    tc_in = TH1F()
    tc_in.Title = "'truth_top_child_init_*'"
    tc_in.xTitle = "Mass (GeV)"
    tc_in.yTitle = "Entries"
    tc_in.xBins = 250
    tc_in.xMin = 0
    tc_in.xMax = 200
    tc_in.xData = Top_Mass_From_Children_init_NoLep
    tc_in.Filename = "TopChildren_init_NoLep.png"
    tc_in.SaveFigure("Plots/TestTops")

    T.Histograms = [t, tc, tc_in]
    T.CompileHistogram()
    T.Filename = "Combined_NoLep.png"
    T.Save("Plots/TestTops/")

    
    # ONLY LEPTONIC TOPS
    T = CombineHistograms()
    T.DefaultDPI = 500
    T.DefaultScaling = 7
    T.LabelSize = 15
    T.FontSize = 10
    T.LegendSize = 10
    T.Title = "Invariant Top Mass Derived from Different Branches (Only Leptonic Decay)"
    T.Log = True

    t = TH1F() 
    t.Title = "'truth_top_*'"
    t.xTitle = "Mass (GeV)"
    t.yTitle = "Entries"
    t.Color = "black"
    t.xBins = 250
    t.xMin = 0
    t.xMax = 200
    t.xData = Top_Mass_Lep
    t.Filename = "TruthTops_Lep.png"
    t.SaveFigure("Plots/TestTops")
    
    tc = TH1F()
    tc.Title = "'truth_top_child_*'"
    tc.xTitle = "Mass (GeV)"
    tc.yTitle = "Entries"
    tc.xBins = 250
    tc.xMin = 0
    tc.xMax = 200
    tc.xData = Top_Mass_From_Children_Lep
    tc.Filename = "TopChildren_Lep.png"
    tc.SaveFigure("Plots/TestTops")

    tc_in = TH1F()
    tc_in.Title = "'truth_top_child_init_*'"
    tc_in.xTitle = "Mass (GeV)"
    tc_in.yTitle = "Entries"
    tc_in.xBins = 250
    tc_in.xMin = 0
    tc_in.xMax = 200
    tc_in.xData = Top_Mass_From_Children_init_Lep
    tc_in.Filename = "TopChildren_init_Lep.png"
    tc_in.SaveFigure("Plots/TestTops")

    T.Histograms = [t, tc, tc_in]
    T.CompileHistogram()
    T.Filename = "Combined_Lep.png"
    T.Save("Plots/TestTops/")

    return True

def TestResonance():
    x = UnpickleObject("SignalSample.pkl")
    x = x.Events 

    # Top mass containers 
    Res_TruthTops = []
    Res_TruthTops_Spec = []
    Cross_TruthTops = []
    Res_Child = []
    Res_Child_init = []
    Res_TruthJet = []
    Res_TruthJet_NoAnomaly = []
    Res_Jet = []
    for i in x:
        ev = x[i]["nominal"]
        
        tops = ev.TruthTops
        Z_ = Particle(True)
        Sigs = []
        Spec = []
        for t in tops:
            # Signal Tops from Resonance 
            if t.Signal == 0:
                Spec.append(t)
            else:
                Sigs.append(t)

        for t in tops:
            tmp = []
            for j in tops:
                if t == j:
                    pass
                elif t.Signal != j.Signal:
                    tmp.append(j) 
            for j in tmp:
                Z_.Decay = [t, j]
                Z_.CalculateMassFromChildren()
                Cross_TruthTops.append(Z_.Mass_GeV)
            break

        # Resonance Mass from Truth Tops 
        Z_.Decay = Sigs
        Z_.CalculateMassFromChildren()
        Res_TruthTops.append(Z_.Mass_GeV)

        Z_.Decay = Spec
        Z_.CalculateMassFromChildren()
        Res_TruthTops_Spec.append(Z_.Mass_GeV)
        
        Z_.Decay = []
        # Resonance Mass from Truth Children
        for t in Sigs:
            Z_.Decay += t.Decay
            Z_.Decay_init += t.Decay_init

        Z_.CalculateMassFromChildren()
        Res_Child.append(Z_.Mass_GeV)
        Res_Child_init.append(Z_.Mass_init_GeV)

        Z_.Decay = []
        Z_.Decay_init = []
        #Resonance Mass from Truth Jets
        for t in Sigs:
            for tc in t.Decay:
                Z_.Decay.append(tc)

        Z_.CalculateMassFromChildren()
        Res_TruthJet.append(Z_.Mass_GeV)
        
        Z_.Decay = []
        #Resonance Mass from Truth Jets Good Matching 
        if ev.Anomaly_TruthMatch == False: 
            for t in Sigs:
                for tc in t.Decay:
                    Z_.Decay.append(tc)
        
            Z_.CalculateMassFromChildren()
            Res_TruthJet_NoAnomaly.append(Z_.Mass_GeV)
 
        Z_.Decay = []  
        #Resonance Mass from Truth Jets
        for t in Sigs:
            for tc in t.Decay:
                if tc.Type == "truthjet":
                    Z_.Decay += tc.Decay
                else:
                    Z_.Decay.append(tc)

        Z_.CalculateMassFromChildren()
        Res_Jet.append(Z_.Mass_GeV)
 
    # Tops from Truth information figures 
    t = TH1F() 
    t.Title = "Resonance Pair"
    t.xTitle = "Mass (GeV)"
    t.yTitle = "Entries"
    t.xMin = 0
    t.xMax = 2500
    t.xBins = 500
    t.xData = Res_TruthTops
    t.Filename = "Resonance_TruthTops.png"
    t.SaveFigure("Plots/TestResonance")

    tx = TH1F() 
    tx.Title = "Spectator Pair"
    tx.xTitle = "Mass (GeV)"
    tx.yTitle = "Entries"
    tx.xMin = 0
    tx.xMax = 2500
    tx.xBins = 500
    tx.xData = Res_TruthTops_Spec
    tx.Filename = "Spectator_TruthTops.png"
    tx.SaveFigure("Plots/TestResonance")

    tp = TH1F() 
    tp.Title = "ResXSpec Pair"
    tp.xTitle = "Mass (GeV)"
    tp.yTitle = "Entries"
    tp.xMin = 0
    tp.xMax = 2500
    tp.xBins = 500
    tp.xData = Cross_TruthTops
    tp.Filename = "Cross_TruthTops.png"
    tp.SaveFigure("Plots/TestResonance")

    Com = CombineHistograms()
    Com.Histograms = [t, tx, tp]
    Com.Title = "Truth Top (truth_top_*) Resonance and Background (Spectator Tops)"
    Com.Filename = "ResSpec.png"
    Com.Save("Plots/TestResonance")

    tc = TH1F()
    tc.Title = "Resonance Mass Derived From 'truth_top_child_*'"
    tc.xTitle = "Mass (GeV)"
    tc.yTitle = "Entries"
    tc.xMin = 0
    tc.xMax = 2500
    tc.xBins = 500
    tc.xData = Res_Child
    tc.Filename = "Resonance_TruthChildren.png"
    tc.SaveFigure("Plots/TestResonance")

    tc_init = TH1F()
    tc_init.Title = "Resonance Mass Derived From 'truth_top_child_init*'"
    tc_init.xTitle = "Mass (GeV)"
    tc_init.yTitle = "Entries"
    tc_init.xMin = 0
    tc_init.xMax = 2500
    tc_init.xBins = 500
    tc_init.xData = Res_Child_init
    tc_init.Filename = "Resonance_TruthChildren_init.png"
    tc_init.SaveFigure("Plots/TestResonance")

    tc = TH1F()
    tc.Title =  "Resonance Mass Derived From 'truth_jets_*'\n (with Detector Leptons)"
    tc.xTitle = "Mass (GeV)"
    tc.yTitle = "Entries"
    tc.xMin = 0
    tc.xMax = 2500
    tc.xBins = 500
    tc.xData = Res_TruthJet
    tc.Filename = "Resonance_TruthJet.png"
    tc.SaveFigure("Plots/TestResonance")

    tc_init = TH1F()
    tc_init.Title = "Resonance Mass Derived From 'truth_jets_*'\n (with Detector Leptons) (Good Matching)"
    tc_init.xTitle = "Mass (GeV)"
    tc_init.yTitle = "Entries"
    tc_init.xMin = 0
    tc_init.xMax = 2500
    tc_init.xBins = 500
    tc_init.xData = Res_TruthJet_NoAnomaly
    tc_init.Filename = "Resonance_TruthJet_GoodMatching.png"
    tc_init.SaveFigure("Plots/TestResonance")

    tc_init = TH1F()
    tc_init.Title = "The Predicted Resonance Mass Derived From 'jets_*'\n (with Detector Leptons)"
    tc_init.xTitle = "Mass (GeV)"
    tc_init.yTitle = "Entries"
    tc_init.xMin = 0
    tc_init.xMax = 2500
    tc_init.xBins = 500
    tc_init.xData = Res_Jet
    tc_init.Filename = "Resonance_Jet.png"
    tc_init.SaveFigure("Plots/TestResonance")

    return True

def TestBackGroundProcesses():
    def CreateEvents(direc, event):
        ev = EventGenerator(direc, Stop = event)
        ev.SpawnEvents()
        ev.CompileEvent(SingleThread = False)
        return ev

    def GetNJets(ev, tree):
        Jet_Number = []
        for i in ev.Events:
            Event = ev.Events[i][tree]
            
            n = 0
            for k in Event.DetectorParticles:
                if k.Type == "jet":
                    n += 1
            Jet_Number.append(n)
        return Jet_Number
    
    dir_ttbar = "/CERN/Grid/Samples/NAF/2021-05-05-2cRC-all/mc16a/postProcessed_ttbar_PhPy8_Total.root"
    dir_4t = "/CERN/Grid/Samples/NAF/2021-05-05-2cRC-all/mc16a/postProcessed_4tops_aMCPy8_AFII.root"
    dir_SingleT = "/CERN/Grid/Samples/NAF/2021-05-05-2cRC-all/mc16a/postProcessed_SingleTop.root"
    dir_SingleT_Rare = "/CERN/Grid/Samples/NAF/2021-05-05-2cRC-all/mc16a/postProcessed_SingleTop_rare.root"
    
    dir_ttH = "/CERN/Grid/Samples/NAF/2021-05-05-2cRC-all/mc16a/postProcessed_ttH.root"
    dir_ttW = "/CERN/Grid/Samples/NAF/2021-05-05-2cRC-all/mc16a/postProcessed_ttW.root"

    dir_ttZ = "/CERN/Grid/Samples/NAF/2021-05-05-2cRC-all/mc16a/postProcessed_ttZ.root"
    dir_VH = "/CERN/Grid/Samples/NAF/2021-05-05-2cRC-all/mc16a/postProcessed_VH.root"

    dir_VV = "/CERN/Grid/Samples/NAF/2021-05-05-2cRC-all/mc16a/postProcessed_VV.root"
    dir_Wjets = "/CERN/Grid/Samples/NAF/2021-05-05-2cRC-all/mc16a/postProcessed_Wjets_Sherpa221.root"

    dir_Zjets_ee = "/CERN/Grid/Samples/NAF/2021-05-05-2cRC-all/mc16a/postProcessed_Zjets_ee_Sherpa221.root"
    dir_Zjets_mumu = "/CERN/Grid/Samples/NAF/2021-05-05-2cRC-all/mc16a/postProcessed_Zjets_mumu_Sherpa221.root"
    dir_Zjets_tautau = "/CERN/Grid/Samples/NAF/2021-05-05-2cRC-all/mc16a/postProcessed_Zjets_tautau_Sherpa221.root"

    
    Processes = [dir_ttbar, dir_4t, dir_SingleT, dir_SingleT_Rare, dir_ttH, dir_VH, dir_VV, dir_Wjets, dir_Zjets_ee, dir_Zjets_tautau, dir_Zjets_mumu]
    Map = {}
    for i in Processes:
        p = i.split("/")
        proc = p[len(p) - 1].strip(".root")
        name = "-".join(proc.split("_")[1:])
        Map[name] = i
        
        ev = CreateEvents(i, 50000)
        PickleObject(ev, proc)
   
    Jets = []
    Names = []
    for i in Map:
        ev = UnpickleObject("postProcessed_" + i.replace("-", "_"))
        Jets.append(GetNJets(ev, "tree"))
        
        if "ttbar" in i:
            i = "ttbar"
        elif "4tops" in i:
            i = "4tops"
        elif "SingleTop-rare" in i:
            i = "SingleTop-rare"
        elif "SingleTop" in i:
            i = "SingleTop"
        elif "ttH" in i:
            i = "ttH"
        elif "ttW" in i:
            i = "ttW"
        elif "ttZ" in i:
            i = "ttZ"
        elif "VH" in i:
            i = "VH"
        elif "VV" in i:
            i = "VV"
        elif "Wjets" in i:
            i = "Wjets"
        elif "Zjets-ee" in i:
            i = "Zjets-ee"
        elif "Zjets-mumu" in i:
            i = "Zjets-mumu"
        elif "Zjets-tautau" in i:
            i = "Zjets-tautau"
        Names.append(i)
    
    J = []
    for i in Jets:
        l = 0
        for k in i:
            l += k
        J.append(k)
    
    Njet_P = TH2F()
    Njet_P.Title = "N-Jets vs Process Considered"
    Njet_P.Filename = "n_jets_process"
    Njet_P.yData = Jets
    Njet_P.xData = Names
    Njet_P.yMin = 0
    Njet_P.xTitle = "Process"
    Njet_P.yTitle = "N-Jets"
    Njet_P.SaveFigure("Plots/Njets/")
    return True

def TestGNNMonitor():
    def Signal(a):
        return int(a.Signal)

    def Energy(a):
        return float(a.e)
    
    def Charge(a):
        return float(a.Signal)

    ev = UnpickleObject("SignalSample.pkl")
    Loader = GenerateDataLoader()
    Loader.AddNodeFeature("x", Charge)
    Loader.AddNodeTruth("y", Signal)
    Loader.AddSample(ev, "nominal", "TruthTops")
    Loader.ToDataLoader()

    ev = UnpickleObject("SignalSample.pkl")
    Sig = GenerateDataLoader()
    Sig.AddNodeFeature("x", Charge)
    Sig.AddNodeTruth("y", Signal)
    Sig.AddSample(ev, "nominal", "TruthTops")

    op = Optimizer(Loader)
    op.DefaultBatchSize = 2000
    op.Epochs = 50
    op.kFold = 10
    op.LearningRate = 1e-6
    op.WeightDecay = 1e-4
    op.DefineEdgeConv(1, 4)
    op.kFoldTraining()
    
    PickleObject(op, "Optimizer.pkl")
    op = UnpickleObject("Optimizer.pkl")


    eva = EvaluationMetrics()
    eva.Sample = op
    eva.LossTrainingPlot("Plots/GNN_Performance_TestMonitor")

    return True

def KinematicsPlotting():
    
    Events = UnpickleObject("SignalSample.pkl")

    d_ETA_Edge_SI = TH1F()
    d_ETA_Edge_DI = TH1F()
    d_ETA_Edge_SI.Title = "Same Parent"
    d_ETA_Edge_DI.Title = "Different Parent"
    d_ETA_Edge_SI.xTitle = "delta eta"
    d_ETA_Edge_DI.xTitle = "delta eta"
    d_ETA_Edge_SI.xBins = 100 
    d_ETA_Edge_DI.xBins = 100 
    d_ETA_Edge_SI.Filename = "Delta_ETA_Same_Index" 
    d_ETA_Edge_DI.Filename = "Delta_ETA_Different_Index" 
    d_ETA_Edge_SI.xMin = 0
    d_ETA_Edge_SI.xMax = 5
    d_ETA_Edge_DI.xMin = 0
    d_ETA_Edge_DI.xMax = 5

    d_Energy_Edge_SI = TH1F()
    d_Energy_Edge_DI = TH1F()
    d_Energy_Edge_SI.Title = "Same Parent"
    d_Energy_Edge_DI.Title = "Different Parent"
    d_Energy_Edge_SI.xTitle = "delta energy (GeV)"
    d_Energy_Edge_DI.xTitle = "delta energy (GeV)"
    d_Energy_Edge_SI.xBins = 100 
    d_Energy_Edge_DI.xBins = 100 
    d_Energy_Edge_SI.Filename = "Delta_Energy_Same_Index" 
    d_Energy_Edge_DI.Filename = "Delta_Energy_Different_Index" 
    d_Energy_Edge_SI.xMin = 0
    d_Energy_Edge_SI.xMax = 1.25*1e3
    d_Energy_Edge_DI.xMin = 0
    d_Energy_Edge_DI.xMax = 1.25*1e3


    d_PHI_Edge_SI = TH1F()
    d_PHI_Edge_DI = TH1F()
    d_PHI_Edge_SI.Title = "Same Parent"
    d_PHI_Edge_DI.Title = "Different Parent"
    d_PHI_Edge_SI.xTitle = "delta phi (rad)"
    d_PHI_Edge_DI.xTitle = "delta phi (rad)"
    d_PHI_Edge_SI.xBins = 100 
    d_PHI_Edge_DI.xBins = 100
    d_PHI_Edge_SI.Filename = "Delta_PHI_Same_Index" 
    d_PHI_Edge_DI.Filename = "Delta_PHI_Different_Index" 
    d_PHI_Edge_SI.xMin = 0
    d_PHI_Edge_SI.xMax = 7
    d_PHI_Edge_DI.xMin = 0
    d_PHI_Edge_DI.xMax = 6

    d_PT_Edge_SI = TH1F()
    d_PT_Edge_DI = TH1F()
    d_PT_Edge_SI.Title = "Same Parent"
    d_PT_Edge_DI.Title = "Different Parent"
    d_PT_Edge_SI.xTitle = "pt (GeV)"
    d_PT_Edge_DI.xTitle = "pt (GeV)"
    d_PT_Edge_SI.xBins = 100
    d_PT_Edge_DI.xBins = 100
    d_PT_Edge_SI.Filename = "Delta_Pt_Same_Index" 
    d_PT_Edge_DI.Filename = "Delta_Pt_Different_Index" 
    d_PT_Edge_SI.xMin = 0
    d_PT_Edge_SI.xMax = 0.6*1e3
    d_PT_Edge_DI.xMin = 0
    d_PT_Edge_DI.xMax = 0.6*1e3

    Mass_Edge_SI = TH1F()
    Mass_Edge_DI = TH1F()
    Mass_Edge_SI.Title = "Same Parent"
    Mass_Edge_DI.Title = "Different Parent"
    Mass_Edge_SI.xTitle = "Mass (MeV)"
    Mass_Edge_DI.xTitle = "Mass (MeV)"
    Mass_Edge_SI.xBins = 100
    Mass_Edge_DI.xBins = 100
    Mass_Edge_SI.Filename = "Mass_Same_Index" 
    Mass_Edge_DI.Filename = "Mass_Different_Index" 
    Mass_Edge_SI.xMin = 0
    Mass_Edge_SI.xMax = 1e3
    Mass_Edge_DI.xMin = 0
    Mass_Edge_DI.xMax = 1e3

    Ratio_Kine_Edge_SI = TH1F()
    Ratio_Kine_Edge_DI = TH1F()
    Ratio_Kine_Edge_SI.Title = "Same Parent"
    Ratio_Kine_Edge_DI.Title = "Different Parent"
    Ratio_Kine_Edge_SI.xTitle = "Arb."
    Ratio_Kine_Edge_DI.xTitle = "Arb."
    Ratio_Kine_Edge_SI.xBins = 100
    Ratio_Kine_Edge_DI.xBins = 100
    Ratio_Kine_Edge_SI.Filename = "Ratio_Kin_Same_Index" 
    Ratio_Kine_Edge_DI.Filename = "Ratio_Kin_Different_Index" 
    Ratio_Kine_Edge_SI.xMin = 0
    Ratio_Kine_Edge_SI.xMax = 5
    Ratio_Kine_Edge_DI.xMin = 0
    Ratio_Kine_Edge_DI.xMax = 5

    dR_Edge_SI = TH1F()
    dR_Edge_DI = TH1F()
    dR_Edge_SI.Title = "Same Parent"
    dR_Edge_DI.Title = "Different Parent"
    dR_Edge_SI.xTitle = "dR"
    dR_Edge_DI.xTitle = "dR"
    dR_Edge_SI.xBins = 100
    dR_Edge_DI.xBins = 100
    dR_Edge_SI.Filename = "DeltaR_Same_Index" 
    dR_Edge_DI.Filename = "DeltaR_Different_Index" 
    dR_Edge_SI.xMin = 0
    dR_Edge_SI.xMax = 7
    dR_Edge_DI.xMin = 0
    dR_Edge_DI.xMax = 7

    SignalTops = TH1F()
    SignalTops.Title = "Signal"
    SignalTops.xTitle = "Mass (GeV)"
    SignalTops.xBins = 100
    SignalTops.Filename = "Mass_Signal_Tops" 
    SignalTops.xMin = 0
    SignalTops.xMax = 180

    SpectatorTops = TH1F()
    SpectatorTops.Title = "Spectator"
    SpectatorTops.xTitle = "Mass (GeV)"
    SpectatorTops.xBins = 100
    SpectatorTops.Filename = "Mass_Spectator_Top" 
    SpectatorTops.xMax = 180
    SpectatorTops.xMin = 0

    for i in Events.Events:
        pc = Events.Events[i]["nominal"].TruthChildren
        
        for e_i in pc:
            for e_j in pc: 
                if e_i == e_j:
                    continue
                elif e_i.Index > e_j.Index:
                    continue
               
                P = Particle(True)
                P.Decay.append(e_i)
                P.Decay.append(e_j)
                P.CalculateMassFromChildren()

                e_i.CalculateMass()
                e_j.CalculateMass()

                if e_i.Index == e_j.Index:
                    Mass_Edge_SI.xData.append(P.Mass_GeV) 
                    d_ETA_Edge_SI.xData.append(abs(e_i.eta - e_j.eta))
                    d_PHI_Edge_SI.xData.append(abs(e_i.phi - e_j.phi))
                    d_Energy_Edge_SI.xData.append(abs(float(e_i.e - e_j.e)) / 1000)
                    d_PT_Edge_SI.xData.append(float(abs(e_i.pt - e_j.pt))/ 1000)
                    dR_Edge_SI.xData.append(e_i.DeltaR(e_j))

                elif e_i.Index != e_j.Index:
                    Mass_Edge_DI.xData.append(P.Mass_GeV) 
                    d_ETA_Edge_DI.xData.append(abs(e_i.eta - e_j.eta))
                    d_PHI_Edge_DI.xData.append(abs(e_i.phi - e_j.phi))
                    d_Energy_Edge_DI.xData.append(abs(float(e_i.e - e_j.e)) / 1000)
                    d_PT_Edge_DI.xData.append(abs(float(e_i.pt - e_j.pt))/ 1000)
                    dR_Edge_DI.xData.append(e_i.DeltaR(e_j))

        mass = [Particle(True), Particle(True), Particle(True), Particle(True)]
        for e_i in pc:
            mass[e_i.Index].Decay.append(e_i)
            mass[e_i.Index].Signal = e_i.Signal 
        
        for e_i in mass:
            e_i.CalculateMassFromChildren()
            if e_i.Signal == 1:
                SignalTops.xData.append(e_i.Mass_GeV)
            else:
                SpectatorTops.xData.append(e_i.Mass_GeV)

    Mass_Edge_SI.SaveFigure("Plots/Kinematics_Original")
    d_ETA_Edge_SI.SaveFigure("Plots/Kinematics_Original")
    d_PHI_Edge_SI.SaveFigure("Plots/Kinematics_Original")
    d_Energy_Edge_SI.SaveFigure("Plots/Kinematics_Original")
    d_PT_Edge_SI.SaveFigure("Plots/Kinematics_Original")
    dR_Edge_SI.SaveFigure("Plots/Kinematics_Original")
    Mass_Edge_DI.SaveFigure("Plots/Kinematics_Original")
    d_ETA_Edge_DI.SaveFigure("Plots/Kinematics_Original")
    d_PHI_Edge_DI.SaveFigure("Plots/Kinematics_Original")
    d_Energy_Edge_DI.SaveFigure("Plots/Kinematics_Original")
    d_PT_Edge_DI.SaveFigure("Plots/Kinematics_Original")
    dR_Edge_DI.SaveFigure("Plots/Kinematics_Original")
    SignalTops.SaveFigure("Plots/Kinematics_Original")
    SpectatorTops.SaveFigure("Plots/Kinematics_Original")

    # Combine the figures into a single one 
    Mass_Edge = CombineHistograms()
    Mass_Edge.Histograms = [Mass_Edge_SI, Mass_Edge_DI]
    Mass_Edge.Title = "Mass of Particle Edges from (un)common Parent Index"
    Mass_Edge.Filename = "Edge_Mass.png"
    Mass_Edge.Save("Plots/Kinematics/")

    dR_Edge = CombineHistograms()
    dR_Edge.Histograms = [dR_Edge_SI, dR_Edge_DI]
    dR_Edge.Title = "$\Delta$R of Particle Edges from (un)common Parent Index"
    dR_Edge.Filename = "Edge_dR.png"
    dR_Edge.Save("Plots/Kinematics/")

    d_phi_Edge = CombineHistograms()
    d_phi_Edge.Histograms = [d_PHI_Edge_SI, d_PHI_Edge_DI]
    d_phi_Edge.Title = "$\Delta \phi$ of Particle Edges from (un)common Parent Index"
    d_phi_Edge.Filename = "Edge_delta_phi.png"
    d_phi_Edge.Save("Plots/Kinematics/")

    d_eta_Edge = CombineHistograms()
    d_eta_Edge.Histograms = [d_ETA_Edge_SI, d_ETA_Edge_DI]
    d_eta_Edge.Title = "$\Delta \eta$ of Particle Edges from (un)common Parent Index"
    d_eta_Edge.Filename = "Edge_delta_eta.png"
    d_eta_Edge.Save("Plots/Kinematics/")

    d_Energy_Edge = CombineHistograms()
    d_Energy_Edge.Histograms = [d_Energy_Edge_SI, d_Energy_Edge_DI]
    d_Energy_Edge.Title = "$\Delta$ Energy of Particle Edges from (un)common Parent Index"
    d_Energy_Edge.Filename = "Edge_delta_Energy.png"
    d_Energy_Edge.Save("Plots/Kinematics/")

    d_PT_Edge = CombineHistograms()
    d_PT_Edge.Histograms = [d_ETA_Edge_SI, d_ETA_Edge_DI]
    d_PT_Edge.Title = "$\Delta P_T$ of Particle Edges from (un)common Parent Index"
    d_PT_Edge.Filename = "Edge_delta_PT.png"
    d_PT_Edge.Save("Plots/Kinematics/")

    return True   

def TopologicalComplexityMassPlot(Input = "LoaderSignalSample.pkl", Type = "Signal"):
    from PathNetOptimizer_cpp import PathCombination
    from PathNetOptimizerCUDA_cpp import ToCartesianCUDA, PathMassCartesianCUDA
    import torch 
        
    if Type == "Signal":
        GenerateTemplate(tree = "tree")
        pass

    Loader = UnpickleObject(Input)
   
    Complexity_Mass = TH2F()
    Complexity_Mass.Title = "Mass Prediction of Combinatorial M chose N-Nodes"
    Complexity_Mass.yTitle = "Invariant Mass (GeV)"
    Complexity_Mass.xTitle = "Complexity (abr.)"
    Complexity_Mass.xMin = 1
    Complexity_Mass.xMax = 15
    Complexity_Mass.xMin = 1
    Complexity_Mass.xBins = 15
    Complexity_Mass.yMin = 0
    Complexity_Mass.yMax = 2000
    Complexity_Mass.yBins = 1000
    Complexity_Mass.Filename = "Complexity_vs_Mass.png"
    events = Loader.DataLoader
    
    del Loader
    Hists = {}
    for i in range(2, 15):
        M = TH1F()
        M.Title = str(i)+"-Nodes"
        M.xTitle = "Invariant Mass (GeV)"
        M.yTitle = "Entries"
        M.xMin = 0
        M.xMax = 2000
        M.xBins = 100
        M.Filename = "M" + str(i) + ".png"
        Hists[i] = M

    for n in events:
        n_nodes = events[n]
        adj = torch.tensor([[i != j for i in range(n)] for j in range(n)], dtype = torch.float, device = "cuda")
        combi = PathCombination(adj, n, n)
        print("-> ", n, len(n_nodes))
        for i in n_nodes:
            P = ToCartesianCUDA(i.eta, i.phi, i.pt, i.e)
            m_cuda = PathMassCartesianCUDA(P[0], P[1], P[2], P[3], combi[0])
            for j, k in zip(m_cuda, combi[0].sum(1)):
                Complexity_Mass.yData.append(float(j))
                Complexity_Mass.xData.append(int(k))
                try:
                    Hists[int(k)].xData.append(float(j))
                except KeyError:
                    break
        events[n] = ""
    del events

    Complexity_Mass.SaveFigure("Plots/TopologicalComplexityMass" + Type)
    
    h = CombineHistograms()
    h.Histograms = [Hists[i] for i in Hists]
    h.Title = "Mass of M-Chose, N-Node (Complexity)"
    h.Filename = "MassComplexity.png"
    h.SaveFigure("Plots/TopologicalComplexityMass" + Type)
    return True

def TestDataSamples():
    GenerateTemplate("", "JetLepton", ["ttbar.pkl"], "TestTTBAR.pkl")
    TopologicalComplexityMassPlot(Input = "TestTTBAR.pkl", Type = "TTBAR")
    return True

def TestWorkingExample4TopsComplexity():
    import torch
    GenerateTemplate(SignalSample = "CustomSignalSample.pkl", Tree = "TopPostFSRChildren", OutputName = "LoaderCustomSignalSample.pkl") 
    ev = UnpickleObject("LoaderCustomSignalSample.pkl")

    op = Optimizer(ev)
    op.DefaultBatchSize = 10
    op.Epochs = 1
    op.kFold = 4
    op.LearningRate = 1e-5
    op.WeightDecay = 1e-3
    op.MinimumEvents = 1
    op.Debug = True
    op.DefinePathNet(Target = "NodeEdges")
    op.kFoldTraining()
    PickleObject(op, "Debug.pkl")
    op = UnpickleObject("Debug.pkl") 
    
    TMP = []
    for i in op.Model.TMP:
        v = i/i.max()
        TMP.append(v)

    PickleObject(TMP, "Matrix.pkl")
    TMP = UnpickleObject("Matrix.pkl") 
    add = torch.zeros(TMP[0].shape, dtype=float, device= TMP[0].device)
    for i in TMP:
        add = add + i
    
    index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    xData = []
    yData = []
    for i in index:
        for j in index:
            xData += [i]*int(add[i-1, j-1])
            yData += [j]*int(add[i-1, j-1])
    
    Complexity_Mass = TH2F()
    Complexity_Mass.Title = "Normalized Summed of Complexity Connectivity"
    Complexity_Mass.yTitle = "Child-j"
    Complexity_Mass.xTitle = "Child-i"
    Complexity_Mass.xMin = 1
    Complexity_Mass.xMax = 12
    Complexity_Mass.yMin = 1
    Complexity_Mass.yMax = 12
    Complexity_Mass.xBins = 12
    Complexity_Mass.yBins = 12
    Complexity_Mass.xData = xData
    Complexity_Mass.yData = yData
    Complexity_Mass.Filename = "Complexity.png"
    Complexity_Mass.SaveFigure("Plots/Complexity_Mass_Projection")



    return True
