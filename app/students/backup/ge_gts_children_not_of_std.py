	 
     
@std.route('/get_gt_all_categories_children_not_of_std', methods=['GET', 'POST'])
@login_required
def get_gt_all_categories_children_not_of_std(std, gt):  
     
    # Get gt's categories
    gt_categories = []    
    for x in get_categories_of(gt):
        if x not in gt_categories:
            gt_categories.append(x)

    print("IN get_gt_categories_children -- gt_categories --: ", gt_categories)
    print("")
       
    gt_all_categories_subs_not_of_std = []
    for ctg in gt_categories:
        gt_all_categories_subs_not_of_std.extend(get_gt_children_of_category_not_of_std(std, gt, ctg.gt_type)) 
    
    print("IN get_gt_all_categories_children_not_of_std -- gt_all_categories_subs_not_of_std --: ", gt_all_categories_subs_not_of_std)
    print("")
    
    return gt_all_categories_subs_not_of_std
 
 
@std.route('/get_gt_children_of_category_not_of_std', methods=['GET', 'POST'])
@login_required
def get_gt_children_of_category_not_of_std(std, gt, Ctegory):

    gt_ctg_children_not_of_std = []
    all_ctg_gts = eval(Categor).query.all()
    for c not in gt.children.all():
        if c.general_txt in all_ctg_gts:
            gt_ctg_children_not_of_std.append(c) 

    print(" IN get_gt_children_of_category_not_of_std", gt_ctg_children_not_of_std)
    
    return gt_ctg_children_not_of_std
