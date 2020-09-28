    																 	
 ###START set selected category		
@prf.route('/set_gt_category/<int:selected_category_title>/<int:selected_gt_id>', methods=['POST'])
def set_gt_category(selected_category_title, selected_gt_id, str_msg):

    ##############import pdb;; pdb.set_trace()
    #print("IN set_prf_category")
    
   # POST case
    selected_category = eval(Category).query.filter(eval(Category).title == selected_category_title).first()   
    #print("In set_prf_age_range SSSSSSSSS Selected category is   type: ", selected_category, selected_category.type, selected_category.__tablename__)
    if selected_category == None:
        flash(str_msg)
        return(url_for('profile.profile_add', from_prf_sort_order=0, selected_ar_title = "בחר קבוצת גיל", selected_category_title = "בחר נושא", selected_scrt_title = "בחר סוג אבטחה" ))
    
    selected_category = general_txt_select2(selected_category.id, eval(Category)) 

    gt = eval(Gt).query.filter(eval(Gt).selected==True).first()
    if gt == None:
        flash("Please select a subject first")
        return(url_for('profile.edit_profile', from_prf_sort_order=3))

    for category in eval(Category).query.all():   #delete the prevois category of the updated profile and ser the new one
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
    tmp_category = eval(Category).query.filter(eval(Category).selected == True).first()
    if tmp_category != None:
        selected_category_title = tmp_category.title   
    else:
        selected_category_title = "msg"        
    return selected_category_title
###end get selected security option	category

##############profile categorys###############	

