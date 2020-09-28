        
        if 'selected_tag' in request.form:
        #print("")
        #print("request.form['selected_tag']", request.form['selected_tag'])
        tag = Tag.query.filter(Tag.title==request.form['selected_tag']).first()
        if tag != None:
            selected_tag = tag
            selected_tag = age_range_select2(selected_tag.id)
        #print("")
        #print("IN update_std_txt tag = ", tag)
        #print("IN update_std_txt selected_tag = ", selected_tag)
        #return student_dsts()   ??????????? ###
    