{% block create_data_tree %}

    // Create the tree model containing TOTAL nodes, with each node having a variable number of children
    function setupDiagram(total) {
		if (total === undefined) total = '{{ student_dsts|length }}';  // total should be the number of destinations
				
		var nodeDataArray = [];
		var i=0;			
		nodeDataArray.push({
		key: i,
		color: go.Brush.randomColor(),
		name: '{{ student.first_name }} {{ student.last_name }}',
		});
		
		i=1;		
	    {% for dest in student_dsts %}  // set the nodes text to students destinations	
{% include "./tree/dst_data.js" %}
			
			nodeDataArray[i].parent = 0;   // all the destinations parent is student
			var j=i+1;
			{% for goal in dest.children.all() if (goal in student_goals) %}  // set the nodes text to destinations goals 	
{% include "./tree/goals_data.js" %}
				
				nodeDataArray[j].parent = nodeDataArray[i].key;				
				var k=j+1;
				{% for todo in goal.children.all() if (todo in student_todos) %}  // set the nodes text to destinations goals 	
{% include "./tree/todos_data.js" %}

					nodeDataArray[k].parent = nodeDataArray[j].key;
					k++; 		
				{% endfor %}  //todos loop			
				j++;
				j=k;
				
			{% endfor %}  //goals loop			
			
			i=j;			
        {% endfor %}  // destinations seting text loop

      myFullDiagram.model = new go.TreeModel(nodeDataArray);
    }	
	
{% endblock create_data_tree %}

	
	