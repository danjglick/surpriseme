document.getElementById("venueBtn").onclick = async () => {
    const zipcode = document.getElementById("zipcode").value
    const response = await fetch(`/api/venue?zipcode=${zipcode}`)
    const data = await response.json()
    document.getElementById("output").innerText = data.message
}