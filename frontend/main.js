document.getElementById("greetBtn").onclick = async () => {
  const name = document.getElementById("name").value
  const res = await fetch(`http://localhost:8000/api/greet?name=${name}`)
  const data = await res.json()
  document.getElementById("output").innerText = data.message
}