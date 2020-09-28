############### START get_public_dsts ###############

@dst.route('/get_public_dsts', methods=['GET', 'POST'])
def get_public_dsts():

    public_scrt = Scrt.query.filter(Scrt.title=='public').first()
    # Get all public dummy std destinations
    dummy_std_gts = Std_generl_txt.query.filter(Std_generl_txt.student_id===0).filter(Std_generl_txt.public_id==public_scrt.id).all()   # dummy student has all dsts
    all_destinations = Destination.query.filter(Destination.hide==False).order_by(Destination.title).all()
    public_destinations=[]
    for gt in dummy_std_gts:
    if gt.general_txt in all_destinations:
       public_destinations.append(gt.general_txt) 

    print("Public dsta are: ", public_destinations)
    return public_destinations

############### END get_public_dsts ###############
