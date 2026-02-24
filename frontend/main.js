document.getElementById("bar_btn").onclick = async () => {
    const zipcode = document.getElementById("zipcode_for_bar").value
    const response = await fetch(`/api/bars?zipcode=${zipcode}`)
    const data = await response.json()
	document.getElementById("bar_output").innerText = data.message
}

document.getElementById("restaurant_btn").onclick = async () => {
    const zipcode = document.getElementById("zipcode_for_restaurant").value
    const response = await fetch(`/api/restaurants?zipcode=${zipcode}`)
    const data = await response.json()
    document.getElementById("restaurant_output").innerText = data.message
}

document.getElementById("park_btn").onclick = async () => {
    const zipcode = document.getElementById("zipcode_for_park").value
    const response = await fetch(`/api/parks?zipcode=${zipcode}`)
    const data = await response.json()
    document.getElementById("park_output").innerText = data.message
}

document.getElementById("movie_btn").onclick = async () => {
	const movie_genre = document.getElementById("movie_genre").value
	const response = await fetch(`/api/movies?movie_genre=${movie_genre}`)
	const data = await response.json()
  	document.getElementById("movie_output").innerText = data.message
}

document.getElementById("album_btn").onclick = async () => {
	const album_genre = document.getElementById("album_genre").value
    const response = await fetch(`/api/albums?album_genre=${album_genre}`)
    const data = await response.json()
    document.getElementById("album_output").innerText = data.message
}