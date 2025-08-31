<script>  
document.getElementById('spiderForm').addEventListener('submit', function(e) {  
    e.preventDefault();  
    const modal = new bootstrap.Modal(document.getElementById('statusModal'));  
    const statusMessage = document.getElementById('statusMessage');  
  
    // Show modal  
    modal.show();  
    statusMessage.textContent = 'Your spider is running...';  
  
    // Start spider  
    fetch("{% url 'run-spider' %}", {  
        method: 'POST',  
        headers: { 'X-CSRFToken': '{{ csrf_token }}' },  
        body: new FormData(this)  
    })  
    .then(() => pollStatus(modal))  
    .catch(error => {  
        statusMessage.textContent = 'Failed to start spider: ' + error;  
    });  
});  
  
function pollStatus(modal, titleElement, messageElement) {  
    const checkInterval = setInterval(() => {  
        fetch(`{% url 'spider-status' %}?${Date.now()}`)  // Cache buster  
            .then(response => {  
                if (!response.ok) throw Error('Network error');  
                return response.json();  
            })  
            .then(data => {  
                console.log('Current status:', data.status);  
  
                if (data.status === 'completed') {  
                    titleElement.textContent = 'Completed!';  
                    messageElement.textContent = 'Spider finished successfully.';  
                    clearInterval(checkInterval);  
                }  
                else if (data.status.startsWith('failed') || data.status.startsWith('error')) {  
                    titleElement.textContent = 'Failed!';  
                    messageElement.textContent = data.status;  
                    clearInterval(checkInterval);  
                }  
                // Keep "running" as default state  
            })  
            .catch(error => {  
                console.error('Polling error:', error);  
                messageElement.textContent = 'Connection error - retrying...';  
            });  
    }, 1500);  // Faster polling interval  
}  
</script>