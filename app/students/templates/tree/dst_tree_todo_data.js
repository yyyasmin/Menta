{% block todos_data_3 %}

	console.log(" INN tree\backup\todos_data_3.js");
	console.log({{ todo.id }});

	{% for sts in statuss %}
		{% if todo.is_parent_of(sts) %}
		
					console.log("IN FOR STS IF TODO...");
					
				nodeDataArray.push(
				{
					key: '{{ todo.id }}',
					parent: '{{ goal.id }}',
					color: '{{todo.title_color}}',
					source: "{{ url_for('static', filename='img/mission1.PNG') }}",	
					
					text_color: '{{ sts.color }}',
					name: '{{ todo.title }}',
					status: 'סטאטוס: {{ sts.title }}',	
				} );
														
		{% endif %}
	{% endfor %}	
		
{% endblock todos_data_3 %}

