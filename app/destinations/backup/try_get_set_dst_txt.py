##############START destination's age range###############

@dst.route('/edit_dst_dst_txt', methods=['GET', 'POST'])
def edit_dst_dst_txt():
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations'))		
    print("In edit_dst_dst_txtss " )
    
    dst_txts = Destination.query.all()

    #POST CASE
    if request.method == 'POST':
        selected_dst_txt = set_dst_txt()
    
    selected_dst_txt = get_selected_dst_txt()
    
    return render_template('./sub_forms/edit_dst_tt.html',  dst=dst, 
                                                            dst_txt=dst_txt)
																
														  		
@dst.route('/edit_dst_dst_txt2/<int:selected_destination_id>', methods=['GET', 'POST'])
def edit_dst_dst_txt2(selected_destination_id):
	print("In edit_dst_dst_txtss2 Request is :", request)
	dst = destination_select2(selected_destination_id)
	return redirect(url_for('destinations.edit_dst_txt'))		

 ###START set selected dst_txt		
@dst.route('/set_dst_txt', methods=['POST'])
def set_dst_txt():
    print("In  set_dst_txt") 

    title = request.form['title']      #Current Description  selection
    body = request.form['description']
    new_destination.title = title
    new_destination.body = body

    #Get existing dst-tag or create new one and set it 
    new_dst_tag = Dst_Tag.query.filter(Dst_Tag.destination_id==new_destination.id and  Dst_Tag.tag_id==new_tag.id).first()
    if new_dst_tag == None:
        new_dst_tag = Dst_Tag(new_destination.id, new_tag.id)       
        new_dst_tag.destination = new_destination
        new_dst_tag.tag = new_tag
        new_dst_tag.destinations.append(new_dst_tag)
        new_destination.tags.append(new_dst_tag)
     
        ###import pdb; pdb.set_trace()    
    db.session.commit()  
    db.session.refresh(new_destination)

    new_destination = destination_select2(new_destination.id)

    db.session.commit() 
    ###import pdb; pdb.set_trace()
    return selected_ar.title
 ###END set selected dst_txt	
    
 ###get selected dst_txt	
@dst.route('/get_selected_ar_title', methods=['GET', 'POST'])
def get_selected_ar_title():
    tmp_dst_txt = Destination.query.filter(Destination.selected == True).first()
    if tmp_dst_txt != None:
        selected_dst_txt_title = tmp_dst_txt.title   
    else:    
        selected_dst_txt_title = ":הכנס כותרת ותאור המטרה"        
    return selected_dst_txt_title
###end get selected dst_txt
 
##############END destination's age range###############
