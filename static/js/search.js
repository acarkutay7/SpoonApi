const searchForm = document.querySelector('#search-form');
const mainSection = document.querySelector('main');

// add an event listener to the search form's submit
searchForm.addEventListener('submit', event => {
    event.preventDefault();

    // get the search query from the form's input element
    const searchQuery = document.querySelector('#searcy-query').value;

    // send a get request to the flask api using fetch()
    fetch('/recipes/search/${searchQuery}')
    .then(response => response.json())
    .then(data => 
        {
            // Once the response is received, display the results in the main section of the page
            displayResults(data);
        })
        .catch(error => console.error(error))
});

// Function to display the search results in the main section
function displayResults(results){
    // Clear any existing results from the main section
    mainSection.innerHTML = 'pasta';

    // Loop through the search results and create a new HTML element for each result
    results.forEach(result => {
        const resultElement = document.createElement('div');
        resultElement.innerHTML =
        <h2>${result.name}</h2>
        resultElement.innerHTML = `
      <h2>${result.name}</h2>
      <img src="${result.image}" alt="${result.name}">
      <ul>
        ${result.ingredients.map(ingredient => `<li>${ingredient}</li>`).join('')}
      </ul>
      <button data-id="${result.id}" data-name="${result.name}" data-image="${result.image}">Save recipe</button>
    `;
    main.appendChild(resultElement);
    })

}