// QR Code Scanner initialization
const html5QrcodeScanner = new Html5QrcodeScanner(
    "qr-reader", { fps: 10, qrbox: 250 });

html5QrcodeScanner.render(onScanSuccess, onScanError);

// Handle successful QR code scan
function onScanSuccess(decodedText, decodedResult) {
    document.getElementById('employeeNumber').value = decodedText;
    // Optional: Stop scanning after successful scan
    html5QrcodeScanner.clear();
}

function onScanError(errorMessage) {
    // handle scan error
    console.error(errorMessage);
}

// Form handling
const form = document.getElementById('attendanceForm');
form.addEventListener('submit', handleSubmit);

async function handleSubmit(event) {
    event.preventDefault();
    
    const employeeNumber = document.getElementById('employeeNumber').value;
    const status = document.querySelector('input[name="status"]:checked').value;
    
    try {
        const response = await fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                worker_id: employeeNumber,
                action: status
            })
        });

        const result = await response.json();
        
        if (result.status === 'success') {
            alert('Attendance recorded successfully!');
            // Reset form
            form.reset();
            // Restart QR scanner
            html5QrcodeScanner.render(onScanSuccess, onScanError);
        } else {
            alert('Error recording attendance: ' + (result.message || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error recording attendance. Please try again.');
    }
}

// Reset button handling
document.getElementById('resetBtn').addEventListener('click', () => {
    // Reset form
    form.reset();
    // Restart QR scanner
    html5QrcodeScanner.render(onScanSuccess, onScanError);
});
