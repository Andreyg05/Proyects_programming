async function callMessage() {
    try {
        const response = await fetch('http://localhost:8000/hello_ud');
        const data = await response.text();
        document.getElementById('result').textContent = data;
    } catch (error) {
        console.error('Error:', error);
    }
}

async function callTable() {
    try {
        const response = await fetch('http://127.0.0.1:8000/products');
        const data = await response.json();

        if (data.length === 0) {
            document.getElementById('result').innerHTML = "<p>No products found</p>";
            return;
        }

        let table = '<table>';
        table += '<tr><th>ID</th><th>Name</th><th>Description</th></tr>';

        data.forEach(item => {
            table += `<tr><td>${item.id}</td><td>${item.name}</td><td>${item.description}</td></tr>`;
        });

        table += '</table>';

        document.getElementById('result').innerHTML = table;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('result').textContent = 'An error occurred while fetching the products.';
    }
}

