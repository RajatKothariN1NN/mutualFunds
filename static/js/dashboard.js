function showFolioInput() {
    document.getElementById('folio-input-container').style.display = 'block';
}

function hideFolioInput() {
    document.getElementById('folio-input-container').style.display = 'none';
}

function submitFolio(event) {
    event.preventDefault(); // Prevent the default form submission

    const folioName = document.getElementById('folio-name').value;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(document.getElementById('folio-form').action, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + getCookie('access') // Include JWT in the Authorization header
        },
        body: JSON.stringify({ name: folioName })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to create folio');
        }
    })
    .then(data => {
        console.log('Folio created:', data);
        hideFolioInput(); // Hide the input after submission
        location.reload();
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Helper function to get a cookie value by name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function handleLogout() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const refreshToken = getCookie('refresh');  // Get refresh token from cookies

    fetch(document.getElementById('logout-form').action, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ refresh_token: refreshToken })
    })
    .then(response => {
        if (response.ok) {
            clearAllCookies();

            // Redirect to the login page
            window.location.href = "/api/auth/login";
        } else {
            throw new Error('Logout failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function clearAllCookies() {
    const cookies = document.cookie.split(";");

    cookies.forEach(cookie => {
        const eqPos = cookie.indexOf("=");
        const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;";
    });
}
