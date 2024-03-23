


function recipeHTML(recipeJSON){
    const username = recipeJSON.user;
    const recipeID = recipeJSON.id;
    const name = recipeJSON.name;
    const description = recipeJSON.description;
    const instructions = recipeJSON.instructions;
    const ingredients = recipeJSON.ingredients;
    let detailsHTML = "<br><button onclick='likeRecipe(\"" + recipeID + "\")'>👍</button> ";
    detailsHTML += "<span id='recipe_" + recipeID + "'><b>" + username + "</b> presents-- " + name + "<br>Description:<br>" + description + "<br>Ingredients:<br>" + ingredients + "<br>Instructions:<br>" + instructions + "</span>";
    return detailsHTML;
}


function addRecipiesToList(recipeJSON) {
    const recipes = document.getElementById("posted-recipes");
    recipes.innerHTML += recipeHTML(recipeJSON);
    recipes.scrollIntoView(false);
    recipes.scrollTop = recipes.scrollHeight - recipes.clientHeight;
}

function sendRecipe() {
    const recipeBox = document.getElementById("recipe-form");
    const recipe = recipeBox.value;
    recipeBox.value = "";

    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200){
            console.log(this.response)
        }
    }
    const recipeJSON = {"recipe": recipe}
    request.open("POST","/submit");
    request.send(JSON.stringify(recipeJSON));
    
    recipeBox.focus();

}

function clearRecipes() {
    const recipes = document.getElementById("posted-recipes");
    recipes.innerHTML = "";
}


function updateRecipes() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            clearRecipes();
            const recipes = JSON.parse(this.response);
            for (const recipe of recipes) {
                addRecipiesToList(recipe);
            }
        }
    }
    request.open("GET", "/recipe");
    request.send();
}

function likeRecipe(recipeID) {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200){
            HTMLFormControlsCollection.log(this.response);
        }
    }
    request.open("POST", "/likeRecipe/" + recipeID);
    request.send();
}



function loginLoaded() {
    document.getElementById("words").innerHTML += "<br/> Javascript says healthy recipes are the foundation of a good diet";

}

function homeLoaded(){
    document.getElementById("jsText").innerHTML +="<br/> Have been waiting for you";

    updateRecipes();
}



