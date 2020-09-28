###set selected security option	scrt
@dst.route('/set_selected_scrt>', methods=['GET', 'POST'])
def set_selected_scrt():
    selected_scrt = request.form['selected_scrt']      #Current Age_range selection

    selected_scrt = Security.query.filter(Security.title == selected_scrt).first()   #Save for next method call
    selected_scrt = age_range_select2(selected_scrt.id)
    return selected_scrt   
###set selected security option scrt


###get selected security option	scrt	
@dst.route('/get_selected_scrt>', methods=['GET', 'POST'])
def get_selected_scrt():
    #If already selected and saved form prevous methods call
    tmp_scrt = Security.query.filter(Security.selected == True).first()
    if tmp_scrt != None:
        selected_scrt = tmp_scrt.title   
    else:
        selected_scrt = ":בחר אופצית אבטחה"        
    return selected_scrt
###end get selected security option	scrt	