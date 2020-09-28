{%block set_diagram_data %}	

    // Create the tree model containing TOTAL nodes, with each node having a variable number of children
    function setupDiagram(total) {

		if (total === undefined) total = '{{ total_gts }}';  // total should be the number of destinations
		var nodeDataArray = [];
		var i=0;			
		nodeDataArray.push({
		key: i,
		color: go.Brush.randomColor(),
		name: '{{ student.first_name }} {{ student.last_name }}',
		});
				
		i=1;		
	    {% for dest in student_dsts  %}  // DESTINATIONS			
			{% include "./tree/dst_data.js" %}
			
			nodeDataArray[i].parent = 0;   // all the destinations parent is student
					
			var j=i+1;

		{% for goal in student_goals if (dest.is_parent_of(goal) ) %}  // GOALS		
			{% include "./tree/goal_data.js" %}
			
				nodeDataArray[j].parent = nodeDataArray[i].key;				
				var k=j+1;
				
					{% for todo in student_todos if ( goal.is_parent_of(todo) ) %}  // TODOS	
						
						{% include "./tree/todo_data.js" %}

						nodeDataArray[k].parent = nodeDataArray[j].key;
						k++; 		
					{% endfor %}  //TODOS		
				j++;
				j=k;
			{% endfor %}  //GOALS		
			
			i=j;			
        {% endfor %}  // DESTINATIONS

      myFullDiagram.model = new go.TreeModel(nodeDataArray);
    }
	
	
{%block set_diagram_data %}	
