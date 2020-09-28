
@slct.route('/tag_select', methods=['GET', 'POST'])
def tag_select():
	print("in pppppppppppppppptag_ssssssssssssssssssselect")

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
		
	#import pdb; pdb.set_trace()

	tages = Profile.query.join(Profile.profiles).filter(Profile.id==profile.id)


	if (tages.count() == 0):
		flash("There is no tages for this student.")
		print ("tages count is 0 ")
		redirect(url_for('flash_err'))
		return render_template('select_pro.html', tages=tages)
		#return redirect(url_for('index'))

	tag = Tag.query.all()		
	for tag in tages:
		tag.selected = False

	if request.method == 'GET':
		return render_template('select_pro.html', tages=tages)
		
	selected_tag_id = int(request.form['selected_pro'])
	tag =Tag.query.get_or_404(selected_tag_id)
	tag.selected = True
		
	db.session.commit()
	#profiles = Profile.query.all()
	print("In tag_select BeFFFFFFFFFFFFFFFore tages edit_tages")
	return redirect(url_for('tages.edit_tages'))		



@slct.route('/tag_select2/<int:selected_tag_id>', methods=['GET', 'POST'])
def tag_select2(selected_tag_id):

	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('index'))

	profile = Profile.query.filter(Profile.selected==True).first()    
	if profile == None:
		flash("Please select an profile first ")
		return redirect(url_for('profile_select'))		
	#print request

	#import pdb; pdb.set_trace()
	tages = Profile.query.join(Profile.tags).filter(Profile.id==profile.id)

	if (tages.count() == 0):
		flash("There is no tages for this student.")
		print ("tages count is 0 ")
		redirect(url_for('flash_err'))
		return render_template('select_pro.html', tages=tages)
		
	profile = Profile.query.filter(Profile.selected==True).first()
	print("In 44444444444444 Begining of tag_select2 profile selected  is:")
	print(profile.id)

	tag = Tag.query.all()		
	for tag in tages:
		tag.selected = False
		
	print(profile.id)
	profile_select2(profile.id)    # fixing bug- selected profile was effected by tag select setting
		
	profile = Profile.query.filter(Profile.selected==True).first()
	print(profile.title)

	tag = Tag.query.get_or_404(selected_tag_id)

	tag.selected = True
	db.session.commit()

	return redirect(url_for('tages.edit_tages'))		
	

