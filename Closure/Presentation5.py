from Functions.IO.Files import Directories
from Functions.IO.IO import PickleObject, UnpickleObject
from Functions.Plotting.Histograms import TH2F, TH1F, CombineHistograms


def Histograms_Template(Title, xTitle, yTitle, bins, Min, Max, Data, FileName = None, Dir = None, Color = None, Weight = None):
    H = TH1F()
    H.Title = Title
    H.xTitle = xTitle
    H.yTitle = yTitle
    H.xBins = bins
    H.xMin = Min
    H.xMax = Max
    H.xData = Data
    H.Alpha = 0.25
    H.Weights = Weight
    
    if Color is not None:
        H.Color = Color

    if FileName != None:
        H.Filename = FileName
        H.SaveFigure("Plots/" + Dir + "/Raw")
    return H

def Histograms2D_Template(Title, xTitle, yTitle, xBins, yBins, xMin, xMax, yMin, yMax, xData, yData, FileName, Dir, Diagonal = False, Weight = None):
    H = TH2F()
    H.Diagonal = Diagonal
    H.Title = Title
    H.xTitle = xTitle
    H.yTitle = yTitle
    H.xBins = xBins 
    H.yBins = yBins 
    H.xMin = xMin
    H.xMax = xMax
    H.yMin = yMin
    H.yMax = yMax
    H.xData = xData
    H.yData = yData
    H.Weights = Weight
    H.FontSize = 30
    H.ShowBinContent = True

    H.Filename = FileName
    H.SaveFigure("Plots/" + Dir)
    return H


def HistogramCombineTemplate(DPI = 500, Scaling = 5, Size = 10):
    T = CombineHistograms()
    T.DefaultDPI = DPI
    T.DefaultScaling = Scaling
    T.LabelSize = Size + 5
    T.FontSize = Size
    T.LegendSize = Size + 2
    return T


