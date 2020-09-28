
############# ufile_gt select 
@slct.route('/ufile_gt_select2/<int:selected_ufile_id>/<int:selected_gt_id>', methods=['GET', 'POST'])
def ufile_gt_select2(selected_ufile_id, selected_gt_id):
    
    ufile_gts = Ufile_general_txt.query.all()

    for ufile_gt in ufile_gts:
        ufile_gt.selected = False

    ufile_gt = Ufile_general_txt.query.filter(Ufile_general_txt.general_txt_id == selected_gt_id).filter(Ufile_general_txt.ufile_id==selected_ufile_id).first()
    if ufile_gt == None:
        flash("Please select a general_txt for Ufile ")
        return redirect(url_for("Ufiles.edit_Ufile_destinations"))
            
    ufile_gt.selected = True
    db.session.commit()

    return ufile_gt
############# ufile_gt select 

	