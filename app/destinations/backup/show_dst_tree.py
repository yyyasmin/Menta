{% block show_dst_tree %}
            
@std.route('/show_dst_tree', methods=['GET', 'POST'])
@login_required
def show_dst_tree():

    print("")
    print("IN show_dst_tree")
    
    ###########import pdb; #pdb.set_trace()
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_destinations'))

    print("")
    print("")
    print("Showing tree of dst : ", dst, dst.id)     


    dst_goals = []    # Get all dst's goals
    for g in dst.children:
        if g.type=='goal':
            print("")
            print("appending goal: ", g, g.id)
            dst_goals.append(g)

    dst_todos = []    # Get all goal's todos
    for g in dst_goals:
        for t in g.children:
            if t.type=='todo':               
                print("")
                print("appending todo: ", t, t.id)
                dst_todos.append(t)



	'''
	all_goals = Goal.query.filter(Goal.hide==False).all()     
    for g in std_gts:
        if g in all_goals:
            student_goals.append(g)
    #goals_not_of_student = list(set(all_goals).difference(set(student_goals)))  #goals_not_of_student = all_destinations - std_destinations
    '''
     

    '''
    student_todos = []    # Get all student's destinations
    all_todos = Todo.query.filter(Todo.hide==False).all()    
    for g in std_gts:
        if g in all_todos:
            student_todos.append(g)
    #todos_not_of_student = list(set(all_todos).difference(set(student_todos)))  #todos_not_of_student = all_destinations - std_destinations
    '''

    #DEBUG ONLY
    print("D", dst.title, dst.id)
    for g in dst_goals: 
        if d.is_parent_of(g):
            print("   G", g.title, g.id)
        for t in dst_todos:
            if g.is_parent_of(t):
                print("         G  T", g.id,  t.id)
    #DEBUG ONLY
    
        
    whos = Accupation.query.all()
    default_who = Accupation.query.filter(Status.default==True).first()

    statuss = Status.query.all()
    default_status = Status.query.filter(Status.default==True).first()
        
    whos = Accupation.query.all()
    default_who = Accupation.query.filter(Accupation.default==True).first()

    tags = Tag.query.all()
    
    std_txts = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).all()
     
    due_date = date.today()
        
    age_ranges = Age_range.query.order_by(Age_range.title).all()
    tags = Tag.query.order_by(Tag.title).all()

    print("")
    print("END OF   show_dst_tree  --- CAlling show_dsts_tree ")
    
    #return render_template('./tree/backup/tree_base.html', std=std, student=std,     
    return render_template('./tree/backup/root_tree_family7.html', std=std, student=std,     
    #return render_template('./tree/show_dsts_tree.js', std=std, student=std,  
                                                        dest=dest,
                                                        dst_goals=dst_goals,
                                                        dst_todos=dst_todos,
                                                        total_gts = 1+len(dst_goals)+len(dst_todos),
                                                        std_txts=std_txts,
                                                        whos=whos
                                                        )			
               
    
    
@std.route('/show_dst_tree2/<int:selected_dst_id>', methods=['GET', 'POST'])
@login_required
def show_dst_tree2(selected_dst_id):
    std = student_select2(selected_dst_id)
    return redirect(url_for('students.show_dst_tree'))

{% endblock show_dst_tree %}
