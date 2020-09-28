#Select a tag from a list 
@slct.route('/tag_select', methods=['GET', 'POST'])
def tag_select():
	#print("1111111111111")
	tags = tag.query.filter(tag.hide == False).all()
	for tag in tags:
		tag.selected = False
	
	if request.method == 'GET':
		return render_template('tags.edit_tags.html', tags=tags)
		
	#print("1111111111111")
		
	selected_tag_id = int(request.form['selected_tag'])
	#print("1111111111111")

	#print ("SSSSSSSSSSSSSelected tag is" )
	#print (selected_tag_id)

	tag = tag.query.get_or_404(selected_tag_id)		
		
	tag.selected = True
	#print(tag.first_name)
	
	db.session.commit()
	
	tag = tag.query.get_or_404(selected_tag_id)
	#print(tag.selected)
	tags = tag.query.filter(tag.hide == False).all()
	#return render_template('show_selected_tag.html', tags=tags)
	return edit_tags()
	
@slct.route('/tag_select2/<int:selected_tag_id>', methods=['GET', 'POST'])
def tag_select2(selected_tag_id):
	
	tags = tag.query.all()
	for tag in tags:
		tag.selected = False

	tag = tag.query.get_or_404(selected_tag_id)				
	tag.selected = True
	
	
	