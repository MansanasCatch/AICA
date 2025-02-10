$(document).ready(function () {
  PostSTT();
  setInterval(GetTrack, 1000);
})

var servoPosX = null;
var servoPosY = null;
function PostTTS(inputText) {
  $.ajax({
    type: "post",
    url: "/speech_start",
    data: { inputText: inputText },
    success: function (response) {
        PostSTT()
    },
  });
}

function GetTrack() {
  $.ajax({
    type: "post",
    url: "/get_track",
    success: function (response) {
        var x = parseInt(response.render_url[0])
        var y = parseInt(response.render_url[1])
        console.log(x + " " + y)
        console.log(servoPosX + " " + servoPosY)
        if(x != servoPosX && y !=servoPosY)
        {
            servoPosX = x;
            servoPosY = y;
            SendTrack()
        }
    },
  });
}

function SendTrack() {
  $.ajax({
    type: "post",
    url: "/send_track",
    success: function (response) {
        console.log("Sent")
    },
  });
}

function PostSTT() {
  $.ajax({
    type: "post",
    url: "/listen_start",
    success: function (response) {
      if(response.role == "AICA"){
        $("#textContainer").prepend(`<p id="textDisplay"><span id="role" style="color:#EC2C40">${response.role}:</span> <span id="text-return">${response.speech}</span></p>`)
        PostTTS(response.speech) 
      }else if(response.role == "User") {
        $("#textContainer").prepend(`<p id="textDisplay"><span id="role" style="color:#6A2D94">${response.role}:</span> <span id="text-return">${response.speech}</span></p>`)
        PostTTS(`Did you say ${response.speech}`) 
      }else{
        $("#textContainer").empty();
        PostSTT()
      }
    },
  });
}
