let filmsData = []

fetch("./data/films.json")
    .then(res => res.json())
    .then(data => {
        data.sort((a, b) => b.box_office - a.box_office)
        filmsData = data
        render(data)
        renderCharts(data)
    })

function formatMoney(value) {
    return "$" + value.toLocaleString()
}

function render(data) {
    const tbody = document.getElementById("tableBody")
    tbody.innerHTML = ""

    data.forEach((film, index) => {
        const row = document.createElement("tr")
        row.innerHTML = `
            <td>${film.title}</td>
            <td>${film.release_year}</td>
            <td>${film.director}</td>
            <td>${formatMoney(film.box_office)}</td>
            <td>${film.country}</td>
        `
        row.addEventListener("click", () => openModal(film, index + 1))
        tbody.appendChild(row)
    })
}

document.getElementById("search").addEventListener("input", (e) => {
    const value = e.target.value.toLowerCase()
    const filtered = filmsData.filter(f => f.title.toLowerCase().includes(value))
    render(filtered)
})

function openModal(film, rank) {
    document.getElementById("modal").style.display = "block"
    document.getElementById("modalTitle").innerText = film.title
    document.getElementById("modalRank").innerText = "#" + rank
    document.getElementById("modalYear").innerText = film.release_year
    document.getElementById("modalDirector").innerText = film.director
    document.getElementById("modalCountry").innerText = film.country
    document.getElementById("modalBox").innerText = formatMoney(film.box_office)
}

document.getElementById("close").onclick = () => {
    document.getElementById("modal").style.display = "none"
}

window.onclick = (e) => {
    if (e.target.id === "modal") {
        document.getElementById("modal").style.display = "none"
    }
}

function renderCharts(data) {
    const counts = {}
    const revenue = {}

    data.forEach(f => {
        counts[f.release_year] = (counts[f.release_year] || 0) + 1
        revenue[f.release_year] = (revenue[f.release_year] || 0) + f.box_office
    })

    const labels = Object.keys(counts).sort((a,b) => a-b)
    const countsValues = labels.map(y => counts[y])
    const revenueValues = labels.map(y => revenue[y])
    const avgValues = labels.map(y => revenue[y]/counts[y])

    new Chart(document.getElementById('filmsChart').getContext('2d'), {
        type: 'bar',
        data: { labels, datasets: [{ label: 'Number of Top Films', data: countsValues, backgroundColor: 'rgba(54, 162, 235, 0.7)' }] },
        options: { responsive: true, scales: { y: { beginAtZero: true, stepSize: 1 } } }
    })

    new Chart(document.getElementById('revenueChart').getContext('2d'), {
        type: 'bar',
        data: { labels, datasets: [{ label: 'Total Box Office ($)', data: revenueValues, backgroundColor: 'rgba(255, 99, 132, 0.7)' }] },
        options: { responsive: true, scales: { y: { beginAtZero: true } } }
    })

    const avgCanvas = document.createElement('canvas')
    avgCanvas.id = 'avgChart'
    document.querySelector('.right-column').appendChild(avgCanvas)

    new Chart(avgCanvas.getContext('2d'), {
        type: 'line',
        data: {
            labels,
            datasets: [{ 
                label: 'Average Box Office per Film ($)', 
                data: avgValues, 
                borderColor: 'rgba(75, 192, 192, 1)', 
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.3
            }]
        },
        options: { responsive: true, scales: { y: { beginAtZero: true } } }
    })
}
