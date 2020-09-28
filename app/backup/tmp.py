
{% extends "layout.html" %} 


{% block content %}

<div class="container">
    <form role="form" method="POST" action=''> 
		<label for="title">Studdent:  id: {{ teacher_already_exist.id }}   first name: {{ teacher_already_exist.first_name }}   last name: {{ teacher_already_exist.last_name }}</label>
		<h2><label for="title">This teacher was removed in the past. Do you want to get him back? </label></h2>
		
		</br>		 
		<button class="btn btn-danger btn-xs" ><a href="{{ url_for('teachers.teacher_add') }}">No thanks</a></button>
		<button class="btn btn-success btn-xs" ><a href="{{ url_for('teachers.teacher_unhide2', selected_teacher_id=teacher_already_exist.id) }}">Yes</a></button>
	</form>
</div>

{% endblock %}