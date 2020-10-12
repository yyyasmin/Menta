	
@slct.route('/test_select2/<int:selected_test_id>', tests=['GET', 'POST'])
def test_select2(selected_test_id):
	
    tests = Test.query.all()
    for test in tests:
        test.selected = False

    test = Test.query.filter(Test.id == selected_test_id).first()
    if test==None:
        flash("Please select a test for thisstudent first")
        redirect(url_for('students.edit_student_tests'))
    
    test.selected = True
    db.session.commit()

    return test
###Select a test from a list 	
