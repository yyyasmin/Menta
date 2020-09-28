    if request.form['submit'] == 'submit_tag':
        selected_tag = request.form['selected_tag']
        selected_ar = Tag.query.filter(Tag.title == selected_tag)
        selected_ar = tag_select2(selected_ar.id)
        
        #If already selected and saved form prevous methos call
        tmp_age_range = Age_range.query.filter(Age_range.query.filter(Age_range.selected == True)
        if tmp_age_range != None:
            selected_age_range = tmp_tag.title   
        else:
            selected_tag = "בחר נושא"