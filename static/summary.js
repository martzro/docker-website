document.addEventListener('DOMContentLoaded', (event) => {
    populatePoopCount();
    populateGroupsDropdown();
    getGroupSubmissions();
});

let currentIndex = 0;

function toggleDateField() {
    const retroCheckbox = document.getElementById('retro');
    const retroDateField = document.getElementById('retro-date');
    if (retroCheckbox.checked) {
        retroDateField.style.display = 'block';
    } else {
        retroDateField.style.display = 'none';
    }
}

function submitPoop() {
    const username = localStorage.getItem('username'); // Retrieve the username from local storage
    const email = localStorage.getItem('email');
    const comment = document.getElementById('comment').value;
    const retro = document.getElementById('retro').checked;
    const retroDate = document.getElementById('retro-date').value;

    const payload = {
        "event_type": "log-poop",
        "user": {
            "userid": "",
            "username":  username,
            "email": email,
            "date": "",
            "is_active": "" 
        },
        "poop": {
            "rownum": "",
            "comment": comment,
            "date": retro ? retroDate : "",
            "is_retro": retro ? retro : ""
        },
        "group": {
            "group_name": "",
            "groupid": "",
            "date": ""
        }
    };

    fetch('http://localhost:8000/event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
        document.getElementById('message').textContent = 'Poop logged successfully!';
        populatePoopCount();
    } else {
        document.getElementById('message').textContent = 'Username does not exist.';
        }
    })
    .catch(error => console.error('Error:', error));
}

function populatePoopCount() {
    const username = localStorage.getItem('username'); 
    const email = localStorage.getItem('email');
    const payload = {
        "event_type": "get-poops-for-user",
        "user": {
            "userid": "",
            "username": username ,
            "email": email,
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

    fetch('http://localhost:8000/event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
        document.getElementById('poop-count').textContent = `${data.count} Poops`;
    } else {
        document.getElementById('poop-count').textContent = `0 Poops`;
    }
    })
    .catch(error => console.error('Error:', error));
}

function populateGroupsDropdown() {
    const username = localStorage.getItem('username'); // Retrieve the username from local storage
    const email = localStorage.getItem('email');
    const payload = {
        "event_type": "get-groups-user-is-in",
        "user": {
            "userid": "",
            "username": username ,
            "email": email,
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

    fetch('http://localhost:8000/event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.groups) {
            localStorage.setItem('group', data.groups[0]);
        } else {
            localStorage.setItem('group', null);
        }
        getGroupSubmissions();

    })
    .catch(error => console.error('Error:', error));
}

function populateAllGroups() {
    const username = localStorage.getItem('username');
    const email = localStorage.getItem('email');
    const payload = {
        "event_type": "get-all-groups",
        "user": {
            "userid": "",
            "username": username ,
            "email": email,
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

    fetch('http://localhost:8000/event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.groups) {
        const allGroupsList = document.getElementById('all-groups-list');
        data.groups.forEach(group => {
            const groupItem = document.createElement('div');
            groupItem.textContent = group;
            const joinButton = document.createElement('button');
            joinButton.textContent = 'Join';
            joinButton.onclick = () => joinGroup(group);
            groupItem.appendChild(joinButton);
            allGroupsList.appendChild(groupItem);
        });
    } else {
        document.getElementById('create-group-section').style.display = 'block';
    }
})
.catch(error => console.error('Error:', error));
}

function joinGroup(group) {
const username = localStorage.getItem('username'); // Retrieve the username from local storage
const email = localStorage.getItem('email');
const payload = {
    "event_type": "add-user-to-group",
    "user": {
        "userid": "",
        "username": username ,
        "email": email,
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
        "group_name": group,
        "groupid": "",
        "date": ""
    }
};

fetch('http://localhost:8000/event', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
})
.then(response => response.json())
.then(data => {
    if (data.success) {
    document.getElementById('message').textContent = `Joined group: ${group}`;
    populateGroupsDropdown(); // Refresh
    } else {
        document.getElementById('message').textContent = `Error joining group: ${group}`;
    }
    })
    .catch(error => console.error('Error:', error));
}

