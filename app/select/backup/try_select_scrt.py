	
#Select a scrt ###########################
@slct.route('/scrt_select', methods=['GET', 'POST'])
def scrt_select():
	#print("1111111111111")
	scrts = Scrt.query.all()
	for scrt in scrts:
		scrt.selected = False
	
	if request.method == 'GET':
		return render_template('edit_scrts.html', scrts=scrts)
		
	#print("1111111111111")
		
	selected_scrt_id = int(request.form['selected_scrt'])
	#print("1111111111111")

	#print ("SSSSSSSSSSSSSelected scrt is" )
	#print (selected_scrt_id)

	scrt = scrt.query.get_or_404(selected_scrt_id)		
		
	scrt.selected = True
	#print(scrt.first_name)
	
	db.session.commit()
	
	scrt = scrt.query.get_or_404(selected_scrt_id)
	#print(scrt.selected)
	scrts = scrt.query.all()
	#return render_template('show_selected_scrt.html', scrts=scrts)
	return edit_scrts()
	
@slct.route('/scrt_select2/<int:selected_scrt_id>', methods=['GET', 'POST'])
def scrt_select2(selected_scrt_id):

    scrts = Scrt.query.all()
    for scrt in scrts:
        scrt.selected = False

    scrt = Scrt.query.get_or_404(selected_scrt_id)				
    scrt.selected = True
    db.session.commit()

    return scrt
#Select a scrt ##########################3
	