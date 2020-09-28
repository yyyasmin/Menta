

@strn.route('/weaknesses_by_profile', methods=['POST', 'GET'])
@login_required
def weaknesses_by_profile():
	
    student = Student.query.filter(Student.selected==True).first()
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('index'))
	
    profile = Profile.query.filter(Profile.selected==True).first()
    print("in weaknesses_by_profile profile selected is")
    print(profile.title)
    if profile == None:
        flash("Please select an profile first ")
        return redirect(url_for('profile_select'))
	
    #import pdb; pdb.set_trace()
    weaknesses = Strength.query.join(Profile.weaknesses).filter(Profile.id==profile.id)
    return render_template('show_profile_weaknesses2.html',
                            student=student,
                            profile=profile,
                            weaknesses=weaknesses
							)

@strn.route('/weaknesses_by_profile2/<int:selected_profile_id>', methods=['POST', 'GET'])
@login_required
def weaknesses_by_profile2(selected_profile_id):
    print("IIn PRRRRRRRRRRRROs AAAAAAAAAAAAAProfile 22222222222222")
    print(selected_profile_id)
    profile_select2(selected_profile_id)
    return redirect(url_for('weaknesses_by_profile'))		
										

@strn.route('/edit_weaknesses', methods=['GET', 'POST'])
@login_required
def edit_weaknesses():
    student = Student.query.filter(Student.selected==True).first()
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('index'))
	
    profile = Profile.query.filter(Profile.selected==True).first()
    print("in weaknesses_by_profile profile selected is")
    print(profile.title)
    if profile == None:
        flash("Please select an profile first ")
        return redirect(url_for('profile_select'))
	
    #import pdb; pdb.set_trace()
    weaknesses = Strength.query.join(Profile.weaknesses).filter(Profile.id==profile.id)
    return render_template('edit_weaknesses.html',
                            student=student,
                            profile=profile,
                            weaknesses=weaknesses
							)

	
@strn.route('/weakness_add', methods=['GET', 'POST'])
def weakness_add():

	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('index'))
		
	profile = Profile.query.filter(Profile.selected==True).first()

	if profile == None:
		flash("Please select an profile first ")
		return redirect(url_for('profile_select'))
	print(profile.title)      
	#print request

	if request.method == 'GET':
		return render_template('weakness_to_profile_add.html', student=student, profile=profile)
	###############################################################################		

		   
	#get data from form and insert to weaknessgress db
	title = request.form.get('title')
	body = request.form.get('description')

	#import pdb; pdb.set_trace() 	
	author_id = current_user._get_current_object().id
	weakness = Strength(title, body, author_id)

	profile.weaknesses.append(weakness)	

	db.session.add(weakness)    
	db.session.commit()  
	db.session.refresh(weakness)

	url = url_for('weaknesses.edit_weaknesses')
	return redirect(url)   
	
#update selected weakness
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@strn.route('/weakness_update/<int:selected_weakness_id>', methods=['GET', 'POST'])
def weakness_update(selected_weakness_id):

    weakness_select2(selected_weakness_id)
		
    weakness = Strength.query.get_or_404(selected_weakness_id)
    print("In PPPPPPPPPPPPweakness UUUUUUUUUUUUUUUUUUUUUUpdate")
    print(selected_weakness_id, weakness.id, weakness.title)
	
    if request.method == 'GET':
        print("GET render update_weakness.html")
        return render_template('update_weakness.html', weakness=weakness)
		
    #get data from form and insert to weaknessgress db
    #import pdb; pdb.set_trace() 	
    weakness.title = request.form.get('title')	
    weakness.body = request.form.get('description')
    
    db.session.commit()  
    db.session.refresh(weakness)
	
    return redirect(url_for('weaknesses.edit_weaknesses'))
	
		
@strn.route('/weakness_delete_for_good', methods=['GET', 'POST'])
#Here author is user_id
def weakness_delete_for_good():
	  
	user = User.query.get_or_404(current_user.id)
	author_id = user.id

	weakness = Strength.query.filter(Strength.selected==True).first()
	if weakness == None:
		flash("Please select a weakness to delete first ")
		return redirect(url_for('select.weakness_select'))
			
	print ("delete selected weakness is " )
	print(weakness.title)      

	db.session.delete(weakness) 

	db.session.commit()  

	return redirect(url_for('weaknesses.edit_weaknesses')) 
		
#delete from index weaknesses list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@strn.route('/weakness_delete_for_good2/<int:selected_weakness_id>', methods=['GET', 'POST'])
#Here author is user_id
def weakness_delete_for_good2(selected_weakness_id):

	print ("SSSSSSSSSSSSSelected weakness is" )
	weakness_select2(selected_weakness_id)
	return redirect(url_for('weaknesses.weakness_delete_for_good')) 	

'''
@strn.route('/weakness_delete', methods=['GET', 'POST'])
#Here author is user_id
def weakness_delete():
	  
	print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
	print(current_user.id)

	user = User.query.get_or_404(current_user.id)
	author_id = user.id

	weakness = weakness.query.filter(weakness.selected==True).first()
	if weakness == None:
		flash("Please select a weakness to delete first ")
		return redirect(url_for('select.weakness_select'))
			
	print ("delete selected weakness is " )
	print(weakness.id)
	
	weakness.hide = True

	db.session.commit()
	#DEBUG
	weakness = weakness.query.filter(weakness.selected==True).first()
	print("After commit set hide to True", weakness.id, weakness.hide)
	#DEBUG
	return redirect(url_for('weaknesses.edit_weaknesses')) 
		
#delete from index weaknesses list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@strn.route('/weakness_delete2/<int:selected_weakness_id>', methods=['GET', 'POST'])
#Here author is user_id
def weakness_delete2(selected_weakness_id):

	print ("SSSSSSSSSSSSSelected weakness is", selected_weakness_id )
	dest = weakness_select2(selected_weakness_id)
	return redirect(url_for('weaknesses.weakness_delete'))

''' 	


