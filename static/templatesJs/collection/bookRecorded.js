jQuery(document).ready(function($) {
  $('#myRecordLi').addClass('active');

});
$(function() {
  $("#example1").DataTable();
  $('#example2').DataTable({
    "paging": true,
    "lengthChange": false,
    "searching": false,
    "ordering": true,
    "info": true,
    "autoWidth": false
  });

  getMainContentData();
});

function getMainContentData() {
  $.ajax({
    url: '/collection/getMyCollection/',
    type: 'GET',
    dataType: 'json',
    data: {}
  })
  .done(function(resp) {
    // console.log(resp);
    var message = resp.message;
    if (resp.status == "success" && message != null) {
      var trs = "";
      for (var i = 0; i < message.length; i++) {
          var tds = "";
          tds = tds + "<td>" + message[i]["idReader"] + "</td>";
          tds = tds + "<td>" + message[i]["idBook"] + "</td>";
          tds = tds + "<td>" + message[i]["bookName"] + "</td>";
          tds = tds + "<td>" + message[i]["createTime"] + "</td>";
          tds = tds + "<td>" + "<a href=javascript:deleteCollection('" + message[i]["idColl"] + "');> deleteCollection"  + "</a>" + "</td>";
          trs = trs + "<tr role='row'>" + tds + '</tr>';
      }
      $("#mainContent").replaceWith("  <tbody id = 'mainContent'>" + trs + "</tbody>");
    }
    else if (resp.status == "fail") {
      var obj = "<div class='col-md-12 col-sm-12'><h4>" + resp.message + "</h4></div>";
      $("#mainContent").replaceWith(obj);
    }
    else{
      var obj = "<div class='col-md-12 col-sm-12'><h4>" + resp.message + "</h4></div>";
      $("#mainContent").replaceWith(obj);
    }
  })
  .fail(function(resp) {
    console.log(resp);
  });
}

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
