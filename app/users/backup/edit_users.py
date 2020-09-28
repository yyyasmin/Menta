

@gt.route('/edit_users', methods=['GET', 'POST'])
@login_required
def edit_users():

    #DEBUG ONLY

    #DEBUG ONLY
           
    users = User.query.all() 

    print("")
    for u in users:
        print("USER ", u.username)
        print("USER IS SUPER ", u.is_super_user)
        print("")
        
    return render_template('edit_users.html', users=users)							
