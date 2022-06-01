$(document).ready(function() {
    $('#btnM1').click(function(event) {
    $('.modal').addClass('show')
    $('#btnM1').css("display", "none")

});
      $('.close__modal',).click(function(event) {
      $('.modal').removeClass('show')
      $('#btnM1').css("display", "flex")
});
});

$(document).ready(function(){
$('#password-checkbox').click(function(event){
if ($(this).is(':checked')){
		$('#password-input').attr('type', 'text');
	} else {
		$('#password-input').attr('type', 'password');
	}
})
});
$(document).ready(function(){
$('#password-checkbox2').click(function(event){
if ($(this).is(':checked')){
		$('#password-input2').attr('type', 'text');
	} else {
		$('#password-input2').attr('type', 'password');
	}
})
});
$(document).ready(function(){
$('#password-checkbox3').click(function(event){
if ($(this).is(':checked')){
		$('#password-input3').attr('type', 'text');
	} else {
		$('#password-input3').attr('type', 'password');
	}
})
});
$(document).ready(function() {
    $('.btn_add__avto').click(function(event) {
    $('.modal').addClass('show')
    $('.btn_add__avto').css("display", "none")

});
      $('.close__modal',).click(function(event) {
      $('.modal').removeClass('show')
      $('.btn_add__avto').css("display", "flex")
});
});
$(document).ready(function() {
$('.slider-wrapper .slide').each(function(i){
   $(this).attr('id', 'slide'+i);
   $('#slide0').addClass('active')
})
$('.dots-wrapper .dot').each(function(i){
   $(this).attr('id', 'dot'+i);
   $('#dot0').addClass('active')
})
});




