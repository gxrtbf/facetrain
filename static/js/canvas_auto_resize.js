var CanvasAutoResize = {
  draw: function() {
    var ctx = document.getElementById('canvas').getContext('2d');
    var canvasContainer = document.getElementById('canvas-container');
    ctx.canvas.width  = canvasContainer.offsetWidth-2;
    ctx.canvas.height = canvasContainer.offsetHeight-2;
  },
 
  initialize: function(){
    var self = CanvasAutoResize;
    self.draw();
    $(window).on('resize', function(event){
      self.draw();
    });
  }
}
 
$(function(argument) {
  CanvasAutoResize.initialize();
});
