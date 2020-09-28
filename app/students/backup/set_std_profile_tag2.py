
@prf.route('/set_std_profile_tag2', methods=['GET', 'POST'])
@login_required
def set_std_profile_tag2():

    print("")
    print("")
    
    if 'profile_submit_btn' in request.form:
        print("request.form['profile_submit_btn']", request.form['profile_submit_btn'])
    
    print("")
    
    
    if 'selected_tag' in request.form:
        print("request.form['selected_tag']", request.form['selected_tag'])
        tag = Tag.query.filter(Tag.title==request.form['selected_tag']).first()
        if tag != None:
            selected_tag = tag
            selected_tag = tag_select2(selected_tag.id)
        print("")
        print("IN set_profile_tag tag = ", tag)
        print("IN set_profile_tag selected_tag = ", selected_tag)
        selected_tag = tag_select2(selected_tag.id)
        print(selected_tag.id)
        print("")
    
    return edit_profile2_by_tag()     
    