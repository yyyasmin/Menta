
@dst.route('/edit_destinations_by_subject', methods=['GET', 'POST'])
@login_required
def edit_destinations_by_subject():
    destinations = Destination.query.order_by(Destination.title).all() 
    age_ranges = Age_range.query.all()
    tags = Tag.query.all() 
    #import pdb; pdb.set_trace()
    #return render_template('edit_destinations_by_subject.html', destinations=destinations, age_ranges=age_ranges, tags=tags )							
    return render_template('edit_dst_by_age_range.html', destinations=destinations, age_ranges=age_ranges, tags=tags)															
