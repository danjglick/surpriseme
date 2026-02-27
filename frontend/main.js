const zipcode = "02118"
const album_genre = "rock"
const movie_genre = "comedy"

const config = {
    go_options: [
        { label: "a bar", endpoint: "bars", params: { zipcode } },
        { label: "a restaurant", endpoint: "restaurants", params: { zipcode } },
        { label: "a park", endpoint: "parks", params: { zipcode } },
        { label: "an art gallery", endpoint: "galleries", params: { zipcode } },
        { label: "a bakery", endpoint: "bakeries", params: { zipcode } },
        { label: "a bookstore", endpoint: "bookstores", params: { zipcode } },
        { label: "a campground", endpoint: "campgrounds", params: { zipcode } },
        { label: "a museum", endpoint: "museums", params: { zipcode } },
        { label: "a nightclub", endpoint: "nightclubs", params: { zipcode } },
        { label: "a movie theater", endpoint: "theaters", params: { zipcode } },
        { label: "a cafe", endpoint: "cafes", params: { zipcode } },
        { label: "a tourist attraction", endpoint: "attractions",  params: { zipcode } },
        { label: "an amusement park", endpoint: "amusement_parks",params: { zipcode } },
        { label: "a bowling alley", endpoint: "bowling_alleys", params: { zipcode } }
    ],
    watch_options: [
        { label: "a movie", endpoint: "movies", params: { movie_genre } }
    ],
    listen_options: [
        { label: "an album", endpoint: "albums", params: { album_genre } }
    ]
}

const trigger_and_target_pairs_for_hiding = [
    ["go", "go_options"], 
    ["watch", "watch_options"], 
    ["listen", "listen_options"],
    ["read", "read_options"],
    ["make", "make_options"],
    ["friend", "friend_options"]
]

for (const [containerId, items] of Object.entries(config)) {
    const container = document.getElementById(containerId);
    for (const item of items) {
        const row = document.createElement("p")
        row.innerHTML = `<span>with ${item.label}</span><button>-></button><p>`
        row.querySelector("button").addEventListener("click", async () => {
            document.querySelectorAll(".result").forEach(element => element.remove())
            const params = typeof item.params === "function" ? item.params() : item.params
            const query = new URLSearchParams(params).toString()
            const response = await fetch(`/api/${item.endpoint}?${query}`)
            const data = await response.json()
            for (let i = 0; i < data.message.length; i++) {
                const obj = data.message[i]
                const name = document.createElement("div")
                const disambiguator = document.createElement("div")
                const description = document.createElement("div")
                name.className = "result"
                disambiguator.className = "result"
                description.className = "result"
                name.innerText = obj.name
                disambiguator.innerText = obj.disambiguator
                description.innerText = obj.description
                if (i > 0) {
                    const br = document.createElement("br")
                    br.className = "result"
                    row.appendChild(br)
                }
                row.appendChild(name)
                row.appendChild(disambiguator)
                row.appendChild(description)
            }
        })
        container.appendChild(row)
    }
}

trigger_and_target_pairs_for_hiding.forEach(([triggerId, targetId]) => {
    document.getElementById(triggerId).addEventListener("click", () => {
        const element = document.getElementById(targetId)
        element.hidden = !element.hidden
    })
})