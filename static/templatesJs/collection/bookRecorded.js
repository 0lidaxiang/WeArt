jQuery(document).ready(function($) {
  $('#myRecordLi').addClass('active');

  $("#example1").DataTable(
    {
      "ajax": '/collection/getMyCollection/',
      "columns": [
            // { "data": "idColl" },
            { "data": "idReader" },
            { "data": "idBook" },
            { "data": "bookName" },
            { "data": "createTime" },
            { "data": "operation" },
        ]
    }
  );
});

function deleteCollection(idCollectionArg) {
  // alert("delete: " + idCollectionArg);
  $.ajax({
    url: '/collection/deleteCollection/',
    type: 'GET',
    dataType: 'json',
    data: {"idCollectionArg" : idCollectionArg}
  })
  .done(function(resp) {
    console.log(resp);
    var message = resp.message;
    if (resp.status == "success") {
      alert("刪除成功！");
      window.location.reload();
    }
    else if (resp.status == "fail") {
      var obj = "<div class='col-md-12 col-sm-12'><h4>" + resp.errorNumber + " , " + resp.message + "</h4></div>";
      $("#mainContent").replaceWith(obj);
    }
    else{
      var obj = "<div class='col-md-12 col-sm-12'><h4>" + resp.errorNumber + " , " + resp.message + "</h4></div>";
      $("#mainContent").replaceWith(obj);
    }
  })
  .fail(function(resp) {
    console.log(resp);
  });
}
