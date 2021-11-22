function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});



var n=document.querySelectorAll('.chat_time');
	for (i=0;i<n.length;i++) {
	  n[i].innerHTML=n[i].innerHTML.replace("ago","");
	  n[i].innerHTML=n[i].innerHTML.replace(/an/,"1");
	  n[i].innerHTML=n[i].innerHTML.replace(/&nbsp;hours?.*?/, 'h');
	  n[i].innerHTML=n[i].innerHTML.replace(/&nbsp;seconds?.*/,"s");
	  n[i].innerHTML=n[i].innerHTML.replace(/&nbsp;minutes?.*/,"m");
	  n[i].innerHTML=n[i].innerHTML.replace(/&nbsp;days?.*/,"d");
};

$('.msg_row').click(function(){
	var id=$(this).attr('id');
	window.location.href='/chat/message_view/'+id+'/'
});

$('.chat_btn').click(function(){
  $('.chat').modal();
  var userid=$(this).closest('.block_header').attr('name')
  var name=$(this).closest('.block_header').find('.block_name b').html()
  $('.chat').attr('name', userid)
  $('.chat').find('.chat_head').html('Text '+name)
});

$('.msg-send').click(function(){
  var text=$(this).siblings('.msg').val();
  var userid=$(this).closest('.chat').attr('name');
  $('.chat').slideUp(500);
  $('.modal-backdrop').remove();
  $('body').removeClass('modal-open');
  if (text){
    $.ajax({
      type:'POST',
      url:'/chat/send_message/',
      data:{'to': userid, 'text':text},
      success: function(){
      	location.reload();
      	$('.alerts p').html('Your text was sent');
      	$('.alerts').show(200);
      	$('.alerts').delay(5000).fadeOut(200)
      }
    });
  }

});
