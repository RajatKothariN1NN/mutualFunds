document.addEventListener('DOMContentLoaded', function() {
    console.log("I am here");

    const aiModal = document.getElementById('ai-modal');
    const aiButton = document.getElementById('ai-recommendation-btn');
    const closeButton = document.querySelector('.close');
    const nextStepButton = document.getElementById('next-step');
    const prevStepButton = document.getElementById('prev-step');

    let currentStep = 0;
    const totalSteps = 8; // Updated to include investment choice step
    let userChoices = {}; // To store user's selections
    let folioId; // To store selected folio ID

    // Open modal when button is clicked
    if (aiButton) {
        aiButton.onclick = function() {
            aiModal.style.display = "block";
            loadStep(currentStep);
        };
    }

    // Close modal on close button click
    if (closeButton) {
        closeButton.onclick = function() {
            aiModal.style.display = "none";
        };
    }

    // Hide modal when clicking outside of it
    window.onclick = function(event) {
        if (event.target === aiModal) {
            aiModal.style.display = "none";
        }
    };

    // Dynamically load content for each step
    function loadStep(step) {
        const recommendationSteps = document.getElementById("recommendation-steps");
        recommendationSteps.innerHTML = ""; // Clear the previous content

        switch(step) {
            case 0:

                recommendationSteps.innerHTML = `
                    <p>Welcome! We will help you curate a portfolio based on your preferences. Click "Get Started" to begin.</p>
                    <button id="get-started">Get Started</button>
                `;
                document.getElementById('get-started').addEventListener('click', () => nextStep());
                break;
            case 1:

                fetch('/fund-types/')
                    .then(response => response.json())
                    .then(data => {
                        let options = data.map(type => `<option value="${type.id}">${type.name}</option>`).join('');
                        recommendationSteps.innerHTML = `
                            <label>Which type of fund are you interested in?</label>
                            <select id="fund-type">${options}</select>
                        `;
                    });
                break;
            case 2:
                fetch('/risk-profiles/')
                    .then(response => response.json())
                    .then(data => {
                        let radios = data.map(profile => `
                            <label class="radio-label"><input type="radio" name="risk-profile" value="${profile.id}"> ${profile.name}</label>
                        `).join('');
                        recommendationSteps.innerHTML = `
                            <label>How would you rate your risk appetite?</label>
                            <div>${radios}</div>
                        `;
                    });
                break;
            case 3:
                fetch('/themes/')
                    .then(response => response.json())
                    .then(data => {
                        let checkboxes = data.map(theme => `
                            <label class="checkbox-label"><input type="checkbox" name="themes" value="${theme.id}"> ${theme.name}</label>
                        `).join('');
                        recommendationSteps.innerHTML = `
                            <label>Which investment themes interest you?</label>
                            <div>${checkboxes}</div>
                        `;
                    });
                break;
            case 4:
                recommendationSteps.innerHTML = `
                    <label>What is your preferred investment duration?</label>
                    <select id="investment-duration">
                        <option value="1">1 Year</option>
                        <option value="3">3 Years</option>
                        <option value="5">5 Years</option>
                        <option value="10">10 Years</option>
                    </select>
                `;
                break;
            case 5:
                recommendationSteps.innerHTML = `
                    <label>What are your expected returns?</label>
                    <select id="expected-returns">
                        <option value="5">5%</option>
                        <option value="10">10%</option>
                        <option value="15">15%</option>
                    </select>
                `;
                break;
            case 6:
                recommendationSteps.innerHTML = `
                    <p>Would you like to invest in your curated portfolio?</p>
                    <button id="yes-invest">Yes</button>
                    <button id="no-invest">No, thank you</button>
                `;
                document.getElementById('yes-invest').addEventListener('click', loadFolioSelection);
                document.getElementById('no-invest').addEventListener('click', () => {
                    aiModal.style.display = "none"; // Close modal
                });
                break;
            case 7:
                // Load existing folios for the user
                fetch('/api/portfolios/folios/')
                    .then(response => response.json())
                    .then(data => {
                        let options = data.map(folio => `<option value="${folio.id}">${folio.name}</option>`).join('');
                        recommendationSteps.innerHTML = `
                            <label>Select an existing folio:</label>
                            <select id="existing-folio">${options}</select>
                            <button id="submit-existing-folio">Submit</button>
                            <button id="create-new-folio">Create New Folio</button>
                        `;
                        document.getElementById('submit-existing-folio').addEventListener('click', redirectToFolioDetail);
                        document.getElementById('create-new-folio').addEventListener('click', loadNewFolioCreation);
                        document.getElementById('existing-folio').addEventListener('change', () => {
                            folioId = document.getElementById('existing-folio').value; // Store selected folio ID
                        });
                    });
                break;
            case 8:
                // Input for new folio name
                recommendationSteps.innerHTML = `
                    <label>Enter the name for your new folio:</label>
                    <input type="text" id="new-folio-name" required>
                    <button id="submit-new-folio">Create Folio</button>
                `;
                document.getElementById('submit-new-folio').addEventListener('click', createNewFolio);
                break;
            default:
                break;
        }

        // Show/Hide Previous button based on the step
        prevStepButton.style.display = step > 0 ? 'inline-block' : 'none';
        nextStepButton.style.display = step > 0 && step < totalSteps - 1 ? 'inline-block' : 'none';
    }

    // Move to the next step
    function nextStep() {
        if (currentStep < totalSteps - 1) {
            storeUserChoice();
            currentStep++;
            loadStep(currentStep);
        }
    }

    // Move to the previous step
    function prevStep() {
        if (currentStep > 0) {
            currentStep--;
            loadStep(currentStep);
        }
    }

    // Store user's selection for the current step
    function storeUserChoice() {
        switch (currentStep) {
            case 1:
                userChoices.fundType = document.getElementById('fund-type').value;
                break;
            case 2:
                userChoices.riskProfile = document.querySelector('input[name="risk-profile"]:checked').value;
                break;
            case 3:
                userChoices.themes = Array.from(document.querySelectorAll('input[name="themes"]:checked')).map(el => el.value);
                break;
            case 4:
                userChoices.investmentDuration = document.getElementById('investment-duration').value;
                break;
            case 5:
                userChoices.expectedReturns = parseFloat(document.getElementById('expected-returns').value);
                // Call API to store user choices after the last step
                saveUserPreferences(userChoices);
                break;
            default:
                break;
        }
    }
    function saveUserPreferences(preferences) {
        const formattedPreferences = {
        fund_types: preferences.fundType ? [preferences.fundType] : [],  // Wrap in an array
        risk_profiles: preferences.riskProfile ? [preferences.riskProfile] : [],  // Wrap in an array
        themes: preferences.themes,  // Already an array
        investment_duration: preferences.investmentDuration,
        expected_returns: preferences.expectedReturns,
    };
        fetch('/user-preferences/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + getCookie('access') // Assuming you're using JWT stored in localStorage
            },
            body: JSON.stringify(formattedPreferences)
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Failed to save preferences');
            }
        })
        .then(data => {
            console.log('User preferences saved:', data);
            // Handle success (e.g., notify the user, proceed to the next action)
        })
        .catch(error => {
            console.error('Error saving preferences:', error);
            // Handle error (e.g., show error message to the user)
        });
    }

    // Redirect to the folio detail page
    function redirectToFolioDetail() {
        if (folioId) {
            window.location.href = `/api/portfolios/folios/${folioId}/`; // Redirect to folio detail page
        }
    }
    function loadFolioSelection() {
        currentStep++;
        loadStep(currentStep);
    }
    // Load new folio creation step
    function loadNewFolioCreation() {
        currentStep++;
        loadStep(currentStep);
    }

    // Create a new folio
    function createNewFolio() {
        const folioName = document.getElementById('new-folio-name').value;

        fetch('/api/portfolios/folios/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Add CSRF token if needed
            },
            body: JSON.stringify({ name: folioName })
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network response was not ok.');
        })
        .then(data => {
            console.log('New folio created:', data);
            folioId = data.id; // Store the new folio ID
            redirectToFolioDetail(); // Redirect to folio detail page
        })
        .catch(error => {
            console.error('Error creating new folio:', error);
        });
    }

    // Get CSRF token for POST requests
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Add event listeners for navigation buttons
    if (nextStepButton) {
        nextStepButton.onclick = nextStep;
    }
    if (prevStepButton) {
        prevStepButton.onclick = prevStep;
    }
});
