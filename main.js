
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('generatorForm');
    const generateBtn = document.getElementById('generateBtn');
    const resultContainer = document.getElementById('resultContainer');
    const generatedText = document.getElementById('generatedText');
    const promptInput = document.getElementById('prompt');

    if (!form || !generateBtn || !resultContainer || !generatedText || !promptInput) {
        console.error('One or more required elements not found in the DOM');
        return;
    }

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const prompt = promptInput.value.trim();
        if (!prompt) {
            alert('Please enter a prompt');
            return;
        }

        // Disable button and show loading state
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Generating...';

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt })
            });

            const data = await response.json();

            // Show result container
            resultContainer.classList.remove('d-none');

            if (data.success) {
                generatedText.textContent = data.message;
                resultContainer.querySelector('.alert').className = 'alert alert-info';
            } else {
                generatedText.textContent = 'Error: ' + data.message;
                resultContainer.querySelector('.alert').className = 'alert alert-danger';
            }
        } catch (error) {
            resultContainer.classList.remove('d-none');
            generatedText.textContent = 'Error: Failed to connect to the server';
            resultContainer.querySelector('.alert').className = 'alert alert-danger';
        }

        // Reset button state
        generateBtn.disabled = false;
        generateBtn.textContent = 'Generate Response';
    });
});
