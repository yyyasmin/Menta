	
@slct.route('/general_txt_select2/<int:selected_general_txt_id>', methods=['GET', 'POST'])
def general_txt_select2(selected_general_txt_id):

    general_txts = General_txt.query.all()
    for general_txt in general_txts:
        general_txt.selected = False

    general_txt = General_txt.query.get_or_404(selected_general_txt_id)				
    general_txt.selected = True
    db.session.commit()

    return general_txt