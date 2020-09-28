
#update selected destination
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@dst.route('/destination_update_at_once/<int:selected_destination_id>/<int:from_dst_sort_order>', methods=['GET', 'POST'])
def destination_update_at_once(selected_destination_id, from_dst_sort_order):
    ###########import pdb; pdb.set_trace()

    updated_dst = destination_select2(selected_destination_id)
    if updated_dst == None:
        flah("please select a destination to update ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=from_dst_sort_order))
    print("\n\n")
    print("In destination_update_at_once for dst start: ", updated_dst.title)
    print("Updateing dst : ", updated_dst.title)

    age_ranges = Age_range.query.all()
    tags = Tag.query.all()    
    scrts = Scrt.query.all() 

    
    selected_ar_title = get_selected_ar_title()
    selected_tag_title = get_selected_tag_title()
    selected_scrt_title = get_selected_scrt_title()
    
    if request.method == 'GET':
        print("GGGGGGGGGGGGGGET")
        return render_template('update_destination.html',
                            dst = updated_dst,
                            age_ranges=age_ranges,
                            tags=tags, 
                            scrts=scrts,
                            selected_ar_title=selected_ar_title, 
                            selected_tag_title=selected_tag_title,
                            selected_scrt_title=selected_scrt_title,
                            from_dst_sort_order=from_dst_sort_order)

    selected_ar = set_dst_age_range()
    selected_tag = set_dst_tag()
    selected_scrt=set_dst_scrt()
                                 
    updated_dst.title = request.form['title']     
    updated_dst.body = request.form['description']
            
    updated_tag = Tag.query.filter(Tag.selected==True).first()
    updated_ar = Age_range.query.filter(Age_range.selected==True).first()
    updated_scrt = Scrt.query.filter(Scrt.selected==True).first()
    
    updated_dst.age_range_id = updated_ar.id
    updated_dst.scrt_id = updated_scrt.id
    
    updated_dst_tag = Dst_Tag.query.filter(Dst_Tag.destination_id==updated_dst.id and  Dst_Tag.tag_id==updated_tag.id).first()
    if updated_dst_tag == None:
        updated_dst = Dst_Tag(update_dst.id, updated_tag.id)       
        updated_dst.destination = update_dst
        updated_dst.tag = updated_tag
        updated_tag.destinations.append(updated_dst_tag)
        updated_dst.tags.append(updated_dst_tag)
 
    ###########import pdb; pdb.set_trace()
        db.session.commit()
        update_dst.selected = False
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=from_dst_sort_order))
################## END Submit Back to destinations list ################ 

### For all submit options except for back to list###
    db.session.commit()
    return render_template('update_destination.html', 
                                                dst = updated_dst,
                                                age_ranges=age_ranges,
                                                tags=tags, 
                                                scrts=scrts,
                                                selected_ar_title=selected_ar_title, 
                                                selected_tag_title=selected_tag_title,
                                                selected_scrt_title=selected_scrt_title,
                                                from_dst_sort_order=from_dst_sort_order)                                

###End Update destination########################
