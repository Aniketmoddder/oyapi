from flask import Flask, request, jsonify
import requests, json, random, string, time
from faker import Faker

app = Flask(__name__)
fake = Faker()
UA = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"

def genp():
    return ''.join(random.choice(string.ascii_letters + string.digits + "!@#$%^&*") for _ in range(12))

def landing(s):
    print("\n========== LANDING PAGE ==========")
    h = {
        "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "accept-language":"en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control":"no-cache",
        "pragma":"no-cache",
        "sec-ch-ua":'"Chromium";v="137","Not/A)Brand";v="24"',
        "sec-ch-ua-mobile":"?1",
        "sec-ch-ua-platform":'"Android"',
        "sec-fetch-dest":"document",
        "sec-fetch-mode":"navigate",
        "sec-fetch-site":"none",
        "upgrade-insecure-requests":"1",
        "user-agent":UA
    }
    r = s.get("https://darkosint.in/", headers=h)
    print("[Landing Status]", r.status_code)
    for c in s.cookies:
        print(c.name, "=", c.value)

def signup(s):
    print("\n========== SIGNUP ==========")
    name = fake.first_name()
    email = fake.first_name().lower()+str(random.randint(1000,9999))+"@gmail.com"
    password = genp()
    print("[Name]", name)
    print("[Email]", email)
    print("[Password]", password)
    p = {"action":"signup","name":name,"email":email,"password":password}
    r = s.post("https://darkosint.in/api/auth.php", data=p)
    print("[Raw Signup]")
    print(r.text)
    try: print("[Signup JSON]\n", json.dumps(json.loads(r.text), indent=4))
    except: print("[Signup JSON Decode Failed]")

def lookup_debug(s, t, q):
    print("\n========== LOOKUP ==========")
    print("[Type]", t)
    print("[Query]", q)
    r = s.post("https://darkosint.in/api/lookup.php", data={"type":t,"query":q})
    print("[Raw Lookup]")
    print(r.text)

    if "<html" in r.text.lower(): 
        return {"error":"Cloudflare block","Developer":"Basic Coders | @SajagOG"}

    try:
        js = json.loads(r.text)
        print("[Parsed JSON]\n", json.dumps(js, indent=4))
    except:
        return {"error":"Not JSON","Developer":"Basic Coders | @SajagOG"}

    try:
        rows = js["data"]["result"]
    except:
        return {"error":"Unexpected JSON structure","Developer":"Basic Coders | @SajagOG"}

    if not rows:
        return {"error":"No records found","Developer":"Basic Coders | @SajagOG"}

    d = rows[0]
    print("\n========== CLEAN ==========")
    print("Name        :", d.get("name"))
    print("Father Name :", d.get("father_name"))
    print("Address     :", d.get("address","").replace("!"," , "))
    print("Mobile      :", d.get("mobile"))
    print("Aadhaar     :", d.get("id_number"))
    print("Email       :", d.get("email"))
    print("Developer   : Basic Coders | @SajagOG")

    return {
        "name": d.get("name"),
        "father_name": d.get("father_name"),
        "address": d.get("address","").replace("!"," , "),
        "mobile": d.get("mobile"),
        "aadhaar": d.get("id_number"),
        "email": d.get("email"),
        "Developer": "Basic Coders | @SajagOG"
    }

@app.route("/")
def home():
    return jsonify({
        "message": "API is running",
        "endpoints": {
            "/num": "Query by phone number",
            "/aadhar": "Query by Aadhaar number"
        },
        "usage": {
            "/num?number=XXXXXXXXXX": "Get info by phone",
            "/aadhar?aadhar=XXXXXXXXXXXX": "Get info by Aadhaar"
        }
    })

@app.route("/num")
def num():
    n = request.args.get("number")
    if not n:
        return {"error":"Missing ?number","Developer":"Basic Coders | @SajagOG"}
    s = requests.Session()
    landing(s)
    signup(s)
    return lookup_debug(s,"mobile",n)

@app.route("/aadhar")
def aad():
    a = request.args.get("aadhar")
    if not a:
        return {"error":"Missing ?aadhar","Developer":"Basic Coders | @SajagOG"}
    s = requests.Session()
    landing(s)
    signup(s)
    return lookup_debug(s,"aadhaar",a)

# Vercel requires this
if __name__ == "__main__":
    app.run()
