   
        
@std.route('/tag_sub_tag_to_profile_add', methods=['GET', 'POST'])
def tag_sub_tag_to_profile_add():
            
    print("")
    print("")
    print("IN tag_sub_tag_to_profile_add ")

    tag_id =  request.form['tag_id']
    sub_tag_id = request.form['sub_tag_id']

    
    #print("tag_id: ", tag_id)
    print("sub_tag_id: ", sub_tag_id)
      
    tag = tag_select2(tag_id)
    sub_tag = sub_tag_select2(sub_tag_id)
    
    print("")
    print("")
    print("IN tag_sub_tag_to_profile_add AFTER SELECT2: ")
    print("tag_id: ", tag.id)
    print("sub_tag_id: ", sub_tag.id)
    
    profile = Profile.query.filter(Profile.selected==True).first()
    profile.set_parent(tag)
    profile.set_parent(sub_tag)
    
    newSubj = Subject('New', 'New', get_author_id())
    
    profile.set_parent(newSubj)
    tag.set_parent(newSubj)
    sub_tag.set_parent(newSubj)
    
    newSubj.set_parent(tag)
    newSubj.set_parent(sub_tag)
    
    db.session.commit()
    
    print("")
    print("")
    print("IN END OF tag_sub_tag_to_profile_add , calling std_edit_profile")
    print("")
    print("")
    
    return std_edit_profile(1)
  
  