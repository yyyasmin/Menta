###Select a status from a list 	
@slct.route('/status_select2/<int:selected_status_id>', methods=['GET', 'POST'])
def status_select2(selected_status_id):
	
    statuss = status.query.all()
    for status in statuss:
        status.selected = False

    status = status.query.get_or_404(selected_status_id)				
    status.selected = True
    return status
###Select a status from a list 	