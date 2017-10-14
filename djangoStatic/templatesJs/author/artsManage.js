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

function deleteBook(idBookArg) {
  $.ajax({
    url: '/book/deleteBook/',
    type: 'GET',
    dataType: 'json',
    data: {"idBook" : idBookArg}
  })
  .done(function(resp) {
    // console.log(resp);
    var message = resp.message;
    if (resp.res == "success") {
      alert("刪除成功！");
      window.location.reload();
    }
    else if (resp.res == "fail") {
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