def TopFragmentation(FileDir, eta_cut = None, pt_cut = None, Plot = True):

    def Cut(jet):
        if eta_cut != None and abs(eta_cut) < abs(jet.eta):
            return True

        if pt_cut != None and float(jet.pt/1000) < pt_cut:
            return True 
        return False


    
    Backup = {}
    Backup["CutJetsPT"] = []
    Backup["CutJetsEta"] = []
    
    Backup["CutJetTopPT"] = []
    Backup["CutJetTopEta"] = []

    Backup["CutJetNonTopPT"] = []
    Backup["CutJetNonTopEta"] = []

    Backup["CutJetTopPTSignal"] = []
    Backup["CutJetTopEtaSignal"] = []

    Backup["CutJetTopPTSpect"] = []
    Backup["CutJetTopEtaSpect"] = []

    Backup["CutJetTopPTMixed"] = []
    Backup["CutJetTopEtaMixed"] = []

    

    Backup["JetPT"] = []
    Backup["JetEta"] = []

    Backup["NonTopJetPT"] = []
    Backup["NonTopJetEta"] = []

    Backup["SignalJetPT"] = []
    Backup["SignalJetEta"] = []

    Backup["MixedJetPT"] = []
    Backup["MixedJetEta"] = []

    Backup["SpecJetPT"] = []
    Backup["SpecJetEta"] = []
    
    Backup["TripletSurvivalPT"] = []
    Backup["TripletSurvivalEta"] = []

    Backup["TripletSurvivalSignalPT"] = []
    Backup["TripletSurvivalSignalEta"] = []

    Backup["TripletSurvivalSpecPT"] = []
    Backup["TripletSurvivalSpecEta"] = []

    Backup["NJets"] = []
    Backup["NJetSignal"] = []
    Backup["NJetSpect"] = []
    Backup["NJetMixed"] = []
    Backup["NJetJunk"] = []

    jet_sum = 0
    jet_remaining = 0

    jet_tops = 0
    jet_tops_signal = 0
    jet_tops_spect = 0
    jet_tops_nocut = 0
    
    n_tops_reco_nocut = 0
    n_tops_reco_cut = 0
    for F in FileDir:
        for ev in F.Events:
            event = F.Events[ev]["nominal"]

            jets = event.Jets
            tops = event.TopPostFSR
            
            jet_sum += len(jets)
            for j in jets:
                # //// Cut  
                if Cut(j):

                    Backup["CutJetsPT"].append(j.pt/1000)
                    Backup["CutJetsEta"].append(j.eta)
                    
                    if -1 in j.JetMapTops:
                        Backup["CutJetNonTopPT"].append(j.pt/1000)
                        Backup["CutJetNonTopEta"].append(j.eta)
                    else:
                        Backup["CutJetTopPT"].append(j.pt/1000)
                        Backup["CutJetTopEta"].append(j.eta)
                       
                        Signal = False
                        Spec = False
                        for k in j.JetMapTops:
                            if tops[k].FromRes == 1:
                                Signal = True 
                            else:
                                Spec = True 
                        
                        if Signal == True and Spec == False:
                            Backup["CutJetTopPTSignal"].append(j.pt/1000)
                            Backup["CutJetTopEtaSignal"].append(j.eta)
                        
                        elif Signal == True and Spec == True:
                            Backup["CutJetTopPTMixed"].append(j.pt/1000)
                            Backup["CutJetTopEtaMixed"].append(j.eta)

                        elif Signal == False and Spec == True:
                            Backup["CutJetTopPTSpect"].append(j.pt/1000)
                            Backup["CutJetTopEtaSpect"].append(j.eta)
                
                # //// Remaining
                else: 
                    jet_remaining += 1

                    Backup["JetPT"].append(j.pt/1000)
                    Backup["JetEta"].append(j.eta)

                    if -1 in j.JetMapTops:
                        Backup["NonTopJetPT"].append(j.pt/1000)
                        Backup["NonTopJetEta"].append(j.eta)
                    else:
                       
                        Signal = False
                        Spec = False
                        for k in j.JetMapTops:
                            if tops[k].FromRes == 1:
                                Signal = True 
                            else:
                                Spec = True 
                        
                        if Signal == True and Spec == False:
                            Backup["SignalJetPT"].append(j.pt/1000)
                            Backup["SignalJetEta"].append(j.eta)
                        
                        elif Signal == True and Spec == True:
                            Backup["MixedJetPT"].append(j.pt/1000)
                            Backup["MixedJetEta"].append(j.eta)

                        elif Signal == False and Spec == True:
                            Backup["SpecJetPT"].append(j.pt/1000)
                            Backup["SpecJetEta"].append(j.eta)
           

            for j in jets:
                if -1 in j.JetMapTops:
                    continue
                jet_tops_nocut += 1

                if Cut(j):
                    continue
                jet_tops += 1

            dic_t = [[] for t in tops]
            for j in jets:
                if -1 in j.JetMapTops:
                    continue
                for l in j.JetMapTops:
                    dic_t[l].append(j)
            it = 0
            for l in dic_t:
                if len(l) == 0:
                    continue
                n_tops_reco_nocut += 1
                
                broke = False
                for j in l:
                    if Cut(j):
                        broke = True
                        break
                if broke == False:
                    n_tops_reco_cut += 1
                    if tops[it].FromRes == 1:
                        jet_tops_signal += 1
                    else:
                        jet_tops_spect += 1
                it += 1

            counted_J = [] 
            for t in tops:
                Broken = False
                for j in jets:
                    if t.Index not in j.JetMapTops:
                        continue
                    if Cut(j):
                        Broken = True
                        break

                if Broken:
                    continue

                for j in jets:
                    if t.Index not in j.JetMapTops or j in counted_J:
                        continue

                    Backup["TripletSurvivalPT"].append(j.pt/1000)
                    Backup["TripletSurvivalEta"].append(j.eta)
                    
                    sig = False
                    spe = False
                    for tk in j.JetMapTops:
                        if tops[tk].FromRes == 1:
                            sig = True
                        else:
                            spe = True
                    
                    counted_J.append(j)

                    if sig:
                        Backup["TripletSurvivalSignalPT"].append(j.pt/1000)
                        Backup["TripletSurvivalSignalEta"].append(j.eta)
                    if spe:
                        Backup["TripletSurvivalSpecPT"].append(j.pt/1000)
                        Backup["TripletSurvivalSpecEta"].append(j.eta)                       

            n = 0 
            n_jjnk = 0
            topCount_Sig = [0 for t in tops]
            topCount_Spe = [0 for t in tops]
            topCount_Mix = [0 for t in tops]
            for j in jets:
                if Cut(j):
                    continue
                n += 1
                if -1 in j.JetMapTops:
                    n_jjnk += 1
                    continue 
                sig = False
                spe = False
                for t in j.JetMapTops:
                    if tops[t].FromRes == 1:
                        sig = True
                    else:
                        spe = True
                
                if sig == True and spe == False:
                    for t in j.JetMapTops:
                        topCount_Sig[t] += 1

                if sig == True and spe == True:
                    for t in j.JetMapTops:
                        topCount_Mix[t] += 1

                if sig == False and spe == True:
                    for t in j.JetMapTops:
                        topCount_Spe[t] += 1

            Backup["NJetSignal"] += topCount_Sig
            Backup["NJetSpect"] += topCount_Spe
            Backup["NJetMixed"] += topCount_Mix
            Backup["NJets"].append(n)
            Backup["NJetJunk"].append(n_jjnk)

    Backup["jet_sum"] = jet_sum
    Backup["jet_remaining"] = jet_remaining
    Backup["jet_tops"] = jet_tops
    Backup["jet_tops_signal"] = jet_tops_signal
    Backup["jet_tops_spect"] = jet_tops_spect
    Backup["jet_tops_nocut"] = jet_tops_nocut
    Backup["n_tops_reco_nocut"] = n_tops_reco_nocut
    Backup["n_tops_reco_cut"] = n_tops_reco_cut
    
    return Backup


