															
@dst.route('/edit_dst_scrt', methods=['GET', 'POST'])
def edit_dst_scrt():
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('select.destination_select'))		
    print("In edit_dst_scrtss " )
    scrts = Scrt.query.all()
    
    #POST CASE
    if request.method == 'POST':
        selected_scrt_title = set_dst_scrt()
    
    selected_scrt_title = get_selected_scrt_title()
    
    return render_template('./sub_forms/scrt/edit_scrt_for_one_dst.html', 
                                                        dst=dst, 
                                                        scrts=scrts,
                                                        selected_scrt_title=selected_scrt_title) 
							