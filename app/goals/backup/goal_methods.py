

##############START goal's methods###############	

@goal.route('/edit_goal_methods', methods=['GET', 'POST'])
def edit_goal_methods():

    ###import pdb; pdb.set_trace()
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=3))	

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destination_goals'))	

    std = get_dummy_student()
    print("In edit_goal_methods dummy_std   goal id : ", std.id, goal.id )
    return render_template('edit_goal_methods.html', dst=dst, goal=goal)                                             
                                                                
														  		
@goal.route('/edit_goal_methods2/<int:selected_goal_id>', methods=['GET', 'POST'])
def edit_goal_methods2(selected_goal_id):
    print("In edit_goal_methods2 Request is :", request)
    goal = goal_select2(selected_goal_id)
    return redirect(url_for('goals.edit_goal_methods'))		


################## START  Update method ################    
@goal.route('/goal_method_update', methods=['GET', 'POST'])
def goal_method_update():

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))	
             
    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))	
        
    method = Method.query.filter(Method.selected==True).first()
    if method == None:
        flash("Please select a method first ")
        return redirect(url_for('goals.edit_goal_methods'))		
 
    print ("In  goal_method_update goal: ", dst, goal, method )

    #DEBUG ONLY

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))	
    #DEBUG ONLY
         
    
    form = Method_form()

    form.title = method.title
    form.body =  method.body
    
    form.who.choices=[]
    form.status.choices=[]
    
    form.who.choices = [(acc.id, acc.title) for acc in Accupation.query.all()]
    for who in Accupation.query.all():
        if method.is_parent_of(who):
            form.who.default = who.id
            break
    
    form.status.choices = [(sts.id, sts.title) for sts in Status.query.all()]
    for sts in Status.query.all():
        if sts.is_parent_of(sts):
            form.who.default = sts.id
            break
                     
    ### GET Case
    if request.method == 'GET': 
        return render_template('update_method.html', form=form, dst=dst)  
        
    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_method_form.html', form=form)
        
    ##################  Fill method fields 
    #######################import pdb;;pdb.set_trace()

    method.title = request.form['title'] 
    method.body =  request.form['body']
    
    who = Accupation.query.filter(Accupation.id==request.form.get('who')).first()
    method.set_parent(who)
    goal.set_parent(who)
    goal.set_parent(method)
    
    who=set_gt_category(method.id, 'Accupation', who.title, "יש לבחור תפקיד אחראי")  

    ##################  Fill method fields   
                
    db.session.commit()  
    db.session.refresh(method)
    
    return redirect(url_for('goals.edit_goal_methods', dst=dst ))   
                                                        
################## START  Update method ################    


@goal.route('/goal_method_update2/<int:selected_method_id>', methods=['GET', 'POST'])
def goal_method_update2(selected_method_id):

    print("In UUUUUUUUUU 222222222222 goal_method_update2 selected_method_id ", selected_method_id)
    
    method = method_select2(selected_method_id)
    return redirect(url_for('goals.goal_method_update'))			


################## START  Add method ################      
@goal.route('/method_to_goal_add', methods=['GET', 'POST'])
def method_to_goal_add():
    print ("In method_to_goal_add  ")
    
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=3))		

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))		

    form = Method_form()

    form.who.choices=[]
    form.status.choices=[]

    form.who.choices = [(acc.id, acc.title) for acc in Accupation.query.all()]
    form.process()

    form.status.choices = [(sts.id, sts.title) for sts in Status.query.all()]
    form.process()

    form.due_date = datetime.today()
    form.process()

    first_sts = Status.query.first()

    ### GET Case
    if request.method == 'GET':
        return render_template('method_to_goal_add.html', dst=dst, goal=goal, form=form)
   

    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('method_to_goal_add.html', form=form)
        
    ########################import pdb;;pdb.set_trace()
                   
    author_id = current_user._get_current_object().id  

    method = Method(request.form['title'], request.form['body'], author_id)        
    db.session.add(method)
        
    print("method.children ", goal.children )
    
    ### asign TO  HUMPTY DUMPTY THE NEW TODO
    hd = get_dummy_student()
    std_gt = attach_gt_to_std(hd.id, method.id) 
   
    default_sts = Status.query.filter(Status.default==True).first()    
    method.set_parent(default_sts)    
    std_gt.status_id = default_sts.id
    
    who = Accupation.query.filter(Accupation.id==request.form.get('who')).first()    
    #who=set_gt_category(method.id, 'Accupation', who.title, "יש לבחור תפקיד אחראי")  
                       
    goal.set_parent(method)
    goal.set_parent(who)
    method.set_parent(who)
            
    db.session.commit()  
    db.session.refresh(method)
    
    ########import pdb;; pdb.set_trace()


    return redirect(url_for('goals.edit_goal_methods'))		

                                                    
################## START  Add method ################    


@goal.route('/method_to_goal_add2/<int:selected_general_txt_id>', methods=['GET', 'POST'])
def method_to_goal_add2(selected_general_txt_id):
	print(selected_general_txt_id)
	goal = goal_select2(selected_general_txt_id)
	return redirect(url_for('goals.method_to_goal_add'))			

	
@goal.route('/method_from_goal_delete', methods=['GET', 'POST'])
def method_from_goal_delete():
	
    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('select.goal_select'))		

    method = Method.query.filter(Method.selected==True).first()
    if method == None:
        flash("Please select a method to delete first ")
        return redirect(url_for('goals.edit_goal_methods'))
            
    print ("delete selected method is " + method.title + " from slected goal " + goal.title )

    goal.children.remove(method)
    db.session.commit()  

    return redirect(url_for('goals.edit_goal_methods')) 
 
 
@goal.route('/method_from_goal_delete2/<int:selected_goal_id>/<int:selected_method_id>', methods=['GET', 'POST'])
def method_from_goal_delete2(selected_goal_id, selected_method_id):

    print("totdo id: ", selected_method_id)
    method = method_select2(selected_method_id)
      
    goal = goal_select2(selected_goal_id)
              
    return redirect(url_for('goals.method_from_goal_delete')) 	

##############goal's methods ###############	

