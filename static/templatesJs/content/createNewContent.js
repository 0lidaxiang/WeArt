jQuery(document).ready(function($) {
  $('#authorFunctionTreeLi').addClass('active');
  $('#authorFunctionTreeUl').addClass('menu-open');
  $('#createNewContentLi').addClass('active');
});

function submitContent() {
  var bookName = $("#bookName").val();
  var chapterOrder = $("#chapterOrder").val();
  var commitContent = $("#commitContent").val();
  var content = $("#content").val();

  $.ajax({
      url: '/content/createAContent/',
      type: 'GET',
      dataType: 'json',
      data: {
        "bookName" : bookName,
        "chapterOrder" : chapterOrder,
        "commitContent" : commitContent,
        "content" : content,
      }
    })
    .done(function(resp) {
      // console.log(resp);
      if (resp.status == "success") {
        var obj = "<div class='box'><div class='box-body' id='mainContent'><div class='col-md-12 col-sm-12'><h4>" + resp.message + "</h4></div></div></div>";
        $("#mainContent").replaceWith(obj);
      }
      else if (resp.status == "fail") {
        var obj = "<div class='box'><div class='box-body' id='mainContent'><div class='col-md-12 col-sm-12'><h4>" + resp.message + "</h4></div></div></div>";
        $("#mainContent").replaceWith(obj);
      }
      else{
        var obj = "<div class='box'><div class='box-body' id='mainContent'><div class='col-md-12 col-sm-12'><h4>" + resp.message + "</h4></div></div></div>";
        $("#mainContent").replaceWith(obj);
      }
    })
    .fail(function(resp) {
      console.log(resp);
    });
}

function getContent() {
  var bookName = $("#bookName").val();
  var chapterOrder = $("#chapterOrder").val();

  $.ajax({
    url: '/content/getContent/',
    type: 'POST',
    dataType: 'json',
    data: {
      "bookName": bookName,
      "chapterOrder": chapterOrder,
   }
  })
  .done(function(resp) {
    var tempstr = "";
    for (var i = 0; i < resp.length; i++) {
      tempstr = tempstr + resp[i];
    }
    console.log(tempstr);
    $("#content").val(tempstr);
  })
  .fail(function() {
    console.log("error");
  })
  .always(function() {
    console.log("complete");
  });

}
