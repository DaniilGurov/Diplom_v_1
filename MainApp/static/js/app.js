$(document).ready(function () {
  $('#btnM1').click(function (event) {
    $('.modal').addClass('show')
    $('#btnM1').css("display", "none")

  });
  $('.close__modal',).click(function (event) {
    $('.modal').removeClass('show')
    $('#btnM1').css("display", "flex")
  });
});
$(document).ready(function () {
  $('.edit_avto').click(function (event) {
    $('.modal').addClass('show')
    $('edit_avto').css("display", "none")

  });
  $('.close__modal',).click(function (event) {
    $('.modal').removeClass('show')
    $('.edit_avto').css("display", "flex")
  });
});


$(document).ready(function () {
  $('.btn__modal__user__edit').click(function (event) {
    $('.modal__content--user').css("display", "none")
    $('.modal__edit__user').css("display", "flex")
    $('.btn__modal__user__edit').css("display", "none")

  });
  $('.close__modal__user__edit',).click(function (event) {
    $('.modal__edit__user').css("display", "none")
    $('.modal__content--user').css("display", "flex")
    $('.btn__modal__user__edit').css("display", "flex")
  });
});


$(document).ready(function () {
  $('#password-checkbox').click(function (event) {
    if ($(this).is(':checked')) {
      $('#password-input').attr('type', 'text');
    } else {
      $('#password-input').attr('type', 'password');
    }
  })
});
$(document).ready(function () {
  $('#password-checkbox2').click(function (event) {
    if ($(this).is(':checked')) {
      $('#password-input2').attr('type', 'text');
    } else {
      $('#password-input2').attr('type', 'password');
    }
  })
});
$(document).ready(function () {
  $('#password-checkbox3').click(function (event) {
    if ($(this).is(':checked')) {
      $('#password-input3').attr('type', 'text');
    } else {
      $('#password-input3').attr('type', 'password');
    }
  })
});
$(document).ready(function () {
  $('.btn_add__avto').click(function (event) {
    $('.modal').addClass('show')
    $('.btn_add__avto').css("display", "none")

  });
  $('.close__modal',).click(function (event) {
    $('.modal').removeClass('show')
    $('.btn_add__avto').css("display", "flex")
  });
});
$(document).ready(function () {
  $('.slider-wrapper .slide').each(function (i) {
    $(this).attr('id', 'slide' + i);
    $('#slide0').addClass('active')
  })
  $('.dots-wrapper .dot').each(function (i) {
    $(this).attr('id', 'dot' + i);
    $('#dot0').addClass('active')
  })

});



$(document).ready(function () {
  $("#phone").mask("+7(999)999-99-99");
  $.mask.definitions['Z'] = "[etyopahkxcbmукенхваросмтETYOPAHKXCBNMУКЕНХВАРОСМТ]";
  $('#inputNumAvto').mask('Z999ZZ99?9');
});




$(document).ready(function () {
  $('.user__input',).change(function (event) {
    $('.btn__user').addClass('show')
  });
});