{% block goal_data %}

	{% for sts in statuss %}
		{% if goal.is_parent_of(sts) %}
			nodeDataArray.push({
				key: j,
				color: nodeDataArray[i].color,
				source: "{{ url_for('static', filename='img/goal3.PNG') }}",							

				text_color: '{{ sts.color }}',
				name: '{{ goal.title }}',
				status: 'סטאטוס: {{ sts.title }}',
				parent: nodeDataArray[i].key,
			} );
																	
		{% endif %}
	{% endfor %}
				
{% endblock goal_data %}
