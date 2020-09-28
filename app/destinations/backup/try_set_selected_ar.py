
###set selected_ar	
@dst.route('/set_selected_ar>', methods=['GET', 'POST'])
def set_selected_ar():
    selected_age_range = request.form['selected_age_range']      #Current Age_range selection

    selected_ar = Age_range.query.filter(Age_range.title == selected_age_range).first()   #Save for next method call
    selected_ar = age_range_select2(selected_ar.id)
    return selected_ar   
###end set selected_ar	

###get selected tag	
@dst.route('/get_selected_tag>', methods=['GET', 'POST'])
def get_selected_tag():
    #If already selected and saved form prevous methods call
    tmp_tag = Tag.query.filter(Tag.selected == True).first()
    if tmp_tag != None:
        selected_tag = tmp_tag.title   
    else:
        selected_tag = "בחר נושא"        
    return selected_tag
###end get selected tag	
