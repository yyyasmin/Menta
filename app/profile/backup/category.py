    																 	
 ###START set selected category		
@prf.route('/set_gt_category/<int:selected_category_title>/<int:selected_gt_id>', methods=['GET', 'POST'])
def set_gt_category(Subject, Tag, selected_category_title, selected_gt_id, str_msg):

    ###################import pdb;; pdb.set_trace()
    #print("IN set_prf_category")
    
   # POST case
    selected_category = eval(Tag).query.filter(eval(Tag).title == selected_category_title).first()   
    #print("In set_prf_age_range SSSSSSSSS Selected category is   type: ", selected_category, selected_category.type, selected_category.__tablename__)
    if selected_category == None:
        flash(str_msg)
        return(url_for('profile.edit_profile'))
    
    selected_category = general_txt_select2(selected_category.id) 

    gt = eval(Subject).query.filter(eval(Subject).selected==True).first()
    if gt == None:
        flash("Please select a Subject first")
        return(url_for('profile.edit_profile', from_prf_sort_order=3))

    for category in eval(Tag).query.all():   #delete the prevois category of the updated profile and ser the new one
        if gt.is_parent_of(category):
            gt.unset_parent(category)
            gt.set_parent(selected_category)
           
    gt.set_parent(selected_category)  # Uncase there is no previous category for gt 
    
    db.session.commit() 
    return selected_category
 ###END set selected age_range	
    
###get selected security option	category	
@prf.route('/get_selected_category_title', methods=['GET', 'POST'])
def get_selected_category_title(msg):
    tmp_category = eval(Tag).query.filter(eval(Tag).selected == True).first()
    if tmp_category != None:
        selected_category_title = tmp_category.title   
    else:
        selected_category_title = "msg"        
    return selected_category_title
###end get selected security option	category
