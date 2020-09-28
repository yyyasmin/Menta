    '''
    std_todos_forms = []

    import pdb; pdb.set_trace()
    
    for g in student_todos:
    
        form = Todo_form()

        form.status.choices=[]
        form.status.choices = [(status.id, status.title) for status in Status.query.all()]
        form.status.default = g.status_id
        form.process()
 
        import pdb; pdb.set_trace()

        form.who.choices=[]
        form.who.choices = [(who.id, who.title) for who in Accupation.query.all()]
        form.who.default = g.who_id
        form.process()
                       
        form.id.data = int(g.todo_id)
        todo = Todo.query.filter(Todo.id==g.todo.id).first()       
        form.title.data = todo.title
        form.body.data =  todo.body
       
        form.due_date = g.due_date
       
        std_todos_forms.append(form)
        
        '''