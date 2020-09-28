 ##############START studets plan report###############
	
@std.route('/plan_report', methods=['GET', 'POST'])
@login_required
def plan_report():
		  
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
  
    ############impor pdb;pdb.set_trace()
    
    std_gts = General_txt.query.join(Std_general_txt).filter(Std_general_txt.student_id==std.id).filter(Std_general_txt.general_txt_id==General_txt.id).all()
    
    ##import pdb; pdb.set_trace()
    
    student_dsts = []    # Get all student's destinations
    all_dsts = Destination.query.filter(Destination.hide==False).all()  
    for d in all_dsts:
        std_dst = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).filter(Std_general_txt.general_txt_id==d.id).first()
        if std_dst !=None:
           student_dsts.append(d)            
    destinations_not_of_student = list(set(all_dsts).difference(set(student_dsts)))  #destinations_not_of_student = all_destinations - std_destinations
   
    print ("std_gts: ", std_gts)
    
    student_goals = []    # Get all student's destinations
    all_goals = Goal.query.filter(Goal.hide==False).all()
    print ("all_goals: ", all_goals)
    for g in std_gts:
        if g in all_goals:
            student_goals.append(g)
    goals_not_of_student = list(set(all_goals).difference(set(student_goals)))  #goals_not_of_student = all_destinations - std_destinations
                                 
    student_todos = []    # Get all student's destinations
    all_todos = Todo.query.filter(Todo.hide==False).all()
    print ("all_todos: ", all_todos)
    for g in std_gts:
        if g in all_todos:
            student_todos.append(g)
    todos_not_of_student = list(set(all_todos).difference(set(student_todos)))  #todos_not_of_student = all_destinations - std_destinations
      
    whos = Accupation.query.all()
    default_who = Accupation.query.filter(Status.body=='default').first()

    statuss = Status.query.all()
    default_status = Status.query.filter(Status.body=='default').first()
        
    whos = Accupation.query.all()
    default_who = Accupation.query.filter(Accupation.body=='default').first()

    tags = Tag.query.all()
    
    std_txts = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).all()


    due_date = date.today()

    ##import pdb; pdb.set_trace()
    #print("std dsts,          ", student_dsts)
    #print("std goals,         ", student_goals)
    #print("std todos          ", student_todos)
    #print("statuss        ", statuss)
    
    age_ranges = Age_range.query.order_by(Age_range.title).all()
    tags = Tag.query.order_by(Tag.title).all()

    return render_template('plan_report/plan_report.html', 
                                                        std=std,  
                                                        student_dsts=student_dsts, destinations_not_of_student=destinations_not_of_student,
                                                        all_goals=all_goals, student_goals=student_goals, goals_not_of_student=goals_not_of_student,
                                                        all_todos=all_todos, student_todos=student_todos, todos_not_of_student=todos_not_of_student,
                                                        std_txts=std_txts,
                                                        statuss=statuss, default_status=default_status,
                                                        whos=whos, default_who=default_who,
                                                        tags=tags, age_ranges=age_ranges,
                                                        due_date=due_date,
                                                        student_staff_teachers=student_staff_teachers,
                                                        profile=profile)
       
@std.route('/plan_report2/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def plan_report2(selected_student_id):
    #####print("In plan_report2 Request is :", request)
    std = student_select2(selected_student_id)

    return redirect(url_for('students.plan_report'))

##############END studets plan report###############	



		  
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
  
    ############impor pdb;pdb.set_trace()
    
    std_gts = General_txt.query.join(Std_general_txt).filter(Std_general_txt.student_id==std.id).filter(Std_general_txt.general_txt_id==General_txt.id).all()
    
    ##import pdb; pdb.set_trace()
    
    student_dsts = []    # Get all student's destinations
    all_dsts = Destination.query.filter(Destination.hide==False).all()  
    for d in all_dsts:
        std_dst = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).filter(Std_general_txt.general_txt_id==d.id).first()
        if std_dst !=None:
           student_dsts.append(d)            
    destinations_not_of_student = list(set(all_dsts).difference(set(student_dsts)))  #destinations_not_of_student = all_destinations - std_destinations
   
    print ("std_gts: ", std_gts)
    
    student_goals = []    # Get all student's destinations
    all_goals = Goal.query.filter(Goal.hide==False).all()
    print ("all_goals: ", all_goals)
    for g in std_gts:
        if g in all_goals:
            student_goals.append(g)
    goals_not_of_student = list(set(all_goals).difference(set(student_goals)))  #goals_not_of_student = all_destinations - std_destinations
                                 
    student_todos = []    # Get all student's destinations
    all_todos = Todo.query.filter(Todo.hide==False).all()
    print ("all_todos: ", all_todos)
    for g in std_gts:
        if g in all_todos:
            student_todos.append(g)
    todos_not_of_student = list(set(all_todos).difference(set(student_todos)))  #todos_not_of_student = all_destinations - std_destinations
      
    whos = Accupation.query.all()
    default_who = Accupation.query.filter(Status.body=='default').first()

    statuss = Status.query.all()
    default_status = Status.query.filter(Status.body=='default').first()
        
    whos = Accupation.query.all()
    default_who = Accupation.query.filter(Accupation.body=='default').first()

    tags = Tag.query.all()
    
    std_txts = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).all()


    due_date = date.today()

    ##import pdb; pdb.set_trace()
    #print("std dsts,          ", student_dsts)
    #print("std goals,         ", student_goals)
    #print("std todos          ", student_todos)
    #print("statuss        ", statuss)
    
    age_ranges = Age_range.query.order_by(Age_range.title).all()
    tags = Tag.query.order_by(Tag.title).all()


    return render_template('./destinations/table_destinations/edit_all_dsts.html', std=std,  
                                                        student_dsts=student_dsts, destinations_not_of_student=destinations_not_of_student,
                                                        all_goals=all_goals, student_goals=student_goals, goals_not_of_student=goals_not_of_student,
                                                        all_todos=all_todos, student_todos=student_todos, todos_not_of_student=todos_not_of_student,
                                                        std_txts=std_txts,
                                                        statuss=statuss, default_status=default_status,
                                                        whos=whos, default_who=default_who,
                                                        tags=tags, age_ranges=age_ranges,
                                                        due_date=due_date)
           