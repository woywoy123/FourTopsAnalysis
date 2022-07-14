def Sort (a,target,Top_Number)
    if isinstance(a, list)
        for i in a:
            target.Index = Top_Number
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
            Final_Particles.append(a)
        elif D1_i == D2_i:
            a.Decay.append(Part_i[D1_i])
            a.Index = Top_Number
            return Sort(Part_i[D1_i], a, Top_Number)
        elif D1_i != D2_i
            Decays = Part_i[D1_i : (D2_i+1)]
            a.Index = Top_Number
            return Sort(Decays,a,Top_Number)
