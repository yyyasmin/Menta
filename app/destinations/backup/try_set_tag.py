@dst.route('/set_dst_tag', methods=['POST'])
def set_dst_tag():
    
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        
    selected_tag = request.form['selected_tag_title']      #Current Tag selection
                                                      
    selected_tag = Tag.query.filter(Tag.title == selected_tag).first()   
    selected_tag = tag_select2(selected_tag.id)    
        
    dst.tag_id = selected_tag.id
    if dst not in selected_tag.destinations:
        selected_tag.destinations.append(dst)
        
    db.session.commit()
    
    return selected_tag.title    
    
###get selected security option	tag	
@dst.route('/get_selected_tag_title', methods=['GET', 'POST'])
def get_selected_tag_title():
    tmp_tag = Tag.query.filter(Tag.selected == True).first()
    if tmp_tag != None:
        selected_tag_title = tmp_tag.title   
    else:
        selected_tag_title = ":בחר אופצית אבטחה"        
    return selected_tag_title
###end get selected security option	tag