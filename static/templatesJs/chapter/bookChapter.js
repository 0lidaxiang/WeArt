$(document).ready(function() {
  getChapterData();
});

function getChapterData() {
  var idBook = $("#idBook").val();
  $.ajax({
    url: '/chapter/getChapter/',
    type: 'GET',
    dataType: 'json',
    data: {"idBook": idBook}
  })
  .done(function(resp) {
    // console.log(resp);
    if (resp.status == "success") {
      allChapter = resp.message

      var obj = "<div id='allChapter' class='col-md-12 col-sm-12 alert alert-success'>";
      tableObj = "<div class='table-responsive'><table class='table'>" ;
      thObj = "<tr><th>序號</th><th>章節ID</th>  <th>章節名稱</th>  <th>章節序號</th> <th>書ID</th>  </tr>";
      obj = obj + tableObj + thObj;

      for (var i in allChapter) {
        obj = obj + "<tr><td>" + (i+1) + "</td><td><a href='/chapter/bookChapter/?idBook= " + allChapter[i].id + "'>" + allChapter[i].id + "</a></td><td>" + allChapter[i].name + "</td><td>" + allChapter[i].chapterOrder + "</td><td>" + allChapter[i].idBook_id + "</td></tr>";
      }
      obj = obj + "</table></div></div>";

      $("#allChapter").replaceWith(obj);
    }
    else if (resp.status == "fail") {
      var obj = "<div class='box'><div class='box-body' id='allChapter'><div class='col-md-12 col-sm-12'><h4>" + resp.message + "</h4></div></div></div>";
      $("#allChapter").replaceWith(obj);
    }
    else{
      var obj = "<div class='box'><div class='box-body' id='allChapter'><div class='col-md-12 col-sm-12'><h4>" + resp.message + "</h4></div></div></div>";
      $("#allChapter").replaceWith(obj);
    }
  })
  .fail(function(resp) {
    console.log(resp);
  });
}
