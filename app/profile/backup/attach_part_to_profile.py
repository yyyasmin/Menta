
@std.route('/attach_prf_part_to_std2/<int:selected_gt_id>/<int:tag_id>/<int:sub_tag_id>/<int:dsply_direction>', methods=['GET', 'POST'])
def attach_prf_part_to_std2(selected_gt_id, tag_id, sub_tag_id, dsply_direction):

    print("")
    print("")
    print(" IN ATTACH_prf_part_to_std2")
    print(" selected_gt_id, tag_id, sub_tag_id", selected_gt_id, tag_id, sub_tag_id)
    print("")
    print("")
    
    gt = gt_type_select2(selected_gt_id)
    
    return std_part_to_prf_add(gt.class_name, gt.id, gt.title, gt.body, tag_id, sub_tag_id, dsply_direction) 

