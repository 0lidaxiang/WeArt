jQuery(document).ready(function($) {
  $('#authorFunctionTreeLi').addClass('active');
  $('#authorFunctionTreeUl').addClass('menu-open');
  $('#createChaptersLi').addClass('active');
});

function createAChapter() {
  var bookName = $('[name="bookname"]').val();
  var chapterName = $('[name="chapterName"]').val();
  var chapterOrder = $('[name="chapterOrder"]').val();

  $.ajax({
      url: '/chapter/createAChapter/',
      type: 'GET',
      dataType: 'json',
      data: {
        "bookName" : bookName,
        "chapterName" : chapterName,
        "chapterOrder" : chapterOrder,
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
