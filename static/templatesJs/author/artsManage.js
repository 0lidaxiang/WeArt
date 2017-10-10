jQuery(document).ready(function($) {
  $('#authorFunctionTreeLi').addClass('active');
  $('#authorFunctionTreeUl').addClass('menu-open');
  $('#manageArtsLi').addClass('active');

  $("#example1").DataTable(
    {
      "ajax": '/book/getMyBook/',
      "columns": [
            { "data": "bookName" },
            { "data": "chapterCount" },
            { "data": "status" },
            { "data": "createTime" },
            { "data": "operation" },
        ]
    }
  );
});

function getMainContentData() {
  $.ajax({
    url: '/book/getMyBook/',
    type: 'GET',
    dataType: 'json',
    data: {}
  })
  .done(function(resp) {
    console.log(resp);
    var message = resp.message;
    if (resp.status == "success" && message != null) {
      var trs = "";
      for (var i = 0; i < message.length; i++) {
          var tds = "";
          tds = tds + "<td>" + message[i]["bookName"] + "</td>";
          tds = tds + "<td>" + message[i]["chapterCount"] + "</td>";
          tds = tds + "<td>" + message[i]["createTime"] + "</td>";
          tds = tds + "<td>" + message[i]["status"] + "</td>";
          tds = tds + "<td>" + "<a href=javascript:deleteBook('" + message[i]["idColl"] + "');> deleteBook"  + "</a>" + "</td>";
          trs = trs + "<tr role='row'>" + tds + '</tr>';
      }
      $("#mainContent").replaceWith("  <tbody id = 'mainContent'>" + trs + "</tbody>");
    }
    else if (resp.status == "fail") {
      var obj = "<div class='col-md-12 col-sm-12'><h4>" + resp.message + "</h4></div>";
      $("#mainContent").replaceWith(obj);
    }
    else{
      var obj = "<div class='col-md-12 col-sm-12'><h4>" + resp.message + "</h4></div>";
      $("#mainContent").replaceWith(obj);
    }
  })
  .fail(function(resp) {
    console.log(resp);
  });
}

function deleteBook(idBookArg) {
  // alert("delete: " + idBookArg);
  $.ajax({
    url: '/book/deleteBook/',
    type: 'GET',
    dataType: 'json',
    data: {"idBook" : idBookArg}
  })
  .done(function(resp) {
    console.log(resp);
    var message = resp.message;
    if (resp.status == "success") {
      alert("刪除成功！");
      window.location.reload();
    }
    else if (resp.status == "fail") {
      var obj = "<div class='col-md-12 col-sm-12'><h4>" + resp.statusNumber + " , " + resp.message + "</h4></div>";
      $("#mainContent").replaceWith(obj);
    }
    else{
      var obj = "<div class='col-md-12 col-sm-12'><h4>" + resp.statusNumber + " , " + resp.message + "</h4></div>";
      $("#mainContent").replaceWith(obj);
    }
  })
  .fail(function(resp) {
    console.log(resp);
  });
}
