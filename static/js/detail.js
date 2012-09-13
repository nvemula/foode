var table_backup = '<tr class="micon"><td class="itname"><a style="color:green;text-decoration:none;" class="itname"></a></td> <td class="rstar" width="30%"></td></tr>';

   $(document).ready(function(){
go();
function go(){
$("#menucontent").show();
$.ajax({url:"/menulistview/" +rest_id+"/",success:function(result){
  if(result.menulists.length!=0)
     { 
        $('#menuresult').hide();
        $('#menutable').show();
        $('#plusitems').show();
  var directive = {
   'div#menutable':{
         'tmp<-menulists':{
                           'h4':'tmp.listname',
                           'tr.micon':{
                           'itm<-tmp.menuitems':{
                               'a.itname':'itm.itemname',
                                'a.itname@href':'/restaurants/?fooditem=#{itm.itemname}',
                                'td.rstar@id':'rstar#{itm.id}', 
                                 'td.rstar@rating':'itm.rrating',         
                             }    
                           }
                                  }
  }
  };//end of directive
  $("#menucontent").render(result,directive);
 }
 else{
$('#menuresult').show();
        $('#menutable').hide();
}  

      $('.rstar').raty({

     start: function() {
     return $(this).attr('rating');
  },
  click: function(score, evt) {
    starid = $(this).attr('id');
    $.ajax({url:"/ratemenuitem/"+starid+"/"+score+"/",success:function(result){   
 }});
  } 
  });
 }});  

}//end of go :)

$('#plusitems').live("click",function(){
$('.menutable-template').hide();
$('#addmenuitems').show();
$(this).hide();
$.ajax({url:"/editmenulistview/" +rest_id+"/",success:function(result){   
                        if(result.menulists.length!=0)
                        { 
                            $('#resultadditems').hide();
                            $('.catg').show();
                            var directive = {
                                   'div.additems-template':{
                                       'tmp<-menulists':{
                                           'h4':'#{tmp.listname}',
                                           'p.new-fooditems':'<div id="itemsadd#{tmp.id}" class="additemstolist" align="center"></div><a class="btn additem" id="add#{tmp.id}" href="##{tmp.id}" style="text-decoration:none;text-align:center;" ><i class="icon-plus icon-black"></i></a><hr\">',
                                         }
                                   }
                            };//end of directive
                            $("#menuitems_content").render(result,directive);
                        }//end of if
                       else{
                             $('#resultadditems').show();
                             $('.catg').hide();
                             $('#doneitems').hide();
                       }//end of else
                       }});  
  });
$('#canceladd').live("click",function(){
$('.menutable-template').show();
$('#addmenuitems').hide();
cleanformtemplate();
$('#plusitems').show();
});
       var j = 1;
	$('.additem').live("click",function() {
                $('#doneitems').show();
                var aid = $(this).attr('id'); 
        var template='<hr"/"><input type="text" class="input-xlarge field listitems" name="listitem'+aid +'z'+ j +'" id="menuitemrem' + j +'" value="Item""/"><a href="#'+aid+'" class="remove removeitems" style="text-decoration:none;text-align:center;" id="rem' + j +'">&nbsp&nbsp<i class="icon-remove icon-black"></i></a><br>';
$(template).fadeIn('slow').appendTo('#items'+aid);
                j++;
        });//end of additem handler

$('.remove').live("click",function() {
                  var id = $(this).attr('id');
                  $('#menuitem'+id).remove();
                  $('#'+id).remove();
		  j--;
            if($('.listitems').length==0){
                                  $('#doneitems').hide();
                  }        
          });  //end of remove for menuitems 

$('#doneitems').live("click",function() {
                  $.ajax({
                        data: $("#menuitemsform").serialize(), // get the form data
                        type: $("#menuitemsform").attr('method'), // GET or POST
                        url: $("#menuitemsform").attr('action'), // the file to call
                        success: function(response) { // on success..
                              cleanmenucontenttemplate();     
                         go();
                          $('.menutable-template').show();
                           $('#addmenuitems').hide();
                          cleanformtemplate();
                          $('#plusitems').show();
                           
                         }
                  });
              return false;
           });//end of submititem click handler
function cleanformtemplate(){
$("div.additems-template:not(:first)").empty();
                          $("div.additems-template:not(:first)").remove();
                          $('.additemstolist').remove(); 
                          $('.additem').remove(); 
}

function cleanmenucontenttemplate(){
$("div.menutable-template:not(:first)").remove();
if($('.micon').length==0){
$(table_backup).appendTo($('table'));
}
else{
                                   $(".micon:not(:first)").remove();
                                   $(".rstar").empty();
}
                                   $('.listitems').remove();
                                   $('.remove').remove();
}
});//end of doc ready
