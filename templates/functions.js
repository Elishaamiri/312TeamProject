


function recipeHTML(recipeJSON){
    const username = recipeJSON.username;
    const recipeID = recipeJSON.id;
    const name = recipeJSON.name;
    // TO DO 3/23/24 
    // finish this shit, make it work, right now this needs to take in the json parse the important info then turn it into valid html text
    let detailsHTML = "<br><button onclick='deleteRecipe(\"" + recipeID + "\")'>X</button> ";
    detailsHTML += "<span id='recipe_" + recipeID + "'><b>" + username + "</b>: " + name + "</span>";
    return detailsHTML;
}


function addRecipiesToList(recipeJSON) {
    const recipes = document.getElementById("posted-recipes");
    recipes.innerHTML += recipeHTML(recipeJSON);
    recipes.scrollIntoView(false);
    recipes.scrollTop = recipes.scrollHeight - recipes.clientHeight;
}

function sendRecipe() {


}