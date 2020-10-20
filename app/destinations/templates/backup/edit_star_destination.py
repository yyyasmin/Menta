################ STARS ##############################################################


@dst.route('/edit_star_destinations/<int:selected_star_id>', methods=['GET', 'POST'])
@login_required
def edit_star_destinations(selected_star_id):

    star = star_select2(selected_star_id)
    
    tags=[]
    tag = Tag.query.filter(Tag.title == Star.title).first()    #get only Tag destinations
    if tag == None:
        flash ("אין לכוכב זה מטרות בבנק. נא הוסף דרך לשונית מטרות שבסרגל הכתום שלמעלה")
        return redirect(url_for('stars.star'))   
    tags.append(tag)
    
    age_ranges = Age_range.query.order_by(Age_range.title).all()
    sub_tags = Sub_tag.query.order_by(Sub_tag.title).all() 
    
    print("IN edit_destinations_by_subject")
    print("")
    print("")
    for d in destinations:
        if d.id > 500:
            print("DST: " ,d, d.title, d.body)
    #DEBUG
    print("")
    print("")
    for tag in tags:
        print("tag", tag.id)
        for sub in sub_tags:
            print("SUB", sub.id)
            for d in destinations:
                if d.is_parent_of(sub):
                    print("DST {0} {1}    SUB: {2} {3}".format(d.id, d.title, sub.id, sub.title))
                if d.is_parent_of(tag):
                    print("DST {0} {1}    TAG: {2} {3}".format(d.id, d.title, tag.id, tag.title))

    return render_template('edit_dst_by_subject.html', destinations=destinations, age_ranges=age_ranges, tags=tags, sub_tags=sub_tags)															


@dst.route('/edit_star_destinations2/<int:selected_star_id>', methods=['GET', 'POST'])
@login_required
def edit_star_destinations2(selected_star_id):
    star = star_select2(selected_star_id)
    return redirect(url_for('destinations.edit_star_destinations'))

################ STARS ##############################################################
