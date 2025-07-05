const searchbox = document.querySelector('.searchbox');
const searchbtn = document.querySelector('.searchbtn');
const recipeContainer = document.querySelector('.recipe-container');
const recipeDetailsContent = document.querySelector('.recipe-details-content');
const recipeCloseBtn = document.querySelector('.recipe-close-btn');

// function to get recipes

const fetchRecipes = async(query) => {
    recipeContainer.innerHTML="<h2>Loading...</h2>";
    try{
    const data = await fetch (`https://www.themealdb.com/api/json/v1/1/search.php?s=${query}`);
    const response = await data.json();

    recipeContainer.innerHTML="";
    response.meals.forEach(meal => {
        const recipediv = document.createElement('div');
        recipediv.classList.add('recipe');
        recipediv.innerHTML=`
        <img src="${meal.strMealThumb}">
        <h3>${meal.strMeal}</h3>
        <p><span>${meal.strArea}</span> Dish</p>
        <p>Belongs to <span>${meal.strCategory}</span> Category</p>`

        const button = document.createElement('button');
        button.textContent="View Recipe";
        recipediv.appendChild(button);

        //Adding EventListner to recipe button
        button.addEventListener('click', ()=>{
            openRecipePopup(meal);

        });
        recipeContainer.appendChild(recipediv);
    });
} catch(error){
     recipeContainer.innerHTML="<h2>Error in Fetching Recipes...</h2>";

}

}
//function to fetch ingredients and measurements 
const fetchIngredients = (meal) =>{
    console.log(meal);
    let ingredientList="";
    for (let i=1; i<=20; i++){
        const ingredients = meal[`strIngredient${i}`];
        if(ingredients){
            const measure=meal[`strMeasure${i}`];
            ingredientList += `<li>${measure} ${ingredients}</li>`
        }
        else{
            break;
        }
    }
    return ingredientList;
}
const openRecipePopup =(meal) =>
{
    recipeDetailsContent.innerHTML=`
    <h2 class="recipeName">${meal.strMeal}</h2>
    <h3>Ingredients:</h3>
    <ul class="ingredientList">${fetchIngredients(meal)}</ul>
    <div class="recipeInstructions">
        <h3>Instructions:</h3>
        <p>${meal.strInstructions}</p>
    </div>
    `
    
    recipeDetailsContent.parentElement.style.display="block";

}
recipeCloseBtn.addEventListener('click', ()=>{
    recipeDetailsContent.parentElement.style.display="none";

});
searchbtn.addEventListener('click',(e)=>{
    e.preventDefault();
    const searchinput = searchbox.value.trim();
    if (!searchinput){
        recipeContainer.innerHTML=`<h2>Type the meal in the search box.</h2>`;
        return;
    }
    fetchRecipes(searchinput);
});