import requests
import json
from datetime import datetime

# URL of the FastAPI server
url = "http://127.0.0.1:8000/event"

# Test the login event
tests = [{
    "event_type": "login",
    "user": {
        "userid": "",
        "username": "test_user" ,
        "email":"",
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
}
,
{
    "event_type": "login",
    "user": {
        "userid": "",
        "username": "roman" ,
        "email":"romanmtz@me.com",
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
},
{
    "event_type": "add-user",
    "user": {
        "userid": "",
        "username": "test_user" ,
        "email":"test@testuser.com",
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
},
{
    "event_type": "log-poop",
    "user": {
        "userid": "",
        "username": "test_user" ,
        "email":"test@testuser.com",
        "date": "",
        "is_active": "" 
    },
    "poop": {
        "rownum": "",
        "comment": "test for test user",
        "date": "",
        "is_retro": ""
    },
    "group": {
        "group_name": "",
        "groupid": "",
        "date": ""
    }
},
{
    "event_type": "log-poop",
    "user": {
        "userid": "",
        "username": "test_user" ,
        "email":"test@testuser.com",
        "date": "",
        "is_active": "" 
    },
    "poop": {
        "rownum": "",
        "comment": "retro for test user",
        "date": datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
        "is_retro": True
    },
    "group": {
        "group_name": "",
        "groupid": "",
        "date": ""
    }
},
{
    "event_type": "add-user",
    "user": {
        "userid": "",
        "username": "test_user2" ,
        "email":"test@testuser.com",
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
},
{
    "event_type": "add-user-to-group",
    "user": {
        "userid": "",
        "username": "test_user" ,
        "email":"test@testuser.com",
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
        "group_name": "the cool test group",
        "groupid": "",
        "date": ""
    }
},
{
    "event_type": "add-group",
    "user": {
        "userid": "",
        "username": "test_user" ,
        "email":"test@testuser.com",
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
        "group_name": "the cool test group",
        "groupid": "",
        "date": ""
    }
},
{
    "event_type": "add-group",
    "user": {
        "userid": "",
        "username": "test_user" ,
        "email":"test@testuser.com",
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
        "group_name": "the cool test group",
        "groupid": "",
        "date": ""
    }
},
{
    "event_type": "add-user-to-group",
    "user": {
        "userid": "",
        "username": "test_user" ,
        "email":"test@testuser.com",
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
        "group_name": "the cool test group",
        "groupid": "",
        "date": ""
    }
},
{
    "event_type": "add-user-to-group",
    "user": {
        "userid": "",
        "username": "test_user" ,
        "email":"test@testuser.com",
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
        "group_name": "cool group",
        "groupid": "",
        "date": ""
    }
},
{
    "event_type": "log-poop",
    "user": {
        "userid": "",
        "username": "roman" ,
        "email":"",
        "date": "",
        "is_active": "" 
    },
    "poop": {
        "rownum": "",
        "comment": "test for roman user",
        "date": "",
        "is_retro": ""
    },
    "group": {
        "group_name": "",
        "groupid": "",
        "date": ""
    }
},
{
    "event_type": "get-group-analytics",
    "user": {
        "userid": "",
        "username": "roman" ,
        "email":"",
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
},
{
    "event_type": "get-groups-user-is-in",
    "user": {
        "userid": "",
        "username": "roman" ,
        "email":"",
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
},
{
    "event_type": "get-poops-from-group",
    "user": {
        "userid": "",
        "username": "roman" ,
        "email":"",
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
        "group_name": "lame group",
        "groupid": "",
        "date": ""
    }
},
{
    "event_type": "get-all-groups",
    "user": {
        "userid": "",
        "username": "roman" ,
        "email":"",
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
},
{
    "event_type": "add-comment",
    "user": {
        "userid": "",
        "username": "roman" ,
        "email":"",
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
    },
    "like": {
        "poopid":"",
        "date":""
    },
    "comment": {
        "poopid":"23",
        "comment":"hello",
        "date":  datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        }
}
]

for i, test in enumerate(tests):
    response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(test))
    print(f"test #:{i}, event_type: {test['event_type']}, {response.json()}")