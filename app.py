import streamlit as st
import requests

# ۱. تنظیمات اولیه ظاهر وب‌سایت
st.set_page_config(page_title="دستیار پاشا", layout="wide")

# استایل شیک و حرفه‌ای تریدینگ‌ویو
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #1c2030 0%, #0c0e17 100%);
    }
    div[data-testid="stColumn"] {
        background-color: #131722 !important;
        padding: 25px !important;
        border-radius: 12px !important;
        border: 1px solid #2a2e39 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .stNumberInput div div input {
        background-color: #1e222d !important;
        color: #ffffff !important;
        border: 1px solid #2a2e39 !important;
        border-radius: 6px !important;
    }
    .stButton button {
        background: linear-gradient(135deg, #2962ff 0%, #1e40af 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 10px !important;
        font-weight: bold;
    }
    h1, h2, h3, p, span, label { color: #d1d4dc !important; }
    h1 { color: #ffffff !important; }
    .stMetric {
        background-color: #1e222d !important;
        padding: 15px !important;
        border-radius: 8px !important;
        border: 1px solid #2962ff !important;
    }
    div[data-testid="stText"] {
        background-color: #1e222d !important;
        padding: 12px !important;
        border-radius: 6px !important;
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ۲. فرمول ریاضی محاسبات جامع پیووت کلاسیک و کاماریلا
def calculate_all_levels(high, low, close):
    range_hl = high - low
    pp = (high + low + close) / 3
    r1 = (2 * pp) - low
    r2 = pp + range_hl
    s1 = (2 * pp) - high
    s2 = pp - range_hl
    
    r4 = close + (range_hl * 1.1 / 2)
    r3 = close + (range_hl * 1.1 / 4)
    s3 = close - (range_hl * 1.1 / 4)
    s4 = close - (range_hl * 1.1 / 2)
    
    return {
        "PP": pp, "R1": r1, "R2": r2, "S1": s1, "S2": s2,
        "R4_cam": r4, "R3_cam": r3, "S3_cam": s3, "S4_cam": s4
    }

# ۳. طراحی ظاهر صفحه
st.title("📈 وب‌سایت شخصی و دستیار معاملاتی پاشا")
st.write("تحلیل فاندامنتال زنده و محاسبات دقیق سطوح بازار")
st.markdown("---")

ستون_راست, ستون_چپ = st.columns([1, 1])

with ستون_راست:
    st.subheader("🧮 ماشین حساب قیمتی")
    high_input = st.number_input("سقف قیمت دیروز (High):", value=4112.0, step=0.01)
    low_input = st.number_input("کف قیمت دیروز (Low):", value=4050.0, step=0.01)
    close_input = st.number_input("قیمت کلوز دیروز (Close):", value=4087.0, step=0.01)
    
    if st.button("محاسبه سطوح"):
        st.session_state.calculated_data = calculate_all_levels(high_input, low_input, close_input)

with ستون_چپ:
    st.subheader("💬 گفتگو با پاشا (تحلیل فاندامنتال)")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "سلام رفیق! موتور هوش مصنوعی جدید و بدون محدودیت فعال شد. بپرس تا بازار رو برات کالبدشکافی کنم!"}]
        
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    if user_say := st.chat_input("سوال خودت رو بپرس..."):
        st.session_state.messages.append({"role": "user", "content": user_say})
        with st.chat_message("user"):
            st.write(user_say)
            
        with st.chat_message("assistant"):
            with st.spinner("پاشا در حال تحلیل بازار..."):
                try:
                    # اتصال به سرور نهایی و کاملاً رایگان بدون نیاز به توکن
                    url = "https://openrouter.ai/api/v1/chat/completions"
                    headers = {
                        "Authorization": "Bearer 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",
                        "Content-Type": "application/json"
                    }
                    payload = {
                        "model": "google/gemini-2.5-flash",
                        "messages": [
                            {"role": "system", "content": "تو یک دستیار فاندامنتال ارشد بازار به نام پاشا هستی. لحن تو باید کاملاً رفیقانه، خلاصه و متمرکز بر تحلیل تکنیکال و بازار باشد. به زبان فارسی روان پاسخ بده و اصلاً جملات تکراری نگو."},
                            {"role": "user", "content": user_say}
                        ]
                    }
                    
                    response = requests.post(url, json=payload, headers=headers, timeout=15)
                    
                    if response.status_code == 200:
                        reply = response.json()['choices'][0]['message']['content']
                    else:
                        reply = "رفیق درخواست ارسال شد اما پاسخ دریافتی نوسان داشت. لطفاً مجدداً سوالت رو بفرست تا بررسی کنم."
                        
                except Exception as e:
                    reply = "خطای اتصال رخ داد. لطفاً وضعیت اینترنت یا فیلترشکن رو بررسی کن و دوباره پیام بده."
                
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

# ۴. بخش نمایش سراسری سطوح محاسباتی
if "calculated_data" in st.session_state:
    st.markdown("---")
    st.subheader("📊 سطوح محاسباتی استخراج شده")
    col1, col2 = st.columns(2)
    data = st.session_state.calculated_data
    with col1:
        st.info("🔹 سطوح پیووت کلاسیک (Classic Pivot Points)")
        st.metric(label="🎯 نقطه پیووت اصلی (PP)", value=f"{data['PP']:.2f}")
        st.text(f"🟢 مقاومت دو (R2): {data['R2']:.2f}")
        st.text(f"🟢 مقاومت یک (R1): {data['R1']:.2f}")
        st.text(f"🔴 حمایت یک (S1): {data['S1']:.2f}")
        st.text(f"🔴 حمایت دو (S2): {data['S2']:.2f}")
    with col2:
        st.info("🔸 سطوح کاماریلا (Camarilla Levels)")
        st.text(f"🔺 مرز شکست صعودی (R4): {data['R4_cam']:.2f}")
        st.text(f"🔺 منطقه فروش/برگشت (R3): {data['R3_cam']:.2f}")
        st.text(f"🔻 منطقه خرید/برگشت (S3): {data['S3_cam']:.2f}")
        st.text(f"🔻 مرز شکست ریزشی (S4): {data['S4_cam']:.2f}")
        
