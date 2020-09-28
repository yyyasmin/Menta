	
		
@user.route('/user_delete_for_good', methods=['GET', 'POST'])
@login_required
#Here author is user_id
def user_delete_for_good():

    user = User.query.filter(User.selected==True).first()
    if user == None:
        flash("Please select a user to delete first ")
        return redirect(url_for('users.edit_users'))
            
    print("")
    print ("delete for good selected user is " )
    print(user.username) 
    print("")
        
    db.session.delete(user)
    db.session.commit()
    flash ("Deleted " + user.username + " object Successfully")
            
    return redirect(url_for('users.edit_users')) 
		
#delete from index users list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@user.route('/user_delete_for_good2/<int:selected_user_id>', methods=['GET', 'POST'])
#Here author is user_id
@login_required

def user_delete_for_good2(selected_user_id):

    #print ("SSSSSSSSSSSSSelected user is" )
    ################import pdb; pdb.set_trace()
    general_txt_select2(selected_user_id)
    return redirect(url_for('users.user_delete_for_good')) 	

