
$(function() {
    $("button").on("click", function() {
	
		console.log("IN function");

		var gt_tag = $("#gt_tag").val();
		
        var firstValue = $("#firstValue").val();
        var secondValue = $("#secondValue").val();
		
        var gt_tag_1 = $("#gt_tag_1").val();
		
        var gt_tag_2 = $("#gt_tag_2").val();
		
        var gt_tag_3 = $("#gt_tag_3").val();
		
        var gt_tag_4 = $("#gt_tag_4").val();
		
        var gt_tag_5 = $("#gt_tag_5").val();
		
        var gt_tag_6 = $("#gt_tag_6").val();
		
        var sub_id = $("#sub_id").text();
		
		console.log("sub_id");
		console.log(sub_id);
		
		console.log("1st");
		console.log(gt_tag_1);
		
		console.log("2nd");
		console.log(gt_tag_2);
		
		console.log("3rd");
		console.log(gt_tag_3);
		
		console.log("4th");
		console.log(gt_tag_4);
		
		
		console.log("5th");
		console.log(gt_tag_5);
		
		
		console.log("6th");
		console.log(gt_tag_6);
		

		$("#gt_tag_1").text(gt_tag_1);
        $("#gt_tag_2").text(gt_tag_2);	
        $("#gt_tag_3").text(gt_tag_3);	
        $("#gt_tag_4").text(gt_tag_4);	
        $("#gt_tag_4").text(gt_tag_5);	
        $("#gt_tag_4").text(gt_tag_6);	

    });
});