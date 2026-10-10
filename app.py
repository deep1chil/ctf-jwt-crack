#!/usr/bin/env python3
"""Challenge: JWT Token Manipulation (Medium)"""
import jwt, datetime, json
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
SECRET = "secret123"
FLAG = "FLAG{jwt_w34k_s3cr3t_cr4ck3d}"

def make_token(username, role="user"):
    return jwt.encode({"sub": username, "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)},
        SECRET, algorithm="HS256")

PAGE = r"""
<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CloudSync — Dashboard</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>
:root{--bg:#0f172a;--card:rgba(15,23,42,.9);--border:rgba(148,163,184,.12);
  --text:#e2e8f0;--text2:#64748b;--cyan:#06b6d4;--cyan2:#0891b2;
  --green:#22c55e;--red:#ef4444;--orange:#f59e0b;
  --font:'Inter',sans-serif;--mono:'JetBrains Mono',monospace}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font:15px/1.6 var(--font);min-height:100vh;
  display:flex;flex-direction:column;align-items:center;padding:32px 16px}
body::before{content:'';position:fixed;inset:0;pointer-events:none;
  background:radial-gradient(ellipse at 50% -20%,rgba(6,182,212,.08),transparent 70%)}
.card{background:var(--card);border:1px solid var(--border);border-radius:16px;
  padding:32px;width:min(92vw,560px);backdrop-filter:blur(12px);margin-bottom:20px}
.badge{display:inline-block;font:600 11px var(--mono);letter-spacing:1.5px;
  text-transform:uppercase;color:var(--cyan);padding:4px 12px;
  border:1px solid rgba(6,182,212,.25);border-radius:6px;margin-bottom:16px}
h1{font-size:26px;font-weight:800;margin-bottom:4px}
.sub{color:var(--text2);font-size:14px;margin-bottom:24px}
.btn{display:inline-block;padding:11px 22px;border:0;border-radius:10px;
  background:linear-gradient(135deg,var(--cyan2),var(--cyan));color:#fff;
  font:600 14px var(--font);cursor:pointer;margin:4px}
.btn:hover{transform:translateY(-1px);box-shadow:0 6px 20px rgba(6,182,212,.3)}
.btn.sm{padding:8px 16px;font-size:13px}
.token-box{background:rgba(0,0,0,.4);border:1px solid var(--border);border-radius:10px;
  padding:14px;margin:14px 0;font:13px var(--mono);word-break:break-all;color:var(--orange);
  line-height:1.7;user-select:all}
#out{margin-top:14px;font:14px var(--mono);padding:14px;border-radius:10px;display:none;
  word-break:break-all;border:1px solid}
.win{background:rgba(34,197,94,.08);color:var(--green);border-color:rgba(34,197,94,.25)!important;display:block!important}
.bad{background:rgba(239,68,68,.08);color:var(--red);border-color:rgba(239,68,68,.25)!important;display:block!important}
.info{background:rgba(6,182,212,.08);color:var(--cyan);border-color:rgba(6,182,212,.25)!important;display:block!important}
label{color:var(--text2);font-size:13px;font-weight:600;display:block;margin-bottom:6px}
input,textarea{width:100%;padding:12px 14px;margin-bottom:14px;background:rgba(0,0,0,.3);
  border:1px solid var(--border);border-radius:10px;color:var(--text);font:14px var(--mono);outline:none;resize:vertical}
input:focus,textarea:focus{border-color:var(--cyan);box-shadow:0 0 0 3px rgba(6,182,212,.15)}
.hint{color:var(--text2);font-size:12px;margin-top:16px;padding:12px;
  border:1px dashed rgba(148,163,184,.15);border-radius:8px}
.step{color:var(--text2);font-size:13px;margin:4px 0}
code{color:var(--cyan);font-family:var(--mono)}
</style></head><body>
<div class="card">
  <span class="badge">Web &middot; JWT</span>
  <h1>CloudSync</h1>
  <p class="sub">File sync platform &mdash; admin panel holds the flag</p>

  <div id="login-section">
    <p class="step"><b>Step 1:</b> Get your user token</p>
    <label>Username</label>
    <input id="user" placeholder="any username" value="hacker">
    <button class="btn" onclick="getToken()">Get Token</button>
  </div>

  <div id="token-section" style="display:none">
    <p class="step"><b>Your JWT Token:</b></p>
    <div class="token-box" id="my-token"></div>
    <button class="btn sm" onclick="navigator.clipboard.writeText(document.getElementById('my-token').textContent)">Copy Token</button>
  </div>

  <div style="margin-top:24px;padding-top:20px;border-top:1px solid var(--border)">
    <p class="step"><b>Step 2:</b> Access the admin panel</p>
    <label>JWT Token</label>
    <textarea id="tok" rows="3" placeholder="Paste your (modified?) token here"></textarea>
    <button class="btn" onclick="accessPanel()">Access Admin Panel</button>
  </div>

  <div id="out"></div>

  <div class="hint">
    <b>Hints:</b><br>
    &bull; JWT tokens have 3 parts: <code>header.payload.signature</code><br>
    &bull; Decode the payload at <code>jwt.io</code> to see your role<br>
    &bull; The signing secret might be... weak. Try cracking it<br>
    &bull; Tools: <code>john</code>, <code>hashcat</code>, or just guess common secrets
  </div>
</div>

<script>
const out=document.getElementById('out');
async function getToken(){
  const u=document.getElementById('user').value.trim();
  if(!u)return;
  const r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({username:u})});
  const d=await r.json();
  if(d.token){
    document.getElementById('my-token').textContent=d.token;
    document.getElementById('token-section').style.display='block';
    document.getElementById('tok').value=d.token;
  }
}
async function accessPanel(){
  const t=document.getElementById('tok').value.trim();
  if(!t)return;out.className='';out.style.display='none';
  const r=await fetch('/api/admin',{headers:{'Authorization':'Bearer '+t}});
  const d=await r.json();
  if(d.flag){out.className='win';out.innerHTML='<b>Admin access granted!</b><br>'+d.flag+'<br><span style="font-size:11px;opacity:.7">Submit this flag on the CTF platform.</span>'}
  else if(d.user){out.className='info';out.innerHTML='Welcome <b>'+d.user+'</b>! Role: <b>'+d.role+'</b><br><span style="opacity:.7">But you need admin role to get the flag...</span>'}
  else{out.className='bad';out.textContent=d.error||'Access denied'}
}
</script>
</body></html>
"""

@app.route("/")
def index():
    return render_template_string(PAGE)

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    if not username:
        return jsonify(error="Username required"), 400
    token = make_token(username, "user")
    return jsonify(token=token, message=f"Logged in as {username} (role: user)")

@app.route("/api/admin")
def admin_panel():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify(error="No token provided. Send Authorization: Bearer <token>"), 401
    token = auth[7:]
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256", "none"])
    except jwt.ExpiredSignatureError:
        return jsonify(error="Token expired"), 401
    except jwt.InvalidTokenError:
        return jsonify(error="Invalid token"), 401
    if payload.get("role") == "admin":
        return jsonify(flag=FLAG, user=payload["sub"], role="admin",
                       message="Full admin access granted!")
    return jsonify(user=payload["sub"], role=payload.get("role", "unknown"),
                   message="Access denied — admin role required")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8004, debug=False)
