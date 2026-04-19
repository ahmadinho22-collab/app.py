import streamlit as st
import random
import string

# إعدادات الصفحة
st.set_page_config(page_title="مستودع الأبحاث الأكاديمي", layout="centered")

# تنسيق مخصص باستخدام CSS لجعل الواجهة أكثر احترافية
st.markdown("""
    <style>
    .main { text-align: right; }
    div.stButton > button:first-child {
        background-color: #ff4b4b;
        color: white;
        width: 100%;
        border-radius: 10px;
    }
    input { text-align: right; }
    </style>
    """, unsafe_allow_config=True)

st.title("📂 مستودع الأبحاث الرقمي")
st.subheader("نموذج رفع الرسائل العلمية")

# إنشاء استمارة (Form) لرفع البيانات
with st.form("upload_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        extra_author = st.text_input("المؤلف الإضافي (إن وجد)")
    with col2:
        main_author = st.text_input("اسم المؤلف الرئيسي *")
        
    thesis_title = st.text_input("عنوان الرسالة البحثية *")
    
    uploaded_file = st.file_uploader("قم برفع الملف بصيغة PDF", type=["pdf"])
    
    # قسم رمز التحقق (CAPTCHA بسيط)
    st.write("---")
    if 'captcha_val' not in st.session_state:
        st.session_state.captcha_val = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    
    captcha_col1, captcha_col2 = st.columns([1, 2])
    with captcha_col1:
        st.info(f"رمز التحقق: **{st.session_state.captcha_val}**")
    with captcha_col2:
        user_captcha = st.text_input("أدخل الرمز الظاهر أمامك")

    submit_button = st.form_submit_button("إرسال ورفع الملف")

# معالجة البيانات عند الضغط على الزر
if submit_button:
    if not main_author or not thesis_title or not uploaded_file:
        st.error("يرجى ملء الحقول الأساسية ورفع الملف.")
    elif user_captcha != st.session_state.captcha_val:
        st.error("رمز التحقق غير صحيح، حاول مرة أخرى.")
        # تغيير الرمز بعد محاولة فاشلة
        st.session_state.captcha_val = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    else:
        # هنا يتم وضع كود حفظ الملف (سواء في قاعدة بيانات أو Google Drive أو local)
        st.success(f"تم استلام رسالة: {thesis_title} بنجاح!")
        # تحديث رمز التحقق للمرة القادمة
        st.session_state.captcha_val = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
