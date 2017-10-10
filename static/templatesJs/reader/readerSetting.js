jQuery(document).ready(function($) {
  $('#readerSettingLi').addClass('active');
});

function modifyReaderName() {
  var userName = $("#userName").val();

  $.ajax({
    url: '/reader/modifyReader/',
    type: 'POST',
    dataType: 'json',
    data: {"argName": "name", "value": userName}
  })
  .done(function(resp) {
    console.log(resp);
    if (resp.res == "success") {
      alert("修改用戶名成功！");
      window.location.reload();
    }
    else if (resp.res == "fail") {
      alert(resp.statusNumber + resp.message);
    }
    else{
      alert(resp.statusNumber + resp.message);
    }
  })
  .fail(function(resp) {
    console.log(resp);
  });
}

function modifyReaderPassword() {
  var password = $("#password").val();

  $.ajax({
    url: '/reader/modifyReader/',
    type: 'POST',
    dataType: 'json',
    data: {"argName": "passwd", "value": password}
  })
  .done(function(resp) {
    console.log(resp);
    if (resp.res == "success") {
      alert("修改密碼成功！");
      window.location.reload();
    }
    else if (resp.res == "fail") {
      alert(resp.statusNumber + resp.message);
    }
    else{
      alert(resp.statusNumber + resp.message);
    }
  })
  .fail(function(resp) {
    console.log(resp);
  });
}
