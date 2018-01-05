$(document).ready(function() {
  getMainContentData();
});

function getMainContentData(idAuthor) {
  var idBook = $("#idBook").val();
  var chapterOrder = $("#chapterOrder").val();

  if (idBook == "") {
    alert("請填寫書籍編號");
    return;
  }

  if (chapterOrder == "") {
    alert("請填寫章節序號");
    return;
  }

  $.ajax({
    url: '/content/showHistory/',
    type: 'GET',
    dataType: 'json',
    data: {"idBook": idBook, "chapterOrder": chapterOrder , "idAuthor": idAuthor}
  })
  .done(function(resp) {
    // console.log(resp);
    $("#idVersion").val(resp.idVersion);
    var content = resp.content;
    if (resp.status == "success" && content != null) {
      var objContent = "<div id='mainContent' class='col-md-12 col-sm-12 alert alert-success'>";
      for (var i = 0; i < content.length; i++) {
          objContent = objContent + content[i] + '<br>';
      }
      objContent = objContent + "</div>";
      $("#mainContent").replaceWith(objContent);

      var authorList = resp.authorList;
      var authorIds = resp.authorIds;
      var objAuthor = "<div id='authorList' class='col-md-12 col-sm-12 alert alert-success'>";
      for (var i = 0; i < authorList.length; i++) {
        objAuthor = objAuthor + "<a class='alink' href='javascript:getMainContentData(" + "\"" + authorIds[i]  + "\"" + ")'>" + authorList[i] + '</a><br>';
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
    getChapterVersionRating();
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

function getChapterVersionRating(idAuthor) {
  var idVersion = $("#idVersion").val();

  $.ajax({
    url: '/voteChapter/getRating/',
    type: 'GET',
    dataType: 'json',
    data: {"idVersion": idVersion}
  })
  .done(function(resp) {
    // console.log(resp);
    if (resp.res == "success") {
      $("#chapterVersionVoteVal").val(resp.message.toFixed(2));
    }
    else if (resp.res == "fail") {
      $("#chapterVersionVoteVal").val(resp.message);
    }
    else{
      $("#chapterVersionVoteVal").val(resp.message);
    }
  })
  .fail(function(resp) {
    console.log(resp);
  });
}
