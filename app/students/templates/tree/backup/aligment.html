// A component for placing text on the canvas including alignment and padding.
// Includes: background color & opacity, 4-point padding, percent fill, alignment
// Created as a component of a Gantt drawing project.
var textOut = function(parent, userOpts){
  var options = {
    pos: {x: 0, y: 0, width: 0, height: 0},
    padding: [0, 0, 0, 0],    
    font: {name: 'Arial', size: '12pt', color: '#ccc'},  
    text: '',
    align: 'left',
    verticalAlign: 'top',
    textDecoration: 'underline',
    lineHeight: 1,
    fill: '',
    fillOpacity: 1,
    
    // following provide the background percentage complete indicator
    percentFill: 'blue',
    percentOpacity: 0.2,
    percent: 0,
    showRect: false
  }
  
  options = $.extend({}, options, userOpts); // merge the input  options with the options.
  console.log(JSON.stringify(options))

  // if a fill is required then output the node
  if (options.fill.length > 0){
    var r1 = new Konva.Rect({
      x: options.pos.x,
      y: options.pos.y,
      width: options.pos.width,
      height: options.pos.height,
      fill: options.fill,
      opacity: options.fillOpacity
    })
    parent.add(r1)
  }
  
  // If showrect is set then show a bounding rect
  if (options.showRect){
    var r2 = new Konva.Rect({
      x: options.pos.x + options.padding[3],
      y: options.pos.y + options.padding[0],
      width: (options.pos.width - (options.padding[3] + options.padding[1])),
      height: (options.pos.height - (options.padding[0] + options.padding[2])),
      stroke: 'cyan',
      strokeWidth: 2
    })
    parent.add(r2)
  }

  // if the percentage marker is required then output the node
  if (options.percent > 0){
    
    var bar = new Konva.Rect({
      x: options.pos.x,
      y: options.pos.y,
      width: ((parseInt(options.percent) /100) * options.pos.width),
      height: options.pos.height,
      fill: options.percentFill,
      opacity: options.percentOpacity
    })
    parent.add(bar)    
  }
  
  
  // we now output the final text node
  var node = new Konva.Text({
      x: options.pos.x + options.padding[3],
      y: options.pos.y + options.padding[0],
      width: (options.pos.width - (options.padding[3] + options.padding[1])),
      height: (options.pos.height - (options.padding[0] + options.padding[2])),
      fontFamily: options.font.name,
      fontSize: options.font.size,
      fill: options.font.color,
      text: options.text,
      align: options.align,
      verticalAlign: options.verticalAlign,
      textDecoration: options.textDecoration,
      lineHeight: options.lineHeight
  })
  parent.add(node)
}
// end of component.


// stage and layer are just setting the scene.
var stage = new Konva.Stage({
  container: 'canvas-container',
  width: 650,
  height: 300
});

var layer = new Konva.Layer();
stage.add(layer);

var group1 = new Konva.Group({})
layer.add(group1)

// This JS object defines the params for the drawing of the text in this instance.
// Param pos gives the target rect, padding gives the padding withing the target rect and follows css convention.
var data = {
    pos: {x: 25, y: 10, width: 200, height: 20},
    padding: [2, 2, 2, 6],
    font: {name: 'Arial', size: '12', color: '#333'},
    text: '50%',
    align: 'center',
    verticalAlign: 'bottom',
    lineHeight: 1,
    textDecoration: '',
    percent: 50,
    fill: 'red'
}

// a 'cell' is drawn to give us a sense of how the text is placed
var cell1 = new Konva.Rect({
   x: data.pos.x, y: data.pos.y, width: data.pos.width, height: data.pos.height, draggable: true, stroke: '#666', strokeWidth: 2
  })
group1.add(cell1);

// Now we override the data params as needed.
data.text = "Create wire frames";
data.percent = 0;
data.align = 'left';
data.fillOpacity= 0.2;

var t1 = new textOut(layer, data)

// Prepare another cell
var group2 = new Konva.Group({})
layer.add(group2)

// Now we override the data params as needed.
data.pos.x = data.pos.x + data.pos.width;
data.pos.width = 80;
data.align = 'center';
data.padding = [2, 2, 2, 2],
data.fillOpacity = 0;

data.text = "50%";
data.percent = 50;
var cell2 = new Konva.Rect({
   x: data.pos.x, y: data.pos.y, width: data.pos.width, height: data.pos.height, draggable: true, stroke: '#666', strokeWidth: 2
  })
group2.add(cell2);

var t2 = new textOut(group2, data)
layer.draw();

layer.draw()
stage.draw()
