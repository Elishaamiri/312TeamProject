
// this will be for sending form data

function shareRecipe() {
    const recipeName = document.getElementById("recipeName")
    const recipeDesc = document.getElementById("recipeDescription")
    const recipeIngr = document.getElementById("recipeIngredients")
    const recipeInstruct = document.getElementById("recipeInstructions")
    
    const name = recipeName.value;
    const desc = recipeDesc.value;
    const ingr = recipeIngr.value;
    const instruct = recipeInstruct.value;

    const request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            console.log(this.response);
        }
    }
    const package = {}
    package["recipeName"] = name;
    package["recipeDescription"] = desc;
    package["recipeIngredients"] = ingr;
    package["recipeInstructions"] = instruct;
    request.open("POST", "/recipes");
    request.send(JSON.stringify(package));
}