def EntryPoint(F):
    
    start_eta = 3
    end_eta = 1
    n_eta = 10
    delta_eta = (abs(end_eta - start_eta)/n_eta)
    Scan_eta = [round(start_eta - delta_eta*j, 3) for j in range(n_eta+1)] 

    start_pt = 10
    end_pt = 110
    n_pt = 10
    delta_pt = (abs(end_pt - start_pt)/n_pt)
    Scan_pt = [start_pt + delta_pt*j for j in range(n_pt+1)] 
    
    for pt in Scan_pt:
        Backup = {}
        for eta in Scan_eta:
            print("Scanning ----> "+ str(pt) + " @ " + str(eta))
            Backup[str(pt) + "_" + str(eta)] = TopFragmentation(F, eta, pt)

        print("Checkpoint ----> "+ str(pt))
        PickleObject(Backup, "FragmentationJets_" + str(pt))


def EntryPointEfficiencyHists():
    #f = "_Cache/CustomSample_tttt_Cache"
    #d = Directories(f).ListFilesInDir(f)
    #
    #F = []
    #for i in d:
    #    F.append(UnpickleObject(i, f))
    #EntryPoint(F)
    #JetAnalysis(F)
    
    B = {}
    for i in Directories("_Pickle/").ListFilesInDir("_Pickle"):
        if "Jets_" not in i:
            continue
        f = UnpickleObject(i)
        B.update(f) 

    PT = []
    ETA = []
    for i in B:
        PT.append(float(i.split("_")[0]))
        ETA.append(float(i.split("_")[1]))
    PT = list(set(PT))
    ETA = list(set(ETA))
    PT.sort()
    ETA.sort()


    print(PT, ETA)
    
    JetSurv = []
    TopSig = []
    TopSpec = []
    TopFrac = []
    JetPurity = []
    Loss = []
    Reco_eff = []
    it = 0
    for pt in PT:
        cuteff = []
        topsigjets = [] 
        topspecjets = []
        cuttopjet = []
        purity = []
        fractLost = []
        reco_tops = []
        for eta in ETA:
            d = B[str(pt) + "_" + str(eta)]
            jet_sum = d["jet_sum"]
            jet_remaining = d["jet_remaining"]
            jet_tops = d["jet_tops"]
            jet_tops_sig = d["jet_tops_signal"]
            jet_tops_spect = d["jet_tops_spect"]
            jet_tops_nocut = d["jet_tops_nocut"]
             
            cuteff.append(float(jet_remaining/jet_sum)*100)
            cuttopjet.append(float(jet_tops/jet_sum)*100)
            purity.append(float(jet_tops/jet_remaining)*100) 
            fractLost.append(100.0 - float(jet_tops/jet_tops_nocut)*100) 

            n_tops_reco_cut = d["n_tops_reco_cut"]
            n_tops_reco_nocut = d["n_tops_reco_nocut"]

            topsigjets.append(float(jet_tops_sig/n_tops_reco_nocut)*100)
            topspecjets.append(float(jet_tops_spect/n_tops_reco_nocut)*100)
            reco_tops.append(float(n_tops_reco_cut/n_tops_reco_nocut)*100)
        JetSurv.append(cuteff)
        TopFrac.append(cuttopjet)
        JetPurity.append(purity)
        Loss.append(fractLost)
        Reco_eff.append(reco_tops)
        
        TopSig.append(topsigjets)
        TopSpec.append(topspecjets)

        #EntryPointPlotHists(str(pt) + "_" + str(ETA[it]))
        it += 1

    Histograms2D_Template("Fraction of Jets Remaining \n (n-jets-remaining/n-jets-event)", "Lowest PT Threshold (GeV)", "Highest Eta Threshold", 
            None, None, min(PT), max(PT), min(ETA), max(ETA), 
            PT, ETA, "JetFraction", "Presentation5/", Weight = JetSurv)

    Histograms2D_Template("Fraction of Jets Remaining With Top Contributions \n (n-jets-tops/n-jets-event)", "Lowest PT Threshold (GeV)", "Highest Eta Threshold", 
            None, None, min(PT), max(PT), min(ETA), max(ETA), 
            PT, ETA, "JetFractionTopContributions", "Presentation5/", Weight = TopFrac)

    Histograms2D_Template("Post Cut Purity of Jets with Top Contributions \n (n-jets-tops/n-jet-remaining)", "Lowest PT Threshold (GeV)", "Highest Eta Threshold", 
            None, None, min(PT), max(PT), min(ETA), max(ETA), 
            PT, ETA, "JetPurityTops", "Presentation5/", Weight = JetPurity)

    Histograms2D_Template("Fractional Loss of Jets with Top Contributions \n (n-jets-tops/n-jets-tops-nocuts)", "Lowest PT Threshold (GeV)", "Highest Eta Threshold", 
            None, None, min(PT), max(PT), min(ETA), max(ETA), 
            PT, ETA, "FractionalLoss", "Presentation5/", Weight = Loss)



    Histograms2D_Template("Fraction of Complete Jet-Sets Forming Tops", "Lowest PT Threshold (GeV)", "Highest Eta Threshold", 
            None, None, min(PT), max(PT), min(ETA), max(ETA), 
            PT, ETA, "TopRecoEff", "Presentation5/", Weight = Reco_eff)

    Histograms2D_Template("Fraction of Complete Jet-Sets Forming a Top - Spectator", "Lowest PT Threshold (GeV)", "Highest Eta Threshold", 
            None, None, min(PT), max(PT), min(ETA), max(ETA), 
            PT, ETA, "Signal-Tops", "Presentation5/", Weight = TopSig)
    
    Histograms2D_Template("Fraction of Complete Jet-Sets Forming a Top - Signal", "Lowest PT Threshold (GeV)", "Highest Eta Threshold", 
            None, None, min(PT), max(PT), min(ETA), max(ETA), 
            PT, ETA, "Spectator-Tops", "Presentation5/", Weight = TopSpec)






