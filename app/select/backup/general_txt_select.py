
@slct.route('/general_txt_select2/<int:selected_general_txt_id>', methods=['GET', 'POST'])
def general_txt_select2(selected_general_txt_id):

    general_txts = General_txt.query.all()
    for general_txt in general_txts:
        general_txt.selected = False

    general_txt = General_txt.query.filter(General_txt.id==selected_general_txt_id).first()
    if general_txt == None:
        flash("Please select a general_txt for student ")
        return redirect(url_for("students.edit_student_general_txts"))
        
    general_txt.selected = True
    db.session.commit()

    return general_txt


############# Std_general_txt select 
@slct.route('/std_general_txt_select2/<int:selected_std_id>/<int:selected_general_txt_id>', methods=['GET', 'POST'])
def std_general_txt_select2(selected_std_id, selected_general_txt_id):

    #std_general_txts = Std_general_txt.query.all()
    
    std_general_txts = Std_geneal_txt.query.filter(Std_geneal_txt.type=='general_txt').all()

    for std_general_txt in std_general_txts:
        std_general_txt.selected = False

    std_general_txt = Std_geneal_txt.query.filter(Std_geneal_txt.id == selected_general_txt_id).filter(Std_geneal_txt.student_id==selected_std_id).first()
    if std_general_txt == None:
        flash("Please select a general_txt for student ")
        return redirect(url_for("students.edit_student_general_txts"))
        
    std_general_txt.selected = True
    db.session.commit()

    return std_general_txt
############# Std_general_txt select 

