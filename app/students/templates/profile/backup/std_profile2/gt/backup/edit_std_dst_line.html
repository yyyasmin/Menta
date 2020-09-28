{% block edit_std_dst_line %}		
	<tr>
	
		<td>{{ std_dst.id }}</td>
				
		<td>{{ std_dst.title }}</td>
		
		<td>{{ std_dst.body }}</td> 
		
		<td>
			<div id="ar_div">
			
				{% for st in std_txts %}
					{% if st.general_txt_id==std_dst.id %}
						<input type="date" style="text-align:center" id="due_date" name="due_date{{ std_dst.id }}" value="{{ st.due_date }}">					
					{% endif %}
				{% endfor %}

			</div>   <!-- ar_div -->
		</td>	
	

		<td>סטאטוס:
			<select class="select" name="sts{{ std_dst.id }}" id="selected_status">	
				{% for sts in statuss %}	
					{% for st in std_txts %}
						{% if st.general_txt_id==std_dst.id %}
							{% if st.status_id==sts.id %}
								<option value="{{ sts.id }}" selected="selected">{{ sts.title }}</option>
							{% else %}
								<option value="{{ sts.id }}">{{ sts.title }}</option>
							{% endif %}
						{% endif %}
					{% endfor %}
				{% endfor %}
			</select>					
		</td>
	
		<td>
			{% set dst_num = std_dst.id * 3 %}	
			<button class="btn btn-success btn-xs" type="submit" name="txt_type_form_button_name" value="{{ dst_num }}">שמור</button>
		</td>
	</tr>
	

	<tr>	
		{% for goal in student_goals %}
			{% if goal in std_dst.children.all() %}
				{% include "./destinations/goals/edit_one_std_dst_goal.html" %}
			{% endif %}
		{% endfor %}
	</tr>
	
	
	<tr>				
		{% for goal in goals_not_of_student %}
			{% include "./destinations/goals/edit_one_std_dst_goal_not_of_std.html" %}
		{% endfor %}
	</tr>	
<!-- FROM https://stackoverflow.com/questions/18091866/background-color-of-selected-option -->

<script>				
$("#color_me").change(function(){
    $("#color_me").attr("color") = $("option:selected", this).attr("color");
});
</script>


{% endblock edit_std_dst_line %}