def EntryPointPlotHists(Cut):
    B = UnpickleObject("FragmentationJets_110.0")
    
    Back = B[Cut]
    pt_cut = str(Cut.split("_")[0]).replace(".0", "")
    eta_cut = str(Cut.split("_")[1])
    string = "PT " + pt_cut + "(GeV) Eta " + eta_cut
    file_s = pt_cut + "-" + eta_cut

    #///// Inspect the rejected Jet kinematics
    # ======= General =======
    H1 = Histograms_Template("All-Jets" , "Momentum (GeV)", "Rejected Jets", 250, 0, 500, Back["CutJetsPT"])
    H2 = Histograms_Template("Top-Jets" , "Momentum (GeV)", "Rejected Jets", 250, 0, 500, Back["CutJetTopPT"])
    H3 = Histograms_Template("Junk-Jets", "Momentum (GeV)", "Rejected Jets", 250, 0, 500, Back["CutJetNonTopPT"])

    H = HistogramCombineTemplate()
    H.Title = "Transverse Momentum of All Rejected Jets: " + string
    H.Histograms = [H1, H2, H3]
    H.Filename = "JetsCutPT"
    H.Save("Plots/Presentation5/" + file_s + "/CutJets")

    H1 = Histograms_Template("All-Jets" , "Eta", "Rejected Jets", 250, -3, 3, Back["CutJetsEta"])
    H2 = Histograms_Template("Top-Jets" , "Eta", "Rejected Jets", 250, -3, 3, Back["CutJetTopEta"])
    H3 = Histograms_Template("Junk-Jets", "Eta", "Rejected Jets", 250, -3, 3, Back["CutJetNonTopEta"])

    H = HistogramCombineTemplate()
    H.Title = "Eta of Rejected Jets: " + string
    H.Histograms = [H1, H2, H3]
    H.Filename = "JetsCutEta"
    H.Save("Plots/Presentation5/" + file_s + "/CutJets")


    # ======= Tops Cut =======
    H = HistogramCombineTemplate()
    H.Title = "Transverse Momentum of Rejected Jets with Top Contributions: " + string
    H1 = Histograms_Template("All" , "Momentum (GeV)", "Rejected Jets", 250, 0, 500, Back["CutJetTopPT"])
    H2 = Histograms_Template("Signal" , "Momentum (GeV)", "Rejected Jets", 250, 0, 500, Back["CutJetTopPTSignal"])
    H3 = Histograms_Template("Spectator", "Momentum (GeV)", "Rejected Jets", 250, 0, 500, Back["CutJetTopPTSpect"])
    H4 = Histograms_Template("Mixed (Signal + Spect)", "Momentum (GeV)", "Rejected Jets", 250, 0, 500, Back["CutJetTopPTMixed"])
    H.Histograms = [H1, H2, H3, H4]
    H.Filename = "JetsCutTopsOnlyPT"
    H.Save("Plots/Presentation5/" + file_s + "/CutJets")

    H = HistogramCombineTemplate()
    H.Title = "Eta of Rejected Jets with Top Contributions: " + string
    H1 = Histograms_Template("All" , "Eta", "Rejected Jets", 250, -3, 3, Back["CutJetTopEta"])
    H2 = Histograms_Template("Signal" , "Eta", "Rejected Jets", 250, -3, 3, Back["CutJetTopEtaSignal"])
    H3 = Histograms_Template("Spectator", "Eta", "Rejected Jets", 250, -3, 3, Back["CutJetTopEtaSpect"])
    H4 = Histograms_Template("Mixed (Signal + Spect)", "Eta", "Rejected Jets", 250, -3, 3, Back["CutJetTopEtaMixed"])
    H.Histograms = [H1, H2, H3]
    H.Filename = "JetsCutTopsOnlyEta"
    H.Save("Plots/Presentation5/" + file_s + "/CutJets")

    #///// Inspect the accepted Jet kinematics
    H = HistogramCombineTemplate()
    H.Title = "Transverse Momentum of Accepted Jets: " + string
    H1 = Histograms_Template("All" , "Momentum (GeV)", "Accepted Jets", 250, 0, 500, Back["JetPT"])
    H2 = Histograms_Template("Junk" , "Momentum (GeV)", "Accepted Jets", 250, 0, 500, Back["NonTopJetPT"])
    H3 = Histograms_Template("Signal", "Momentum (GeV)", "Accepted Jets", 250, 0, 500, Back["SignalJetPT"])
    H4 = Histograms_Template("Spectator", "Momentum (GeV)", "Accepted Jets", 250, 0, 500, Back["SpecJetPT"])
    H5 = Histograms_Template("Mixed (Signal + Spect)", "Momentum (GeV)", "Accepted Jets", 250, 0, 500, Back["MixedJetPT"])
    H.Histograms = [H5, H4, H3, H2, H1]
    H.Filename = "JetsPT"
    H.Save("Plots/Presentation5/" + file_s + "/Accepted")

    H = HistogramCombineTemplate()
    H.Title = "Eta of Accepted Jets: " + string
    H1 = Histograms_Template("All" , "Eta", "Accepted Jets", 250, -3, 3, Back["JetEta"])
    H2 = Histograms_Template("Junk" , "Eta", "Accepted Jets", 250, -3, 3, Back["NonTopJetEta"])
    H3 = Histograms_Template("Signal", "Eta", "Accepted Jets", 250, -3, 3, Back["SignalJetEta"])
    H4 = Histograms_Template("Spectator", "Eta", "Accepted Jets", 250, -3, 3, Back["SpecJetEta"])
    H5 = Histograms_Template("Mixed (Signal + Spect)", "Eta", "Accepted Jets", 250, -3, 3, Back["MixedJetEta"])
    H.Histograms = [H1, H2, H3, H4, H5]
    H.Filename = "JetsEta"
    H.Save("Plots/Presentation5/" + file_s + "/Accepted")


    #///// Inspect Accepted Jet Kinematics originating from Surviving Triplets
    H = HistogramCombineTemplate()
    H.Title = "Transverse Momentum of Top Contributing Jets with Jet-Set Intact: " + string
    H1 = Histograms_Template("All" , "Momentum (GeV)", "Accepted Jets", 250, 0, 500, Back["TripletSurvivalPT"])
    H2 = Histograms_Template("Signal" , "Momentum (GeV)", "Accepted Jets", 250, 0, 500, Back["TripletSurvivalSignalPT"])
    H3 = Histograms_Template("Spectator", "Momentum (GeV)", "Accepted Jets", 250, 0, 500, Back["TripletSurvivalSpecPT"])
    H.Histograms = [H1, H2, H3]
    H.Filename = "JetsPT_Triplets"
    H.Save("Plots/Presentation5/" + file_s + "/Accepted")

    H = HistogramCombineTemplate()
    H.Title = "Eta of Top Contributing Jets with Jet-Set Intact: " + string
    H1 = Histograms_Template("All" , "Momentum (GeV)", "Accepted Jets", 250, -3, 3, Back["TripletSurvivalEta"])
    H2 = Histograms_Template("Signal" , "Momentum (GeV)", "Accepted Jets", 250, -3, 3, Back["TripletSurvivalSignalEta"])
    H3 = Histograms_Template("Spectator", "Momentum (GeV)", "Accepted Jets", 250, -3, 3, Back["TripletSurvivalSpecEta"])
    H.Histograms = [H1, H2, H3]   
    H.Filename = "JetsEta_Triplets"
    H.Save("Plots/Presentation5/" + file_s + "/Accepted")

    H = HistogramCombineTemplate()
    H.Title = "N-Jets Passed Per Event Due to Cut: " + string
    H1 = Histograms_Template("All"      , "N-Jets", "Entries", 10, 0, 10, Back["NJets"])
    H2 = Histograms_Template("Signal"   , "N-Jets", "Entries", 10, 0, 10, Back["NJetSignal"])
    H3 = Histograms_Template("Spectator", "N-Jets", "Entries", 10, 0, 10, Back["NJetSpect"])
    H4 = Histograms_Template("Mixed"    , "N-Jets", "Entries", 10, 0, 10, Back["NJetMixed"])
    H5 = Histograms_Template("Junk"     , "N-Jets", "Entries", 10, 0, 10, Back["NJetJunk"])
    H.Histograms = [H5, H4, H3, H2, H1]
    H.Filename = "N-Jets"
    H.Save("Plots/Presentation5/" + file_s + "/Accepted")






