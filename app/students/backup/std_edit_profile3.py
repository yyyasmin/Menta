	
##############START studets stds###############	
	
@std.route('/edit_std_profile', methods=['GET', 'POST'])
@login_required
def edit_std_profile():
    
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
      
    print("")
    print("IN edit_profile2_by_tag")
    print("")
    
    profile = reset_and_get_profile(0)
         
    tags = Tag.query.order_by(Tag.title).all()
    default_tag = Tag.query.filter(Tag.selected==True).first()
    if default_tag == None:
        default_tag = Tag.query.filter(Tag.default==True).first()
         
    prf_subjects=[]
    all_subjects = Subject.query.all()
    for s in all_subjects:
        if profile.is_parent_of(s):
            prf_subjects.append(s)
        
    prf_weaknesses=[]
    all_weaknesses = Weakness.query.all()
    for s in all_weaknesses:
        if profile.is_parent_of(s):
            prf_weaknesses.append(s)
        
    prf_strengths=[]
    all_strengths = Strength.query.all()
    for s in all_strengths:
        if profile.is_parent_of(s):
            prf_strengths.append(s)
        
        
    return render_template('./destinations/profile/backup/edit_profile2.html.html', std=std, student=std,  
                            prf_subjects=prf_subjects, prf_weaknesses=prf_weaknesses, prf_strengths=prf_strengths )															

    tags = Tag.query.order_by(Tag.title).all() 
    default_tag = Tag.query.filter(Tag.selected==True).first()
    if default_tag == None:
        default_tag = Tag.query.filter(Tag.default==True).first()
     
    print("")
    print("")
