$(function(){

    index = 1
    recordlist = [0,0,0,0,0,0]

    initCanvas()
    initStatus()

    var video = document.getElementById('video');
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');

    var tracker = new tracking.ObjectTracker('face');
    tracker.setInitialScale(4);
    tracker.setStepSize(2);
    tracker.setEdgesDensity(0.1);

    var trackTask = tracking.track('#video', tracker, { camera: true });
    tracker.on('track', function(event) {
        context.clearRect(0, 0, canvas.width, canvas.height);
        if(event.data.length ==0){

        }else{
            event.data.forEach(function(rect) {
                context.strokeStyle = '#F5A433';
                context.lineWidth = 2;
                context.strokeRect(rect.x, rect.y, rect.width, rect.height);

                if(recordlist[index-1] == 0){
                    var canvas_temp_main = document.getElementById('temp');
                    var temp_main = canvas_temp_main.getContext('2d');
                    temp_main.drawImage(video, 0, 0, canvas_temp_main.width, canvas_temp_main.height);
                    
                    var canvas_temp = document.getElementById('canvas-temp' + index.toString());
                    var temp = canvas_temp.getContext('2d');
                    temp.drawImage(canvas_temp_main, rect.x-parseInt((canvas_temp.width - rect.width)*0.5)+20, rect.y-parseInt((canvas_temp.height - rect.height)*0.7), canvas_temp.width-40, canvas_temp.height, 0, 0, canvas_temp.width, canvas_temp.height);

                    // var canvas_temp = document.getElementById('canvas-temp' + index.toString());
                    // var targetctxImageData = canvas_temp_main.getContext('2d').getImageData(rect.x-parseInt((canvas_temp.width - rect.width)*0.5), rect.y-parseInt((canvas_temp.height - rect.height)*0.7), canvas_temp.width, canvas_temp.height);
                    // var ctx = canvas_temp.getContext('2d');
                    // ctx.putImageData(targetctxImageData, 0, 0);
                }
            });
        }  
    });
})

function initCanvas(){
    var canvasContainer = document.getElementById('canvas-container');
    width = parseInt(canvasContainer.offsetWidth*0.9) - 2
    height = parseInt(canvasContainer.offsetHeight*0.9) - 2

    resizeCanvas('canvas', width, height)
    resizeCanvas('temp', width, height)
    resizeVideo('video', width, height)

    var canvasTempContainer = document.getElementById('canvas-temp-container1');
    width = canvasTempContainer.offsetWidth - 4;
    height = canvasTempContainer.offsetHeight - 4;

    resizeCanvas('canvas-temp1', width, height, '#eeeeee')
    resizeCanvas('canvas-temp2', width, height, '#eeeeee')
    resizeCanvas('canvas-temp3', width, height, '#eeeeee')
    resizeCanvas('canvas-temp4', width, height, '#eeeeee')
    resizeCanvas('canvas-temp5', width, height, '#eeeeee')
    resizeCanvas('canvas-temp6', width, height, '#eeeeee')
}

function resizeCanvas(ids, width, height, color=null){

    var ctx = document.getElementById(ids).getContext('2d');
    ctx.canvas.width = width;
    ctx.canvas.height = height;
    if(color!=null){
        ctx.rect(0,0,width,height);
        ctx.fillStyle = color;
        ctx.fill();
    }
}

function resizeVideo(ids, width, height){
    var video = document.getElementById(ids);
    video.width = width;
    video.height = height;
}

function initStatus(){
    $("#preview").attr("disabled","true");
    $("#canvas-temp-container" + index.toString()).addClass("bottom_main");
}

function changeStatus(){

    if(index==1){
        $("#preview").attr("disabled","true");
    }else if(index==6){
        $("#next").attr("disabled","true");
    }else{
        $("#preview").attr("disabled",false);
        $("#next").attr("disabled",false);
    }

    if(recordlist[index-1] == 1){
        $("#qxok").removeClass("btn-info");
        $("#qxok").addClass("btn-warning");
        $("#qxok").text('重新拍摄');
    }else{
        $("#qxok").removeClass("btn-warning");
        $("#qxok").addClass("btn-info");
        $("#qxok").text('拍摄');
    }

    $("#canvas-temp-container" + index.toString()).addClass("bottom_main");
    $("#canvas-temp-container" + index.toString()).removeClass("bottom_normal");
} 

function preview(){
    $("#canvas-temp-container" + index.toString()).removeClass("bottom_main");
    $("#canvas-temp-container" + index.toString()).addClass("bottom_normal");
    index = index - 1
    changeStatus()
}

function next(){
    $("#canvas-temp-container" + index.toString()).removeClass("bottom_main");
    $("#canvas-temp-container" + index.toString()).addClass("bottom_normal");
    index = index + 1
    changeStatus()
}

function qxok(){
    if(recordlist[index-1] == 0){
        $("#canvas-temp-container" + index.toString()).removeClass("bottom_main");
        $("#canvas-temp-container" + index.toString()).addClass("bottom_normal");
        recordlist[index-1] = 1
        index = index + 1
    }else{
        recordlist[index-1] = 0
    }
    changeStatus()
}

function dataURItoBlob (base64Data) {
    var byteString;
    if (base64Data.split(',')[0].indexOf('base64') >= 0)
        byteString = atob(base64Data.split(',')[1]);
    else
        byteString = unescape(base64Data.split(',')[1]);
    var mimeString = base64Data.split(',')[0].split(':')[1].split(';')[0];
    var ia = new Uint8Array(byteString.length);
    for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    return new Blob([ia], {type: mimeString});
}

function submitData(){

    for(var i=0;i<6;i++){
        if(recordlist[i] == 0){
            alert('第'+i.toString()+'张照片未拍摄')
            return true;
        }
    }

    var formData = new FormData();
    for(var i=0;i<6;i++){
        var canvas_temp = document.getElementById('canvas-temp' + (i+1).toString());
        var base64Data = canvas_temp.toDataURL("image/png", 1.0);
        var blob = dataURItoBlob(base64Data);
        formData.append('file[]', blob);
    }
    formData.append('username', $('#username').val())

    $.ajax({
        type: 'POST',
        url: "../api/v1/uploadface/",
        data: formData,
        async: true,
        contentType: false,
        processData: false,
        success: function(dataset){
            document.getElementById('info').innerHTML = dataset['info']

            $('#myModal').modal('show');
            setTimeout(function(){
                $("#myModal").modal("hide")
            },5000);
        },
        error: function(){
            alert('请求错误！')

            $('#myModal').modal('show');
            setTimeout(function(){
                $("#myModal").modal("hide")
            },5000);
        }
    })
}