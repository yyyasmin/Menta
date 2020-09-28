{% block set_dst_data %}	

 	
    // Create the tree model containing TOTAL nodes, with each node having a variable number of children
    function setupDiagram(total) {
	
	
		if (total === undefined) total = '{{ total_gts }}';  // total should be the number of destinations
		var nodeDataArray = [];
		var i=0;	
					
		{% for sts in statuss if (sts.id == dest.status_id) %}
		
				wondow.alert(dest);
				
				nodeDataArray.push({
					key: i,
					color: go.Brush.randomColor(),
					color2: '{{ sts.color }}',
					name: '{{ dest.title }}',
					status: 'סטאטוס: {{ sts.title }}',	
				},
				);	
									
		{% endfor %}
		
		i=1;		
		{% for goal in dst_goals if (dest.is_parent_of(goal) ) %}  // GOALS		
			
			window.alert(goal);
			
			{% include "./tree/goal_data.js" %}
				
			nodeDataArray[i].parent = 0;   // all the destinations parent is student
					
			var j=i+1;

			{% for todo in dst_todos if ( goal.is_parent_of(todo) ) %}  // TODOS	
				
				window.alert(todo);
				
				{% include "./tree/todo_data.js" %}

				nodeDataArray[j].parent = nodeDataArray[i].key;				
				var k=j+1;
				
					for (forth_level_idx = 1; forth_level_idx < 6; i++) {  // 4th-LEVEL	
						
						window.alert("4th level");
						window.alert(forth_level_idx);

						nodeDataArray[k].parent = nodeDataArray[j].key;
						k++; 		
					}  //4th-LEVEL		
				j++;
				j=k;
			{% endfor %}  //TODOS		
			
			i=j;			
        {% endfor %}  // DESTINATIONS
		

    }
			
	
{% endblock set_dst_data %}	
