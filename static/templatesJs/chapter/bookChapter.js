$(document).ready(function() {
  getChapterData();
});

function getChapterData() {
  var idBook = $("#idBook").val();
  var bookName = $("#bookName").val();

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
      thObj = "<tr>  <th>章節序號</th> <th>章節名稱</th>  <th>書名</th>  </tr>";
      obj = obj + tableObj + thObj;

      for (var i in allChapter) {
        lineNumber = parseInt(i) + 1
        obj = obj + "<tr>" +  "<td>" + allChapter[i].chapterOrder + "</td>"  + "<td><a class='alink'  href='/content/chapterContent/?idBook=" + idBook + "&chapterOrder=" + allChapter[i].chapterOrder + "&chapterName=" + allChapter[i].name + "&bookName=" + bookName + "'>" + allChapter[i].name + "</a></td><td>" +  allChapter[i].book_name + "</td></tr>";
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
