{% extends "layout.html" %}

{% block content %}

<style>

table {
    font-family: arial, sans-serif;
    border-collapse: separate;
    width: 100%;
}

td, th {
    border: 1px solid #dddddd;
    padding: 5px;
	align: center;
}

tr:nth-child(even) {
    background-color: #dddddd;
}

table, th, td {
    border: 1px solid black;
	text-align: center;
}

#add_button  {
	-webkit-font-smoothing:subpixel-antialiased;
	background-color:#efeff5;
	margin-left:10%;
	margin-right:10%;
}

</style>

<div> IN C:\Users\yasmi\Documents\מנטא\app\destinations\templates\edit_dst_by_age_range.html </div>

<h2><center>רשימת מטרות לפי קבוצות גיל</center></h2>	
	<button class="btn btn-info btn-xs" id="add_button"><h5><strong>
		<a href="{{ url_for('destinations.dsply_dst_form', from_dst_sort_order=2) }}">הוסף מטרה</a>
	<strong></h5></button>
	</br></br>
	
	{% for ar in age_ranges %}
		</br></br>
		<th><h4><strong>קבוצת גיל:   {{ ar.title }}</strong></h4></th>

		<table style="width:100%">

		<tr id="header_row">			
			<th>קבוצת גיל</th>
			<th>נושא</th>
			<th>מטרה</th> 
			<th>פעולות עריכה</th>
		</tr>
		{% for tag in tags %}			
			{% for dst in ar.destinations %}	
				{% for dt in dst.tags %}
					{% if dt.tag_id == tag.id %}

				<tr>
					<td>{{ ar.title }}</td>
					<td>{{ tag.title }}</td>
					<td>{{ dst.title }}</td>
					
					<td>	
					{% with from_dst_sort_order=2 %}		
						{% include "./sub_forms/edit_dst_actions.html" %}
					{% endwith %}
					</td>
					
				</tr>
					{% endif %}
				{% endfor %}				
			{% endfor %}								
		{% endfor %}  <!-- tags -->
		</table>
	{% endfor %}  <!-- ar -->
	
{% endblock %}