########## START attach_gt_to_std #############################

@std.route('/attach_gt_to_std/<int:std_id>/<int:gt_id>', methods=['GET', 'POST'])
def attach_gt_to_std(std_id, gt_id):

    ### asign TO  HUMPTY DUMPTY THE NEW TODO
    std_gt = Std_general_txt.query.filter(Std_general_txt.student_id==std_id).filter(Std_general_txt.general_txt_id==gt_id).first()
    if std_gt == None:
        std_gt = Std_general_txt(std_id, gt_id)
        std_gt.due_date = due_date
        sts = Status.query.filter(Status.body=='default').first()
        std_gt.status_id = sts.id 

        gt = General_txt.query.filter(General_txt.id==gt_id).first()        
        std = Student.query.filter(Student.id==std_id).first()
        if std_gt not in gt.students:
            gt.students.append(std_gt)
        if std_gt not in std.general_txts:
            std.general_txts.append(std_gt)
        
    db.session.commit()
    return std_gt    

########## START attach_gt_to_std #############################
