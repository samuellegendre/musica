// Data - Constants - Statements

const EVENT_JS_CLICK = "click"
const EVENT_JS_SUBMIT = "submit"
const HTTP_METHOD_DELETE = "DELETE"
const HTTP_METHOD_PATCH = "PATCH"
const HTTP_METHOD_PUT = "PUT"
const NUMBER_OBJECTS_PER_PAGE = 10

// Behaviours - Utils
async function sendData(urlEndpoint, httpMethod, data) {
    let response = await fetch(urlEndpoint, {
        method: httpMethod,
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    return response.json()
}

function fetchData(urlEndpoint) {
    return fetch(urlEndpoint).then(response => response.json()).then(data => {
        return data
    })
}

function internationalizeApplication(i18n) {
    for (let [key, value] of Object.entries(i18n)) {
        let element = document.querySelector(key)

        element.textContent = value.toString()
    }
}

function calculateNumberPages(numberObjects) {
    let numberPages = Math.ceil(numberObjects / NUMBER_OBJECTS_PER_PAGE)
    if (numberPages === 0) {
        return 1
    } else {
        return numberPages
    }
}

function updateTable(table, data) {
    let tableBody = ""

    try {
        data.forEach(object => {
            tableBody += "<tr>"

            for (let key in object) {
                tableBody += "<td>" + object[key] + "</td>"
            }

            tableBody += "<td><div class='hstack gap-3'><button type='button' class='btn btn-outline-dark'>" +
                "Modifier</button><button type='button' class='btn btn-outline-danger'>Supprimer</button></div></td></tr>"
        })
    } catch (e) {
    }

    table.innerHTML = tableBody
}

function updateSelect(select, data) {
    let options = ""

    data.forEach(object => {
        options += "<option value='" + object.id + "'>" + object.name + "</option>"
    })

    select.innerHTML = options
}