import matplotlib.pyplot as plt
import matplotlib
from matplotlib import colors
matplotlib.use("agg")
from networkx.drawing.nx_agraph import to_agraph
from Functions.IO.Files import WriteDirectory
from Functions.Tools.Alerting import Notification
import os
import numpy as np


class GenericAttributes:
    def __init__(self):
        self.Title = ""
        self.xTitle = ""
        self.yTitle = ""
        self.zTitle = ""
        
        self.xMin = ""
        self.yMin = ""
        self.zMin = ""
        
        self.xMax = ""
        self.yMax = ""
        self.zMax = ""
        
        self.xBins = ""
        self.yBins = ""
        self.Align = "left"
        
        self.Alpha = 0.5
        self.Color = ""
        self.Marker = "o"
        self.Style = ""
        self.Filename = ""

        self.DefaultScaling = 15
        self.DefaultDPI = 500
        self.Compiled = False
        self.FontSize = 16
        self.LabelSize = 30
        self.LegendSize = 10
        self.LegendPos = "upper right"
        self.TitleSize = 20
        
        self.xData = []
        self.yData = []

        self.xLabels = []
        self.yLabels = []

        self.Weights = None
    
    def Init_PLT(self):
        self.PLT = plt
        self.PLT.figure(figsize=(self.DefaultScaling, self.DefaultScaling), dpi = self.DefaultDPI)
        self.PLT.rcParams.update({"font.size":self.FontSize, "axes.labelsize" : self.LabelSize, "legend.fontsize" : self.LegendSize, "figure.titlesize" : self.TitleSize})
        self.PLT.rcParams["text.usetex"] = True
    
    def xAxis(self):
        if self.Compiled:
            return 
        if self.xMin == "":
            self.xMin = min(self.xData)

        if self.xMax == "":
            self.xMax = max(self.xData)

        if self.xBins == "":
            self.xBins = int(max(self.xData))

        delta = float(self.xMax - self.xMin)/float(self.xBins)
        self.xMin -= delta*0.5
        self.xMax += delta*0.5
        self.xBins += int(delta)

    def yAxis(self):
        if self.yMin == "":
            self.yMin = min(self.yData)
    
        if self.yMax == "":
            self.yMax = max(self.yData)

        if self.yBins == "":
            self.yBins = int(max(self.yData))

        delta = float(self.yMax - self.yMin)/float(self.yBins)
        self.yMin -= delta*0.5
        self.yMax += delta*0.5
        self.yBins += int(delta)

    def CheckGivenData(self, Data):
        for i in Data:
            if isinstance(i, str):
                return True

    def TransformData(self, Data, Labels):
        nData = getattr(self, Data)
        nLabels = getattr(self, Labels)
        if self.CheckGivenData(nData):
            nLabels = nData.copy()
            nData = []
            for i in range(len(nLabels)):
                nData.append(i)
            setattr(self, Data, nData) 
            setattr(self, Labels, nLabels) 

class SharedMethods(WriteDirectory, Notification):
    def __init__(self):
        WriteDirectory.__init__(self)
        Notification.__init__(self)
        self.Caller = "PLOTTING"
        self.Verbose = True

    def SaveFigure(self, dir = ""):
        if self.Compiled != True:
            try:
                self.CompileHistogram()
            except AttributeError:
                self.CompileGraph()
        
        if self.Filename == "":
           self.Filename = self.Title + ".png"
        
        self.Notify("SAVING FIGURE AS +-> " + self.Filename)
        if dir == "":
            self.MakeDir("Plots/")
            self.ChangeDir("Plots/")
        else:
            self.MakeDir(dir)
            self.ChangeDir(dir)
         
        if self.Caller != "PLOTTING":
            self.PLT.close("all")
            A = to_agraph(self.G)
            A.layout("dot")

            if ".png" not in self.Filename:
                A.draw(self.Filename + ".png")
            else:
                A.draw(self.Filename)
            self.ChangeDirToRoot()
            return None 
        
        if ".png" not in self.Filename:
            self.PLT.savefig(self.Filename + ".png", bbox_inches="tight")
        else: 
            self.PLT.savefig(self.Filename, bbox_inches="tight")

        self.ChangeDirToRoot()
        self.PLT.close("all")
        del self.PLT

class TH1F(SharedMethods, GenericAttributes):
    def __init__(self, PLT = ""):

        self.Normalize = False
        self.Log = False

        SharedMethods.__init__(self)
        GenericAttributes.__init__(self)

    def CompileHistogram(self):
        self.Init_PLT()
        self.TransformData("xData", "xLabels")
        self.PLT.title(self.Title)
        self.xAxis()
        
        if len(self.yData) == len(self.xData):
            Update = []
            for i in self.xData: 
                for k in range(self.yData[i]): 
                    Update.append(i)
            self.xData = Update
        self.PLT.hist(self.xData, bins = self.xBins, range=(self.xMin, self.xMax), alpha = self.Alpha, log = self.Log, density = self.Normalize, weights = self.Weights)

        if len(self.xLabels) != 0:
            self.TransformData("xLabels", "xData")
            self.PLT.xticks(self.xLabels, self.xData, rotation = 45, rotation_mode = "anchor", ha = "right")

        self.PLT.xlabel(self.xTitle)
        self.PLT.ylabel(self.yTitle)
        self.Compiled = True

