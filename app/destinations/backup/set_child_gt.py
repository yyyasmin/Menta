
 ###START set selected age_range		
@dst.route('/set_dst_child', methods=['POST'])
def set_dst_child(title, class_name):

    print("In  set_gt_child TILE : ", title) 
    
   # POST case
    selected_child = eval(class_name).query.filter(eval(class_name).title == title).first()   
    if selected_child == None:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_dst_form_for_update.html')
    
    selected_child = gt_type_select2(selected_child.id)



    dst = Destination.query.filter(Destination.selected==True).first()

    old_dst_child=None
    for ar in eval(class_name).query.all():   #delete the prevois child of the updated destination 
        if dst.is_parent_of(ar):
            dst.unset_parent(ar)
            
    #print(" 111 IN set_gt_child dst.children is: ", dst.children )
    
    dst.set_parent(selected_child)
    
    #print(" 222 IN set_gt_child dst.children is: ", dst.children )
   
    db.session.commit()

    #####################import pdb;; pdb.set_trace()
    return selected_child
 ###END set selected age_range	
    