const socket = new WebSocket("ws://"+window.location.host+"/reviews")
const reviewholder = document.getElementById("posted-reviews")

socket.onmessage = (e) => {
     addReviewToList(JSON.parse(e.data))
};

function reviewHTML(dataJson){
     let msg = dataJson["review"]
     let user = dataJson['username']
     let reviewId = dataJson['id'] 
     let htmlRet = `<div class='review_holder' id='${reviewId}}'>\n<h3>${user}</h3>\n<p>${msg}<\\p>\n<\\div>`  
     return htmlRet
}

function addReviewToList(dataJson){
     reviewholder.innerHTML += reviewHTML(dataJson)
     reviewholder.scrollIntoView(false);
     reviewholder.scrollTop = reviewholder.scrollHeight - reviewholder.clientHeight;
}

function obtainReviews(){
     const request = new XMLHttpRequest();
     const scrollPosition = window.scrollY;
     request.onreadystatechange = function () {
          if (this.readyState === 4 && this.status === 200) {
              const recipes = JSON.parse(this.response);
              console.log(recipes)
              for (const recipe of recipes) {
                  addReviewToList(recipe);
              }
              window.scrollTo(0, scrollPosition);       
          }
      } 

      request.open("GET","/getReviews")
      request.send()
}

function sendReview(){
    let review = document.getElementById("reviewInput")
    socket.send(review)
}

