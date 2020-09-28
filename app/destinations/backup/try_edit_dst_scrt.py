##############destination's scrt ###############

@dst.route('/edit_dst_scrt', methods=['GET', 'POST'])
def edit_dst_scrt():
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('select.destination_select'))		
    print("In edit_dst_scrtss " )
    scrts = Scrt.query.all()
    return render_template('./sub_forms/edit_ar_for_one_dst.html', dst=dst, scrts=scrts) 
																
														  		
@dst.route('/edit_dst_scrt2/<int:selected_destination_id>', methods=['GET', 'POST'])
def edit_dst_scrt2(selected_destination_id):
	print("In edit_dst_scrtss2 Request is :", request)
	dst = destination_select2(selected_destination_id)
	return redirect(url_for('destinations.edit_dst_scrt'))		

	
@dst.route('/update_dst_scrt', methods=['GET', 'POST'])
def update_dst_scrt():
    
    #import pdb; pdb.set_trace()
    #if request.form['submit'] == 'submit_scrt':
    selected_scrt = request.form['selected_scrt']      #Current Scrt selection
            
    if request.method == 'GET':
        return render_template('edit_ar_for_one_dst.html', scrts=scrts, 
                                                           tags=tags, 
                                                           selected_scrt = selected_scrt, 
                                                           selected_tag = selected_tag)

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        
    selected_ar = Scrt.query.filter(Scrt.title == selected_scrt).first()   
    selected_ar = scrt_select2(selected_ar.id)    
        
    dst.scrt_id = selected_ar.id
    db.session.commit()  

    return redirect(url_for('destinations.edit_destinations')) 
    
##############destination's scrt ###############
 	

	