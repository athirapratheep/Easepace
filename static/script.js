document.addEventListener("DOMContentLoaded", function() {
    var h1Element = document.querySelector("header h1");
    var letters = h1Element.textContent.split("");
  
    h1Element.innerHTML = ""; // Clear the content of the h1 element
  
    letters.forEach(function(letter, index) {
      var span = document.createElement("span");
      span.textContent = letter;
  
      if (index === 1 || index === 3 ) {
        span.classList.add("letter-green");
      } 
      
  
      h1Element.appendChild(span);
    });
  });
  