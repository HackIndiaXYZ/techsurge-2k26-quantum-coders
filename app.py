import streamlit as st
import os,re
from urllib.parse import urlparse
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(page_title="FinShield AI",page_icon="🛡️")
st.title("🛡️ FinShield AI")
st.subheader("Your Financial Safety Assistant")
st.write("Detect scams before you act.")

if "history" not in st.session_state:
    st.session_state.history=[]

def save(s,c):
    st.session_state.history.insert(0,(s,c))
    st.session_state.history=st.session_state.history[:10]

def ai(prompt):
    try:
        if not os.getenv("GEMINI_API_KEY"): return None
        c=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        return c.models.generate_content(
            model="gemini-3.6-flash",contents=prompt).text
    except:
        return None

def detect(t):
    t=t.lower();s=0;w=[];c="Other"
    if "otp" in t:s+=35;c="OTP Scam";w+=["OTP is requested."]
    if any(x in t for x in ["pay","payment","transfer","fee","upi"]):
        s+=25;c="Fake Payment Request";w+=["Money is requested."]
    if any(x in t for x in ["urgent","immediately","today","now"]):
        s+=20;w+=["Creates urgency."]
    if any(x in t for x in ["won","prize","reward","lottery"]):
        s+=30;c="Prize Scam";w+=["Prize or reward is mentioned."]
    if any(x in t for x in ["account blocked","account suspended"]):
        s+=25;c="Account Blocking Scam";w+=["Threatens account action."]
    if "http://" in t or "https://" in t:
        s+=15;w+=["Contains a link."]
    while len(w)<3:w+=["Verify independently."]
    return min(s,100),c,w[:3]

def show(s,c,w,source,amount=""):
    if s>=70:st.error(f"🚨 HIGH RISK — {s}/100")
    elif s>=40:st.warning(f"⚠️ MEDIUM RISK — {s}/100")
    else:st.success(f"🟢 LOW RISK — {s}/100")
    st.progress(s)
    st.info(f"🏷️ {c}  |  🧠 {source}")
    if amount:st.info(f"💰 Amount: {amount}")
    st.markdown("### ⚠️ Warning Signs")
    for x in w:st.write("🔸",x)
    st.markdown("### 🛡️ Recommended Actions")
    st.write("✅ Verify through an official channel.")
    st.write("✅ Never share OTP, PIN, password or CVV.")
    st.write("✅ Do not pay until verified.")

msg,link,pay,hist=st.tabs(
    ["📩 Message Scanner","🔗 Link Scanner","💳 Payment Scanner","🕘 History"])

with msg:
    t=st.text_area("Paste suspicious message",height=130)
    if st.button("🔍 Analyze Message",use_container_width=True):
        if t.strip():
            s,c,w=detect(t)
            show(s,c,w,"FinShield Detector")
            save(s,c)
        else:st.warning("Paste a message first.")

with link:
    u=st.text_input("Paste suspicious URL")
    if st.button("🔗 Check Link",use_container_width=True):
        if u.strip():
            if not u.startswith("http"):u="https://"+u
            p=urlparse(u);w=[]
            if p.scheme=="http":w+=["No HTTPS."]
            if re.match(r"^\d{1,3}(\.\d{1,3}){3}$",p.hostname or ""):
                w+=["Uses an IP address."]
            if "@" in u:w+=["Contains @ symbol."]
            if len(u)>100:w+=["URL is unusually long."]
            if any(x in u.lower() for x in ["login","verify","otp","payment","refund"]):
                w+=["Contains suspicious words."]
            s=min(100,len(w)*25)
            if not w:w=["No obvious structural warning found."]
            show(s,"Link Safety",w,"URL Scanner")
            save(s,"Link Safety")
        else:st.warning("Enter a URL first.")

with pay:
    t=st.text_area("Paste payment request",height=120)
    a=st.text_input("💰 Amount",placeholder="₹999")
    if st.button("🛡️ Analyze Payment",use_container_width=True):
        if t.strip():
            s,c,w=detect(t)
            show(s,c,w,"FinShield Detector",a)
            save(s,c)
        else:st.warning("Paste a payment request first.")

with hist:
    st.subheader("🕘 Recent Scans")
    if st.session_state.history:
        for s,c in st.session_state.history:
            icon="🚨" if s>=70 else "⚠️" if s>=40 else "🟢"
            st.write(f"{icon} **{c}** — {s}/100")
    else:
        st.info("No scans yet.")

st.divider()
st.info("🛡️ FinShield AI — Stay alert. Stay safe.")