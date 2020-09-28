		
@app.route('/subjects/add', methods=['GET', 'POST'])
def subjects_add():
    print("IIIIIn CCCCCCCCCCCCons AAAAAAAAAAAAAAAAAd")
    user = User.query.get_or_404(g.user.id)
    author_id = user.id
	
    
    student = Student.query.filter(Student.selected==True).first()
    if student == None:
        flash("PPPPPPPPPPPPPPPPPPPPPPlease select a student first ")
        return redirect(url_for('index'))
        
    profile = Profile.query.filter(Profile.selected==True).first()
    
    if profile == None:
        flash("PPPPPPPPPPPPlease select an pppppppppppppppppppppppppppppp first ")
        return redirect(url_for('profile_select'))
    print(profile.title)      
    
    if request.method == 'GET':
        return render_template('add_subjects.html', profile=profile)
           
    #get data from form and insert to studentgress db
	
    body = request.form.get('description')
	
    subject = Interest_subject(title, body)	
    profile.subjects.append(subject)	
	   
    db.session.add(subject)    
    db.session.commit()  
    db.session.refresh(subject)
    url = url_for('subjects_by_profile')
    return redirect(url)   
	