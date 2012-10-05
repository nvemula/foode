

var tmpfooditems = [];
var tmpfoodlists = [];
var mcount=0;
var table_backup = '<tr class="micon"><td class="itname"><a style="color:green;text-decoration:none;" class="itname"></a></td></tr>';
var input_backup = '<input type="text" class="field input-xlarge menuitems" value=""/><a class="delitems" href="#"></a>';
var prelists_backup = '<input type="text" class="oldfoodlists field input-xllarge" value="" flag="yes"/><a class="remlists" style="text-decoration:none;" href="#deleteModal"></a>';
$(function(){
 
foodlistgo();

  mcount++;
$("#saveslug").click(function(){
  $.ajax({
        data: $("#slug-editform").serialize(), // get the form data
                type: $("#slug-editform").attr('method'), // GET or POST
                url: $("#slug-editform").attr('action'), // the file to call
                success: function(response) { // on success..
                    $("#slug_result").html(response); // update the DIV
                }
            });
      return false
    });


$('#basic_info').click(function () {
    $(this).addClass('active');
    $('div#editbasic').show();
    $('div#menubook').hide();
    $('#menu_book').removeClass('active');
    $('#basicsettings').show();    
    $('#advanced').hide();    
    $('#advancedtab').removeClass('active');
    $("#basictab").addClass('active');
     
});

$("#advancedtab").click(function(){
$("#basictab").parent().removeClass('active');
$('#advancedtab').parent().addClass('active');

$('#basicsettings').hide();    
    $('#advanced').show();    

});

$("#basictab").click(function(){
$("#advancedtab").parent().removeClass('active');
$('#basictab').parent().addClass('active');

$('#basicsettings').show();    
    $('#advanced').hide();    

});

$('#menu_book').click(function () {
  $(this).addClass('active');
  $('#menubook').show();
  $('div#editbasic').hide();

  $('#basic_info').removeClass('active');  
  if(mcount>0){
    cleaner();
   }
  foodlistgo();
  mcount++;

});

$('#editlist').click(function(){
$('.foodlisttabs').hide();
$('.currentlists').show();
$('#savelists').show(); 
$('#menuitemsbook').hide();
$('#editingfoodlists').show();

});



$('#editagain').live("click",function(){
$('#foodlistspreview').hide();
$('#foodlists').show();
$('.foodlisttabs').show();
$('#savelists').show(); 
$('#menuitemsbook').show();
$("#menuitemsresultcontent").hide();
$(".currentmenuitems").show();
$("#saveitems").show();
$("#preitems").show();
cleaner();

foodlistgo();


});


$('.foodlist-template').live("click",function(){
$('.foodlist-template').removeClass('active');
$('div.preaddeditems').hide();
var id = $(this).attr('id');
var target = $(this).attr('cp');
$('div#'+target).show();
$('#'+id).addClass('active');




});




});

function foodlistgo(){
      $.ajax({url:"/editmenulistview/" +rest_id+"/",
              success:function(result){
                                 var json;
                                if(result.menulists.length!=0)
                                  {
                                    $('#resultcitems').hide();
                                 $('.prelists').show();
                                  $('.preitems').show();
                                  $('.edit-mini-template').show();

                                $("#saveitems").show();
                                 $('.additem').show();
                                $('#foodlist-content').show();
                                $('.remlists').show();
                                $('.oldfoodlists').show();
                                var directive = {
                                         'div.preaddeditems':{
                                                 'tmp<-menulists':{
                                                            '.@id':'listheading#{tmp.id}',
                                                            'h4':'tmp.listname',
                                                            'div.addfooditems-template@id':'itemsadd#{tmp.id}',
                                                            'a.additem@id':'add#{tmp.id}',
                                                            'div.edit-mini-template':{
                                                                  'itm<-tmp.menuitems':{
                                                                        'input@value':'itm.itemname' ,
                                                                        'input@name':'itm.id',  
                                                                        'input@id':'citemremi#{itm.id}',
                                                                        'a.delitems':'<i class="icon-remove icon-white"></i>',
                                                                        'a.delitems@id':'delremi#{itm.id}', 
                                                                        'a.delitems@href':'#br#{itm.id}',                                                              'span@id':'br#{itm.id}',   
                                                                                                                                                               
                                                                         } 
                                                                      }
                                                                  }
                                                  }
                           };/*end of directive*/

                           $(".currentmenuitems").render(result,directive);
                           var directive = {
                                              '.foodlist-template':{
                                                               'tmp<-menulists':{ '.@id':'foodlist#{tmp.id}',
                                                                                  '.@cp': 'listheading#{tmp.id}',
                                                                                  'a':'#{tmp.listname}<i class="icon-chevron-right"></i>',
                                                                                  'a@href':'#listheading#{tmp.id}',

                                                                                 }
                                                                    }
                                                   };/*end of directive*/
                                       $("#foodlist-content").render(result,directive); 
                                       $(".foodlist-template:first").addClass('active');
                                       $('div.preaddeditems').hide();
                                       $('div.preaddeditems:first').show();
                                       $('#resultclists').hide();
                                      $('.prelists').show();
                     var directive = {
                              'div.preaddedlists':{
                                  'tmp<-menulists':{
                                          'input@value':'tmp.listname',
                                          'input@name':'tmp.id',
                                          'input@id':'clistreml#{tmp.id}',
                                          'a.remlists':'&nbsp<i class="icon-remove icon-black"></i>',
                                          'a.remlists@id':'reml#{tmp.id}'
                                      }
                   }
              };/*end of directive*/
              $(".currentlists").render(result,directive);
                                   
                                       
                                  }
                                else
                                  {         $('.prelists').hide();
                                            $('.preitems').hide();
                                           $('#resultcitems').show();
                                           $('.edit-mini-template').hide();
                                           $("#saveitems").hide();
                                          $('.additem').hide();
                                          $('#foodlist-content').hide();
                                  }
}});/*end of ajax*/
 $('#foodlistspreview').hide();
$('.foodlisttabs').show();
               $('#foodlists').show();
}/*end of foodlistgo*/

