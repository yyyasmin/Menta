		
@dst.route('/goal_delete_for_good', methods=['GET', 'POST'])
#Here author is user_id
def goal_delete_for_good():

	user = User.query.get_or_404(current_user.id)
	author_id = user.id
    
	goal = Goal.query.filter(Goal.selected==True).first()
	if goal == None:
		flash("Please select a goal to delete first ")
		return redirect(url_for('select.goal_select'))
			
	print ("delete selected goal is " )
	print(goal.title)      

	gggs = GGG.query.join(Goal.gggs).filter(Goal.id==goal.id)
	for ggg in gggs:
		redirect(url_for('gggs.ggg_delete2(ggg.id)'))
	db.session.delete(goal) 

	db.session.commit()  

	return redirect(url_for('detinations.edit_goals')) 
		
#delete from index goals list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@dst.route('/goal_delete_for_good2/<int:selected_goal_id>', methods=['GET', 'POST'])
#Here author is user_id
def goal_delete_for_good2(selected_goal_id):

	print ("SSSSSSSSSSSSSelected goal is" )
	goal_select2(selected_goal_id)
	return redirect(url_for('goals.goal_delete_for_good')) 	

