

@slct.route('/star_select2/<int:selected_subject_id>', methods=['GET', 'POST'])
def star_select2(selected_star_id):

    stars = Star.query.all()		
    for star in stars:
        star.selected = False

    star = Star.query.filter(Star.id==selected_star_id).first()
    if sbj == None:
        flash("Please select a star plese ")
        return redirect(url_for("profile.edit_profile_by_tag"))

    sbj.selected = True
    db.session.commit()

    return star	

