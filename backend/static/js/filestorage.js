$(function () {

  $(".file-upload").click(function () {
    $("#file_upload").click();
  });

  $("#file_upload").fileupload({
    dataType: 'json',
    sequentialUploads: true,

    start: function (e) {
      $(".progress-bar").css({"width": "0%"});
      $(".progress-bar").text("0%");
      $("#upload_progressbar").show();
    },

    stop: function (e) {
      $("#upload_progressbar").hide();
    },

    progressall: function (e, data) {
      var progress = parseInt(data.loaded / data.total * 100, 10);
      var css_str = progress + "%";
      var txt_str = "uploaded " + progress + "%";
      $(".progress-bar").css({"width": css_str});
      $(".progress-bar").text(txt_str);
    },

    done: function (e, data) {
      if (data.result.is_valid) {
        $("#file_list tbody").prepend(
          "<tr><td><a href='" + data.result.url + "'>" + data.result.name + "</a></td></tr>"
        );
        $("#clean_up").addClass("visible").removeClass("invisible");
        $(".in-stock-visible").addClass("visible").removeClass("invisible");
        $(".in-stock-unhide").removeClass("d-none");
      }
    }

  });

});