$('.delitems').live("click",function() {
                  var id = $(this).attr('id');
                  $(this).remove();
                  $('#'+id).remove();
		  sid=id.slice(3)
                  $('#citem'+sid).remove(); 
                  tid=id.slice(7)
                  $.ajax({url:'/' +tid+'/removemenuitem/',success:function(result){
                      $('#p'+sid).html (result);
                  }});   
                  });  /*end of delete for currentitems*/

$('#saveitems').live("click",function() {
                $("#saveitems").hide();
                $("#preitems").hide();
                newfooditemshandler();
                cleanmenupreview();
                      go();
                $('.currentmenuitems').hide();
                    
                 $('#foodlistspreview').show();
     
               $('#foodlists').hide();
               $('.foodlisttabs').show();
               $('.currentlists').hide();
                $.ajax({
                    data: $(".preitems").serialize(), /* get the form data*/
                    type: $(".preitems").attr('method'), /* GET or POST*/
                    url: $(".preitems").attr('action'), /* the file to call*/
                    success: function(response) { /* on success..*/
                    
                    }
                });
                return false;

 

           });/*endof save fooditems*/

var j = 1;
	$('.additem').live("click",function() {

                var aid = $(this).attr('id'); 
        var template='<input type="text" class="addedmenuitems input-xlarge " name="listitem'+aid +'z'+ j +'" id="menuitemrem' + j +'" value="Item" "/"><a href="#'+aid+'" style="text-decoration:none;" class="remove removeitems" id="rem' + j +'">&nbsp<i class="icon-remove icon-white"></i></a><br>';
$(template).fadeIn('slow').appendTo('#items'+aid);
                tmp = "menuitemrem"+j;
                tmpfooditems.push(tmp);
                j++;
        });/*end of add new fooditems handler*/

$('.remove').live("click",function() {
                  var id = $(this).attr('id');
                  $('#menuitem'+id).remove();
                  $('#'+id).remove();
		  j--;      
          });  /*end of remove for newly added fooditems*/ 

function go(){
$("#menuitemsresultcontent").show();
$.ajax({url:"/editmenulistview/" +rest_id+"/",success:function(result){
  if(result.menulists.length!=0)
     { 
        $('#menutable').show();

  var directive = {
   'div#menutable':{
         'tmp<-menulists':{
                           'h4':'tmp.listname',
                           'tr.micon':{
                           'itm<-tmp.menuitems':{
                               'a.itname':'itm.itemname',
                             }    
                           }
                                  }
  }
  };//end of directive
 var teplc = $("#menuitemsresultcontent").compile( directive );
 $("#menuitemsresultcontent").render(result,teplc);
 }
 else{
$('#menuresult').show();
$('#menutable').hide();
}  

 }});  //end of ajaxsuccess

}//end of go :)



function newfooditemshandler(){

if($('input.addedmenuitems').length>0){
                     for(var i=0;i<tmpfooditems.length;i++){
                       var currentvalue = $("#"+tmpfooditems[i]).attr("value");/*get current value*/
                        $("#"+tmpfooditems[i]).attr("value",currentvalue);/*assign current value*/
                      }/*end of forloop*/
                 for(var c=0;c<$('.addfooditems-template').length;c++)
                 {

                  $("#newmenuitemsform").append($('.addfooditems-template').eq(c).html());
                 }
                 $('.addfooditems-template:not(:first)').remove();
                 $('.addfooditems-template').empty();         
                 

             $.ajax({data: $("#newfooditems-tempform").serialize(), /* get the form data*/
                        type: $("#newfooditems-tempform").attr('method'), /* GET or POST*/
                        url: $("#newfooditems-tempform").attr('action'), /* the file to call*/
                        success: function(response) { /* on success..*/
                       /* alert(response);*/ /*$('#menuitems_content').html(response); */ /* update the DIV*/
                         }
                  });
      return true;
      }/*end of if*/
else return false;
}/*end of submitting newly added fooditems*/
$('.modal-del').live("click",function() {
                  var id = $(this).attr('id');
		  sid=id.slice(3);
                  if($('.remlists').length==1){
                   $('#'+sid).hide();
                  $('#clist'+sid).hide(); 
                  $('#clist'+sid).attr('flag','no'); 
                  } 
                  else{
                  $('#'+sid).remove();
                  $('#clist'+sid).remove(); 
                  }
                  tid=id.slice(7)
                  $('#deleteModal').modal('toggle');
                  $.ajax({url:'/'+tid+'/removemenulist/',success:function(result){
                   }});   
                  j--;
                  });  /*end of delete for currentlists*/ 
