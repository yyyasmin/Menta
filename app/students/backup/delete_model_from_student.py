		
@std.route('/todo_from_student_delete', methods=['GET', 'POST'])
@login_required
def std_todo_delete():

    std_todo = Std_todo.query.filter(Std_todo.selected==True).first()
    if std_todo == None:
        flash("Please select a todo first ")
        return redirect(url_for('students.edit_student_todos'))

    db.session.delete(std_todo)
    db.session.commit()

    return  redirect(url_for('students.edit_student_todos'))  #no change in students staff todos
        
@std.route('/std_todo_delete2/delete/<int:selected_std_id>/<int:selected_todo_id>', methods=['GET', 'POST'])
@login_required
def std_todo_delete2(selected_std_id, selected_todo_id):

    std_todo = std_todo_select2(selected_std_id, selected_todo_id)
    return  redirect(url_for('students.std_todo_delete'))  
     