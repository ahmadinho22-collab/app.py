import streamlit as st
import random
import string
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload
import io

# --- إعدادات الوصول إلى Google Drive ---
# ملاحظة: يجب وضع بيانات الاعتماد في st.secrets عند النشر على GitHub
def upload_to_drive(file, folder_id, file_name):
    # تحميل بيانات الاعتماد من Secrets (للأمان)
    creds_info = st.secrets["gcp_service_account"]
    creds = service_account.Credentials.from_service_account_info(creds_info)
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    
    # تحويل الملف المرفوع إلى تنسيق يفهمه Google Drive
    media = MediaIoBaseUpload(io.BytesIO(file.getvalue()), mimetype='application/pdf')
    
    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    return uploaded_file.get('id')

# --- واجهة المستخدم ---
st.set_page_config(page_title="مستودع الأبحاث", page_icon="🎓")

# تحسين المظهر
st.markdown("""
    <style>
    .stApp { text-align: right; }
    div[data-testid="stMarkdownContainer"] > p { text-align: right; }
    .main-title { color: #2E4053; font-size: 40px; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🎓 مستودع الأبحاث الأكاديمي</p>', unsafe_allow_html=True)
st.info("يرجى تعبئة البيانات التالية لرفع البحث الخاص بك إلى المستودع الرقمي.")

# إدارة حالة رمز التحقق
if 'captcha_text' not in st.session_state:
    st.session_state.captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

with st.form("research_form"):
    title = st.text_input("عنوان الرسالة / البحث *")
    main_author = st.text_input("اسم المؤلف الرئيسي *")
    co_author = st.text_input("المؤلف المشارك (إن وجد)")
    
    uploaded_pdf = st.file_uploader("ارفق ملف البحث (صيغة PDF فقط) *", type="pdf")
    
    st.write("---")
    # عرض رمز التحقق
    c1, c2 = st.columns([1, 2])
    with c1:
        st.code(st.session_state.captcha_text, language="text")
    with c2:
        captcha_input = st.text_input("أدخل رمز التحقق الظاهر بجانبك لمنع الإغراق *")

    submit = st.form_submit_button("رفع الملف الآن")

if submit:
    if not (title and main_author and uploaded_pdf and captcha_input):
        st.warning("الرجاء إكمال كافة الحقول المطلوبة.")
    elif captcha_input.upper() != st.session_state.captcha_text:
        st.error("رمز التحقق غير صحيح، يرجى المحاولة مرة أخرى.")
        st.session_state.captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    else:
        try:
            # معالجة الرفع (يجب وضع Folder ID الخاص بك هنا)
            FOLDER_ID = "ضع_هنا_ID_مجلد_جوجل_درايف" 
            file_name = f"{main_author} - {title}.pdf"
            
            with st.spinner('جاري رفع الملف إلى المستودع...'):
                # ملاحظة: هذه الدالة تتطلب إعداد Secrets للعمل
                # upload_to_drive(uploaded_pdf, FOLDER_ID, file_name)
                
                st.success(f"تم رفع '{title}' بنجاح! شكراً لمساهمتك.")
                
            # تحديث رمز التحقق بعد النجاح
            st.session_state.captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        except Exception as e:
            st.error(f"حدث خطأ أثناء الرفع: {e}")
