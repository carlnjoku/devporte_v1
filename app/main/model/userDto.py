from flask_restplus import Namespace, fields
import json
from werkzeug.datastructures import FileStorage


class UserDto:
    api = Namespace('user', description='User operations including create, edit, view and delete')

    upload_parser = api.parser()
    upload_parser.add_argument('avatarBlob', location='files',
                            type=FileStorage, required=True)

    parser = api.parser()
    parser.add_argument('x-access-token', required=True, location='headers')

    #parser = api.parser()
    #parser.add_argument('file', type=FileStorage, location='files', required=True)

    signup = api.model('signup details', {
        'email': fields.String(required=True, description='user email address'),
        'firstname': fields.String(required=True, description='user firstname'),
        'lastname': fields.String(required=True, description='user last name'),
        'user_type': fields.String(required=True, description='user type'),
        'country': fields.String(required=True, description='user type'),
        'company_name': fields.String(required=False, description='user type'),
        'state': fields.String(required=True, description='user type'),
        'password': fields.String(required=True, description='user password'),
        
       
    })

    email_confirmation = api.model('email_confirmation', {
        'firstname': fields.String(required=True, description='recipient firstname'),
        'lastname': fields.String(required=True, description='recipient lastname'),
        'email': fields.String(required=True, description='recipient email address'),
        'userId': fields.String(required=True, description='recipient userId'),
       
    })

    profile = api.model('Minimal profile', {
        'userId': fields.String(required=True, description='recipient userId'),
        'expertise': fields.List(fields.String,required=True, description="List of users expertise"),
        'linkedin': fields.Url(required=True, description='User linkedin profile link'),
        'github': fields.Url(required=True, description='User github profile link'),
        'website': fields.Url(description="User's personal website url"),
        'experience': fields.String(required=True,description=''),
        'tzone': fields.String(required=True,description='timezone'),
        'availability': fields.String(required=True, description='user availability to work'),
        'pastprojects': fields.String(description="User's past project"),
        'about': fields.String(required=True,description=""),
        'avatarBlob': fields.String(required=True,description=""),
        'professional_title': fields.String(required=True, description='User professional title'),
        'calling_code': fields.String(description=''),
        'postal': fields.String(required=True,description=''),
        'geoLoc': fields.Raw(description='Geo location'),
        'phone': fields.String(required=True, description='Phone number'),
        'experience_Level': fields.String(required=True, description='Experience level'),
        'project_type': fields.String(required=True, description=''),
        'primary_skills': fields.List(fields.Raw, required=True, description='List of primary skills'),
        'secondary_skills': fields.List(fields.Raw, required=True, description='List of secondary skills'),
        'updated_on': fields.String(required=True, description='Time updated'),
       
    })

    emp_contact = api.model('employer contact', {
        '_id': fields.String(required=True, description='user id'),
        'firstname': fields.String(required=True, description='employer firstname'),
        'lastname': fields.String(required=True, description='employer last name'),
        'phone': fields.String(required=True, description='employer phone'),
        'address': fields.String(required=True, description='address'),
        'website': fields.String(required=True, description='website'),
        'about_us': fields.String(required=True, description='about employer'),
    })

    change_pass = api.model('chnage password', {
        '_id': fields.String(required=True, description='user id'),
        'old_password': fields.String(required=True, description='old password'),
        'new_password': fields.String(required=True, description='new password'),
    })

    fileupload = api.model('Upload file', {
        'avatarBlob': fields.String(required=True,description=""),
    })
    
"""
{
  "userId": "b2b3c199-7cbc-4e87-932a-8e1798d3e234",
  "expertise": [
    "Python", "Scala"
  ],
  "linkedin": "http://www.linkedin.com/kalifa",
  "github": "http://www.github.com/kalifa",
  "website": "http://www.kalifa.com",
  "experience": "2",
  "tzone": "2383",
  "availability": "2months",
  "pastprojects": "long",
  "about": "I am a a good developer",
  "avatarBlob": "string",
  "professional_title": "Fullstack developer",
  "calling_code": "234",
  "postal": "23401",
  "geoLoc": {
    "ip": "197.210.45.78",
    "is_eu": false,
    "city": "Lagos",
    "region": "Lagos",
    "region_code": "LA",
    "country_name": "Nigeria",
    "country_code": "NG",
    "continent_name": "Africa",
    "continent_code": "AF",
    "latitude": 6.4474,
    "longitude": 3.3903,
    "postal": null,
    "calling_code": "234",
    "flag": "https://ipdata.co/flags/ng.png",
    "emoji_flag": "\ud83c\uddf3\ud83c\uddec",
    "emoji_unicode": "U+1F1F3 U+1F1EC",
    "asn": {
        "asn": "AS29465",
        "name": "MTN NIGERIA Communication limited",
        "domain": "mtnonline.com",
        "route": "197.210.45.0/24",
        "type": "isp"
    },
    "carrier": {
        "name": "MTN",
        "mcc": "621",
        "mnc": "30"
    },
    "languages": [
        {
            "name": "English",
            "native": "English"
        }
    ],
    "currency": {
        "name": "Nigerian Naira",
        "code": "NGN",
        "symbol": "\u20a6",
        "native": "\u20a6",
        "plural": "Nigerian nairas"
    },
    "time_zone": {
        "name": "Africa/Lagos",
        "abbr": "WAT",
        "offset": "+0100",
        "is_dst": false,
        "current_time": "2020-04-30T23:12:36.770396+01:00"
    },
    "threat": {
        "is_tor": false,
        "is_proxy": false,
        "is_anonymous": false,
        "is_known_attacker": false,
        "is_known_abuser": false,
        "is_threat": false,
        "is_bogon": false
    },
    "count": "2"
},
  "phone": "08033164340",
  "experience_Level": "expert",
  "project_type": "long",
  "primary_skills": [
    {
        "title" : "Python",
        "year" : 2
    }, 
    {
        "title" : "PHP",
        "year" : 6
    }
  ],
  "secondary_skills": [
    {
        "title" : "UI/UX",
        "year" : 6
    }, 
    {
        "title" : "AdobeXD",
        "year" : 5
    } 
  ],
  "updated_on": "string"
}
"""
