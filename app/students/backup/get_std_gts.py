
@std.route('/get_gt_categories_children', methods=['GET', 'POST'])
@login_required
def get_gt_all_categories_children(gt):  
     
    # Get gt's categories
    gt_categories = []    
    for x in get_categories_of(gt):
        if x not in gt_categories:
            gt_categories.append(x)

    print("IN get_gt_categories_children -- gt_categories --: ", gt_categories)
    print("")
       
    gt_all_categories_subs = []
    for ctg in gt_categories:
        gt_all_categories_subs.extend(get_gt_children_of_category(gt, ctg.gt_type)) 
    
    print("IN get_gt_categories_children -- gt_all_categories_subs --: ", gt_all_categories_subs)
    print("")
    
    return gt_all_categories_subs
 
 

@std.route('/get_gt_children_of_category', methods=['GET', 'POST'])
@login_required
def get_gt_children_of_category(gt, Ctegory):

    gt_ctg_children = []
    all_ctg_gts = eval(Categor).query.all()
    for c in gt.children.all():
        if c.general_txt in all_ctg_gts:
            gt_ctg_children.append(c) 

    print(" IN get_gt_children_of_category", gt_ctg_children)
    
    return gt_ctg_children

