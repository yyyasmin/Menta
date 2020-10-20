<!DOCTYPE html>
<html>
<title>W3.CSS</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<body>
<div class="w3-container">

<h2>Accordion Buttons</h2>
<p>You can use any HTML element to open the accordion content. We prefer a button with a w3-block class, because it spans the entire width of its parent element, just like the accordion content (100% width). Remember that buttons in W3.CSS are centered by default. Use the w3-left-align class if you want them left aligned instead. However, you do not have to follow our approach.</p>

<button onclick="myFunction('Demo1')" class="w3-button w3-light-grey">
Normal button</button>

<div id="Demo1" class="w3-hide w3-container w3-light-grey">
  <p>Lorem ipsum...</p>
</div>
<button onclick="myFunction('Demo2')" class="w3-button w3-block w3-left-align w3-green">
Left aligned and full-width</button>

<div id="Demo2" class="w3-hide w3-container">
  <p>Lorem ipsum...</p>
</div>

<button onclick="myFunction('Demo3')" class="w3-btn w3-block w3-red">
Centered and full-width</button>

<div id="Demo3" class="w3-hide w3-container w3-center w3-pale-red">
  <p>Centered content as well!</p>
</div>

</div>
<script>
function myFunction(id) {
  var x = document.getElementById(id);
  if (x.className.indexOf("w3-show") == -1) {
    x.className += " w3-show";
  } else { 
    x.className = x.className.replace(" w3-show", "");
  }
}
</script>

</body>
</html>
