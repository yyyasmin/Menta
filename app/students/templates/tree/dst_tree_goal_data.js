{% block goal_data_3 %}

	console.log(" INN tree\backup\goal_data_3.js");
	console.log({{ goal.id }});

	{% for sts in statuss %}
		{% if goal.is_parent_of(sts) %}
		
			nodeDataArray.push({
				key: '{{ goal.id }}',
				parent: '{{ dest.id }}', 

				color: '{{goal.title_color}}',
				source: "{{ url_for('static', filename='img/goal3.PNG') }}",							

				text_color: '{{ sts.color }}',
				name: '{{ goal.title }}',
				status: 'סטאטוס: {{ sts.title }}',
			} );
																	
		{% endif %}
	{% endfor %}
				
{% endblock goal_data_3 %}
