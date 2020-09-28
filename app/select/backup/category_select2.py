	
@slct.route('/category_select2/<int:selected_category_id>', methods=['GET', 'POST'])
def category_select2(selected_category_id):

    categories = Category.query.all()
    for category in categories:
        category.selected = False

    category = Category.query.get_or_404(selected_category_id)				
    category.selected = True
    db.session.commit()

    return category