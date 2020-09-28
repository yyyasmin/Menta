##############destination's age range###############

@dst.route('/edit_dst_age_range', methods=['GET', 'POST'])
def edit_dst_age_range():

	destination = Destination.query.filter(Destination.selected==True).first()
	if destination == None:
		flash("Please select a destination first ")
		return redirect(url_for('select.destination_select'))		
	print("In edit_dst_age_rangess " )
	return render_template('./sub_forms/edit_ar_form.html', destination=destination) 
																
														  		
@dst.route('/edit_dst_age_range2/<int:selected_destination_id>', methods=['GET', 'POST'])
def edit_dst_age_range2(selected_destination_id):
	print("In edit_dst_age_rangess2 Request is :", request)
	dst = destination_select2(selected_destination_id)
	return redirect(url_for('destinations.edit_dst_age_range'))		
    
##############destination's age range###############
