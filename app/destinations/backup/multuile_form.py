@dst.route('/destination_add', methods=['GET', 'POST'])
def destination_add():

    age_ranges = Age_range.query.all()
    tags = Tag.query.all()   
    
    if request.method == 'GET':
        age_ranges = Age_range.query.all()
        tags = Tag.query.all()
        return render_template('try_mf.html', age_ranges=age_ranges, tags=tags, 
                                              selected_age_range = "Defaul selected age range", 
                                              selected_tag = "Defaul selected age tag")
           
        age_range=""
        tag = ""

    if request.form['submit'] == 'submit_age_range':
        selected_age_range = request.form['selected_age_range']
        age_range = Age_range.query.filter(Age_range.title == age_range_title)
                
    if request.form['submit'] == 'submit_tag':
        selected_tag = request.form['selected_tag']
        tag = Tag.query.filter(Tag.title == tag_title)
        
    '''
    #import pdb; pdb.set_trace() 	
    author_id = current_user._get_current_object().id

    destination = Destination(title, body, age_range.id, author_id)	
    destination.tags.append(tag)

    import pdb; pdb.set_trace()
    dummy_std = get_dummy_student()
    dummy_std.destinations.append(destination)

    db.session.add(destination)    
    db.session.commit()  
    db.session.refresh(destination)

    url = url_for('destinations.edit_destinations')
    return redirect(url)   
    '''
    return render_template('try_mf.html', age_ranges=age_ranges, tags=tags, 
                                          selected_age_range = selected_age_range, selected_tag = selected_tag)


@