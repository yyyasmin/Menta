
	
##############START studets stds###############	
	
@std.route('/edit_student_stds', methods=['GET', 'POST'])
@login_required
def edit_student_stds():

    
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
  
    ############impor pdb;pdb.set_trace()
    
    student_dsts = []
    all_dsts = Destination.query.all()  
    for d in all_dsts:
        if d in std.general_txts:
           student_dsts.append(d) 
    
    student_goals = []
    all_goals = Goal.query.all() 
    for d in student_dsts:
        for g in all_goals:
            if g in d.children:
               student_goals.append(g) 
          

    statuss = Status.query.all()
    whos = Accupation.query.all()
    
    statuss = Status.query.all()
    whos = Accupation.query.all()

    todos_not_of_student = get_std_todos_not_of_student()
    due_date = date.today()
    
    import pdb; pdb.set_trace()
    print( "std: ", std)
    print( "std: ", std)

    print( "student_stds: ", student_stds)
    print( "student_todos: ", student_todos)
    print( "todos_not_of_student: ", todos_not_of_student)
          

    return render_template('./stds/edit_std_dsts.html', std=std,  
                                                        student_dsts=student_dsts,
                                                        student_goals=student_goals,
                                                        statuss=statuss, whos=whos, due_date=due_date)
                                                
														  		
@std.route('/edit_student_stds2/<int:selected_student_id>/<int:selected_destination_id>', methods=['GET', 'POST'])
@login_required
def edit_student_stds2(selected_student_id, selected_destination_id):

    std = student_select2(selected_student_id)
    std = destination_select2(selected_destination_id)
    ##print("In edit_student_stds2 std std :", std, std.id)

    return edit_student_stds()
