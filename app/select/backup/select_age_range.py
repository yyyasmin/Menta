	
#Select a age_range ###########################
@slct.route('/age_range_select', methods=['GET', 'POST'])
def age_range_select():
	#print("1111111111111")
	age_ranges = age_range.query.filter(age_range.hide == False).all()
	for age_range in age_ranges:
		age_range.selected = False
	
	if request.method == 'GET':
		return render_template('age_ranges.edit_age_ranges.html', age_ranges=age_ranges)
		
	#print("1111111111111")
		
	selected_age_range_id = int(request.form['selected_age_range'])
	#print("1111111111111")

	#print ("SSSSSSSSSSSSSelected age_range is" )
	#print (selected_age_range_id)

	age_range = age_range.query.get_or_404(selected_age_range_id)		
		
	age_range.selected = True
	#print(age_range.first_name)
	
	db.session.commit()
	
	age_range = age_range.query.get_or_404(selected_age_range_id)
	#print(age_range.selected)
	age_ranges = age_range.query.filter(age_range.hide == False).all()
	#return render_template('show_selected_age_range.html', age_ranges=age_ranges)
	return edit_age_ranges()
	
@slct.route('/age_range_select2/<int:selected_age_range_id>', methods=['GET', 'POST'])
def age_range_select2(selected_age_range_id):
	
	age_ranges = age_range.query.all()
	for age_range in age_ranges:
		age_range.selected = False

	age_range = age_range.query.get_or_404(selected_age_range_id)				
	age_range.selected = True
#Select a age_range ##########################3
	
	