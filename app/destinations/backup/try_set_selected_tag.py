###set selected_ar	
@dst.route('/set_selected_tag>', methods=['GET', 'POST'])
def set_selected_tag():	
    selected_tag = request.form['selected_tag']      #Current Tag selection
    
    last_selected_tag = Tag.query.filter(Tag.title == selected_tag).first()   #Save for next method call
    last_selected_tag = tag_select2(last_selected_tag.id)
       
    return last_selected_tag
 ###end set selected tag
 

###get selected age_range	
@dst.route('/get_selected_ar>', methods=['GET', 'POST'])
def get_selected_ar():
    #If already selected and saved form prevous methos call
    tmp_age_range = Age_range.query.filter(Age_range.selected == True).first()
    if tmp_age_range != None:
        selected_age_range = tmp_age_range.title   
    else:
        selected_age_range = "בחר קבוצת גיל"
                 
    return selected_age_range
###get save selected age_range
