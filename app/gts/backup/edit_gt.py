
@gt.route('/edit_gt', methods=['GET', 'POST'])
@login_required
def edit_gt():

    #DEBUG ONLY

    #DEBUG ONLY
           
    gts = General_txt.query.order_by(General_txt.class_name).order_by(General_txt.class_name).order_by(General_txt.title).all() 

    '''
    print("")
    for g in gts:
        print("g g.class_name", g, g.class_name)
        print("")
    '''
    
    i=0
    for g in gts:
        g.odd = (i%2 == 1)
       
    #################import pdb; pdb.set_trace()
    return render_template('edit_gt.html', gts=gts)							
		
     