
#update selected file
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@rsrc.route('/file/update/<int:selected_file_id>', methods=['GET', 'POST'])
def file_update(selected_file_id):

    author_id = current_user._get_current_object().id
    
    destination = Destination.query.filter(Destination.selected==True).first()
    if destination == None:
        flash("Please select a destination first ")
        return redirect(url_for('index'))
        
    goal = Goal.query.filter(Goal.selected==True).first()
    print(" In file_update goal selected is")
    print(goal.title)
    
    if goal == None:
        flash("Please select an goal first ")
        return redirect(url_for('goal_select'))
    print(goal.title)      
    #print request
    
    file_select2(selected_file_id)	
    file = Resource.query.get_or_404(selected_file_id)
	
    if request.method == 'GET':
        return render_template('update_file.html', goal=goal, file=file)
		
    #get data from form and insert to destinationgress db
    ###import pdb; pdb.set_trace() 	
    file.title = request.form.get('title')
    file.body = request.form.get('description')
    
    db.session.commit()  
    db.session.refresh(file)
	
    return redirect(url_for('resources.files_by_resource'))		
#end update selected file 	