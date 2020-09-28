
##############goal's todos###############	

@goal.route('/edit_goal_todos', methods=['GET', 'POST'])
def edit_goal_todos():

	goal = Goal.query.filter(Goal.selected==True).first()
	if goal == None:
		flash("Please select a goal first ")
		return redirect(url_for('select.goal_select'))		
	print("In edit_goal_todos student for show tree: " )
	return render_template('edit_goal_todos.html', goal=goal) 
																
														  		
@goal.route('/edit_goal_todos2/<int:selected_goal_id>', methods=['GET', 'POST'])
def edit_goal_todos2(selected_goal_id):
	print("In edit_goal_todos2 Request is :", request)
	dst = goal_select2(selected_goal_id)
	return redirect(url_for('goals.edit_goal_todos'))		

	
@goal.route('/todo_to_goal_add', methods=['GET', 'POST'])
def todo_to_goal_add():
    author_id = current_user._get_current_object().id

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('select.goal_select'))		

    if request.method == 'GET':
        return render_template('todo_to_goal_add.html', goal=goal)
           
    #get data from form and insert to todogress db
    title = request.form.get('title')
    body = request.form.get('description')

    ##import pdb; pdb.set_trace() 	

    todo = Todo(title, body)
    todo.files.append(uploaded_file)

    db.session.add(todo)    	
    goal.todos.append(todo)   
    db.session.commit()  
    db.session.refresh(todo)
    url = url_for('goals.edit_goal_todos' )
    return redirect(url)   

@goal.route('/todo_to_goal_add2/<int:selected_goal_id>', methods=['GET', 'POST'])
def todo_to_goal_add2(selected_goal_id):
	print(selected_goal_id)
	goal = goal_select2(selected_goal_id)
	return redirect(url_for('goals.todo_to_goal_add'))			

	
@goal.route('/todo_from_goal_delete', methods=['GET', 'POST'])
def todo_from_goal_delete():
	
	goal = Goal.query.filter(Goal.selected==True).first()
	if goal == None:
		flash("Please select a goal first ")
		return redirect(url_for('select.goal_select'))		


	todo = Todo.query.filter(Todo.selected==True).first()
	if todo == None:
		flash("Please select a todo to delete first ")
		return redirect(url_for('select.todo_select'))
			
	print ("delete selected todo is " + todo.title + " from slected goal " + goal.title )

	goal.todos.remove(todo)
	db.session.commit()  

	return redirect(url_for('goals.edit_goal_todos')) 

@goal.route('/todo_from_goal_delete2/<int:selected_goal_id><int:selected_todo_id>', methods=['GET', 'POST'])
#Here author is user_id
def todo_from_goal_delete2(selected_goal_id, selected_todo_id):
	goal = goal_select2(selected_goal_id)

	todo = todo_select2(selected_todo_id)
	return redirect(url_for('goals.todo_from_goal_delete')) 	

##############goal's todos###############	

