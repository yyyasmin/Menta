        import pdb; pdb.set_trace()
        
        todo_sts_name = "sts"+ str(std_txt.general_txt_id)
        print( "request.form[todo_sts_name]", request.form[todo_sts_name])
        
        todo_date_name = "due_date" + str(std_txt.general_txt_id)
        print( "request.form[todo_date_name]", request.form[todo_date_name])
        
        todo_who_name = "who"+ str(std_txt.general_txt_id)
        print( "request.form[todo_who_name]", request.form[todo_who_name])
        
        selected_todo_status = Status.query.filter(Status.id==request.form[todo_sts_name]).first()
        if selected_todo_status != None:
            std_txt.status_id = selected_todo_status.id  
        todo_due_date = request.form[todo_date_name]                
        if todo_due_date != None:
            std_txt.due_date = todo_due_date
        who = Accupation.query.filter(Accupation.id==request.form.get(todo_who_name)).first()
        if who != None:
            std_txt.acc_id = who.id
   