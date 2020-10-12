

##############START goal's tests###############	

@goal.route('/edit_goal_tests', tests=['GET', 'POST'])
def edit_goal_tests():

    #####import pdb; pdb.set_trace()
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=3))	

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))	

    std = get_dummy_student()
    print("In edit_goal_tests dummy_std   goal id : ", std.id, goal.id )
    return render_template('edit_goal_tests.html', dst=dst, goal=goal)                                             
                                                                
														  		
@goal.route('/edit_goal_tests2/<int:selected_goal_id>', tests=['GET', 'POST'])
def edit_goal_tests2(selected_goal_id):
    print("In edit_goal_tests2 Request is :", request)
    goal = goal_select2(selected_goal_id)
    return redirect(url_for('goals.edit_goal_tests'))		


################## START  Update test ################    
@goal.route('/goal_test_update', tests=['GET', 'POST'])
def goal_test_update():

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))	
             
    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))	
        
    test = Test.query.filter(Test.selected==True).first()
    if test == None:
        flash("Please select a test first ")
        return redirect(url_for('goals.edit_goal_tests'))		
 
    print ("In  goal_test_update goal: ", dst, goal, test )

    #DEBUG ONLY

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations_goals'))	
    #DEBUG ONLY
   
    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))	
    #DEBUG ONLY
         
    
    form = Test_form()

    form.title = test.title
    form.body =  test.body
    
    form.who.choices=[]
    form.test_type.choices=[]
    
    form.who.choices = [(acc.id, acc.title) for acc in Accupation.query.all()]
    for who in Accupation.query.all():
        if test.is_parent_of(who):
            form.who.default = who.id
            break
    
    form.test_type.choices = [(mt.id, mt.title) for mt in Test_type.query.all()]
    for mt in Test_type.query.all():
        if test.is_parent_of(mt):
            form.test_type.default = mt.id
            break
                    
    ### GET Case
    if request.test == 'GET': 
        return render_template('update_test.html', form=form, dst=dst, goal=goal)  
        
    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_test_form.html', form=form)
        
    ##################  Fill test fields 
    #########################import pdb;;pdb.set_trace()

    test.title = request.form['title'] 
    test.body =  request.form['body']
    
    who = Accupation.query.filter(Accupation.id==request.form.get('who')).first()
    test_type = Test_type.query.filter(Test_type.id==request.form.get('test_type')).first()
    
    test.set_parent(who)
    test.set_parent(test_type)
    goal.set_parent(who)
    goal.set_parent(test)
    
    who=set_gt_category(test.id, 'Accupation', who.title, "יש לבחור תפקיד אחראי")  

    ##################  Fill test fields   
                
    db.session.commit()  
    db.session.refresh(test)
    
    return redirect(url_for('goals.edit_goal_tests', dst=dst, goal=goal ))   
                                                        
################## START  Update test ################    


@goal.route('/goal_test_update2/<int:selected_test_id>', tests=['GET', 'POST'])
def goal_test_update2(selected_test_id):

    print("In UUUUUUUUUU 222222222222 goal_test_update2 selected_test_id ", selected_test_id)
    
    test = test_select2(selected_test_id)
    return redirect(url_for('goals.goal_test_update'))			


################## START  Add test ################      
@goal.route('/test_to_goal_add', tests=['GET', 'POST'])
def test_to_goal_add():
    print ("In test_to_goal_add  ")
    
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=3))		

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))		

    form = Todo_form()
    
    form.test_type.choices=[]

    form.due_date = datetime.today()
    form.process()

    first_sts = Status.query.first()

    ### GET Case
    if request.test == 'GET':
        return render_template('test_to_goal_add.html', dst=dst, goal=goal, form=form)
   

    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('test_to_goal_add.html', form=form)
        
        
    print ("POST -- In test_to_goal_add -- POST   ")
                       
    author_id = current_user._get_current_object().id  

    test = Test(request.form['title'], request.form['body'], author_id)        
    db.session.add(test)
        
    print("test.children ", goal.children )
    
    ### asign TO  HUMPTY DUMPTY THE NEW TODO
    hd = get_dummy_student()
    std_gt = attach_gt_to_std(hd.id, test.id) 
   
    default_sts = Status.query.filter(Status.default==True).first()    
    test.set_parent(default_sts)    
    std_gt.status_id = default_sts.id
                               
    goal.set_parent(test)
    
            
    db.session.commit()  
    db.session.refresh(test)
    
    ##########import pdb;; pdb.set_trace()


    return redirect(url_for('goals.edit_goal_tests'))		

                                                    
################## START  Add test ################    


@goal.route('/test_to_goal_add2/<int:selected_general_txt_id>', tests=['GET', 'POST'])
def test_to_goal_add2(selected_general_txt_id):
	print(selected_general_txt_id)
	goal = goal_select2(selected_general_txt_id)
	return redirect(url_for('goals.test_to_goal_add'))			

	
@goal.route('/test_from_goal_delete', tests=['GET', 'POST'])
def test_from_goal_delete():
	
    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('select.goal_select'))		

    test = Test.query.filter(Test.selected==True).first()
    if test == None:
        flash("Please select a test to delete first ")
        return redirect(url_for('goals.edit_goal_tests'))
            
    print ("delete selected test is " + test.title + " from slected goal " + goal.title )

    goal.children.remove(test)
    db.session.commit()  

    return redirect(url_for('goals.edit_goal_tests')) 
 
 
@goal.route('/test_from_goal_delete2/<int:selected_goal_id>/<int:selected_test_id>', tests=['GET', 'POST'])
def test_from_goal_delete2(selected_goal_id, selected_test_id):

    print("totdo id: ", selected_test_id)
    test = test_select2(selected_test_id)
      
    goal = goal_select2(selected_goal_id)
              
    return redirect(url_for('goals.test_from_goal_delete')) 	

##############goal's tests ###############	

