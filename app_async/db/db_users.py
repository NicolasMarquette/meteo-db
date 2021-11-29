"""Fake users database"""

users = {
  "alice": {
    "username": "alice",
    "hashed_password": "$2b$12$rpnsAp6oTeI34cZFkqHMu.cyjO8YWbSxcPwxzi2tln7Z4ks2CNVLK",
    "admin": False,
  },
  "bob": {
    "username": "bob",
    "hashed_password": "$2b$12$alOu/MsHr1HQpCe19KU16eRl88tddB8mVawbNATEMtjohW9qrOGu.",
    "admin": False,
  },
  "clementine": {
    "username": "clementine",
    "hashed_password": "$2b$12$MQXRLnaFJz/0.ZlmDxk0N.SgJXuQy0rroPq.WFWsXG8Lsd78It9XK",
    "admin": False,
  },
  "admin": {
    "username": "admin",
    "hashed_password": "$2b$12$eB9q2GPsiTmrOVyUJlhCC.69IdpEBibFpEDg7XrZmj9c96jPtuCpu",
    "admin": True,
  }
}
