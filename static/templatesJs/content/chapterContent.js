$(document).ready(function() {
  getContentData();
  getotherVersionContentData();
});

function getContentData() {
  var idBook = $("#idBook").val();
  var chapterOrder = $("#chapterOrder").val();

  $.ajax({
    url: '/content/readerGetContent',
    type: 'GET',
    dataType: 'json',
    data: {"idBook": idBook, "chapterOrder": chapterOrder}
  })
  .done(function(resp) {
    // console.log(resp);
    if (resp.status == "success") {
      mainContent = resp.message

      var obj = "<div id='mainContent' class='col-md-12 col-sm-12 alert alert-success'>";
      for (var i = 0; i < mainContent.length; i++) {
        obj = obj + mainContent[i] + '<br>';
      }
      obj = obj + "</div>";

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

function getotherVersionContentData() {
  var idBook = $("#idBook").val();
  var chapterOrder = $("#chapterOrder").val();

  $.ajax({
    url: '/content/showHistory/',
    type: 'GET',
    dataType: 'json',
    data: {"idBook": idBook, "chapterOrder": chapterOrder}
  })
  .done(function(resp) {
    console.log(resp);
    if (resp.status == "success") {
      mainContent = resp.history
      var obj = "<div id='otherVersionContent' class='col-md-12 col-sm-12 alert alert-success'>";
      for (var i = 0; i < mainContent.length; i++) {
        obj = obj + mainContent[i] + '<br>';
      }
      obj = obj + "</div>";
      $("#otherVersionContent").replaceWith(obj);

      mainContent = resp.logs
      var obj = "<div id='logsContent' class='col-md-12 col-sm-12 alert alert-success'>";
      for (var i = 0; i < mainContent.length; i++) {
        obj = obj + mainContent[i] + '<br>';
      }
      obj = obj + "</div>";
      $("#logsContent").replaceWith(obj);
    }
    else if (resp.status == "fail") {
      var obj = "<div class='box'><div class='box-body' id='logsContent'><div class='col-md-12 col-sm-12'><h4>" + resp.message + "</h4></div></div></div>";
      $("#mainContent").replaceWith(obj);
    }
    else{
      var obj = "<div class='box'><div class='box-body' id='logsContent'><div class='col-md-12 col-sm-12'><h4>" + resp.message + "</h4></div></div></div>";
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