$('.remlists').live("click",function() {
                  var id = $(this).attr('id');
                  $('.modal-del').attr("id",'del'+id);
                  $('#deleteModal').modal('toggle');

              });  /*end of remove for currentlists*/ 


var i = 1;
$('#add').live("click",function() {

var aid=$(this).attr("id");
var template = '<input type="text" class="field newfoodlistinputs" name="dynamiclist' + i +' " id="newfoodlist' + i +'" value="Category"  "/"><a style="text-decoration:none;" href="#'+aid+'" class="remove-templists" id ="foodlist' + i +'" >&nbsp&nbsp<i class="icon-remove icon-black"></i></a>';
 $(template).fadeIn('slow').appendTo('#newfoodlists-form');
                var tmp ="newfoodlist"+i; 
                tmpfoodlists.push(tmp);
                   i++;

});/*end of add new food categories handler*/

$('.remove-templists').live("click",function() {
                  var id = $(this).attr('id');
                  $('#new'+id).remove();
                  $(this).remove();
                  i--;
});/*end of remove new food categories handler*/

$('#savelists').live("click",function() {
                  $("#savelists").hide();
                  $("#prelists").hide();
                  $('#menuitemsbook').show();
                  $('#editingfoodlists').hide();
                  if($("input.oldfoodlists").length==1 && $("input.oldfoodlists:first").attr('flag')=="no"){

                    /*do nothing just checking if deleted element is edited*/
                  }
                  else{
                  
                  $.ajax({
                      data: $(".prelists").serialize(), /*get the form data*/
                      type: $(".prelists").attr('method'), /* GET or POST*/
                      url: $(".prelists").attr('action'), /* the file to call*/
                             success: function(response) { /* on success..*/

                             /*$('.currentlists').html(response); /* update the DIV*/
                            }
                  });/*end of ajax request edit current foodlists*/
                }
                 if($('.newfoodlistinputs').length>0)
                 {
                      for(var k=0;k<tmpfoodlists.length;k++){
                       var currentvalue = $("#"+tmpfoodlists[k]).attr("value");/*get current value*/
                        $("#"+tmpfoodlists[k]).attr("value",currentvalue);/*assign current value*/
                      }/*end of forloop*/
                $.ajax({
                     data: $('#newfoodlists-form').serialize(), /* get the form data*/
                     type: $('#newfoodlists-form').attr('method'), /* GET or POST*/
                     url: $('#newfoodlists-form').attr('action'), /* the file to call*/
                     success: function(response) { /* on success..*/

                    /* update the DIV*/
                 }
               });/*end of ajax request add new food categories*/
                 }  
                cleaner();
               foodlistgo();   
               $('.foodlisttabs').show();
               $('.currentlists').hide();
              return false;
          });/*end of save list*/

function cleaner(){
$('.foodlist-template:not(:first)').remove();
$('.foodlist-template:first').removeClass('active');
$('.preaddedlists:not(:first)').remove();
$('#newfoodlists-form').empty();
$('.preaddeditems:not(:first)').remove();
$('.addfooditems-template:not(:first)').remove();
$('.addfooditems-template').empty();
if($('.edit-mini-template').length==0 || $('.edit-mini-template').length==1){
/*if there are no menuitems pure deletes edit-mini-template.So,add the backup and it is moved coz inserBefore is used.Clone the added backup and prepend to some div and change the class back to original .This goes on*/
$('.edit-mini-template:first').remove();
$('.backup-edit-mini-template:first').insertBefore($('.addfooditems-template:first'));
$('.backup-edit-mini-template:first').addClass('edit-mini-template');
$('.edit-mini-template:first').removeClass('backup-edit-mini-template');
$('.edit-mini-template:first').clone().appendTo($("#menuitemsresultcontent"));
$('.edit-mini-template:last').addClass('backup-edit-mini-template');
$('.backup-edit-mini-template:last').removeClass('edit-mini-template');
}
else{
$('.edit-mini-template:not(:first)').remove();
}
$('#newmenuitemsform').empty();
if($('input.menuitems').length==1)
{
$(input_backup).appendTo($('.edit-mini-template:first'));
}
if($('input.oldfoodlists').length==0)
{
$(prelists_backup).appendTo($('.preaddedlists:first'));
}
$('.currentmenuitems').show();
$("#menuitemsresultcontent").hide();
cleanmenupreview();
}


function cleanmenupreview(){
$("div.menutable-template:not(:first)").remove();
if($('.micon').length==0){
$(table_backup).appendTo($('table'));
}
else{
$(".micon:not(:first)").remove();
}
}


