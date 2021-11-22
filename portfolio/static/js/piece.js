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

		$('.star').click(function(){
			var cur=$(this).find('i');
			var num=parseInt($(this).find('.lnum').html())
			var id=$(this).closest('.com_boss').attr('name')
			if (cur.hasClass('sglow')) {
			  cur.removeClass('sglow');
			  cur.siblings('.lnum').html(num-1)
			}
			else{
			  cur.addClass('sglow');
			  cur.siblings('.lnum').html(num+1)
			}
			$.ajax({
				type: 'POST',
				url:'/portfolio/plike_piece/',
				data:{'piece_id':id}
			});

		});

		$('.share-piece').click(function(){
			if ($(this).closest('.pshare').siblings('.pshares').is(':visible')){
		    	$(this).closest('.pshare').siblings('.pshares').hide(200);
		    }
		    else{
		    	$(this).closest('.pshare').siblings('.pshares').show(200);
		    }
		  });

		$('.share-piece').blur(function(){
			console.log('lol')
		    $(this).closest('.pshare').siblings('.pshares').hide(200);
		  });

		function del_pcom(t) {
		  c=t.closest('tr');
		  c.slideUp(200);
		  $.ajax({
		    type: 'POST',
		    url: '/portfolio/delete_pcomment/',
		    data: {'pcid': c.attr('id')},

		  });
		}

		$('.pcom_delete').click(function(){
		  del_pcom($(this));
		});


		$('.pups').click(function(){
		  console.log('mon')
		  var cur=$(this)
		  var id=$(this).closest('tr').attr('id')
		  var unum=$(this).closest('td').find('.unum')
		  var num=parseInt(unum.html())
		  if (cur.hasClass('sglow')) {
		        cur.removeClass('sglow');
		        unum.html(num-1)
		      }
		      else{
		        cur.addClass('sglow');
		        unum.html(num+1)
		      }
		  $.ajax({
		    type:'POST',
		    url:'/portfolio/up_pcom/',
		    data: {'pcid':id}
		  });

		});

		$('.pcom_form').submit(function(event){
		  event.preventDefault();
		 	f=$(this).find('.pcomment_edit')
		  p=$(this).closest('.row').attr('id')
		  t=f.val()
		  if (t) {
			  $.ajax({
			  	type:'POST',
			  	url:'/portfolio/write_pcomment/',
			  	data:{'piece_id':p, 'text':t},
			  	dataType:'json',
			  	success: function(data) {
			  		f.closest('.com_boss').find('.pcoms tbody').prepend('<tr id="'+data.comment.id+'">'+
            '<td class="col-xs-1 pcom_img">'+
              '<a href="/users/profile_view/'+data.comment.user+'">'+
              '<img  src="'+data.comment.image_url+'" style="position: relative; border-radius: 30px;">'+
              '</a>'+
            '</td>'+
            '<td class="col-xs-3 col-md-5 com_tex"  style="vertical-align: middle; position: relative;bottom: 5px;">'+
              '<p>'+data.comment.rant+'</p>'+
              '<a href="javascript:void(0)" class="pcom_delete"><i class="fa fa-trash" style="color: #000;"></i></a>'+
            '</td>'+
            '<td class="col-xs-1 pcom_upv" style="position: relative;left: 6.5%">'+
              '<p style="position: relative;"><i class="material-icons pups" style="font-size: 22px; color: #9336a3">change_history</i><div style="position: relative; bottom: 15px; left:8px">0</div></p>'+
            '</td>'+             
          '</tr>')
				f.closest('.com_boss').find('.com_count').html('Comments ('+data.comment.count+')')
				f.val('')
				$('.pcom_delete').click(function(){
				  del_pcom($(this));
				});
			  	}
			  });
			}
		});