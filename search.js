
function search_query_function(){
    const query = document.getElementById("search_query").value;
    fetch(`/search?query=${query}`)
        .then(response => response.json())
        .then(data => { 
            console.log(data)
            let returnedURLs = document.getElementById("urls");
            returnedURLs.innerHTML = "";

                data.results.forEach(item => {
                    let li = document.createElement("li");
                    li.textContent = item;
                    returnedURLs.appendChild(li);
                });
            })
        .catch(error => console.error("Error fetching search results:", error));
}
