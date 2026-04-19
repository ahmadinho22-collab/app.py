import streamlit as st
import random
import string
import io

# --- 1. إعدادات الصفحة والتصميم ---
st.set_page_config(page_title="مستودع الأبحاث الأكاديمي", page_icon="🎓", layout="centered")

# تنسيق CSS احترافي (تم تصحيح الخطأ هنا)
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    div.stButton > button:first-child {
        background-color: #ff4b4b;
        color: white;
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-size: 18px;
    }
    .stTextInput > div > div > input {
        text-align: right;
        direction: rtl;
    }
    /* تنسيق عنوان الصفحة */
    .main-title {
        text-align: center;
        color: #1f3044;
        font-family: 'Arial';
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">📂 مستودع الأبحاث الرقمي</h1>', unsafe_allow_html=True)

# --- 2. منطق رمز التحقق (CAPTCHA) ---
if 'captcha_text' not in st.session_state:
    st.session_state.captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

def refresh_captcha():
    st.session_state.captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

# --- 3. بناء واجهة الإدخال (Form) ---
with st.form("upload_form", clear_on_submit=False):
    st.subheader("نموذج رفع البيانات")
    
    main_author = st.text_input("اسم المؤلف الرئيسي *")
    extra_author = st.text_input("المؤلف الإضافي (إن وجد)")
    thesis_title = st.text_input("عنوان الرسالة البحثية *")
    
    st.write("---")
    uploaded_file = st.file_uploader("قم برفع الملف بصيغة PDF فقط *", type=["pdf"])
    
    st.write("---")
    st.write("🛡️ رمز التحقق لمنع الإغراق")
    
    col_cap1, col_cap2 = st.columns([1, 2])
    with col_cap1:
        # عرض الرمز بشكل واضح
        st.info(f"الرمز: **{st.session_state.captcha_text}**")
    with col_cap2:
        user_captcha = st.text_input("أدخل الرمز الظاهر أمامك *")

    submit_button = st.form_submit_button("إرسال ورفع الملف")

# --- 4. معالجة البيانات عند الإرسال ---
if submit_button:
    if not main_author or not thesis_title or not uploaded_file:
        st.error("⚠️ يرجى تعبئة الحقول الأساسية ورفع ملف PDF.")
    elif user_captcha.upper() != st.session_state.captcha_text:
        st.error("❌ رمز التحقق غير صحيح، حاول مرة أخرى.")
        refresh_captcha()
        st.rerun()
    else:
        try:
            # ملاحظة: كود الرفع الفعلي لـ Google Drive يتطلب إعداد Secrets 
            # سنقوم هنا بمحاكاة النجاح، وإذا أردت تفعيل الرفع الفعلي سنقوم بخطوة Secrets لاحقاً
            
            with st.spinner('جاري معالجة ورفع الملف...'):
                # هنا يتم استدعاء دالة الرفع (موقوفة مؤقتاً حتى تضع بيانات الاعتماد)
                # upload_to_drive(uploaded_file, "FOLDER_ID", f"{main_author}_{thesis_title}.pdf")
                
                st.success(f"✅ تم استلام البحث بنجاح: {thesis_title}")
                st.balloons()
            
            # تحديث الرمز للمرة القادمة
            refresh_captcha()
            
        except Exception as e:
            st.error(f"حدث خطأ أثناء الرفع: {str(e)}")

# تذييل الصفحة
st.markdown("---")
st.caption("نظام إدارة المستودعات البحثية - 2026")
