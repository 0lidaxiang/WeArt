jQuery(document).ready(function($) {
  $('#authorFunctionTreeLi').addClass('active');
  $('#authorFunctionTreeUl').addClass('menu-open');
  $('#createNewBookLi').addClass('active');
});

function createABook() {
  var bookName = $('[name="newBookName"]').val();

  $.ajax({
      url: '/book/createABook/',
      type: 'GET',
      dataType: 'json',
      data: {
        "newBookName" : bookName,
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
