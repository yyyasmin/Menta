	
@dst.route('/update_dst_age_range', methods=['GET', 'POST'])
def update_dst_age_range():
                          	    
    if request.form['submit'] == 'submit_age_range':
        selected_age_range = request.form['selected_age_range']      #Current Age_range selection
        
        selected_ar = Age_range.query.filter(Age_range.title == selected_age_range).first()   #Save for next method call
        selected_ar = age_range_select2(selected_ar.id)
        
        if request.method == 'GET':
            return render_template('add_destination.html', age_ranges=age_ranges, 
                                                           tags=tags, 
                                                           selected_age_range = selected_age_range, 
                                                           selected_tag = selected_tag)
    
  