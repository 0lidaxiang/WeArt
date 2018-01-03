jQuery(document).ready(
    function () {
    var $versionRating = $('#versionRating');
    $versionRating.rating({
        min: 0,
        max: 5,  //star socre
        step: 0.1,
        size: "xs",
        showClear: false,
    });

    $versionRating.on('rating.change', function () {
        var idVersion = $('#idVersion').val();
        var rating = $('#versionRating').val();

        var chapterFileName = $('#idBook').val() + $('#chapterOrder').val();

        $.ajax({
          url: '/voteChapter/chapterVersionVote/',
          type: 'GET',
          dataType: 'json',
          data: {
            "idVersion": idVersion,
            "rating": rating,
            "chapterFileName" : chapterFileName,
          }
        })
        .done(function(resp) {
          console.log(resp);
          if (resp.res == "success") {
            alert("投票成功");
            window.location.reload();
          }
          else if(resp.res == "fail1"){
            window.location.href = resp.message
          }
          else{
            alert(resp.message);
          }
        })
        .fail(function(resp) {
          console.log("fail");
          console.log(resp);
        });

    });

});