function getGroupSubmissions() {
    const group = localStorage.getItem('group');
    const username = localStorage.getItem('username');
    const email = localStorage.getItem('email');
    if (!group) return;

    const payload = {
        "event_type": "get-poops-from-group",
        "user": {
            "userid": "",
            "username": username,
            "email": email,
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
            "group_name": group,
            "groupid": "",
            "date": ""
        }
    };

    fetch('http://localhost:8000/event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        const groupContent = document.getElementById('group-content');
        groupContent.innerHTML = ''; // Clear previous submissions

        if (data.submissions && data.submissions.length > 0) {
            data.submissions.forEach(submission => {
                const activityItem = document.createElement('div');
                activityItem.className = 'activity-item';

                const user = document.createElement('h3');
                user.textContent = submission[1];
                activityItem.appendChild(user);

                const comment = document.createElement('p');
                comment.textContent = submission[2];
                activityItem.appendChild(comment);

                const date = document.createElement('p');
                date.textContent = submission[3] || ''; // Handle missing date
                activityItem.appendChild(date);

                const actions = document.createElement('div');
                actions.className = 'actions';

                const likeButton = document.createElement('button');
                likeButton.innerHTML = '❤️'; // Heart emoji
                likeButton.onclick = () => likeSubmission(submission[0]);
                actions.appendChild(likeButton);

                const commentButton = document.createElement('button');
                commentButton.innerHTML = '💬'; // Speech balloon emoji
                commentButton.onclick = () => commentOnSubmission(submission[0]);
                actions.appendChild(commentButton);

                activityItem.appendChild(actions);
                groupContent.appendChild(activityItem);
            });
        } else {
            const noSubmissionsMessage = document.createElement('p');
            noSubmissionsMessage.textContent = 'No submissions found for this group.';
            groupContent.appendChild(noSubmissionsMessage);
        }
    })
    .catch(error => console.error('Error:', error));
}
    

function showCreateGroupPopup() {
    document.getElementById('create-group-popup').style.display = 'flex';
}

function closeCreateGroupPopup() {
    document.getElementById('create-group-popup').style.display = 'none';
}

function createGroup() {
    const groupName = document.getElementById('new-group-name').value;
    const username = localStorage.getItem('username'); // Retrieve the username from local storage
    const email = localStorage.getItem('email');

    const payload = {
        "event_type": "add-group",
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
            "group_name": groupName,
            "groupid": "",
            "date": ""
        }
    };

    fetch('http://localhost:8000/event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const addUserToGroupPayload = {
                event_type: 'add-user-to-group',
                user: {
                    username: username,
                    email: ''
                },
                group: {
                    group_name: groupName
                }
            };

            fetch('http://localhost:8000/event', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(addUserToGroupPayload)
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('message').textContent = `Group created and joined: ${groupName}`;
                closeCreateGroupPopup();
                populateGroupsDropdown(); // Refresh the groups dropdown
            })
            .catch(error => console.error('Error:', error));
        } else {
            document.getElementById('message').textContent = 'Failed to create group.';
        }
    })
    .catch(error => console.error('Error:', error));
}

function logout() {
    localStorage.removeItem('username'); // Clear the username from local storage
    window.location.href = '/'; // Redirect to the login page
}

        
function showPoopForm() {
    document.getElementById('poop-form').style.display = 'block';
}

function closePoopForm() {
    document.getElementById('poop-form').style.display = 'none';
}
function closeGroupForm() {
    document.getElementById('join-group-form').style.display = 'none';
}

function toggleDateField() {
    const retroDate = document.getElementById('retro-date');
    retroDate.style.display = retroDate.style.display === 'none' ? 'block' : 'none';
}

function showJoinGroupForm() {
    document.getElementById('join-group-form').style.display = 'block';
}



        

       

        

