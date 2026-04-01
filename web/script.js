let filmsData = []

fetch("films.json")
    .then(res => res.json())
    .then(data => {
        data.sort((a, b) => b.box_office - a.box_office)
        filmsData = data
        render(data)
        renderChart(data)
    })

function formatMoney(value) {
    return "$" + value.toLocaleString()
}

function getFlag(country) {
    return country
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

function renderChart(data) {
    const counts = {}

    data.forEach(film => {
        counts[film.release_year] = (counts[film.release_year] || 0) + 1
    })

    const labels = Object.keys(counts).sort((a, b) => a - b)
    const values = labels.map(year => counts[year])

    const ctx = document.getElementById('filmsChart').getContext('2d')
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Top Films',
                data: values,
                backgroundColor: 'rgba(54, 162, 235, 0.7)'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    stepSize: 1
                }
            }
        }
    })
}