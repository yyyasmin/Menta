 ###START set selected age_range		
@dst.route('/set_dst_age_range', methods=['POST'])
def set_dst_age_range(selected_ar_title):
    print("In  set_dst_age_range TTT title is: ", selected_ar_title) 
    
    selected_ar_title = selected_ar_title      #Current Age_range selection

   # POST case
    selected_ar = Age_range.query.filter(Age_range.title == selected_ar_title).first()   
    print("In set_dst_age_range SSSSSSSSS Selected ar is   type: ", selected_ar, selected_ar.type, selected_ar.__tablename__)
    if selected_ar == None:
        flash("יש לבחור קבוצת גיל")
        return(url_for('destinations.destination_add', from_dst_sort_order=0, selected_ar_title = "בחר קבוצת גיל", selected_tag_title = "בחר נושא", selected_scrt_title = "בחר סוג אבטחה" ))
    
    selected_ar = age_range_select2(selected_ar.id) 
    print(" selected_ar BBBBBBBBBBBBBBBBBB BRFORE : ", selected_ar)
    selected_ar = Age_range.query.filter(Age_range.id==selected_ar.id).first()
    print(" selected_ar AAAAAAAAAAAAAAAAAAA AFTER : ", selected_ar)

    dst = Destination.query.filter(Destination.selected==True).filter(Destination.type=='destination').first()
    ar_dst = General_txt_general_choice.query.filter(General_txt_general_choice.general_txt_id==dst.id).filter(General_txt_general_choice.general_choice_id==selected_ar.id).first()
    
    if ar_dst == None:    
        ar_dst = General_txt_general_choice(dst.id, selected_ar.id)        
        db.session.add(ar_dst)        
        db.session.commit() 
        print("***************************************")
        print("ar dst: ", ar_dst, ar_dst.general_txt_id, ar_dst.general_txt_id)
        if dst != None:                       
            if ar_dst not in selected_ar.general_txts:
                selected_ar.general_txts.append(ar_dst)
            if ar_dst not in dst.general_choices:
                dst.general_choices.append(ar_dst)
            
    db.session.commit() 
    return selected_ar
 ###END set selected age_range	
    