    prev_who = Status.query.filter(Status in txt.children.all()).delete()
    print(prev_who)    
    if who not in txt.children.all():
        txt.children.append(who)
        
    pts = General_txt.query.filter(General_txt in who.parents.all()).delete()
    print(pts)   
    if txt not in who.parents.all():
        who.parents.append(txt)
     