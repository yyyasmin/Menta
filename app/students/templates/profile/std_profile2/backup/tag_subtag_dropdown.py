            
    ################## UPDATE PROFILE sub_tag ##################
    if 'selected_sub_tag' in request.form:
        print("request.form['selected_sub_tag']", request.form['selected_sub_tag'])
        sub_tag = Tag.query.filter(Tag.title==request.form['selected_sub_tag']).first()
        if sub_tag != None:
            selected_sub_tag = sub_tag
            selected_sub_tag = tag_select2(selected_sub_tag.id)
        print("")
        print("IN set_profile_tag sub_tag = ", sub_tag)
        print("IN set_profile_tag selected_sub_tag = ", selected_sub_tag)
        tag.set_paren(sub_tag);
        selected_sub_tag = sub_tag_select2(selected_sub_tag.id)
        print(selected_sub_tag.id)
        print("")
        
        db.session.commit()
        return edit_std_profile()
            
    db.session.commit()                 
    return edit_std_profile()
      
    