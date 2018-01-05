$(document).ready(function() {
  getRecommendArts();
});

function getRecommendArts() {
  $.ajax({
    url: '/recommend/getRecommendArts/',
    type: 'GET',
    dataType: 'json',
    data: {"amount": 10}
  })
  .done(function(resp) {
    // console.log(resp);
    if (resp.status == "success") {
      bookAll = resp.message

      var obj = "<div id='bookAll' class='col-md-12 col-sm-12 alert'>";
      tableObj = "<div class='table-responsive'><table class='table'>" ;
      thObj = "<tr><th>序號</th>  <th>書名</th>  <th>作者昵稱</th> <th>章節數量</th>  </tr>";
      obj = obj + tableObj + thObj;

      var lineNumber = 0;
      for (var i in bookAll) {
        lineNumber = parseInt(i) + 1;
        obj = obj + "<tr><td>" + lineNumber + "</td><td style='color: red;'><a class='alink' href='/chapter/bookChapter/?idBook=" + bookAll[i].id + "&bookName=" + bookAll[i].name + "'>" + bookAll[i].name + "</a></td>" +  "<td>" + bookAll[i].author_name + "</td><td> " + bookAll[i].chapterCount  + "</td></tr>";
      }
      obj = obj + "</table></div></div>";

      $("#bookAll").replaceWith(obj);
    }
    else if (resp.status == "fail") {
      var obj = "<div class='box'><div class='box-body' id='bookAll'><div class='col-md-12 col-sm-12'><h4>" + resp.message + "</h4></div></div></div>";
      $("#bookAll").replaceWith(obj);
    }
    else{
      var obj = "<div class='box'><div class='box-body' id='bookAll'><div class='col-md-12 col-sm-12'><h4>" + resp.message + "</h4></div></div></div>";
      $("#bookAll").replaceWith(obj);
    }
  })
  .fail(function(resp) {
    console.log(resp);
  });
}
