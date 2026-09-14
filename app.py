import streamlit as st
import re
from urllib.parse import urlparse

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="FinShield AI",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- CUSTOM STYLE ----------------

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.hero {
    padding: 25px;
    border-radius: 18px;
    background-color: #0b1f3a;
    color: white;
    margin-bottom: 25px;
}

.card {
    padding: 20px;
    border-radius: 16px;
    background-color: white;
    border: 1px solid #e5e7eb;
    margin-bottom: 15px;
}

.small {
    color: #cbd5e1;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">

<h1>🛡️ FinShield AI</h1>

<p style="font-size:20px;">
Your AI-powered Financial Safety Assistant
</p>

<p class="small">
Detect phishing, fake payment requests, OTP scams and suspicious links before you act.
</p>

</div>
""", unsafe_allow_html=True)

# ---------------- HISTORY ----------------

if "history" not in st.session_state:
    st.session_state.history = []


def save(score, category):
    st.session_state.history.insert(
        0,
        (score, category)
    )

    st.session_state.history = (
        st.session_state.history[:10]
    )


# ---------------- SCAM DETECTOR ----------------

def detect(text):

    text = text.lower()

    score = 0
    warnings = []
    category = "Other"

    # OTP detection
    if "otp" in text:

        score += 35
        category = "OTP Scam"

        warnings.append(
            "OTP is requested."
        )

    # Payment detection
    if any(
        word in text
        for word in [
            "pay",
            "payment",
            "transfer",
            "fee",
            "upi"
        ]
    ):

        score += 25
        category = "Fake Payment Request"

        warnings.append(
            "Money is requested."
        )

    # Urgency detection
    if any(
        word in text
        for word in [
            "urgent",
            "immediately",
            "today",
            "now",
            "act fast",
            "within minutes"
        ]
    ):

        score += 20

        warnings.append(
            "Creates urgency or pressure."
        )

    # Prize detection
    if any(
        word in text
        for word in [
            "won",
            "prize",
            "reward",
            "lottery",
            "cashback",
            "congratulations"
        ]
    ):

        score += 30

        category = "Prize Scam"

        warnings.append(
            "Prize or reward is mentioned."
        )

    # Account blocking detection
    if any(
        word in text
        for word in [
            "account blocked",
            "account suspended",
            "account will be blocked",
            "account will be suspended"
        ]
    ):

        score += 25

        category = "Account Blocking Scam"

        warnings.append(
            "Threatens account action."
        )

    # Link detection
    if (
        "http://" in text
        or "https://" in text
    ):

        score += 15

        warnings.append(
            "Contains a link."
        )

    # Personal information detection
    if any(
        word in text
        for word in [
            "password",
            "pin",
            "cvv",
            "card number",
            "bank details"
        ]
    ):

        score += 25

        warnings.append(
            "Requests sensitive financial information."
        )

    # Make sure we have at least 3 warnings
    while len(warnings) < 3:

        warnings.append(
            "Verify the request independently."
        )

    score = min(score, 100)

    return (
        score,
        category,
        warnings[:3]
    )


# ---------------- RESULT DISPLAY ----------------

def show_result(
    score,
    category,
    warnings,
    source,
    amount=""
):

    # Risk level

    if score >= 70:

        st.error(
            f"🚨 HIGH RISK — {score}/100"
        )

    elif score >= 40:

        st.warning(
            f"⚠️ MEDIUM RISK — {score}/100"
        )

    else:

        st.success(
            f"🟢 LOW RISK — {score}/100"
        )

    # Progress bar

    st.progress(score)

    # Result cards

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="card">
            <b>🏷️ Category</b>
            <br>
            {category}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="card">
            <b>🧠 Detection</b>
            <br>
            {source}
            </div>
            """,
            unsafe_allow_html=True
        )

    # Amount

    if amount:

        st.info(
            f"💰 Payment Amount: {amount}"
        )

    # Warning signs

    st.markdown(
        "### ⚠️ Warning Signs"
    )

    for warning in warnings:

        st.write(
            "🔸",
            warning
        )

    # Actions

    st.markdown(
        "### 🛡️ What You Should Do"
    )

    st.write(
        "✅ Verify through an official channel."
    )

    st.write(
        "✅ Never share OTP, PIN, password or CVV."
    )

    st.write(
        "✅ Do not make a payment until verified."
    )


# ---------------- TABS ----------------

