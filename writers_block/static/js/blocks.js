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

 var n=document.querySelectorAll('.block_time, .com_time');
        for (i=0;i<n.length;i++) {
          n[i].innerHTML=n[i].innerHTML.replace("ago","");
          n[i].innerHTML=n[i].innerHTML.replace(/an/,"1");
          n[i].innerHTML=n[i].innerHTML.replace(/&nbsp;hours?.*?/, 'h');
          n[i].innerHTML=n[i].innerHTML.replace(/&nbsp;seconds?.*/,"s");
          n[i].innerHTML=n[i].innerHTML.replace(/&nbsp;minutes?.*/,"m");
          n[i].innerHTML=n[i].innerHTML.replace(/&nbsp;days?.*/,"d");
      };



//main search stuff
    var m_srch=$('#main_search')
    var options={
      url:function(phrase){
        return 'https://api.themoviedb.org/3/search/multi?api_key=4ce570b5135503d520df426d7989073f&query='+phrase.replace(/\s+/,'+')        
      },
      getValue:function(element) {
        if (element.title){
          return element.title;
        }
        else {
          return element.name;
        }
      },
      listLocation: 'results',
      theme: "round",
      requestDelay: 500,
      list: {
          maxNumberOfElements: 10,

          showAnimation: {
                type: "fade", //normal|slide|fade
                time: 400,
                callback: function() {}
              },

              hideAnimation: {
                type: "slide", //normal|slide|fade
                time: 400,
                callback: function() {}
              },

          onChooseEvent: function(){
            var movie_id=m_srch.getSelectedItemData().id;
            var g=m_srch.getSelectedItemData().media_type[0]+'d'
            window.location.href='/index/'+g+'/'+movie_id
          }
        },
      template: {
        type: 'custom',
        method: function(value, item){
          var t=item.media_type
          if (t=='movie'){
            var j= item.poster_path ? 'https://image.tmdb.org/t/p/w92'+item.poster_path : '/static/images/search_back.jpeg'
            return '<a class="search_link" href="/index/md/'+item.id+'"><img src="'+j+'" class="result_img" style="max-width:45px"><span class="search_title" alt="'+item.title+' poster">'+item.title+'</span><span class="search_date">'+item.release_date+'</span><span class="search_typ">Movie</span></a>'
          }
          else if (t=='tv'){
            var j= item.poster_path ? 'https://image.tmdb.org/t/p/w92'+item.poster_path : '/static/images/search_back.jpeg'
            return '<a class="search_link" href="/index/td/'+item.id+'"><img src="'+j+'" class="result_img" style="max-width:45px"><span class="search_title" alt="'+item.name+' poster">'+item.name+'</span><span class="search_date">'+item.first_air_date+'</span><span class="search_typ">TV</span></a>'
          }
          else {
            var j= item.profile_path ? 'https://image.tmdb.org/t/p/w92'+item.profile_path : '/static/images/search_back.jpeg'
            return '<a class="search_link" href="/index/pd/'+item.id+'" style="text-decoration:none; color:#000"><img src="'+j+'" class="result_img" style="max-width:45px" alt="'+item.name+' profile"><span class="search_title">'+item.name+'</span><span class="search_typ">Person</span>'
          }

        }        
        }
      }
    m_srch.easyAutocomplete(options);

  <!---->






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

  $('.share-btn').click(function(){
      if ($(this).closest('.bookmark').siblings('.shares').is(':visible')){
        $(this).closest('.bookmark').siblings('.shares').hide(200);
      }
      else{
        $(this).closest('.bookmark').siblings('.shares').show(200);
      }
  });

  $('.shares').blur(function(){
      $(this).closest('.bookmark').siblings('.shares').hide(200);
  });

  $('.block_del_btn').click(function(){
      var id=$(this).closest('.well').attr('id');
      $('#del_confirm').attr('name', id);
      $('#del_confirm').modal();
  });

  
  $('.foll_link').on('click', function(){
    var user_id=$(this).attr('id')
    fl=$(this)
    fc=$(this).closest('.follow_btn').find('.follower_count')
    $.ajax({
      type:'POST',
      url:'/users/fu/'+user_id+'/',
      success: function(json){
        if (json.foll){
          fc.html(function(){
            return parseInt(fc.html())+1
          });
          fl.html('Unfollow')
        }
        else{
          fc.html(function(){
            return parseInt(fc.html())-1
          });
          fl.html('Follow')
        }
      }
    });
  });  


  $('.del_conf').click(function(){
    var id=$(this).closest('.modal').attr('name');
    var well=$('#'+id);
    $('#del_confirm').hide();
    $('.modal-backdrop').remove();
    $('body').removeClass('modal-open');
    $(well).hide(200);
    $.ajax({
      type:'POST',
      url:'/index/abd/',
      data:{'block_id':id},
    });
  });


    //like button
    $('.like').click(function(){
          var cur=$(this).find('i').first();
          var num=parseInt(cur.siblings('.lnum').html())
          cur_id=cur.attr('id')
          if (cur.hasClass('fa-hand-paper-o')) {
            cur.removeClass('fa-hand-paper-o');
            cur.addClass('fa-hand-spock-o sglow');
            cur.siblings('.lnum').html(num+1)
            var like=1

          }
          else{
            cur.removeClass('fa-hand-spock-o sglow');
            cur.addClass('fa-hand-paper-o');
            cur.siblings('.lnum').html(num-1)
            var like=0
          }

          $.ajax({
            type:'POST',
            url:'/index/abl/',
            data: {'block_id':cur_id, 'like': like}
          });
        });

      $('.yolike').click(function(){
        var cur=$(this).find('i').first();
        var num=parseInt(cur.siblings('.lnum').html())
        if (cur.hasClass('fa-hand-paper-o')) {
          cur.removeClass('fa-hand-paper-o');
          cur.addClass('fa-hand-spock-o sglow');
          cur.siblings('.lnum').html(num+1)

        }
        else{
          cur.removeClass('fa-hand-spock-o sglow');
          cur.addClass('fa-hand-paper-o');
          cur.siblings('.lnum').html(num-1)
        }

      });

    $('.bups').click(function(){
      var cur=$(this)
      var id=$(this).closest('tr').attr('id')
      var unum=$(this).closest('td').find('.unum')
      var num=parseInt(unum.html())
      if (cur.hasClass('sglow')) {
            cur.removeClass('sglow');
            unum.html(num-1)
            var like=1
          }
          else{
            cur.addClass('sglow');
            unum.html(num+1)
            var like=0
          }
      $.ajax({
        type:'POST',
        url:'/index/acu/',
        data: {'cid':id, 'like':like}
      });

    });

    function del_com(t) {
      var c=t.closest('tr');
      c.slideUp(200);
      $.ajax({
        type: 'POST',
        url: '/index/acd/',
        data: {'cid': c.attr('id')},

      });
    }

    $('.com_delete').click(function(){
      del_com($(this));
      var cn=$(this).closest('.comment_box').siblings('.block_body').find('.comments .cnum')
      var cnu=parseInt(cn.html())
      console.log(cnu)
      cn.html(cnu-1)
      
    });



    //comment post ajax
    $('.com_form').submit(function(event){
      event.preventDefault();
      var f=$(this);
      var t=f.find('.comment_edit').val();
      if (t) {
        $.ajax({
          url:'//freegeoip.net/json/?callback=?',
          async:false,
          success: function(data) {
          var ip_addr=data.ip
          f.siblings('.coms').find('tbody').prepend(
          '<tr class="new_com">'+
          '<td class="col-xs-1 com_img">'+
            '<img height="45" width="45" src="https://www.gravatar.com/avatar/'+ip_addr+'?f=y&d=monsterid" style="position: relative;">'+
          '</td>'+
          '<td class="col-xs-8 com_tex"  style="vertical-align: middle; position: relative;bottom: 5px;">'+
            '<p>'+t+'</p>'+ '&nbsp;'+
            '<a href="javascript:void(0)" class="com_delete"><i class="fa fa-trash" style="color: #000;"></i></a>'+
          '</td>'+
          '<td class="col-xs-1">'+
            '<p style="position: relative;"><i class="material-icons bups" style="font-size: 18px; color: #9336a3">change_history</i><div style="position: relative; bottom: 15px; left:5px">0</div></p>'+
          '</td>'+             
          '</tr>')
          }
        });
        var c=f.closest('.comment_box')
        var b=c.attr('name');
        $.ajax({
          type: 'POST',
          url:f.attr('action'),
          data: {'block_id':b, 'text':t},
          dataType:'json',
          success: function(data) {
              f.find('.comment_edit').val('');
              f.closest('.comment_box').siblings('.block_body').find('.comments .cnum').html(data.comment.num);
              $('.new_com').attr('id', data.comment.id)
              $('.com_delete').click(function(){
                del_com($(this));
                var cn=$(this).closest('.comment_box').siblings('.block_body').find('.comments .cnum')
                var cnu=parseInt(cn.html())
                console.log(cnu)
                cn.html(cnu-1)
              });
            }
          });
        } 
    });

  
