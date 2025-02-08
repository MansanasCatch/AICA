$(document).ready(function () {
  PostSTT();
})

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
