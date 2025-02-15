$(document).ready(function () {
  Is_human_detected();
  //setInterval(GetTrack, 1000);
})

function SendAIRequest(contMessage) {
  $.ajax({
    type: "post",
    url: "/SendAIRequest",
    data:{contMessage:contMessage},
    success: function (response) {
      $("#textContainer").prepend(`<p id="textDisplay"><span id="role" style="color:#EC2C40">AICA:</span> <span id="text-return">${response.content}</span></p>`)
      PostTTS(response.content)
    },
  });
}

var globalis_human_detected= false;
function Is_human_detected() {
  $.ajax({
    type: "post",
    url: "/is_human_detected",
    success: function (response) {
      if (response.is_human_detected) {
        PostSTT();
      } else {
        setTimeout(Is_human_detected, 3000);
      }
    },
  });
}

var servoPosX = null;
var servoPosY = null;
function PostTTS(inputText) {
  $.ajax({
    type: "post",
    url: "/speech_start",
    data: { inputText: inputText },
    success: function (response) {
      Is_human_detected()
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
      if (x != servoPosX && y != servoPosY) {
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
      if(response.speech.indexOf("hello") != -1){
        SendAIRequest("hello");
      }else{
        if (response.role == "AICA") {
          if(response.speech != null && response.speech != ""){
            $("#textContainer").prepend(`<p id="textDisplay"><span id="role" style="color:#EC2C40">${response.role}:</span> <span id="text-return">${response.speech}</span></p>`)
            PostTTS(response.speech)
          }else {
            $("#textContainer").empty();
            Is_human_detected();
          }
        } else if (response.role == "User") {
          if(response.speech != null && response.speech != ""){
            $("#textContainer").prepend(`<p id="textDisplay"><span id="role" style="color:#6A2D94">${response.role}:</span> <span id="text-return">${response.speech}</span></p>`)
          }
          SendAIRequest(response.speech);
        } else {
          $("#textContainer").empty();
          Is_human_detected();
        }
      }
    },
  });
}
