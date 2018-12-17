$(function(){

    SUBSTATUS = false

    var video = document.getElementById('video');
    var canvas = document.getElementById('canvas');
    var canvas_temp = document.getElementById('canvas-temp');

    var context = canvas.getContext('2d');
    var temp = canvas_temp.getContext('2d');

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
                temp.drawImage(video, 0, 0, canvas.width, canvas.height);

                var canvas_submit = document.getElementById('canvas-sub');
                var targetctxImageData = canvas_temp.getContext('2d').getImageData(rect.x-parseInt((canvas_submit.width - rect.width)*0.5), rect.y-parseInt((canvas_submit.height - rect.height)*0.7), canvas_submit.width, canvas_submit.height);

                var ctx = canvas_submit.getContext('2d');
                ctx.putImageData(targetctxImageData, 0, 0);

                var base64Data = canvas_submit.toDataURL("image/png", 1.0);
                var blob = dataURItoBlob(base64Data);
                submitImg(blob);

            });
        }  
    });
})

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

function submitImg(blob){
    if(!SUBSTATUS){

        SUBSTATUS = true

        var formData = new FormData();
        formData.append('img', blob);

        $.ajax({
            type: 'POST',
            url: "../api/v1/imagelogin/",
            data: formData,
            async: true,
            contentType: false,
            processData: false,
            success: function(dataset){
                console.log(dataset)
                SUBSTATUS = false
            },
            error: function(){
                alert('请求错误！')
            }
        })
    }
}