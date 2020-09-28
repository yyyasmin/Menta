	
@std.route('/student_gts', methods=['GET', 'POST'])
@login_required
def student_gts():

    
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
  
    ############impor pdb;pdb.set_trace()
    
    std_gts = General_txt.query.join(Std_general_txt).filter(Std_general_txt.student_id==std.id).filter(Std_general_txt.general_txt_id==General_txt.id).all()
    
    ########import pdb;; pdb.set_trace()
    
    student_gts = []    # Get all student's destinations
    all_gts = Subjects.query.filter(Subjects.hide==False).all()  
    for d in all_gts:
        std_gt = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).filter(Std_general_txt.general_txt_id==d.id).first()
        if std_gt !=None:
           student_gts.append(d)            
    destinations_not_of_student = list(set(all_gts).difference(set(student_gts)))  #destinations_not_of_student = all_destinations - std_destinations
   

    
    std_txts = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).all()


    ########import pdb;; pdb.set_trace()
    ####print("std gts,          ", student_gts)
    ####import pdb; pdb.set_trace()
    #print("std goals,         ", student_goals)
    ####print("std todos          ", student_todos)
    ####print("statuss        ", statuss)
    
    tags = Tag.query.order_by(Tag.title).all()


    return render_template('./gt/table_destinations/edit_profile.html', std=std,  
                                                        student_gts=student_gts, destinations_not_of_student=destinations_not_of_student,
                                                        all_goals=all_goals, student_goals=student_goals, goals_not_of_student=goals_not_of_student,
                                                        all_todos=all_todos, student_todos=student_todos, todos_not_of_student=todos_not_of_student,
                                                        std_txts=std_txts,
                                                        statuss=statuss, default_status=default_status,
                                                        whos=whos, default_who=default_who,
                                                        tags=tags, age_ranges=age_ranges,
                                                        due_date=due_date)
                                                
														  		
@std.route('/student_gts2/<int:selected_student_id>/<int:selected_destination_id>', methods=['GET', 'POST'])
@login_required
def student_gts2(selected_student_id, selected_destination_id):

    std = student_select2(selected_student_id)
    std = destination_select2(selected_destination_id)
    ########print("In student_gts2 std std :", std, std.id)

    return student_gts()

