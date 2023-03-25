$('#menuClick').on('change', function() {
    if ($('#menuClick').is(':checked')) {
        $('.menuContainer').css('left', '50%');
        $('.menuContainer').css('box-shadow', '20px 0 125px #000');
        $('#header').css('filter', 'blur(15px)', 'filter', 'brightness(50%)');
    } else {
        $('.menuContainer').css('left', '100%');
        $('.menuContainer').css('box-shadow', '0px 0 0px #000');
        $('#header').css('filter', 'blur(0px)', 'filter', 'brightness(100%)');
    }
});

$(document).on('mousemove', function(e){
    $('#cursor').css({
       left:  e.pageX,
       top:   e.pageY
    });
});

$('#menuIcon').on('mouseover', function(){
    $('#cursor').css({
        width: '60px',
        height: '60px'
    })
})

$('#menuIcon').on('mouseleave', function(){
    $('#cursor').css({
        width: '10px',
        height: '10px'
    })
})

$('.menuLink').on('mouseover', function(){
    $('#cursor').css({
        width: '0px',
        height: '0px'
    })
})

$('.menuLink').on('mouseleave', function(){
    $('#cursor').css({
        width: '10px',
        height: '10px'
    })
})

$('.contact').on('mouseover', function(){
    $('#cursor').css({
        width: '0px',
        height: '0px'
    })
})

$('.contact').on('mouseleave', function(){
    $('#cursor').css({
        width: '10px',
        height: '10px'
    })
})

$('#emailUsLink').on('mouseover', function(){
    $('#cursor').css({
        width: '30px',
        height: '30px'
    })
})

$('#emailUsLink').on('mouseleave', function(){
    $('#cursor').css({
        width: '10px',
        height: '10px'
    })
})

$(document).on('mousedown', () => {
    $('#cursor').css({
        transform: 'scale(1.5) translate(-25%,-25%)'
    })
})

$(document).on('mouseup', () => {
    $('#cursor').css({
        transform: 'scale(1) translate(-50%,-50%)'
    })
})

function toggleUploadForm() {
  const uploadFormContainer = document.getElementById("uploadFormContainer");
  const chatBoxContainer = document.getElementById("chatBoxContainer");

  if (uploadFormContainer.style.display === "none") {
    uploadFormContainer.style.display = "block";
    chatBoxContainer.style.display = "none";
  } else {
    uploadFormContainer.style.display = "none";
  }
}

function toggleChatBox() {
  const uploadFormContainer = document.getElementById("uploadFormContainer");
  const chatBoxContainer = document.getElementById("chatBoxContainer");

  if (chatBoxContainer.style.display === "none") {
    chatBoxContainer.style.display = "block";
    uploadFormContainer.style.display = "none";
  } else {
    chatBoxContainer.style.display = "none";
  }
}

$(document).ready(function() {
  $("#chatForm").on("submit", function(event) {
    event.preventDefault();

    let userMessage = $("#userMessage").val();

    $.ajax({
        url: "/send_message",
        method: "POST",
        data: {
            user_message: userMessage
        },
        success: function(response) {
            // Display the user message in the middle of the webpage
            const resultDiv = document.getElementById("searchResults");
            resultDiv.innerHTML = response.message;
        }
    });
  });
  $("#toggleUploadFormButton").on("click", toggleUploadForm);
  $("#toggleChatBoxButton").on("click", toggleChatBox);
});


//$(document).ready(function() {
//  $("#chatForm").on("submit", function(event) {
//    event.preventDefault();
//
//    let userMessage = $("#userMessage").val();
//
//    $.ajax({
//        url: "/send_message",
//        method: "POST",
//        data: {
//            user_message: userMessage
//        },
//        success: function(response) {
//            displayResults(response);
//        }
//    });
//  });
//  $("#toggleUploadFormButton").on("click", toggleUploadForm);
//  $("#toggleChatBoxButton").on("click", toggleChatBox);
//});

function displayResults(response) {
    const resultsContainer = document.getElementById("resultsContainer");
  
    // Clear any previous results
    resultsContainer.innerHTML = "";
  
    // Iterate over the results and display them
    for (const result of response.results) {
      const resultDiv = document.createElement("div");
      resultDiv.classList.add("text-block");
      resultDiv.innerHTML = result.page_content;
      resultsContainer.appendChild(resultDiv);
    }
  }
  




$(document).on('mousemove', e => {
    $('#bubble:nth-child(1)').css({
        top: (50 + e.pageY/250 + '%'),
        left: (50 + (e.pageX)/350 + '%')
    })

    $('#bubble:nth-child(2)').css({
        top: (40 + e.pageY/200 + '%'),
        left: (40 + (e.pageX)/225 + '%')
    })

    $('#bubble:nth-child(3)').css({
        top: (60 + e.pageY/500 + '%'),
        left: (60 - (e.pageX)/450 + '%')
    })

    $('#bubble:nth-child(4)').css({
        top: (40 - e.pageY/250 + '%'),
        left: (60 - (e.pageX)/400 + '%')
    })

    $('#bubble:nth-child(5)').css({
        top: (60 - e.pageY/350 + '%'),
        left: (40 + (e.pageX)/250 + '%')
    })

    $('#bubble:nth-child(6)').css({
        top: (40 - e.pageY/400 + '%'),
        left: (50 + (e.pageX)/500 + '%')
    })

    $('#bubble:nth-child(7)').css({
        top: (60 + e.pageY/400 + '%'),
        left: (50 + (e.pageX)/500 + '%')
    })

    $('#bigLetter').css({
        left: (80 - e.pageX/500 + '%')
    })
})