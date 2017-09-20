$(document).ready(function() {
  getRecommendArts();
});

function getRecommendArts() {
  $.ajax({
    url: '/home/getRecommendArts/',
    type: 'GET',
    dataType: 'json',
    data: {"amount": 10}
  })
  .done(function(resp) {
    // console.log(resp);
    if (resp.status == "success") {
      bookAll = resp.message

      var obj = "<div id=‘mainContent’ class='col-md-12 col-sm-12 alert alert-success'>";
      tableObj = "<div class='table-responsive'><table class='table'>" ;
      thObj = "<tr><th>序號</th><th>書ID</th>  <th>書名</th>  <th>作者ID</th> <th>備註</th>  </tr>";
      obj = obj + tableObj + thObj;

      for (var i in bookAll) {
        obj = obj + "<tr><td>" + (i+1) + "</td><td><a href='#'>" + bookAll[i].id + "</a></td><td>" + bookAll[i].name + "</td><td>" + bookAll[i].idAuthor_id + "</td><td></td></tr>";
      }
      obj = obj + "</table></div></div>";

      $("#bookAll").replaceWith(obj);
    }
    else if (resp.status == "fail") {
      var obj = "<div class='box'><div class='box-body' id='mainContent'><div class='col-md-12 col-sm-12'><h4>" + resp.message + "</h4></div></div></div>";
      $("#bookAll").replaceWith(obj);
    }
    else{
      var obj = "<div class='box'><div class='box-body' id='mainContent'><div class='col-md-12 col-sm-12'><h4>" + resp.message + "</h4></div></div></div>";
      $("#bookAll").replaceWith(obj);
    }
  })
  .fail(function(resp) {
    console.log(resp);
  });

}
