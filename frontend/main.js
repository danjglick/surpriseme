const zipcode = "02128"

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
        { label: "a movie", endpoint: "movies", params: () => ({ movie_genre: window.movie_genre }) },
    ],
    listen_options: [
        { label: "an album", endpoint: "albums", params: () => ({ album_genre: window.album_genre }) }
    ]
}

const trigger_and_target_pairs_for_hiding = [
    ["go", "go_options"], 
    ["watch", "watch_options"], 
    ["listen", "listen_options"]
]

for (const [containerId, items] of Object.entries(config)) {
    const container = document.getElementById(containerId);
    for (const item of items) {
        const row = document.createElement("div");
        const output = document.createElement("p");
        row.innerHTML = `<span>with ${item.label}</span><button>-></button>`;
        row.querySelector("button").addEventListener("click", async () => {
            const params = typeof item.params === "function" ? item.params() : item.params
            const query = new URLSearchParams(params).toString();
            const res = await fetch(`/api/${item.endpoint}?${query}`);
            const data = await res.json();
            output.innerText = data.message;
        });
        row.appendChild(output);
        container.appendChild(row);
    }
}

trigger_and_target_pairs_for_hiding.forEach(([triggerId, targetId]) => {
    document.getElementById(triggerId).addEventListener("click", () => {
        const element = document.getElementById(targetId);
        element.hidden = !element.hidden;
    })
})