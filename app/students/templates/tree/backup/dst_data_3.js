{% block dst_data_3 %}

			console.log(" INN tree/backup/dst_data_3.js");

			console.log("{{ DDDD dest.id }}");
			console.log( {{ dest.id }} );
			console.log("{{ TTT dest.title }}");
			console.log( {{ dest.title }} );

				
			console.log("IN FOR STS IF DST...");

			nodeDataArray.push({
				key: '{{ dest.id }}',
				parent: 0, 
				color: '{{ dest.color_txt }}',
				source: "{{ url_for('static', filename='img/goal.PNG') }}",
				text_color: '{{ sts.color }}',
				name: '{{ dest.title }}',
				
			} );
																			
			
{% endblock dst_data_3 %}
