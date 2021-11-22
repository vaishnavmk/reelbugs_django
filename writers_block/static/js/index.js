  $(".sidebar").stickySidebar({
    topSpacing: 20,
    bottomSpacing: 20,
    containerSelector: '.main-content',
    innerWrapperSelector: '.sidebar__inner'
  }); 

$('.block_del_btn').click(function(){
    var id=$(this).closest('.well').attr('id');
    $('#del_confirm').attr('name', id);
    $('#del_confirm').modal();
});

$('.del_conf').click(function(){
  var id=$(this).closest('.modal').attr('name');
  var well=$('#'+id)
  console.log(id)
  $.ajax({
    type:'POST',
    url:'/index/delete_block/',
    data:{'block_id':id, csrfmiddlewaretoken:'{{csrf_token}}'},
    dataType:'json',
    success: function(data){
      $(well).hide(200);
      console.log('done');
      $('#del_confirm').hide();
      $('.modal-backdrop').remove();
      $('body').removeClass('modal-open');
    }
  });
  return false;
});

  $(document).ready(function(){
    $("#myBtn").click(function(){
        $("#block_writer").modal();
      });

    $('#block_writer').on('shown.bs.modal', function () {
        $('#id_content').focus();
    })
  });

  var n=document.querySelectorAll('.block_time, .com_time');
    for (i=0;i<n.length;i++) {
      n[i].innerHTML=n[i].innerHTML.replace("ago","");
      n[i].innerHTML=n[i].innerHTML.replace(/an/,"1");
      n[i].innerHTML=n[i].innerHTML.replace(/&nbsp;hours?.*?/, 'h');
      n[i].innerHTML=n[i].innerHTML.replace(/&nbsp;seconds?.*/,"s");
      n[i].innerHTML=n[i].innerHTML.replace(/&nbsp;minutes?.*/,"m");
      n[i].innerHTML=n[i].innerHTML.replace(/&nbsp;days?.*/,"d");
  };

  //comment toggle
  $('.comments').click(function(){
    if ($(this).hasClass('com_active')) {
      $(this).removeClass('com_active');
      $(this).closest('.block_body').siblings('.comment_box').slideUp();
    }
    else {
      $(this).addClass('com_active');
       $(this).closest('.block_body').siblings('.comment_box').slideDown(200, function(){
        $(this).find('textarea').focus();
      });
    }
  });

  //like button
  $('.like').click(function(){
    var cur=$(this);
    cur_id=cur.children().eq(0).attr('id')
    $.ajax({
      type:'POST',
      url:'{%url "like_block"%}',
      data: {'block_id':cur_id, csrfmiddlewaretoken:'{{csrf_token}}'},
      dataType:'json',
      success: function(data) {
        cur.html('<i id="'+cur_id+'" class="fa fa-hand-spock-o" aria-hidden="true"></i>&nbsp;'+data.likes);
        if (data.liked){
          cur.find('i').addClass('lglow');
        }
        else{
          cur.find('i').removeClass('lglow');
        }       
      }
    });
  });

  $('.share-btn').click(function(){
    if ($(this).closest('.bookmark').siblings('.shares').is(":visible")){
      $(this).closest('.bookmark').siblings('.shares').hide(200);
    }
    else{
      $(this).closest('.bookmark').siblings('.shares').show(200);
    }
  });


  $('[data-toggle="tooltip"]').tooltip({trigger:'hover'});
  $("#myBtn").click(function(){
          $("#block_writer").modal();
  }); 

  //comment post ajax
  $('.com_form').submit(function(event){
    event.preventDefault();
    var f=$(this);
    var t=f.find('.comment_edit').val();
    if (t) {
      var b=f.closest('.comment_box').attr('name');
      $.ajax({
        type: 'POST',
        url:f.attr('action'),
        data: {'block_id':b, csrfmiddlewaretoken:'{{csrf_token}}', 'text':t},
        dataType:'json',
        success: function(data) { 
          console.log(data.comment);
          f.siblings('.coms').prepend(
          '<div class="container comment" style=" width: inherit; min-height: 40px;">'+
            '<div class="row" style="overflow: hidden;">'+
              '<div class="col-xs-1 com_img">'+
                '<img src="'+data.comment.image_url+'">'+
              '</div>'+
              '<div class="col-xs-11 com_tex">'+
                '<p>'+data.comment.rant+'</p>'+
              '</div>'+  
            '</div>'+
            '<hr style="padding: 1px; margin: 1px;">'+
          '</div>')
          f.find('.comment_edit').val('');
        }
      }); 
    }
  });
