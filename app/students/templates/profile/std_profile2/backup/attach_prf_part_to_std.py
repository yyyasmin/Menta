
@std.route('/attach_prf_part_to_std2/<int: selected_gt_id>', methods=['GET', 'POST'])
def attach_prf_part_to_std2(selected_gt_id):

    print("")
    print("")
    print(" IN gt_to_profile_ADD2")
            
    gt = gt_type_select2(selected_gt_id)
    return std_part_to_prf_add(gt.type, gt.title, gt.body) 
