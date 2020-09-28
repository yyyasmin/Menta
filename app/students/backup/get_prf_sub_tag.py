
#FROM  https://stackoverflow.com/questions/45131503/unable-to-receive-data-from-ajax-call-flask
@std.route('/get_sub_tag_profile', methods=['GET', 'POST'])
def get_sub_tag_profile():
        
    if 'selected_tag' in request.form:
        tag = Tag.query.filter(Tag.id==request.form['selected_tag']).first()
        if tag != None:
            selected_tag = tag_select2(tag.id)
        print("")
        print("IN update_std_txt tag = ", tag)
        print("IN update_std_txt selected_tag = ", selected_tag)
    
    if 'save_st' in request.form:
        print("")
        print("request.form['save_st']", request.form['save_st'])
        
        #FROM https://stackoverflow.com/questions/4289331/how-to-extract-numbers-from-a-string-in-python
        ### EXTRACT NUMBER FROM STRING
        sub_tag_id = re.sub(r"\D", "", request.form['save_st'])
        print("")
        print("sub_tag ID:", sub_tag_id)
        sub_tag = Sub_tag.query.filter(Sub_tag.id==sub_tag_id).first()
        if sub_tag != None:
            selected_sub_tag = sub_tag_select2(sub_tag.id)
    
    print("")
    print("IN get_updated_settings calling update_std_txt2 with tag:{0}  --- sub_tag:{1}   :".format( selected_tag.id, selected_sub_tag.id))
    print("")
    print("")
    
    sub_tag = Sub_tag.query.filter(Sub_tag.id==sub_tag_id).first()
    print("")
    print("IN END OF get_sub_tag_profile BEFORE profile select -- sub_tag:", sub_tag)
    
    
    prf = reset_and_get_profile(0)
   
    sub_tag = Sub_tag.query.filter(Sub_tag.id==sub_tag_id).first()
    print("")
    print("IN END OF get_sub_tag_profile AFTER profile select -- sub_tag:", sub_tag)
        
    
    prf.set_parent(tag)
    prf.set_parent(sub_tag)
    
    db.session.commit()
    
    
    print(" IN END OF get_sub_tag_profile")
    print("")
    print("prf", prf.id)
    print("tag", tag)
    print("sub_tag", sub_tag)
    print("prf.is_parent_of(tag)", prf.is_parent_of(tag))
    print("prf.is_parent_of(sub_tag)", prf.is_parent_of(sub_tag))
         
    return redirect(url_for('profile.std_edit_profile', selected_student_id=selected_student_id, from_prf_sort_order=3 ))
   
   #FROM https://stackoverflow.com/questions/41268096/getting-flask-to-alter-selected-value-in-html-drop-down
               