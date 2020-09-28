{% block dst_data %}
		
			{% for sts in statuss %}
				{% if dest.is_parent_of(sts) %}
					nodeDataArray.push({
						
						key: i,
						color: go.Brush.randomColor(),
						source: "{{ url_for('static', filename='img/goal.png') }}",
						text_color: '{{ sts.color }}',
						name: '{{ dest.title }}',
						status: 'סטאטוס: {{ sts.title }}',
						parent: 0,
						
					} );
																			
				{% endif %}
			{% endfor %}
			
			console.log("In dst_dsta.js");
			console.log("i");
			console.log(i);
			console.log("nodeDataArray[i]");
			console.log(nodeDataArray[i]);
			
{% endblock dst_data %}
