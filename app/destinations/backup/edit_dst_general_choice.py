    
##############START destination's age range###############

@dst.route('/edit_dst_age_range', methods=['GET', 'POST'])
def edit_dst_age_range():
    dst = Destination.query.filter(Destination.selected==True).filter(Destination.type=='destination').first()
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=1))		
    print("In edit_dst_age_rangess DDD dst title is: ",  dst.title  )
    
    age_ranges = Age_range.query.all()

    #POST CASE
    if request.method == 'POST':
        selected_ar_title = set_dst_age_range()
    
    selected_ar_title = get_selected_ar_title()
    
    return render_template('./sub_forms/ar/edit_ar_for_one_dst.html', 
                                                        dst=dst, 
                                                        age_ranges=age_ranges,
                                                        selected_ar_title=selected_ar_title) 
																
	