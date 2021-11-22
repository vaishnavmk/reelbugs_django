 var n=document.querySelectorAll('.notif_time,');
        for (i=0;i<n.length;i++) {
          n[i].innerHTML=n[i].innerHTML.replace("ago","");
          n[i].innerHTML=n[i].innerHTML.replace(/an/,"1");
          n[i].innerHTML=n[i].innerHTML.replace(/&nbsp;hours?.*?/, 'h');
          n[i].innerHTML=n[i].innerHTML.replace(/&nbsp;seconds?.*/,"s");
          n[i].innerHTML=n[i].innerHTML.replace(/&nbsp;minutes?.*/,"m");
          n[i].innerHTML=n[i].innerHTML.replace(/&nbsp;days?.*/,"d");
      };