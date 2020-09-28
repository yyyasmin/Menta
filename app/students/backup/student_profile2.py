	
@std.route('/student_profile2', methods=['GET', 'POST'])
@login_required
def student_profile2():
    
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
      
    std_gts = General_txt.query.join(Std_general_txt).filter(Std_general_txt.student_id==std.id).filter(Std_general_txt.general_txt_id==General_txt.id).all()
        
    student_profile2 = []    # Get all student's destinations
    all_dsts = Destination.query.filter(Destination.hide==False).all()  
    for d in std_gts:
        if d in all_dsts:
            student_profile2.append(d)            
    dsts_not_of_student = list(set(all_dsts).difference(set(student_profile2)))  #destinations_not_of_student = all_destinations - std_destinations
           
    student_goals = []    # Get all student's destinations
    all_goals = Goal.query.filter(Goal.hide==False).all()
    i=0
    for g in std_gts:
        if g in all_goals:
            student_goals.append(g)
    goals_not_of_student = list(set(all_goals).difference(set(student_goals)))  #goals_not_of_student = all_destinations - std_destinations
                                 
    student_todos = []    # Get all student's destinations
    all_todos = Todo.query.filter(Todo.hide==False).all()    
    for g in std_gts:
        if g in all_todos:
            student_todos.append(g)
    todos_not_of_student = list(set(all_todos).difference(set(student_todos)))  #todos_not_of_student = all_destinations - std_destinations
    
    #DEBUG ONLY
    print("")
    print("")    
    for d in student_profile2:
        print("D", d.title, d.id)
        for g in student_goals: 
            if d.is_parent_of(g):
                print("   G", g.title, g.id)
            for t in student_todos:
                if g.is_parent_of(t):
                    print("       T", t.title, t.id)
    print("")
    print("")  
          
    for d in dsts_not_of_student:
        print("D  NOT_OF_STD ", d.title, d.id)
        for g in goals_not_of_student:
            if d.is_parent_of(g):
                print("   G  NOT_OF_STD", g.title, g.id)
            for t in todos_not_of_student:
                if g.is_parent_of(t):
                    print("       T  NOT_OF_STD", t.title, t.id)
    print("")
    print("")
    #DEBUG ONLY

    print("1111111111111111111111111111111")

    whos = Accupation.query.all()
    default_who = Accupation.query.filter(Status.default==True).first()
    print("2222222222222222222222222222222")

    statuss = Status.query.all()
    default_status = Status.query.filter(Status.default==True).first()
    print("33333333333333333333333333")
        
    tags = Tag.query.order_by(Tag.title).all() 
    default_tag = Tag.query.filter(Tag.selected==True).first()
    if default_tag == None:
        default_tag = Tag.query.filter(Tag.default==True).first()
     
    age_ranges = Age_range.query.order_by(Age_range.from_age).all()     
    default_ar = Age_range.query.filter(Age_range.selected==True).first()
    if default_ar == None:
        default_ar = Tag.query.filter(Age_range.default==True).first()
      
    print("44444444444444444444444444444")

    std_txts = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).all()

    due_date = date.today()
    print("5555555555555555555555555555555555")
     
    print("")
    print("")

    print("")
    print("")
    print("")
    print("")
  
    return render_template('./destinations/table_destinations/edit_all_dsts_6.html', std=std,  
                                                        student_profile2=student_profile2, dsts_not_of_student=dsts_not_of_student,
                                                        all_goals=all_goals, student_goals=student_goals, goals_not_of_student=goals_not_of_student,
                                                        all_todos=all_todos, student_todos=student_todos, todos_not_of_student=todos_not_of_student,
                                                        std_txts=std_txts,
                                                        statuss=statuss, default_status=default_status,
                                                        whos=whos, default_who=default_who,
                                                        tags=tags, default_tag=default_tag,
                                                        age_ranges=age_ranges, default_ar=default_ar)
