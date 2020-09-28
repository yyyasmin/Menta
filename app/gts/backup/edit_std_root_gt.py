	
################ START studets gts ##################
	
@std.route('/edit_std_root_gt', methods=['GET', 'POST'])
@login_required
def edit_std_root_gt(gt_root_class_name, gt_root_sub1_class_name, gt_root_sub2_class_name, gt_root_sub3_class_name):   # for example: for student_subjects  ==> gt_root_class_name = 'Subject' stored  gt.gt_type

    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
        
        
    std_gt_root = eval(gt_root_class_name).query.filter(eval(gt_root_class_name).selected==True).first()
    if std_gt_root == None:   # CASE 1 given GT IS THE ROOT
        flash("Please select a student plan part to show ")
        return redirect(url_for('students.edit_students'))
        
    print("")
    print("")
    print("std_gt_root", std_gt_root, std_gt_root.general_txt.title)
       
    ###########################################################
    # Get students gts of Type gt_root_sub1_class_name                              #
    ###########################################################
    for std_gt_sub1 in std.general_txts:

        #################import pdb; #pdb.set_trace()
        
        print("")
        print("std_gt_sub1", std_gt_sub1.student, std_gt_sub1.general_txt, std_gt_sub1.general_txt.title)
         
        if std_gt_sub1.general_txt.gt_type == gt_root_class_name:
            std_gts.append(std_gt.general_txt)
   
#''' 
print("")
print("")   
print("std_gts", std_gts)
print("")
print("")
#'''
all_gts  = eval(gt_root_class_name).query.all()                                                  
gts_not_of_student = list(set(all_gts).difference(set(std_gts)))  #main_gts_not_of_student = all_main_gts - std_gts

##print("std_gts", std_gts)
##print("")

# Get gt's categories
gt_categories = []  
for std_gt in std_gts:    
    for x in get_categories_of(std_gt):
        if x not in gt_categories:
            gt_categories.append(x)

#####################import pdb; #pdb.set_trace()

##################################################################                                
######### Level2 -- gt_root_class_name's children of Type in Categories ##########
##################################################################     
gt_subs = []
gt_subs_not_of_std=[]
for gt in std_gts: 
    gt_subs.extend(get_gt_all_categories_children(gt))     
    gt_subs_not_of_std = gt_subs_not_of_std+get_gt_all_categories_children_not_of_std(std, gt)  #main_gts_not_of_student = all_main_gts - std_gts

#'''
#NOT OF DEBUG 
print("gt_subs : ", gt_subs)
print("")
print("gt_subs_not_of_std : ",gt_subs_not_of_std)    
#NOT OF DEBUG
#'''       

##################################################################                                
######### Level3 -- gt_root_class_name's children of Type in Categories ##########
##################################################################        
gt_sub_subs = []
gt_sub_subs_not_of_std = []
if gt_root_sub2_class_name != 'None':
    for gt in gt_subs: 
        gt_sub_subs.extend(get_gt_all_categories_children(gt))            
        gt_subs_not_of_std = gt_subs_not_of_std+get_gt_all_categories_children_not_of_std(std, gt)  #main_gts_not_of_student = all_main_gts - std_gts

##################################################################                                
######### Level4 -- gt_root_class_name's children of Type in Categories ##########
##################################################################        
gt_sub_sub_subs = []
gt_sub_sub_subs_not_of_std = []
if gt_root_sub3_class_name != 'None':
    for gt in gt_sub_subs: 
        gt_sub_sub_subs.extend(get_gt_all_categories_children(gt))  
        gt_sub_sub_subs_not_of_std = gt_sub_sub_subs_not_of_std+get_gt_all_categories_children_not_of_std(std, gt)  #main_gts_not_of_student = all_main_gts - std_gts

#'''
print("")
print("")
print("gt_sub_subs", gt_sub_sub_subs)
print("")
print("gt_sub_sub_subs_not_of_std", gt_sub_sub_subs_not_of_std)
print("")
print("")
#'''

whos = Accupation.query.all()
default_who = Accupation.query.filter(Accupation.default==True).first()

statuss = Status.query.all()
default_status = Status.query.filter(Status.default==True).first()
    
tags = Tag.query.order_by(Tag.title).all() 
default_tag = Tag.query.filter(Tag.selected==True).first()
if default_tag == None:
    default_tag = Tag.query.filter(Tag.default==True).first()
 
age_ranges = Age_range.query.order_by(Age_range.from_age).all()     
default_ar = Age_range.query.filter(Age_range.selected==True).first()
if default_ar == None:
    default_ar = Age_range.query.filter(Age_range.default==True).first()

std_txts = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).all()

due_date = date.today()
  
print("")
print("")
print("IN edit_std_root_gt, BEFORE calling edit_all_main_gts.html --- gt_subs: ", gt_subs)
print("")
print("")
return render_template('./gts/table_gts/edit_all_main_gts.html', std=std,  
                                                    std_gts=std_gts, gts_not_of_student=gts_not_of_student, gt_categories=gt_categories,
                                                    gt_subs=gt_subs, gt_subs_not_of_std=gt_subs_not_of_std,
                                                    gt_sub_subs=gt_sub_subs, gt_sub_subs_not_of_std=gt_sub_subs_not_of_std,
                                                    statuss=statuss, default_status=default_status,
                                                    whos=whos, default_who=default_who,
                                                    tags=tags, age_ranges=age_ranges,
                                                    due_date=due_date)
