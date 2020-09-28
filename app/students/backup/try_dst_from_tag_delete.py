############# Start Delete dst from tag #############
@std.route('/dst_from_tag_delete', methods=['GET', 'POST'])
def dst_from_tag_delete():
	##import pdb; pdb.set_trace()
	tag = Tag.query.filter(Tag.selected==True).first()
	if tag == None:
		flash("Please select a tag first ")
		return redirect(url_for('destinations.destinations_by_tag'))

	dst = Destination.query.filter(Destination.selected==True).first()
	if dst == None:
		flash("Please select a dst first ")
		return redirect(url_for('destinations.edit_destinations'))
		
	#print("SSSSSRRRRR IN tag_from_dst_delete   deleteing tag %s from dst %s :",tag.id, dst.id )			
	dst_tag = Dst_Tag.query.filter(Dst_Tag.tag_id == tag.id).filter(Dst_Tag.dst_id==dst.id).first()   #update dst_tag
	if dst_tag:	
		##import pdb; pdb.set_trace()
		print ("deleting  Dst_TAG  ", dst_tag.destination_id,dst_tag.tag_id)
		db.session.delete(dst_tag)
		db.session.commit()
	
	return  redirect(url_for('destinations.destinations_by_tag'))  #no change in tags staff dsts
		
@std.route('/dst_from_tag_delete2/delete/<int:selected_dst_id>/<int:selected_tag_id>', methods=['GET', 'POST'])
def dst_from_tag_delete2(selected_dst_id, selected_tag_id):
	#print("In DDDDDDDDDDDD tag_from_dst_delete2")
	std = tag_select2(selected_tag_id)
	if selected_dst_id:
		#print(selected_dst_id)
		tchr = dst_select2(selected_dst_id)
	return  redirect(url_for('tags.dst_from_tag_delete'))  
############# Start Delete dst from tag #############

	