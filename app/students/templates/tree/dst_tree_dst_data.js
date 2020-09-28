{% block dst_data_3 %}

			console.log(" INN tree/backup/dst_data_3.js");

			console.log({{ dest.id }});			
		
			nodeDataArray.push({
				key: '{{ dest.id }}',
				parent: 0, 
				color: '{{ dest.title_color }}',
				source: "{{ url_for('static', filename='img/goal.png') }}",
				name: '{{ dest.title }}',
				
			} );
																	
			
{% endblock dst_data_3 %}
