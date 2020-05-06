$(document).ready(function () {

  $(document).on("focus", ".form__phone-0", function (e) {
    e.preventDefault();
    $(this).parents('.form__phone-group').find(".check-wp").css({
      'background': '#fff',
      'borderColor': '#2568ef'
    })

    if ($(this).parents('.form__phone-group').find(".check-wp").css('display') === 'none') {
      $(this).parents('.form__phone-group').next().slideDown();
    } else {

    }


  });
  $(document).on("blur", ".form__phone-0", function (e) {
    e.preventDefault();
    $(this).parents('.form__phone-group').next().slideUp();
    $(this).parents('.form__phone-group').find(".check-wp").css({
      'background': '#f5f5f5',
      'borderColor': '#eaedf2'

    })
  });

  $(document).on("click", ".add-wp-0", function (e) {
    e.preventDefault();
    $(this).siblings('.form__phone-group').find(".check-wp").css({
      "display": "flex"
    });
    $(this).siblings('.form__phone-group').find(".check-wp__input").prop("checked", true);
    $('.check-wp__input-0').val('checked-true');
    console.log($(this).siblings('.form__phone-group').find(".check-wp__input").prop("checked", true));
    $(this).siblings('.form__phone-group').find(".form__phone").addClass('form__phone--input');
    $(this).slideUp();
  });
  $(document).on("click", ".check-wp__input-0", function () {

    $(this).prop("checked", false);
    $('.check-wp__input-0').val('');
    $(this).parent().css({
      "display": "none"
    });
    $(this).parents('.form__phone-group').find(".form__phone").removeClass('form__phone--input');
  });

});


// Add row
let row = 1;
let remaining = 2;





$(document).on("click", ".add-phone", function (e) {
  e.preventDefault();

  var newRow = '<div class="form-group__phone" id="row' + row + '">' +
    '<div class="valid-check valid-hide  valid-check-' + row + '">&#10004;</div>' +
    '  <span id="error-receiver-number " ></span>' +
    '<span id="error-msg" class="valid-hide text-danger d-block  text-right error-msg-' + row + '"></span>' +
    '  <div class="form__phone-group">' +
    ' <input type="text" name="add-phone-' + row + '" value="add-phone-' + row + '" class="form-control form__control form__phone form__phone-' + row + '" id="phoneNumber-' + row + '">' +
    '<button class="remove-phone btn btn-purple delete-row" id="add-phone-' + row + '">' +
    '<i class="fas fa-minus "></i>' +
    '    </button>' +
    ' </div>' +

    '</div>'
  $('.form-group__phone-div').append(newRow);
  
  for (num = 0; num < 3; num++) {
    $(document).on("focus", `.form__phone-${num}`, function (e) {
      e.preventDefault();
      $(this).parents('.form__phone-group').find(".check-wp").css({
        'background': '#fff',
        'borderColor': '#2568ef'
      })

      if ($(this).parents('.form__phone-group').find(".check-wp").css('display') === 'none') {
        $(this).parents('.form__phone-group').next().slideDown();
      } else {

      }


    });
    $(document).on("blur", `.form__phone-${num}`, function (e) {
      e.preventDefault();
      $(this).parents('.form__phone-group').next().slideUp();
      $(this).parents('.form__phone-group').find(".check-wp").css({
        'background': '#f5f5f5',
        'borderColor': '#eaedf2'

      })
    });

    $(document).on("click", `.add-wp-${num}`, function (e) {
      e.preventDefault();
      $(this).siblings('.form__phone-group').find(".check-wp").css({
        "display": "flex"
      });
      $(this).siblings('.form__phone-group').find(".check-wp__input").prop("checked", true);
      $(this).siblings('.form__phone-group').find(".check-wp__input").val('checked-true');
      console.log($(this).siblings('.form__phone-group').find(".check-wp__input").prop("checked", true));
      $(this).siblings('.form__phone-group').find(".form__phone").addClass('form__phone--input');
      $(this).slideUp();
    });
    $(document).on("click", `.check-wp__input-${num}`, function () {

      $(this).prop("checked", false);
      $(this).val('');
      $(this).parent().css({
        "display": "none"
      });
      $(this).parents('.form__phone-group').find(".form__phone").removeClass('form__phone--input');
    });
  }
  function UpdateRemaining(isAdd) {
    if (isAdd) {
      remaining = remaining - 1;
    } else {
      remaining = remaining + 1;
    }
  
    $('#remaining').text(remaining);
    if (remaining == 0) {
      $('.add-phone').prop("disabled", true);
      $('#add-phone-1').prop("disabled", true);
    } else {
      $('.add-phone').prop("disabled", false);
      $('#add-phone-1').prop("disabled", false);
    }
  }
 UpdateRemaining(true);
  function intlInput() {
    let num = row;
    row++;
    console.log(num)
    var input = document.querySelector(`#phoneNumber-${num}`);
  
  
    $(`#phoneNumber-${num}`).intlTelInput({
  
      separateDialCode: false,
      initialCountry: "az",
      autoPlaceholder: "polite",
  
  
    });
  
  
  
    var minLength = 6;
    $(`#phoneNumber-${num}`).val('+994');
    $(`#phoneNumber-${num}`).on('keydown keyup change', function (evt) {
      var charLength = $(this).val().length;
      if (charLength < minLength) {
        $(`.error-msg-${num}`).text('Minimum ' + minLength + ' required.');
        $(`.valid-check-${num}`).addClass("valid-hide");
      } else if (charLength > minLength) {
        $(`.valid-check-${num}`).removeClass("valid-hide");
        $(`.error-msg-${num}`).text('');
      }
  
  
    });
    $(`#phoneNumber-${num}`).on('keypress', function (evt) {
      var charCode = (evt.which) ? evt.which : event.keyCode
      if (charCode != 43 && charCode > 31 && (charCode < 48 || charCode > 57))
        return false;
  
      return true;
  
    });
  
  
  }
 
  intlInput();


  
  return false;





});

// Remove criterion
$(document).on("click", ".delete-row", function () {
  if (row > 1) {
    $(this).closest('.form-group__phone').remove();
    row--;
  }
  function UpdateRemaining(isAdd) {
    if (isAdd) {
      remaining = remaining - 1;
    } else {
      remaining = remaining + 1;
    }
  
    $('#remaining').text(remaining);
    if (remaining == 0) {
      $('.add-phone').prop("disabled", true);
      $('#add-phone-1').prop("disabled", true);
    } else {
      $('.add-phone').prop("disabled", false);
      $('#add-phone-1').prop("disabled", false);
    }
  }
  UpdateRemaining(false);
  intlInput(true);
  return false;
});