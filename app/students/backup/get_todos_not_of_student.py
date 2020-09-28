
@std.route('/try_get_goals_not_of_student', methods=['GET', 'POST'])
@login_required
def try_get_goals_not_of_student():
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
    all_dst_goals = Goal.query.join(Destination).filter(Goal.dst_id == dst.id)

    student_goals = Goal.query.join(Std_goal).filter(Std_goal.student_id==student.id).filter(Std_goal.goal_id==Goal.id).all()

    goals_with_no_students = Goal.query.filter(~Goal.students.any()).all()

    goals_not_of_student = list(set(all_dst_goals).difference(set(student_goals)))  #goals_not_of_student = all_dst_goals-student_goals

    goals_not_of_student.extend(goals_with_no_students)

    return goals_not_of_student

