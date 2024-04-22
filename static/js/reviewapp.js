let socket = io('https://'+window.location.host,{
     secure: true
     }
)

// let socket = io()

const reviewholder = document.getElementById("posted-reviews")
let Globalusername = ""

socket.on('connect',(e)=>{
     console.log('a')
})

socket.on('reviewMessage', function (e) {
          console.log(`MESSAGE RECIEVED ${e.username}`)
          addReviewToList(e,true)
     }
);

function reviewHTML(dataJson,dataTypeObject=false){
     let username = ""
     let msg = ""
     let reviewId = ""
     if(dataTypeObject){
          username = dataJson.username 
          msg = dataJson.review
          reviewId = dataJson.id 
     }
     else{
          username = dataJson['username']
          msg = dataJson['review']
          reviewId = dataJson['id']
     }
     
     let htmlRet = `<div class='review_holder' id='${reviewId}}'>\n<h3>Reviewer: ${username}</h3>\n<p>${msg}</p>\n</div>`  
     return htmlRet
}

function addReviewToList(dataJson,ObjectDataType = false){
     reviewholder.innerHTML += reviewHTML(dataJson,ObjectDataType)
     reviewholder.scrollIntoView(false);
     reviewholder.scrollTop = reviewholder.scrollHeight - reviewholder.clientHeight;
}

async function obtainReviews(){
     const request = new XMLHttpRequest();
     const usernameRequest = new XMLHttpRequest();
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

     usernameRequest.onreadystatechange = function () {
          if (this.readyState === 4 && this.status === 200){
               const jsondata = JSON.parse(this.response)
               Globalusername = jsondata['username']
          }
     }
     
     await usernameRequest.open('GET','/obtainUsername')
     await usernameRequest.send()
     request.open("GET","/getReviews")
     request.send()
}

function sendReview(){
    let review = document.getElementById("reviewInput").value
    socket.emit('message',{'data':review,'username':Globalusername})
    document.getElementById("reviewInput").value = ""
}

