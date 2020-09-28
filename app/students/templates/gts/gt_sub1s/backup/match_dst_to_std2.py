   
##############START match_dst_to_dst ###############	

@dst.route('/match_dst_to_dst', methods=['POST'])
@login_required
def match_dst_to_std():

    ###################import pdb;;;;;pdb.set_trace()
    #print("IN dst_to_student_add")
    ###########################impor pdb;pdb.set_trace()
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('destination.edit_students'))

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_student_destinations'))		
   
    statuss = Status.query.all()
    
    #print(" dst dst dst ", dst, dst, dst )

    new_std_dst = Std_general_txt.query.filter(Std_general_txt.student_id == dst.id).filter(Std_general_txt.general_txt_id==dst.id).first()
    new_dst = False
    if new_std_dst == None:   #new Std_dst
        new_dst = True
        new_std_dst = Std_general_txt(dst.id, dst.id)                
        new_std_dst.general_txt = dst
        new_std_dst.student = std    
        new_std_dst.general_txt_id = dst.id
        new_std_dst.student_id = std.id
        new_std_dst.due_date = request.form.get('due_date') 
       
        sts_title = request.form.get('selected_status')
        sts = Status.query.filter(Status.title==sts_title).first() 
        dst.children.append(sts)
        new_std_dst.status_id = sts.id
        

    #print("dst is  for dst is : Std_dst student is  ", dst_dst, dst)
    
    dst.selected = False
    #DEBUG
    db.session.commit() 
    db.session.refresh(dst)
    db.session.refresh(dst)
    db.session.refresh(dst_dst)

    ###print("dst_to_student_add METHOD", request.method)
    return  redirect(url_for('students.edit_student_dsts')) 
        
		
@dst.route('/match_dst_to_dst2/<int:selected_dst_id>', methods=['GET', 'POST'])
@login_required
def match_std_to_dst2(selected_dst_id):

    #print("IN match_dst_to_dst2   dst ", selected_dst_id)
    
    ###import_pdb; pdb.set_trace()
    dst = dst_select2(selected_dst_id)
    
    return match_dst_to_dst()
    
##############END match_dst_to_dst ###############	

