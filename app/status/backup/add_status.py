 
### FROM https://www.youtube.com/watch?v=I2dJuNwlIH0&feature=youtu.be
### FROM https://github.com/PrettyPrinted/dynamic_select_flask_wtf_javascript
################## START  Ddsply_status_form ################    
@status.route('/add_status/<int:from_status_sort_order>', methods=['GET', 'POST'])
def add_status(from_status_sort_order):
    print ("In dsply_status_form from_status_sort_order=: ", from_status_sort_order)

    form = Dst_form()

    form.color.choices=[]
    form.status.choices=[]

    form.color.choices = [(color.id, color.title) for ar in Age_range.query.all()]
    form.status.choices = [(status.id, status.title) for tag in Tag.query.all()]

    ### GET Case
    if request.method == 'GET':
        return render_template('dsply_status_form.html', form=form)

    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור צבע")
        return render_template('dsply_status_form.html', form=form)

    color = Color.query.filter_by(id=form.color.data).first()
    status = Status.query.filter_by(id=form.status.data).first()

    ##############old_status_scrt pdb.set_trace()
    new_status_title = form.status_title.data
    return status_add(from_status_sort_order, color.title, status.title, new_status_title)
