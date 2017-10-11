function addCollection(idBookArg) {
  $.ajax({
    url: '/collection/addCollection/',
    type: 'GET',
    dataType: 'json',
    data: {"idBook": idBookArg}
  })
  .done(function(resp) {
    // console.log(resp);
    var errorNumber = resp.errorNumber;
    var message = resp.message;
    if (resp.status == "success" && message != null) {
      alert("收藏成功！");
      window.location.href = "/chapter/bookChapter/?idBook=" + idBookArg
    }
    else if (resp.status == "fail") {
      alert(errorNumber + "收藏失敗："　+ message)
    }
    else{
      alert("未知錯誤：　" + errorNumber　+ message)
    }
  })
  .fail(function(resp) {
    console.log("addCollection fail");
    console.log(resp);
  });
}

function goToAddCollection() {
  var lastUrl = window.location.href;
  var idBook = $("#idBook").val();

  $.ajax({
    url: '/collection/goToAddCollection/',
    type: 'GET',
    dataType: 'json',
    data: {"idBook": idBook, "lastUrl": lastUrl}
  })
  .done(function(resp) {
    // console.log(resp);
    if (resp.status == "success1") {
      window.location.href = resp.message
    }
    else if (resp.status == "success2") {
      addCollection(resp.message);
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
