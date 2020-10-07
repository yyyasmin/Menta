
@std.route('/std_edit_profile/<int:dsply_direction>', methods=['GET', 'POST'])
@login_required
def std_edit_profile(dsply_direction):

    print("")
    print("")
    print("IN get_profile_data")
    
    
    print("")
    
    #DEBUG - ARESE!

    #DEBUG - ARESE!
    
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
        
    profile = reset_and_get_profile(std.id)
    
    
    tags = Tag.query.order_by(Tag.title).all()
    default_tag = Tag.query.filter(Tag.selected==True).first()
    if default_tag == None:
        for t in tags:
            if t.default==True:
                default_tag = t
    if default_tag == None:
        default_tag = Tag.query.filter(Tag.title=='כללי').first()
        if default_tag == None:
            default_tag = Tag('כללי', 'general', get_author_id())
            db.session.add(default_tag)
            db.session.commit()
    
    print("")
    print("")
    print("DEFAULT TAG: ", default_tag.id, default_tag.body)
    print("")
    
    sub_tags = Sub_tag.query.all()
    std_sub_tags = []
    for st in sub_tags:
        if default_tag.is_parent_of(st):
            std_sub_tags.append(st)
            

    default_sub_tag = Sub_tag.query.filter(Sub_tag.selected==True).first()
    if default_sub_tag == None:
        for st in std_sub_tags:
            print("SUB-TAG: ", st.id, st.body)
            if st.default==True:
                default_sub_tag = st
                break
    if default_sub_tag == None:
        default_sub_tag = Sub_tag.query.filter(Sub_tag.title == 'כללי').first()
        if default_sub_tag == None:
            default_sub_tag = Sub_tag('כללי', 'general', get_author_id())
            db.session.add(default_sub_tag)
            db.session.commit()
                
    all_tag = Tag.query.filter(Tag.body=='all').first()
    all_sub_tag = Sub_tag.query.filter(Sub_tag.body=='all').first()
    all_sub_tags = all_sub_tag
    
    
    
    print("")
    print("")
    print("IN END OF std_edit_profile DEFAULT-TAG: {0}  DEFAULT-SUB-TAG: {1}".format(
                                        default_tag.id, default_sub_tag==None))
    print("")
    
    
    form = Gt_form()
    
    form.tag.choices = [(tag.id, tag.title) for tag in tags]
    form.tag.default = default_tag.id
    form.process()
    
    form.sub_tag.choices = [(sub_tag.id, sub_tag.title) for sub_tag in std_sub_tags]
    form.sub_tag.default = default_sub_tag.id
    form.process()
    
    prf_subjects=[]
    subjects_not_of_prf=[]
    all_subjects = Subject.query.all()
    for s in all_subjects:
        if profile.is_parent_of(s):
            prf_subjects.append(s)
        else:
            if s.hide == False: 
                subjects_not_of_prf.append(s)
            
    prf_weaknesses=[]
    weaknesses_not_of_prf=[]
    all_weaknesses = Weakness.query.all()
    for s in all_weaknesses:
        if profile.is_parent_of(s):
            prf_weaknesses.append(s)
        else:
            if s.hide == False:
                weaknesses_not_of_prf.append(s)
            
    prf_strengths=[]
    strengths_not_of_prf=[]
    all_strengths = Strength.query.all()
    for s in all_strengths:
        if profile.is_parent_of(s):
            prf_strengths.append(s)
        else:
            if s.hide == False:
                strengths_not_of_prf.append(s)
            
            
    user = User.query.get_or_404(current_user._get_current_object().id)
    author_id = user.id
    
    sbj = Subject.query.filter(Subject.title=='Subject_data').first()
    if sbj==None:
        sbj = Subject('Subject_data', 'Subject_data', author_id)
        #sbj.odd_color = '#e6f2ff'   
        #sbj.even_color = '#cce5ff'
       
    strn = Strength.query.filter(Strength.title=='Subject_data').first()
    if strn==None:
        strn = Strength('Strength_data', 'Strength_data', author_id)
  
    weak = Weakness.query.filter(Weakness.title=='Subject_data').first()
    if weak==None:
        weak = Weakness('Weakness', 'Weakness', author_id)
   
    gray = Gray.query.filter(Gray.title=='gray data').first()
    if gray==None:
        gray = Gray('Gray', 'Gray', author_id)


    
    print("")
    print("")
    print("std_edit_profile")
    print("SBJ ODD: ", sbj.odd_color)
    print("SBJ EVEN: ", sbj.even_color)
    print("")
    print("STRN ODD: ", strn.odd_color)
    print("STRN EVEN: ", strn.even_color)
    print("")
    print("WEAK ODD: ", weak.odd_color)
    print("WEAK EVEN: ", weak.even_color)
    print("")
    print("")
  
    print("IN END OF std_edit_profile Calling std_edit_profile.html")
    print("")
    print("")
    
    if dsply_direction == 1:
        return render_template('./profile/horizontal_dsply/std_edit_profile.html', 
                                std=std,
                                profile=profile, 
                                sbj=sbj, strn=strn, weak=weak, gray=gray,
                                tags=tags, default_tag=default_tag, all_tag=all_tag,
                                sub_tags=sub_tags, default_sub_tag=default_sub_tag, all_sub_tags=all_sub_tags, all_sub_tag=all_sub_tag,
                                prf_subjects=prf_subjects, subjects_not_of_prf=subjects_not_of_prf,
                                prf_weaknesses=prf_weaknesses, weaknesses_not_of_prf=weaknesses_not_of_prf,
                                prf_strengths=prf_strengths, strengths_not_of_prf=strengths_not_of_prf )

    else:
        return render_template('./profile/vertical_dsply/profile_verical_dsply.html', 
                                std=std, form=form, 
                                profile=profile, 
                                sbj=sbj, strn=strn, weak=weak, gray=gray,
                                tags=tags, default_tag=default_tag, all_tag=all_tag,
                                sub_tags=sub_tags, default_sub_tag=default_sub_tag, all_sub_tags=all_sub_tags, all_sub_tag=all_sub_tag,
                                prf_subjects=prf_subjects, subjects_not_of_prf=subjects_not_of_prf,
                                prf_weaknesses=prf_weaknesses, weaknesses_not_of_prf=weaknesses_not_of_prf,
                                prf_strengths=prf_strengths, strengths_not_of_prf=strengths_not_of_prf )

			