$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null){
       return null;
    }
    else{
       return results[1] || 0;
    }
}

function loginReader() {
  var userName = $("#userName").val();
  var passwd = $("#passwd").val();
  var lastUrl = decodeURIComponent($.urlParam('lastUrl'));

  $.ajax({
    url: '/reader/loginReader/',
    type: 'POST',
    dataType: 'json',
    data: {"userName": userName, "passwd": passwd, "lastUrl": lastUrl}
  })
  .done(function(resp) {
    // console.log(resp);
    if (resp.status == "success") {
      window.location.href = resp.message
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
