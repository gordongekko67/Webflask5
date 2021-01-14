function getData() {
    var canvas = document.getElementById("inputCanvas");
    var imageData = canvas.context.getImageData(0, 0, canvas.width, canvas.height);
    var data = imageData.data;
    var outputData = []
    for(var i = 0; i < data.length; i += 4) {
      var brightness = 0.34 * data[i] + 0.5 * data[i + 1] + 0.16 * data[i + 2];
      outputData.push(brightness);
    }
    $.post( "/postmethod", {
      canvas_data: JSON.stringify(outputData)
    }, function(err, req, resp){
      window.location.href = "/results/"+resp["responseJSON"]["uuid"];
    });
  }