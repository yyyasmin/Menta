{% block todos_data %}
	
	{% for std_todo in std_txts if ( todo.id == std_todo.general_txt_id ) %}
			
		{% for sts in statuss if (sts.id == std_todo.status_id) %}
						
				nodeDataArray.push(
				{
					key: k,
					color: nodeDataArray[i].color,
					source: "{{ url_for('static', filename='img/mission1.PNG') }}",							
					text_color: '{{ sts.color }}',
					name: '{{ todo.title }}',
					status: 'סטאטוס: {{ sts.title }}',	
				} );
														
		{% endfor %}
		
	{% endfor %}
		
{% endblock todos_data %}

