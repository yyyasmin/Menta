
        
#FROM https://youtu.be/I2dJuNwlIH0?t=583
@std.route('/tag_sub_tag_to_profile_add/<tag_id>/<sub_tag_id>', methods=['GET', 'POST'])
def tag_sub_tag_to_profile_add(tag_id, sub_tag_id):
            
    print("")
    print("")
    print("IN tag_sub_tag_to_profile_add ")
    print("tag_id: ", tag_id)
    print("sub_tag_id: ", sub_tag_id)
      
    tag = Tag.query.filter(Tag.id==tag_id).first()
    sub_tag = Sub_tag.query.filter(Sub_tag.id==tag_id).first()
    
    profile = Profile.query.filter(Profile.selected==True).first()
    profile.set_parent(tag)
    profile.set_parent(sub_tag)
    db.session.commit()
    return std_edit_profile()
  
  
################ SCRIPT #############################

	sub_tag_select.onchange = function(){

		sub_tag_id = sub_tag_select.value;
		console.log("IN sub_tag_select.onchange SUB_TAG_ID:");
		console.log(sub_tag_id);
		
		fetch('/tag_sub_tag_to_profile_add/' + sub_tag_id + '/' + sub_tag_id);

	}
