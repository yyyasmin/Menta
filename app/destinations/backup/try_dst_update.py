#update selected destination
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@dst.route('/destination_update/<int:selected_destination_id>', methods=['GET', 'POST'])
def destination_update(selected_destination_id):

    destination_select2(selected_destination_id)
        
    updated_dst = Destination.query.filter(Age_range.id == dst.age_range_id).first()
	if updated_dst == None:
		flash("Please select a destination to delete first ")
		return redirect(url_for('select.edit_destinations'))
			
    print("In PPPPPPPPPPPPDestination UUUUUUUUUUUUUUUUUUUUUUpdate")
    print(selected_destination_id, updated_dst.id, updated_dst.title)

    author_id = current_user._get_current_object().id        
    age_ranges = Age_range.query.all()
    tags = Tag.query.all() 

	selected_age_range = Age_range.query.filter(Age_range.id == updated_dst.age_range_id).first()
	if selected_age_range == None:
		get_default_age_range()
			
	print ("update selected ar is " )
	print(selected_age_range.title)

	selected_tag = Tag.query.filter(Tag in updated_dst.tags).first()
	if selected_tag == None:
		selected_tag = ":בחר נושא"
			
	print ("update selected tag  is " )
	print(selected_tag.title)

    if request.method == 'GET':
        return render_template('update_destination.html', age_ranges=age_ranges, tags=tags, 
                                                          selected_age_range = selected_age_range, 
                                                          selected_tag = selected_tag)
                                              
                                              	    
    if request.form['submit'] == 'submit_age_range':
        selected_age_range = request.form['selected_age_range']      #Current Age_range selection
        
        selected_ar = Age_range.query.filter(Age_range.title == selected_age_range).first()   #Save for next method call
        selected_ar = age_range_select2(selected_ar.id)
        
        #If already selected and saved form prevous methods call
        tmp_tag = Tag.query.filter(Tag.selected == True).first()
        if tmp_tag != None:
            selected_tag = tmp_tag.title   
        else:
            selected_tag = "בחר נושא"
            
        return render_template('add_destination.html', age_ranges=age_ranges, tags=tags, 
                                                       selected_age_range = selected_age_range, selected_tag = selected_tag)
                          
   
    if request.form['submit'] == 'submit_tag':
        selected_tag = request.form['selected_tag']      #Current Tag selection
        
        last_selected_tag = Tag.query.filter(Tag.title == selected_tag).first()   #Save for next method call
        last_selected_tag = tag_select2(last_selected_tag.id)
        
        #If already selected and saved form prevous methos call
        tmp_age_range = Age_range.query.filter(Age_range.selected == True).first()
        if tmp_age_range != None:
            selected_age_range = tmp_age_range.title   
        else:
            selected_age_range = "בחר קבוצת גיל"
                
        return render_template('add_destination.html', age_ranges=age_ranges, tags=tags, 
                                                       selected_age_range = selected_age_range, 
                                                       selected_tag = selected_tag)
                                                                                      
    if request.form['submit'] == 'submit_description': 
        title = request.form['title']      #Current Description  selection
        body = request.form['description']
        public = request.form['public']
        
        last_selected_age_range = Age_range.query.filter(Age_range.selected == True).first()
                
        last_selected_tag = Tag.query.filter(Tag.selected == True).first()
        new_destination.tags.append(last_selected_tag)
        
        last_selected_age_range = Age_range.query.filter(Age_range.selected == True).first()
        updated_dst.age_range_id = last_selected_age_range.id
        updated_dst.public = public
        #import pdb; pdb.set_trace()
        
        db.session.commit()  
        db.session.refresh(new_destination)

        url = url_for('destinations.edit_destinations')
        return redirect(url)   
#end update selected destination


		