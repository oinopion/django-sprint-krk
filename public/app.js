$(function() {
   $(".external").click(function(ev){
       ev.preventDefault();
       window.open(this.href);
   });
});