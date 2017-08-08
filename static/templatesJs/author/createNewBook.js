jQuery(document).ready(function($) {
  $('#authorFunctionTreeLi').addClass('active');
  $('#authorFunctionTreeUl').addClass('menu-open');
  $('#createNewBookLi').addClass('active');
});

function createABook() {
  var bookName = $('[name="newBookName"]').val();
  console.log(bookName);

  $.ajax({
      url: '/author/createABook/',
      type: 'GET',
      dataType: 'json',
      data: {
        "newBookName" : bookName,
      }
    })
    .done(function(resp) {
      console.log(resp);
      // updateHtml(resp);
    })
    .fail(function(resp) {
      console.log(resp);
    });
}

// function  updateHtml(resp){
//   if (resp.status == "success") {
//     if (!resp.isAuthor) {
//       var obj = "<div class='box'><div class='box-body' id='mainContent'><div class='col-md-1 col-sm-12'><input name='closeFunctionBtn' type='button' class='btn btn-success pull-left' value='啟用' onclick='modifyAuthorStatus()' /><input type='hidden' id='nextAuthorStatus' value='acitve'/></div><div class='col-md-6 col-sm-12'><h4>您尚未啟用作者賬號功能,啓用後才可以查看作者專區</h4></div></div></div>";
//       $("#mainContent").replaceWith(obj);
//     } else if (resp.isAuthor) {
//       var obj = "<div class='box'><div class='box-body' id='mainContent'><div class='col-md-1 col-sm-12'><input name='closeFunctionBtn' type='button' ";
//
//       if (resp.authorStatus == "active") {
//         obj = obj + "class='btn btn-danger pull-left' value='關閉' onclick='modifyAuthorStatus()' /><input type='hidden' id='nextAuthorStatus' value='inactive'/></div><div class='col-md-3 col-sm-12'><h4>您已經啟用作者賬號功能</h4></div></div></div>";
//       } else if (resp.authorStatus == "inactive") {
//         obj = obj + "class='btn btn-success pull-left' value='啟用' onclick='modifyAuthorStatus()' /><input type='hidden' id='nextAuthorStatus' value='active'/></div><div class='col-md-6 col-sm-12'><h4>您已經關閉作者賬號功能,啓用後才可以查看作者專區</h4></div></div></div>";
//       } else {
//         obj = obj + "class='btn btn-success pull-left' value='啟用' onclick='modifyAuthorStatus()' /><input type='hidden' id='nextAuthorStatus' value='active'/></div><div class='col-md-3 col-sm-12'><h4>您的作者賬號功能處於 " + resp.authorStatus + "狀態，請聯繫客服</h4></div></div></div>";
//       }
//       $("#mainContent").replaceWith(obj);
//     }
//   } else {
//     var obj = "<div class='box'><div class='box-body' id='mainContent'><div class='col-md-3 col-sm-12'><h4>Server 錯誤，請重新登錄後嘗試</h4></div></div></div>";
//     $("#mainContent").replaceWith(obj);
//   }
// }
