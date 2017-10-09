$(document).ready(function() {
  getMainContentData();
});

function getMainContentData(idAuthor) {
  var idBook = $("#idBook").val();
  var chapterOrder = $("#chapterOrder").val();

  $.ajax({
    url: '/content/showHistory/',
    type: 'GET',
    dataType: 'json',
    data: {"idBook": idBook, "chapterOrder": chapterOrder , "idAuthor": idAuthor}
  })
  .done(function(resp) {
    // console.log(resp);
    var content = resp.content;
    if (resp.status == "success" && content != null) {
      var objContent = "<div id='mainContent' class='col-md-12 col-sm-12 alert alert-success'>";
      for (var i = 0; i < content.length; i++) {
          objContent = objContent + content[i] + '<br>';
      }
      objContent = objContent + "</div>";
      $("#mainContent").replaceWith(objContent);

      var authorList = resp.authorList;
      var objAuthor = "<div id='authorList' class='col-md-12 col-sm-12 alert alert-success'>";
      for (var i = 0; i < authorList.length; i++) {
        objAuthor = objAuthor + "<a href='javascript:getMainContentData(" + "\"" + authorList[i]  + "\"" + ")'>" + authorList[i] + '</a><br>';
      }
      objAuthor = objAuthor + "</div>";
      $("#authorList").replaceWith(objAuthor);
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

function writeMyVersion() {
  var lastUrl = window.location.href;
  var idBook = $("#idBook").val();

  $.ajax({
    url: '/content/readerWriteAContentHtml/',
    type: 'GET',
    dataType: 'json',
    data: {"idBook": idBook, "lastUrl": lastUrl}
  })
  .done(function(resp) {
    // console.log(resp);
    if (resp.status == "success") {
      window.location.href = resp.message
    }
    else if (resp.status == "fail") {
      alert(resp.message);
    }
    else{
      alert(resp.message);
    }
  })
  .fail(function(resp) {
    console.log(resp);
  });
}
