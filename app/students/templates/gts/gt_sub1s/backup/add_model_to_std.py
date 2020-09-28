	
##############START TRY studets todos###############	

@std.route('/try_todo_to_student_add', methods=['GET'])
@login_required
def try_todo_to_student_add():
    ########impor pdb;pdb.set_trace()
    #print("IN todo_to_student_add")
    ###########################impor pdb;pdb.set_trace()
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('destination.edit_students'))

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_student_destinations'))		

    #print("IN try_todo_to_student_add Request methi", request.method)
    ########impor pdb;pdb.set_trace()
    #### GET case
            
    todos_not_of_student = try_get_todos_not_of_student()
    if len(todos_not_of_student) < 1:
        flash("כל המשימות של יעדזה כבר משוייכות לתלמיד. אפשר ליצור משימה חדשה דרך יצירת מטרות-יעדים-משימות.")
        ########impor pdb;pdb.set_trace()
        redirect(url_for('destinations.edit_destinations_todos'))

    statuss = Status.query.all()
    due_date = date.today()
    return render_template('./todos/backup/edit_todos_not_of_std.html', std=std, dst=dst, 
                                                                todos_not_of_student=todos_not_of_student,
                                                                statuss=statuss, due_date=due_date)
	
##############START match_todo_to_std ###############	

@std.route('/match_todo_to_std', methods=['POST'])
@login_required
def match_todo_to_std():
    ########impor pdb;pdb.set_trace()
    #print("IN todo_to_student_add")
    ###########################impor pdb;pdb.set_trace()
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('destination.edit_students'))

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_student_destinations'))		
   
    todo = Todo.query.filter(Todo.selected==True).first()
    if todo == None:
        flash("Please select a todo first ")
        return redirect(url_for('students.edit_student_todos'))

    #DEBUG
    #DEBUG
    #########impor pdb;pdb.set_trace()
    statuss = Status.query.all()

    std_todo = Std_todo.query.filter(Std_todo.student_id == std.id).filter(Std_todo.todo_id==todo.id).first()

    if std_todo == None:   #new Std_todo
        std_todo = Std_todo(std.id, todo.id)        

    std_todo.todo_title = todo.title
    std_todo.todo_body = todo.body
    
    std_todo.todo = todo
    std_todo.student = std    
    std_todo.dst_id = dst.id
    
    sts_title = request.form.get('selected_status')
    sts = Status.query.filter(Status.title==sts_title).first() 
    #print("selected sts is", sts)   
    std_todo.status_id = sts.id
    std_todo.status_title = sts.title
    std_todo.status_color = sts.color
    
    std_todo.due_date = request.form.get('due_date') 
   
    std.todos.append(std_todo)			
    todo.students.append(std_todo)
        
    #print ("In match_todo_to_std NEW: student date  sts:",  std_todo.todo, std_todo.student, std_todo.due_date, std_todo.status_title)
    #DEBUG
    std_todo = Std_todo.query.filter(Std_todo.todo_id == todo.id).filter(Std_todo.student_id==std.id).first() 	
    #print("New todo is  for std is : Std_todo student is  ", std_todo, std)
    todo.selected = False
    #DEBUG
    db.session.commit() 
    db.session.refresh(std)
    db.session.refresh(todo)
    db.session.refresh(std_todo)

    ##print("todo_to_student_add METHOD", request.method)
    return  redirect(url_for('students.edit_student_todos')) 
        
		
	
@std.route('/match_todo_to_std2/<int:selected_todo_id>', methods=['GET', 'POST'])
@login_required
def match_todo_to_std2(selected_todo_id):

    #print("IN match_todo_to_std2   todo ", selected_todo_id)
    #####impor pdb;pdb.set_trace()
    
    todo = todo_select2(selected_todo_id)
    
    return match_todo_to_std()
    
##############END match_todo_to_std ###############	


                                            
@std.route('/try_get_student_todos', methods=['GET', 'POST'])
@login_required
def try_get_student_todos():
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
        
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_student_destinations'))		
        

    student_todos = Todo.query.join(Std_todo).filter(Std_todo.dst_id==dst.id).filter(Std_todo.student_id==std.id).all()

    return student_todos


@std.route('/try_get_todos_not_of_student', methods=['GET', 'POST'])
@login_required
def try_get_todos_not_of_student():
    student = Student.query.filter(Student.selected==True).first()
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
        
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_student_destinations'))		

    #DEBUG
    ###########################impor pdb;pdb.set_trace()	
    all_dst_todos = Todo.query.join(Destination).filter(Todo.dst_id == dst.id)

    student_todos = Todo.query.join(Std_todo).filter(Std_todo.student_id==student.id).filter(Std_todo.todo_id==Todo.id).all()

    todos_with_no_students = Todo.query.filter(~Todo.students.any()).all()

    todos_not_of_student = list(set(all_dst_todos).difference(set(student_todos)))  #todos_not_of_student = all_dst_todos-student_todos

    todos_not_of_student.extend(todos_with_no_students)

    return todos_not_of_student


	