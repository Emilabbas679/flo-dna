// // // FOR  INDEX.HTML  INDEX-3.HTML İNTERNATİONAL TELEPHONE İNPUT
$(document).ready(function () {

  // var input = document.querySelector("#phoneNumber-0"),

  //   errorMsg = document.querySelector("#error-msg"),
  //   validMsg = document.querySelector("#valid-msg");
  // validCheckDefault = document.querySelector(".valid-check-0");
  // //   // initialise plugin
  // var iti = window.intlTelInput(input, {
  //   utilsScript: "libs/intl-tel-input/build/js/utils.js"
  // });

  // //   // here, the index maps to the error code returned from getValidationError - see readme
  // var errorMap = ["Invalid number", "Invalid country code", "Too short", "Too long", "Invalid number"];

  // //   // FOR ACCOUNT-SIGN-IN-COVER2.HTML
  $("#phoneNumber-0").intlTelInput({
    // preferredCountries: ["us", "ca"],
    separateDialCode: false,
    initialCountry: "az",
    autoPlaceholder: "polite",
    // allowDropdown: false,

    // separateDialCode: true,

  });

//  let countryDialCodeDefault = $("#phoneNumber-0").intlTelInput("getSelectedCountryData").dialCode;


//   $("#phoneNumber-0").val('+' + countryDialCodeDefault);
//   input.addEventListener('countrychange', function () {

//     var countryDialCodeDefault = $("#phoneNumber-0").intlTelInput("getSelectedCountryData").dialCode;
//     console.log(countryDialCodeDefault);
//     $("#phoneNumber-0").val('+' + countryDialCodeDefault);

//   });

//   let reset = function () {
//     input.classList.remove("error");
//     errorMsg.innerHTML = "";
//     errorMsg.classList.add("valid-hide");
//     // validMsg.classList.add("valid-hide");
//     validCheckDefault.classList.add("valid-hide");
//   };



//   //   // on blur: validate
//   input.addEventListener('blur', function () {
//     console.log(validCheckDefault)
//     reset();
//     if (input.value.trim()) {

//       if (iti.isValidNumber()) {
//         // validMsg.classList.remove("valid-hide");
//         validCheckDefault.classList.remove("valid-hide");
//       } else {
//         input.classList.add("error");
//         let errorCode = iti.getValidationError();
//         errorMsg.innerHTML = errorMap[errorCode];
//         errorMsg.classList.remove("valid-hide");
//       }
//     }
//   });


//   // on keyup / change flag: reset
//   input.addEventListener('change', reset);
//   input.addEventListener('keyup', reset);


var minLength = 6;

$("#phoneNumber-0").val('+994' );
$('#phoneNumber-0').on('keydown keyup change', function(){
  var charLength = $(this).val().length;
  if(charLength < minLength){
      $('.error-msg-0').text('Minimum '+minLength+' required.');
      $(".valid-check-0").addClass("valid-hide");
  }else if(charLength > minLength){
     $(".valid-check-0").removeClass("valid-hide");
      $('.error-msg-0').text('');
  }
});

$('#phoneNumber-0').on('keypress', function(evt){
  var charCode = (evt.which) ? evt.which : event.keyCode
  if (charCode != 43 && charCode > 31 && (charCode < 48 || charCode > 57))
     return false;

  return true;
 
});




  $("#phoneNumber-4").intlTelInput({
    // preferredCountries: ["us", "ca"],
    separateDialCode: false,
    initialCountry: "az",
    autoPlaceholder: "polite",
    // allowDropdown: false,

    // separateDialCode: true,

  });




$("#phoneNumber-4").val('+994' );
$('#phoneNumber-4').on('keydown keyup change', function(){
  var charLength = $(this).val().length;
  if(charLength < minLength){
      $('.error-msg-4').text('Minimum '+minLength+' required.');
      $(".valid-check-4").addClass("valid-hide");
  }else if(charLength > minLength){
     $(".valid-check-4").removeClass("valid-hide");
      $('.error-msg-4').text('');
  }
});

$('#phoneNumber-4').on('keypress', function(evt){
  var charCode = (evt.which) ? evt.which : event.keyCode
  if (charCode != 43 && charCode > 31 && (charCode < 48 || charCode > 57))
     return false;

  return true;

});

});