def JetAnalysis(D):

    Backup = {}
    Backup["DeltaR_TopJet_All"] = []
    Backup["DeltaR_TopJet_Signal"] = []
    Backup["DeltaR_TopJet_Spectator"] = []
    Backup["DeltaR_TopJet_Leptonic_Signal"] = []
    Backup["DeltaR_TopJet_Leptonic_Spect"] = []

    Backup["DeltaR_JetsOfSameTop_All"] = []
    Backup["DeltaR_JetsOfSameTop_Signal"] = []
    Backup["DeltaR_JetsOfSameTop_Spectator"] = []

    Backup["DeltaR_TopJet_Top_1"] = []
    Backup["DeltaR_TopJet_Top_2"] = []
    Backup["DeltaR_TopJet_Top_3"] = []
    Backup["DeltaR_TopJet_Top_4"] = []
    Backup["DeltaR_TopJet_Top_5"] = []
    Backup["DeltaR_TopJet_Top_21"] = []

    Backup["DeltaR_TopTruthJet_Top_1"] = []
    Backup["DeltaR_TopTruthJet_Top_2"] = []
    Backup["DeltaR_TopTruthJet_Top_3"] = []
    Backup["DeltaR_TopTruthJet_Top_4"] = []
    Backup["DeltaR_TopTruthJet_Top_5"] = []
    Backup["DeltaR_TopTruthJet_Top_21"] = []

    Backup["TruthTopResPT"] = []
    Backup["TruthTopSpecPT"] = []
    Backup["TruthTopResE"] = []
    Backup["TruthTopSpecE"] = []

    for F in D:
        for ev in F.Events:
            event = F.Events[ev]["nominal"]

            jets = event.Jets
            truthjets = event.TruthJets
            tops = event.TopPostFSR
            
            lepto = []
            for t in tops:
                t.Decay = []
                if len(list(set([11, 13, 15]) & set([abs(p.pdgid) for p in t.Decay_init]))) > 0:
                    lepto.append(t.Index)
                t.Decay_init = []

            for j in jets:
                if -1 in j.JetMapTops:
                    continue

                for t in j.JetMapTops:
                    tops[t].Decay.append(j)

            for j in truthjets:
                if -1 in j.GhostTruthJetMap:
                    continue

                for t in j.GhostTruthJetMap:
                    tops[t].Decay_init.append(j)
                


            for t in tops:

                if t.FromRes == 1:
                    Backup["TruthTopResPT"].append(t.pt/1000)
                    Backup["TruthTopResE"].append(t.e/1000)
                else:
                    Backup["TruthTopSpecPT"].append(t.pt/1000)
                    Backup["TruthTopSpecE"].append(t.e/1000)

                for j in t.Decay_init:
                    if t.FromRes == 1:
                        
                        if abs(j.pdgid) == 1:
                            Backup["DeltaR_TopTruthJet_Top_1"].append(j.DeltaR(t))

                        if abs(j.pdgid) == 2:
                            Backup["DeltaR_TopTruthJet_Top_2"].append(j.DeltaR(t))
                        
                        if abs(j.pdgid) == 3:
                            Backup["DeltaR_TopTruthJet_Top_3"].append(j.DeltaR(t))

                        if abs(j.pdgid) == 4:
                            Backup["DeltaR_TopTruthJet_Top_4"].append(j.DeltaR(t))

                        if abs(j.pdgid) == 5:
                            Backup["DeltaR_TopTruthJet_Top_5"].append(j.DeltaR(t))

                        if abs(j.pdgid) == 21:
                            Backup["DeltaR_TopTruthJet_Top_21"].append(j.DeltaR(t))

                for j in t.Decay:
                    if t.FromRes == 1:
                        Backup["DeltaR_TopJet_Signal"].append(j.DeltaR(t))

                        if len(j.JetMapGhost) != 1 or -1 in j.JetMapGhost:
                            continue
                        
                        if j.truthPartonLabel == 1:
                            Backup["DeltaR_TopJet_Top_1"].append(j.DeltaR(t))

                        if j.truthPartonLabel == 2:
                            Backup["DeltaR_TopJet_Top_2"].append(j.DeltaR(t))
                        
                        if j.truthPartonLabel == 3:
                            Backup["DeltaR_TopJet_Top_3"].append(j.DeltaR(t))

                        if j.truthPartonLabel == 4:
                            Backup["DeltaR_TopJet_Top_4"].append(j.DeltaR(t))

                        if j.truthPartonLabel == 5:
                            Backup["DeltaR_TopJet_Top_5"].append(j.DeltaR(t))

                        if j.truthPartonLabel == 21:
                            Backup["DeltaR_TopJet_Top_21"].append(j.DeltaR(t))

                    
                    if t.FromRes == 0:
                        Backup["DeltaR_TopJet_Spectator"].append(j.DeltaR(t))
                    
                    if t.Index in lepto and t.FromRes == 1:
                        Backup["DeltaR_TopJet_Leptonic_Signal"].append(j.DeltaR(t))

                    if t.Index in lepto and t.FromRes == 0:
                        Backup["DeltaR_TopJet_Leptonic_Spect"].append(j.DeltaR(t))

                    Backup["DeltaR_TopJet_All"].append(j.DeltaR(t))

                for j in t.Decay:
                    for k in t.Decay:
                        if j == k:
                            continue
                        Backup["DeltaR_JetsOfSameTop_All"].append(j.DeltaR(k))

                        if t.FromRes == 1:
                            Backup["DeltaR_JetsOfSameTop_Signal"].append(j.DeltaR(k))

                        if t.FromRes == 0:
                            Backup["DeltaR_JetsOfSameTop_Spectator"].append(j.DeltaR(k))


    OutputDir = "Presentation5/WeirdJet"
    T = HistogramCombineTemplate()    
    deltaR = "$\Delta$R"
    T.Title = "Resonance Top - "+ deltaR + " Between Matched Jet"
    HT_3 = Histograms_Template("Jet-Flavour PDGID-1", deltaR, "Sampled Jets" , 100, 0, 3, Backup["DeltaR_TopJet_Top_1"]) 
    HT_4 = Histograms_Template("Jet-Flavour PDGID-2", deltaR, "Sampled Jets" , 100, 0, 3, Backup["DeltaR_TopJet_Top_2"])
    HT_5 = Histograms_Template("Jet-Flavour PDGID-3", deltaR, "Sampled Jets" , 100, 0, 3, Backup["DeltaR_TopJet_Top_3"])
    HT_6 = Histograms_Template("Jet-Flavour PDGID-4", deltaR, "Sampled Jets" , 100, 0, 3, Backup["DeltaR_TopJet_Top_4"])
    HT_7 = Histograms_Template("Jet-Flavour PDGID-5", deltaR, "Sampled Jets" , 100, 0, 3, Backup["DeltaR_TopJet_Top_5"])
    HT_8 = Histograms_Template("Jet-Flavour PDGID-21", deltaR, "Sampled Jets" , 100, 0, 3, Backup["DeltaR_TopJet_Top_21"])
    T.Histograms = [HT_3, HT_4, HT_5, HT_6, HT_7, HT_8]
    T.Filename = "dR_debug"
    T.Save("Plots/" + OutputDir)

    T = HistogramCombineTemplate()    
    T.Title = "Resonance Top - " + deltaR + " Between Matched Truth Jet"
    HT_3 = Histograms_Template("Jet-Flavour PDGID-1", "$\Delta$R", "Sampled Jets" , 100, 0, 3,  Backup["DeltaR_TopTruthJet_Top_1"]) 
    HT_4 = Histograms_Template("Jet-Flavour PDGID-2", "$\Delta$R", "Sampled Jets" , 100, 0, 3,  Backup["DeltaR_TopTruthJet_Top_2"])
    HT_5 = Histograms_Template("Jet-Flavour PDGID-3", "$\Delta$R", "Sampled Jets" , 100, 0, 3,  Backup["DeltaR_TopTruthJet_Top_3"])
    HT_6 = Histograms_Template("Jet-Flavour PDGID-4", "$\Delta$R", "Sampled Jets" , 100, 0, 3,  Backup["DeltaR_TopTruthJet_Top_4"])
    HT_7 = Histograms_Template("Jet-Flavour PDGID-5", "$\Delta$R", "Sampled Jets" , 100, 0, 3,  Backup["DeltaR_TopTruthJet_Top_5"])
    HT_8 = Histograms_Template("Jet-Flavour PDGID-21", "$\Delta$R", "Sampled Jets" , 100, 0, 3, Backup["DeltaR_TopTruthJet_Top_21"])
    T.Histograms = [HT_3, HT_4, HT_5, HT_6, HT_7, HT_8]
    T.Filename = "dR_debug_truthjet"
    T.Save("Plots/" + OutputDir)


    T = HistogramCombineTemplate()    
    T.Title = deltaR + " Between Top and Jets"
    HT_0 = Histograms_Template("All", deltaR, "Sampled Jets", 100, 0, 3, Backup["DeltaR_TopJet_All"])  
    HT_2 = Histograms_Template("Signal", deltaR, "Sampled Jets", 100, 0, 3, Backup["DeltaR_TopJet_Signal"]) 
    HT_3 = Histograms_Template("Spectator", deltaR, "Sampled Jets", 100, 0, 3, Backup["DeltaR_TopJet_Spectator"]) 
    HT_4 = Histograms_Template("Leptonic-Signal", deltaR, "Sampled Jets", 100, 0, 3, Backup["DeltaR_TopJet_Leptonic_Signal"])
    HT_5 = Histograms_Template("Leptonic-Spect", deltaR, "Sampled Jets", 100, 0, 3, Backup["DeltaR_TopJet_Leptonic_Spect"])
    T.Histograms = [HT_2, HT_3, HT_4, HT_5, HT_0]
    T.Filename = "dR_JetTop"
    T.Save("Plots/" + OutputDir)

    T = HistogramCombineTemplate()    
    T.Title = deltaR + " Between Jets with Common Top"
    HT_0 = Histograms_Template("All", deltaR, "Sampled Jets", 100, 0, 3, Backup["DeltaR_JetsOfSameTop_All"])  
    HT_2 = Histograms_Template("Signal", deltaR, "Sampled Jets", 100, 0, 3, Backup["DeltaR_JetsOfSameTop_Signal"]) 
    HT_3 = Histograms_Template("Spectator", deltaR, "Sampled Jets", 100, 0, 3, Backup["DeltaR_JetsOfSameTop_Spectator"]) 
    T.Histograms = [HT_2, HT_3, HT_0]
    T.Filename = "dR_JetJet"
    T.Save("Plots/" + OutputDir)

    T = HistogramCombineTemplate()    
    T.Title = "Transverse Momentum of Truth Tops"
    HT_2 = Histograms_Template("Signal", "Momentum (GeV)", "Sampled Tops", 250, 0, 1500, Backup["TruthTopResPT"]) 
    HT_3 = Histograms_Template("Spectator", "Momentum (GeV)", "Sampled Tops", 250, 0, 1500, Backup["TruthTopSpecPT"]) 
    T.Histograms = [HT_2, HT_3]
    T.Filename = "TruthTopPT"
    T.Save("Plots/" + OutputDir)

    T = HistogramCombineTemplate()    
    T.Title = "Energy Truth Tops"
    HT_2 = Histograms_Template("Signal", "Energy (GeV)", "Sampled Tops", 250, 0, 1500, Backup["TruthTopResE"]) 
    HT_3 = Histograms_Template("Spectator", "Energy (GeV)", "Sampled Tops", 250, 0, 1500, Backup["TruthTopSpecE"]) 
    T.Histograms = [HT_2, HT_3]
    T.Filename = "TruthTopE"
    T.Save("Plots/" + OutputDir)








