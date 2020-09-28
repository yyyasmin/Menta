
 ###START set selected age_range		
@dst.route('/set_dst_age_range', methods=['POST'])
def set_dst_age_range(selected_scrt_title):
    print("In  set_dst_age_range TTT title is: ", selected_scrt_title) 
    
    selected_scrt_title = selected_scrt_title      #Current Scrt selection

   # POST case
    selected_scrt = Scrt.query.filter(Scrt.title == selected_scrt_title).first()   
    print("In set_dst_age_range SSSSSSSSS Selected scrt is   type: ", selected_scrt, selected_scrt.type, selected_scrt.__tablename__)
    if selected_scrt == None:
        flash("יש לבחור קבוצת גיל")
        return(url_for('destinations.destination_add', from_dst_sort_order=0, selected_scrt_title = "בחר קבוצת גיל", selected_scrt_title = "בחר נושא", selected_scrt_title = "בחר סוג אבטחה" ))
    
    selected_scrt = age_range_select2(selected_scrt.id) 
    print(" selected_scrt BBBBBBBBBBBBBBBBBB BRFORE : ", selected_scrt)
    selected_scrt = Scrt.query.filter(Scrt.id==selected_scrt.id).first()
    print(" selected_scrt AAAAAAAAAAAAAAAAAAA AFTER : ", selected_scrt)

    dst = Destination.query.filter(Destination.selected==True).first()

    old_dst_scrt=None
    for scrt in Scrt.query.all():   #delete the prevois age_range of the updated destination 
        if dst.is_pscrtent_of(scrt):
            old_dst_scrt = scrt
            break
   
    if old_dst_scrt != None:
        if dst in old_dst_scrt.pscrtents:
            if old_dst_scrt in dst.children:
                dst.children.remove(old_dst_scrt)
            if dst in old_dst_scrt.pscrtents:
                old_dst_scrt.pscrtents.remove(dst)
                
    if selected_scrt not in dst.children:
        dst.children.append(selected_scrt)
    if dst not in selected_scrt.pscrtents:
        selected_scrt.pscrtents.append(dst)
                
    #old_dst_scrt pdb.set_trace()
    
    db.session.commit() 
    return selected_scrt
 ###END set selected age_range	
    