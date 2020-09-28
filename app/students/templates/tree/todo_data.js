{% block todo_data %}

	{% for sts in statuss %}
		{% if todo.is_parent_of(sts) %}
			nodeDataArray.push({
				key: k,
				color: nodeDataArray[i].color,
				source: "{{ url_for('static', filename='img/mission2.PNG') }}",							

				text_color: '{{ sts.color }}',
				name: '{{ todo.title }}',
				status: 'סטאטוס: {{ sts.title }}',
				parent: nodeDataArray[j].key,
			},
			);														
		{% endif %}
	{% endfor %}
				
{% endblock todo_data %}
