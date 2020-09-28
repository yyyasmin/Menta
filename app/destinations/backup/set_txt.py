
 ###START set selected tag		
@dst.route('/set_dst_tag', methods=['POST'])
def set_dst_tag(selected_tag_title):
    print("In  set_dst_tag TTT title is: ", selected_tag_title) 
    
    selected_tag_title = selected_tag_title      #Current Tag selection

   # POST case
    selected_tag = Tag.query.filter(Tag.title == selected_tag_title).first()   
    print("In set_dst_tag SSSSSSSSS Selected tag is   type: ", selected_tag, selected_tag.type, selected_tag.__tablename__)
    if selected_tag == None:
        flash("יש לבחור קבוצת גיל")
        return(url_for('destinations.destination_add', from_dst_sort_order=0, selected_tag_title = "בחר קבוצת גיל", selected_tag_title = "בחר נושא", selected_tag_title = "בחר סוג אבטחה" ))
    
    selected_tag = tag_select2(selected_tag.id) 
    print(" selected_tag BBBBBBBBBBBBBBBBBB BRFORE : ", selected_tag)
    selected_tag = Tag.query.filter(Tag.id==selected_tag.id).first()
    print(" selected_tag AAAAAAAAAAAAAAAAAAA AFTER : ", selected_tag)

    dst = Destination.query.filter(Destination.selected==True).first()
    old_dst_tag = Tag.query.join(Destination).filter(Tag in Destination.children).first()   #delete the prevois tag of the updated destination 
    if old_dst_tag != None
        dst.children.remove(old_dst_tag)
        dst.children.append(selected_tag)
        
    db.session.commit() 
    return selected_tag
 ###END set selected tag	
    