class TH2F(SharedMethods, GenericAttributes):
    
    def __init__(self, PLT = ""):
        self.Normalize = True
        SharedMethods.__init__(self)
        GenericAttributes.__init__(self)
        self.Diagonal = False
        self.ShowBinContent = False

    def ShowBins(self, hist, xbins, ybins):
        skip = 1
        delx = abs(self.xBins[0] - self.xBins[1])
        dely = abs(self.yBins[0] - self.yBins[1])
        for i in range(len(self.yBins)-1):
            if i/skip - int(i/skip)  != 0:
                continue
            for j in range(len(self.xBins)-1):
                self.PLT.text(xbins[j]+ delx*0.5, ybins[i] + dely*0.5, round(hist.T[i, j], 2), color = "black", ha = "center", va = "center", fontweight = "bold", size = "20")

   
    def SetBinContent(self):
        self.xBins = self.xData.copy()
        del_x = abs(self.xBins[0]-self.xBins[1])
        self.xBins += [max(self.xBins)+del_x]
        self.xBins = list(np.array(self.xBins) - del_x*0.5)

        self.yBins = self.yData.copy()
        del_y = abs(self.yBins[0]-self.yBins[1])
        self.yBins += [max(self.yBins)+del_y]
        self.yBins = list(np.array(self.yBins) - del_y*0.5)

        if len(self.Weights) == len(self.xData) and len(self.Weights[0]) == len(self.yData):
            self.Weights = [self.Weights[x][y] for x in range(len(self.xData)) for y in range(len(self.yData))] 
            x_t = [x for x in self.xData for y in self.yData]
            y_t = [y for x in self.xData for y in self.yData]
            self.xData = x_t
            self.yData = y_t


    def CompileHistogram(self):
        self.Init_PLT()
        self.Colorscheme = self.PLT.cm.rainbow
        self.TransformData("xData", "xLabels")
        self.TransformData("yData", "yLabels")
        self.PLT.title(self.Title)

        if self.Weights != None:
            self.SetBinContent()

        if len(self.yData) == len(self.xData) and self.Weights == None: 
            if not isinstance(self.yData[0], list):
                pass
            else:
                yUpdate = []
                xUpdate = []
                for i in self.xData:
                    for j in self.yData[i]: 
                        yUpdate.append(j)
                        xUpdate.append(i)
                self.xData = xUpdate
                self.yData = yUpdate


        if self.Weights == None:
            self.xAxis()
            self.yAxis()

        hist, xbins, ybins, im = self.PLT.hist2d(self.xData, self.yData, bins = [self.xBins, self.yBins], 
                range=[[self.xMin, self.xMax], [self.yMin, self.yMax]], 
                cmap = self.Colorscheme, weights = self.Weights)

        
        self.PLT.xticks(self.xData)
        self.PLT.yticks(self.yData)
        self.PLT.xlabel(self.xTitle)
        self.PLT.ylabel(self.yTitle)
        self.PLT.colorbar()

        if self.ShowBinContent:
            self.ShowBins(hist, xbins, ybins)

        if self.Diagonal:
            self.PLT.plot([self.xMin, self.xMax], [self.yMin, self.yMax], ls="--", c=".3")

        if len(self.xLabels) != 0:
            self.TransformData("xLabels", "xData")
            self.PLT.xticks(self.xLabels, self.xData, rotation = 45, rotation_mode = "anchor", ha = "right")
        if len(self.yLabels) != 0:
            self.PLT.yticks(self.yLabels, self.yData, rotation = 45, rotation_mode = "anchor", ha = "right")
        self.Compiled = True

class CombineHistograms(SharedMethods, GenericAttributes):
    def __init__(self):
        SharedMethods.__init__(self)
        GenericAttributes.__init__(self) 
        self.Normalize = False
        self.Histograms = []
        self.Title = ""
        self.Log = False
        self.Compiled = False

    def CompileHistogram(self):
        self.Init_PLT()
        if self.Title != "":
            self.PLT.title(self.Title)
        
        self.Histograms = [i for i in self.Histograms if len(i.xData) != 0]
        
        for i in range(len(self.Histograms)):
            H = self.Histograms[i]
            if H.Color != "":
                self.PLT.hist(H.xData, bins = H.xBins, range=(H.xMin,H.xMax), 
                        label = H.Title, alpha = H.Alpha, log = self.Log, color = H.Color, 
                        density = self.Normalize, histtype = "stepfilled", edgecolor = "black")
            else: 

                col = ["blue", "orange", "green", "red", "cyan", "purple"]
                ec = colors.to_rgba(col[i])
                c = colors.to_rgba(col[i])
                self.PLT.hist(H.xData, bins = H.xBins, range=(H.xMin,H.xMax), 
                        label = H.Title, facecolor = (c[0], c[1], c[2], H.Alpha), log = self.Log, density = self.Normalize, 
                        edgecolor = (ec[0], ec[1], ec[2], 1), histtype = "stepfilled", linewidth = 0.5)
                

        if len(self.Histograms) != 0:
            self.PLT.xlabel(self.Histograms[0].xTitle)
            self.PLT.ylabel(self.Histograms[0].yTitle)
        self.PLT.legend(loc=self.LegendPos)
        if self.Filename == "":
            self.Filename = self.Title + ".png"
        self.Compiled = True
        self.PLT.tight_layout()

    def Save(self, dir):
        self.SaveFigure(dir) 
        for i in self.Histograms:
            del i
        self.PLT = ""


