function login() {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const payload ={
        "event_type": "login",
        "user": {
            "userid": "",
            "username": username ,
            "email":email,
            "date": "",
            "is_active": "" 
        },
        "poop": {
            "rownum": "",
            "comment": "",
            "date": "",
            "is_retro": ""
        },
        "group": {
            "group_name": "",
            "groupid": "",
            "date": ""
        }
    };

    fetch('http://poopsheet.com/api/event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('message').textContent = 'Login successful!';
            localStorage.setItem('username', username); // Store the username in local storage
            localStorage.setItem('email', email);
            window.location.href = '/summary'; // Redirect to the summary page
        } else {
            document.getElementById('message').textContent = 'Username does not exist.';
        }
    })
    .catch(error => console.error('Error:', error));
}

function makeUser() {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;

    const payload = {
        "event_type": "add-user",
        "user": {
            "userid": "",
            "username": username,
            "email":email,
            "date": "",
            "is_active": "" 
        },
        "poop": {
            "rownum": "",
            "comment": "",
            "date": "",
            "is_retro": ""
        },
        "group": {
            "group_name": "",
            "groupid": "",
            "date": ""
        }
    };

    fetch('http://poopsheet.com/api/event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('message').textContent = 'Username created! You can now log in.';
        } else {
            document.getElementById('message').textContent = 'Username not available.';
        }
    })
    .catch(error => console.error('Error:', error));
}

