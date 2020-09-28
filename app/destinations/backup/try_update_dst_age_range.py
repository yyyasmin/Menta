	
@dst.route('/update_dst_age_range', methods=['GET', 'POST'])
def update_dst_age_range():
                          	    
    if request.form['submit'] == 'submit_age_range':
        selected_age_range = request.form['selected_age_range']      #Current Age_range selection
            
    if request.method == 'GET':
        return render_template('edit_ar_for_one_dst.html', age_ranges=age_ranges, 
                                                           tags=tags, 
                                                           selected_age_range = selected_age_range, 
                                                           selected_tag = selected_tag)

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        
    selected_ar = Age_range.query.filter(Age_range.title == selected_age_range).first()   
    selected_ar = age_range_select2(selected_ar.id)    
        
    dst.age_range_id = selected_ar.id
    selected_ar.append(dst)
    db.session.commit()  

	return redirect(url_for('destinations.edit_destinations')) 
