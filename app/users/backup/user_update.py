@usr.route('/user_update/<int:selected_user_id>', methods=['GET', 'POST'])
@login_required
def user_update(selected_user_id):

    user = General_txt.query.filter(General_txt.id == selected_user_id).first()
    if user == None:
        flash("Please select a Category to update first")
        return edit_users()
			
    if request.method == 'GET':
        #print("GET render update_user.html")
        return render_template('update_user.html', user=user)
        
    user.username = request.form.get('username')
    user.email = request.form.get('email')
   
    user.is_super_user = request.form.get('is_super_user') == 'on'
    
    print("")
    print("IN user_update user.is_super_user: ", user.is_super_user)
    print("")
    print("")
        
    db.session.commit()  
    db.session.refresh(user)
	
    return redirect(url_for('users.edit_users'))
	