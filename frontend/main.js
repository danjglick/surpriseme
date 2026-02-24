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

document.getElementById("gallery_btn").onclick = async () => {
    const zipcode = document.getElementById("zipcode_for_gallery").value
    const response = await fetch(`/api/galleries?zipcode=${zipcode}`)
    const data = await response.json()
    document.getElementById("gallery_output").innerText = data.message
}

document.getElementById("bakery_btn").onclick = async () => {
    const zipcode = document.getElementById("zipcode_for_bakery").value
    const response = await fetch(`/api/bakeries?zipcode=${zipcode}`)
    const data = await response.json()
    document.getElementById("bakery_output").innerText = data.message
}

document.getElementById("bookstore_btn").onclick = async () => {
    const zipcode = document.getElementById("zipcode_for_bookstore").value
    const response = await fetch(`/api/bookstores?zipcode=${zipcode}`)
    const data = await response.json()
    document.getElementById("bookstore_output").innerText = data.message
}

document.getElementById("campground_btn").onclick = async () => {
    const zipcode = document.getElementById("zipcode_for_campground").value
    const response = await fetch(`/api/campgrounds?zipcode=${zipcode}`)
    const data = await response.json()
    document.getElementById("campground_output").innerText = data.message
}

document.getElementById("museum_btn").onclick = async () => {
    const zipcode = document.getElementById("zipcode_for_museum").value
    const response = await fetch(`/api/museums?zipcode=${zipcode}`)
    const data = await response.json()
    document.getElementById("museum_output").innerText = data.message
}

document.getElementById("nightclub_btn").onclick = async () => {
    const zipcode = document.getElementById("zipcode_for_nightclub").value
    const response = await fetch(`/api/nightclubs?zipcode=${zipcode}`)
    const data = await response.json()
    document.getElementById("nightclub_output").innerText = data.message
}

document.getElementById("theater_btn").onclick = async () => {
    const zipcode = document.getElementById("zipcode_for_theater").value
    const response = await fetch(`/api/theaters?zipcode=${zipcode}`)
    const data = await response.json()
    document.getElementById("theater_output").innerText = data.message
}

document.getElementById("cafe_btn").onclick = async () => {
    const zipcode = document.getElementById("zipcode_for_cafe").value
    const response = await fetch(`/api/cafes?zipcode=${zipcode}`)
    const data = await response.json()
    document.getElementById("cafe_output").innerText = data.message
}

document.getElementById("attraction_btn").onclick = async () => {
    const zipcode = document.getElementById("zipcode_for_attraction").value
    const response = await fetch(`/api/attractions?zipcode=${zipcode}`)
    const data = await response.json()
    document.getElementById("attraction_output").innerText = data.message
}

document.getElementById("amusement_park_btn").onclick = async () => {
    const zipcode = document.getElementById("zipcode_for_amusement_park").value
    const response = await fetch(`/api/amusement_parks?zipcode=${zipcode}`)
    const data = await response.json()
    document.getElementById("amusement_park_output").innerText = data.message
}

document.getElementById("bowling_alley_btn").onclick = async () => {
    const zipcode = document.getElementById("zipcode_for_bowling_alley").value
    const response = await fetch(`/api/bowling_alleys?zipcode=${zipcode}`)
    const data = await response.json()
    document.getElementById("bowling_alley_output").innerText = data.message
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