const zipcode = "02118"
const album_genre = "rock"
const movie_genre = "comedy"
const lat = "42.364661"
const lng = "-71.032229"

const config = {
    go_options: [
        { label: "a walk", endpoint: "walk", params: { lat, lng } },
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
        { label: "a movie", endpoint: "movies", params: { movie_genre } },
        { label: "a tv show" },
        { label: "live sports" },
        { label: "a youtube channel" },
    ],
    listen_options: [
        { label: "an album", endpoint: "albums", params: { album_genre } },
        { label: "a podcast" },
        { label: "an audiobook" }
    ], 
    read_options: [
        { label: "a book" },
        { label: "a news source" },
        { label: "a wikipedia article" },
        { label: "a subreddit" },
    ],
    make_options: [
        { label: "a recipe" },
        { label: "a craft project" },
        { label: "a science project" },
        { label: "a game" },
    ],
    connection_options: [
        { label: "a new friend" },
        { label: "an event" },
        { label: "a meetup group" },
        { label: "a class" },
        { label: "a debate" },
    ]
}

const trigger_and_target_pairs_for_hiding = [
    ["go", "go_options"], 
    ["watch", "watch_options"], 
    ["listen", "listen_options"],
    ["read", "read_options"],
    ["make", "make_options"],
    ["connection", "connection_options"],
]

for (const [containerId, items] of Object.entries(config)) {
    const container = document.getElementById(containerId);
    for (const item of items) {
        const section = document.createElement("p")
        section.innerHTML = `<span>with ${item.label}</span>&nbsp;<button>-></button><p>`
        section.querySelector("button").addEventListener("click", async () => {
            document.querySelectorAll(".result").forEach(element => element.remove())
            const params = typeof item.params === "function" ? item.params() : item.params
            const query = new URLSearchParams(params).toString()
            const response = await fetch(`/api/${item.endpoint}?${query}`)
            const data = await response.json()
            for (let i = 0; i < data.message.length; i++) {
                result = data.message[i] 

                const scrollRow = document.createElement("div"); scrollRow.className = "scroll-row"
                for (let j = 0; j < result.photos.length; j++) {
                    const photo = document.createElement("img")
                    photo.className = "result"
                    photo.src = result.photos[j]
                    scrollRow.appendChild(photo)
                }
                section.append(scrollRow)
                
                const name = document.createElement("div")
                name.className = "result"
                name.innerText = result.name
                section.appendChild(name)
                
                const actionInfo = document.createElement("span")
                actionInfo.classList.add("result", "availability")
                actionInfo.innerText = "Open now"
                for (let i = 0; i < result.links.length; i++) {
                    const link = document.createElement("a")
                    link.className = "result"
                    link.href = result.links[i].href
                    link.target = "_blank"
                    const icon = document.createElement("img")
                    icon.className = "result"
                    icon.src = result.links[i].src
                    console.log(result.links[i].href)
                    link.appendChild(icon)
                    actionInfo.appendChild(link)
                }
                section.appendChild(actionInfo)

                const description = document.createElement("div")
                description.className = "result"
                description.innerText = result.description
                section.appendChild(description)
                
                if (i < 2) {
                    const blankLine = document.createElement("br")
                    blankLine.className = "result"
                    section.appendChild(blankLine)
                }
            }
        })
        container.appendChild(section)
    }
}

trigger_and_target_pairs_for_hiding.forEach(([triggerId, targetId]) => {
    const trigger = document.getElementById(triggerId)
    const target = document.getElementById(targetId)
    trigger.addEventListener("click", () => {
        target.hidden = !target.hidden
        const chevron = trigger.querySelector(".chevron")
        chevron.textContent = target.hidden ? "▶" : "▼"
    })
})