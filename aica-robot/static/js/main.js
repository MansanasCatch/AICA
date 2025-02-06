$(document).on("click", "#btnListen", function (e) {
  PostSTT();
});

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
      $("#inputText").val(response.speech);
      PostTTS(response.speech) 
    },
  });
}
