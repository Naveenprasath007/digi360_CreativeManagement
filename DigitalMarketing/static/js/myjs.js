// function showname () {
//     var name = document.getElementById('file-upload'); 
//     alert('Selected file: ' + name.files.item(0).name);
//     alert('Selected file: ' + name.files.item(0).size);
//     alert('Selected file: ' + name.files.item(0).type);
//   };

function choosefile() {
  var element = document.getElementById("accountSection");
  element.classList.toggle("active");
}


function GetFileSizeNameAndType()
    {
    var fi = document.getElementById('file-upload'); // GET THE FILE INPUT AS VARIABLE.

    var totalFileSize = 0;

    // VALIDATE OR CHECK IF ANY FILE IS SELECTED.
    if (fi.files.length > 0)
    {
        var fsize = fi.files.item(0).size;
        totalFileSize = totalFileSize + fsize;
    }
    document.getElementById('divTotalSize').innerHTML ='<br /> ' + 'File Name is <b>' + fi.files.item(0).name + "</b> Total File(s) Size is <b>" + Math.round(totalFileSize / 1024*0.0009765625) + "</b> MB" +'</b> and File Type is <b>' + fi.files.item(0).type + "</b>.";
}

// function requiredchecklist() {
//   var x = document.getElementById("myCheck").required;
// }




function myFunction() {
    var element = document.getElementById("accountSection");
    element.classList.toggle("active");
 }

 $('.messege-info').hide().fadeIn(500).delay(2000).fadeOut(500);  


 $(document).ready(function(){
    $("select").change(function(){
        $(this).find("option:selected").each(function(){
            var optionValue = $(this).attr("value");
            if(optionValue){
                $(".box").not("." + optionValue).hide();
                $("." + optionValue).show();
            } else{
                $(".box").hide();
            }
        });
    }).change();
  });







  $("input[type='radio']").change(function(){
   
    if($(this).val()=="No")
    {
        $("#btncolor").hide();
        $("#btncolor1").show();
        $("#Reason").attr('required', '');
        
    }
    else
    {
           $("#btncolor").show();
           $("#btncolor1").hide();
           $("#Reason").removeAttr('required', '');


    }
        
    });


    

    // color changing
    // $("input[type='radio']").change(function(){
   
    //   if($(this).val()=="No")
    //   {
    //     var element = document.getElementById("btncolor");
    //     element.classList.toggle("approval");;
    //   }
    //   else
    //   {
    //     var element = document.getElementById("btncolor");
    //     element.classList.toggle("rejected");;
    //   }
          
    //   });






// list and grid view
    $(document).ready(function(){
        $("#hide").click(function(){
          $("#Listview").hide();
        });
        $("#hide").click(function(){
          $("#Gridview").show();
        });
      });

      $(document).ready(function(){
        $("#show").click(function(){
          $("#Gridview").hide();
        });
        $("#show").click(function(){
          $("#Listview").show();
        });
      });

// File Search
      function filterDivisions() {
        var input, filter, divisions, division, i, txtValue;
        input = document.getElementById("search-input");
        filter = input.value.toUpperCase();
        divisions = document.getElementById("Listview");
        division = divisions.getElementsByClassName("finding");

        for (i = 0; i < division.length; i++) {
          txtValue = division[i].textContent || division[i].innerText;
          if (txtValue.toUpperCase().indexOf(filter) > -1) {
            division[i].style.display = "";
          } else {
            division[i].style.display = "none";
          }
        }
      }

    
// Load spinner

  $(window).on('load', function () {
    $('#loading').hide();
  }) 


  function loaded() {
    $("#loading-message").show();
  }


function selectImage(element, imageId) {
    const selectedImageInput = document.getElementById('selectedImage');
    const selectedImages = document.getElementsByClassName('selected');
    Array.from(selectedImages).forEach(img => img.classList.remove('selected'));
    element.classList.add('selected');
    selectedImageInput.value = imageId;
  }

function selectImage1(element, imageId) {
    const selectedImageInput = document.getElementById('selectedImage1');
    const selectedImages = document.getElementsByClassName('selected1');
    Array.from(selectedImages).forEach(img => img.classList.remove('selected1'));
    element.classList.add('selected1');
    selectedImageInput.value = imageId;
  }




  tinymce.init({
    selector: 'textarea#default',
    width: 1000,
    height: 300,
    plugins:[
        'advlist', 'autolink', 'link', 'image', 'lists', 'charmap', 'prewiew', 'anchor', 'pagebreak',
        'searchreplace', 'wordcount', 'visualblocks', 'code', 'fullscreen', 'insertdatetime', 'media', 
        'table', 'emoticons', 'template', 'codesample'
    ],
    toolbar: 'undo redo | styles | bold italic underline | alignleft aligncenter alignright alignjustify |' + 
    'bullist numlist outdent indent | link image | print preview media fullscreen | ' +
    'forecolor backcolor emoticons',
    menu: {
        favs: {title: 'menu', items: 'code visualaid | searchreplace | emoticons'}
    },
    menubar: 'favs file edit view insert format tools table',
    content_style: 'body{font-family:Helvetica,Arial,sans-serif; font-size:16px}'
});



