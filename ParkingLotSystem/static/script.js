document.getElementById('display-empty-slots').addEventListener('click', async () => {
    const response = await fetch('/display_empty_slots');
    const data = await response.json();
    document.getElementById('output').innerText = data.message;
});

document.getElementById('park-vehicle').addEventListener('click', async () => {
    const vehicleNumber = prompt('Enter vehicle number:');
    if (vehicleNumber) {
        const response = await fetch('/park_vehicle', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ vehicle_number: vehicleNumber })
        });
        const data = await response.json();
        document.getElementById('output').innerText = data.message;
    }
});

document.getElementById('remove-vehicle').addEventListener('click', async () => {
    const vehicleNumber = prompt('Enter vehicle number:');
    if (vehicleNumber) {
        const response = await fetch('/remove_vehicle', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ vehicle_number: vehicleNumber })
        });
        const data = await response.json();
        document.getElementById('output').innerText = data.message;
    }
});
