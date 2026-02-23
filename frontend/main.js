document.getElementById("greetBtn").onclick = async () => {
  const name = document.getElementById("name").value
  const res = await fetch(`/api/greet?name=${name}`)
  const data = await res.json()
  document.getElementById("output").innerText = data.message
}