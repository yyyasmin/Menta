
    dst = Destination.query.filter(Destination.selected==True).first() 
    import pdb; pdb.set_trace()
    old_dst_tag = General_txt_general_choice.query.join(Tag).filter(Tag.id==General_txt_general_choice.general_choice_id).filter(General_txt_general_choice.general_txt_id==dst.id).first()    #delete the prevois tag of the updated destination 
    db.session.delete(old_dst_tag)
    
    #### Set the new tag ####
    tag_dst = General_txt_general_choice(dst.id, selected_tag.id)    
    db.session.add(tag_dst)        
    db.session.commit() 
    print("***************************************")
    print("tag dst: ", tag_dst, tag_dst.general_txt_id, tag_dst.general_txt_id)
    if dst != None:                       
        if tag_dst not in selected_tag.general_txts:
            selected_tag.general_txts.append(tag_dst)
        if tag_dst not in dst.general_choices:
            dst.general_choices.append(tag_dst)
        