class CombineTGraph(SharedMethods, GenericAttributes):
    
    def __init__(self):
        SharedMethods.__init__(self)
        GenericAttributes.__init__(self)
        self.Normalize = False
        self.Lines = []
        self.Title = ""
        self.Log = False
        self.yMin = 0
        self.yMax = 1
        self.Compiled = False
    
    def CompileLine(self):
        self.Init_PLT()
        if self.Title != "":
            self.PLT.title(self.Title)

        for i in range(len(self.Lines)):
            H = self.Lines[i]

            if H.ErrorBars:
                self.PLT.errorbar(x = H.xData, y = H.yData, yerr = [H.Lo_err, H.Up_err], color = H.Color, linestyle = "-", capsize = 3, linewidth = 1, alpha = H.Alpha, label = H.Title)
            else: self.PLT.plot(H.xData, H.yData, marker = H.Marker, color = H.Color, linewidth = 1, alpha = H.Alpha, label = H.Title)
        
        self.PLT.ylim(self.yMin, self.yMax)

        if len(self.Lines) != 0:
            self.PLT.xlabel(self.Lines[0].xTitle)
            self.PLT.ylabel(self.Lines[0].yTitle)
        self.PLT.legend(loc="upper right")
        self.PLT.tight_layout()
        self.Filename = self.Title + ".png"
        self.Compiled = True

    def Save(self, dir):
        self.CompileLine()
        self.SaveFigure(dir) 



class SubfigureCanvas(SharedMethods):
    def __init__(self):
        self.FigureObjects = []
        self.Title = ""
        self.DefaultScaling = 8
        self.DefaultDPI = 500
        SharedMethods.__init__(self)
        self.Compiled = False

    def AddObject(self, obj):
        self.FigureObjects.append(obj)
    
    def AppendToKey(self, key, val):
        if val != "":
            self.__dic[key] = val

    def AppendToPLT(self, hist):
        self.__dic = {}
        self.AppendToKey("align", hist.Align)
        self.AppendToKey("bins", hist.xBins)
        self.AppendToKey("range", (hist.xMin, hist.xMax))
        self.AppendToKey("density", hist.Normalize)
        self.AppendToKey("align", hist.Align)
        
        self.PLT.subplot(int(str(self.y) + str(self.x) + str(self.k)))
        self.PLT.title(hist.Title)
        self.PLT.hist(hist.xData, **self.__dic)
        self.PLT.xlabel(hist.xTitle)
        self.PLT.ylabel(hist.yTitle)       
    
    def CompileHistogram(self):
        self.PLT = plt
        self.PLT.figure(figsize = (len(self.FigureObjects)*self.DefaultScaling, self.DefaultScaling), dpi = self.DefaultDPI)
        
        self.y = 1
        self.x = len(self.FigureObjects)
        self.k = 0
        for i in self.FigureObjects:
            self.k += 1
            self.AppendToPLT(i)

        self.Compiled = True

class TGraph(SharedMethods, GenericAttributes):

    def __init__(self):
        SharedMethods.__init__(self)
        GenericAttributes.__init__(self)
        self.ErrorBars = False
        self.Compiled = True

    def Line(self):
        err = []
        self.Up_err = []
        self.Lo_err = []
        if isinstance(self.yData[0], list) == True:
            self.ErrorBars = True
            tmp = []
            for i in self.yData:
                av = np.array(i)
                tmp.append(np.average(av))
                err.append(np.std(av))  
                self.Up_err.append(abs(np.average(av)+np.std(av)))
                self.Lo_err.append(abs(np.average(av)-np.std(av)))
                
            self.yData = tmp
        
        self.yBins = 1
        self.xAxis()
        self.yAxis()

        self.Init_PLT()
        if self.ErrorBars:
            self.PLT.errorbar(x = self.xData, y = self.yData, yerr = [self.Lo_err, self.Up_err], color = self.Color, linestyle = "-", capsize = 3, linewidth = 1)
        else:
            self.PLT.plot(self.xData, self.yData, marker = self.Marker, color = self.Color, linewidth = 1)
        self.PLT.xlabel(self.xTitle)
        self.PLT.ylabel(self.yTitle)
        self.PLT.xlim(0, self.xMax)
        self.PLT.ylim(0, self.yMax*2)
    
    def Save(self, dir):
        self.Line()
        self.SaveFigure(dir) 