message_tab, link_tab, payment_tab, history_tab = st.tabs(
    [
        "📩 Message Scanner",
        "🔗 Link Scanner",
        "💳 Payment Scanner",
        "🕘 Scan History"
    ]
)


# ==================================================
# MESSAGE SCANNER
# ==================================================

with message_tab:

    st.markdown(
        "### 📩 Message Scam Detection"
    )

    st.caption(
        "Paste an SMS, WhatsApp message, email or suspicious notification."
    )

    message = st.text_area(
        "Suspicious message",
        height=150,
        placeholder=(
            "Example: URGENT! Your bank account will be "
            "blocked today. Verify your account immediately "
            "by clicking this link and entering your OTP..."
        )
    )

    if st.button(
        "🔍 Analyze Message",
        use_container_width=True
    ):

        if message.strip():

            score, category, warnings = detect(
                message
            )

            show_result(
                score,
                category,
                warnings,
                "FinShield Detector"
            )

            save(
                score,
                category
            )

        else:

            st.warning(
                "Please paste a message first."
            )


# ==================================================
# LINK SCANNER
# ==================================================

with link_tab:

    st.markdown(
        "### 🔗 Suspicious Link Detection"
    )

    st.caption(
        "Checks the URL structure without opening the website."
    )

    url = st.text_input(
        "Suspicious URL",
        placeholder="https://example.com/login"
    )

    if st.button(
        "🔗 Check Link",
        use_container_width=True
    ):

        if url.strip():

            if not url.startswith(
                ("http://", "https://")
            ):

                url = "https://" + url

            parsed = urlparse(url)

            warnings = []

            # HTTP check

            if parsed.scheme == "http":

                warnings.append(
                    "The URL does not use HTTPS."
                )

            # IP address check

            if re.match(
                r"^\d{1,3}(\.\d{1,3}){3}$",
                parsed.hostname or ""
            ):

                warnings.append(
                    "The URL uses an IP address instead of a domain name."
                )

            # @ symbol

            if "@" in url:

                warnings.append(
                    "The URL contains an @ symbol."
                )

            # Long URL

            if len(url) > 100:

                warnings.append(
                    "The URL is unusually long."
                )

            # Suspicious words

            if any(
                word in url.lower()
                for word in [
                    "login",
                    "verify",
                    "otp",
                    "payment",
                    "refund",
                    "account"
                ]
            ):

                warnings.append(
                    "The URL contains suspicious keywords."
                )

            # Risk score

            score = min(
                100,
                len(warnings) * 25
            )

            if not warnings:

                warnings = [
                    "No obvious structural warning found."
                ]

            show_result(
                score,
                "Link Safety",
                warnings[:3],
                "URL Scanner"
            )

            save(
                score,
                "Link Safety"
            )

        else:

            st.warning(
                "Please enter a URL first."
            )


# ==================================================
# PAYMENT SCANNER
# ==================================================

with payment_tab:

    st.markdown(
        "### 💳 Payment Scam Detection"
    )

    st.caption(
        "Analyze suspicious payment or money-transfer requests."
    )

    payment_message = st.text_area(
        "Payment request",
        height=130,
        placeholder=(
            "Example: Congratulations! You won ₹50,000. "
            "Pay ₹999 processing fee to claim your reward."
        )
    )

    amount = st.text_input(
        "💰 Amount",
        placeholder="₹999"
    )

    if st.button(
        "🛡️ Analyze Payment",
        use_container_width=True
    ):

        if payment_message.strip():

            score, category, warnings = detect(
                payment_message
            )

            show_result(
                score,
                category,
                warnings,
                "FinShield Detector",
                amount
            )

            save(
                score,
                category
            )

        else:

            st.warning(
                "Please enter a payment request."
            )


# ==================================================
# HISTORY
# ==================================================

with history_tab:

    st.markdown(
        "### 🕘 Recent Scans"
    )

    if st.session_state.history:

        for score, category in st.session_state.history:

            if score >= 70:

                icon = "🚨"

            elif score >= 40:

                icon = "⚠️"

            else:

                icon = "🟢"

            st.markdown(
                f"""
                <div class="card">
                {icon}
                <b>{category}</b>
                <br>
                Risk Score:
                <b>{score}/100</b>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.info(
            "No scans yet. Start by analyzing a message."
        )


# ---------------- FOOTER ----------------

st.divider()

st.markdown(
    """
    <center>
    🛡️ <b>FinShield AI</b>
    • Stay Alert • Stay Safe
    </center>
    """,
    unsafe_allow_html=True
)