
################## START  Update todo ################    
@todo.route('/goal_todo_update', methods=['GET', 'POST'])
def goal_todo_update():
    print ("In dsply_todo_form  ")
    
    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))		

    todo = Todo.query.filter(Todo.selected==True).first()
    if todo == None:
        flash("Please select a goal first ")
        return redirect(url_for('goals.edit_goal_todos'))		


    form = Todo_form()

    form.who.choices=[]
    form.status.choices=[]
    
    form.who.choices = [(acc.id, acc.title) for acc in Accupation.query.all()]
    form.who.default = todo.who_id
    
    form.status.choices = [(sts.id, sts.title) for sts in Status.query.all()]
    form.status.default = todo.status_id
    
    form.due_date = todo.due_date
    
    sts_color = todo.status.color
    
    if request.method == 'POST': 
        ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
        print ("form.validate_on_submit", form.validate_on_submit)

        if not form.validate_on_submit:
            flash("יש לבחור קטגוריה")
            return render_template('dsply_todo_form.html', form=form)

        acc = Accupation.query.filter_by(id=form.who.data).first()
        status = Status.query.filter_by(id=form.status.data).first()
        due_date = form.due_date.data
 
        #import pdb; pdb.set_trace()
        new_todo_title = form.title.data
        new_todo_body =  form.body.data
        
        print("ar Tag scrt: ", ar.title, tag.title, scrt.title, new_todo_title)
        ### FROM https://stackovenew_todo_titlerflow.com/questions/44242802/python-flask-validate-selectfield

        author_id = current_user._get_current_object().id
       
        todo.who_id = acc.id
        todo.who_title = acc.title
        todo.status_id = status.id
        todo.due_date = due_date
        
        db.session.add(todo)    	
        goal.todos.append(todo)
        acc.todos.append(todo)
        
        db.session.commit()  
        db.session.refresh(todo)
        url = url_for('goals.edit_goal_todos' )
        return redirect(url)   
   
    return render_template('dsply_todo_form.html', form=form, from_todo_sort_order=from_todo_sort_order)
                                                    
################## START  Update todo ################    
