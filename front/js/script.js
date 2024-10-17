document.addEventListener("DOMContentLoaded", function() {
    // Cridem a l'endpoint de l'API fent un fetch
    fetch("http://127.0.0.1:8000/alumne/list")
        .then(response => {
            if (!response.ok) {
                throw new Error("Error a la resposta del servidor");
            }
            return response.json();
        })
        .then(data => {
            const alumnesTableBody = document.querySelector("#tablaAlumne tbody");
            alumnesTableBody.innerHTML = ""; // Netejar la taula abans d'afegir res
            
            // Iterar sobre los alumnos y agregarlos al DOM
            data.forEach(alumne => {
                const row = document.createElement("tr");

                Object.values(alumne).forEach(column => {
                    const columnContaier = document.createElement("td");
                    columnContaier.textContent = column;
                    row.appendChild(columnContaier);
                })
                alumnesTableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Error capturat:", error);
            alert("Error al carregar la llista d'alumnes");
        });
});