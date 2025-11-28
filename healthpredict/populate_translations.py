import polib
import os

# Dictionary of translations
translations = {
    "Health Prediction Platform": {
        "hi": "स्वास्थ्य भविष्यवाणी मंच",
        "ja": "健康予測プラットフォーム",
        "zh_Hans": "健康预测平台",
        "ur": "صحت کی پیشن گوئی کا پلیٹ فارم"
    },
    "Home": {
        "hi": "घर",
        "ja": "ホーム",
        "zh_Hans": "首页",
        "ur": "گھر"
    },
    "About": {
        "hi": "के बारे में",
        "ja": "約",
        "zh_Hans": "关于",
        "ur": "کے بارے میں"
    },
    "Services": {
        "hi": "सेवाएं",
        "ja": "サービス",
        "zh_Hans": "服务",
        "ur": "خدمات"
    },
    "Assessment": {
        "hi": "मूल्यांकन",
        "ja": "評価",
        "zh_Hans": "评估",
        "ur": "تشخیص"
    },
    "Dashboard": {
        "hi": "डैशबोर्ड",
        "ja": "ダッシュボード",
        "zh_Hans": "仪表板",
        "ur": "ڈیش بورڈ"
    },
    "Profile": {
        "hi": "प्रोफ़ाइल",
        "ja": "プロフィール",
        "zh_Hans": "个人资料",
        "ur": "پروفائل"
    },
    "Assessment History": {
        "hi": "मूल्यांकन इतिहास",
        "ja": "評価履歴",
        "zh_Hans": "评估历史",
        "ur": "تشخیص کی تاریخ"
    },
    "Logout": {
        "hi": "लॉग आउट",
        "ja": "ログアウト",
        "zh_Hans": "登出",
        "ur": "لاگ آؤٹ"
    },
    "Login": {
        "hi": "लॉग इन करें",
        "ja": "ログイン",
        "zh_Hans": "登录",
        "ur": "لاگ ان کریں"
    },
    "Register": {
        "hi": "पंजीकरण",
        "ja": "登録",
        "zh_Hans": "注册",
        "ur": "رجسٹر کریں"
    },
    "Predictive Healthcare": {
        "hi": "भविष्यवाणी स्वास्थ्य सेवा",
        "ja": "予測医療",
        "zh_Hans": "预测性医疗保健",
        "ur": "پیشن گوئی صحت کی دیکھ بھال"
    },
    "Powered by AI": {
        "hi": "एआई द्वारा संचालित",
        "ja": "AI搭載",
        "zh_Hans": "由人工智能驱动",
        "ur": "AI کے ذریعہ تقویت یافتہ"
    },
    "Start Assessment": {
        "hi": "मूल्यांकन शुरू करें",
        "ja": "評価を開始",
        "zh_Hans": "开始评估",
        "ur": "تشخیص شروع کریں"
    },
    "View Dashboard": {
        "hi": "डैशबोर्ड देखें",
        "ja": "ダッシュボードを表示",
        "zh_Hans": "查看仪表板",
        "ur": "ڈیش بورڈ دیکھیں"
    },
    "Get Started": {
        "hi": "शुरू करें",
        "ja": "始める",
        "zh_Hans": "开始",
        "ur": "شروع کریں"
    },
    "Learn More": {
        "hi": "अधिक जानें",
        "ja": "もっと詳しく",
        "zh_Hans": "了解更多",
        "ur": "مزید جانیں"
    },
    "Advanced Health Prediction": {
        "hi": "उन्नत स्वास्थ्य भविष्यवाणी",
        "ja": "高度な健康予測",
        "zh_Hans": "高级健康预测",
        "ur": "اعلی درجے کی صحت کی پیشن گوئی"
    },
    "Heart Disease": {
        "hi": "हृदय रोग",
        "ja": "心臓病",
        "zh_Hans": "心脏病",
        "ur": "دل کی بیماری"
    },
    "Diabetes Risk": {
        "hi": "मधुमेह जोखिम",
        "ja": "糖尿病リスク",
        "zh_Hans": "糖尿病风险",
        "ur": "ذیابیطس کا خطرہ"
    },
    "Cancer Screening": {
        "hi": "कैंसर स्क्रीनिंग",
        "ja": "がん検診",
        "zh_Hans": "癌症筛查",
        "ur": "کینسر کی اسکریننگ"
    },
    "Stroke Prevention": {
        "hi": "स्ट्रोक रोकथाम",
        "ja": "脳卒中予防",
        "zh_Hans": "中风预防",
        "ur": "فالج کی روک تھام"
    },
    "Platform Statistics": {
        "hi": "मंच सांख्यिकी",
        "ja": "プラットフォーム統計",
        "zh_Hans": "平台统计",
        "ur": "پلیٹ فارم کے اعدادوشمار"
    },
    "Health Assessments": {
        "hi": "स्वास्थ्य मूल्यांकन",
        "ja": "健康評価",
        "zh_Hans": "健康评估",
        "ur": "صحت کے جائزے"
    },
    "Prediction Accuracy": {
        "hi": "भविष्यवाणी सटीकता",
        "ja": "予測精度",
        "zh_Hans": "预测准确性",
        "ur": "پیشن گوئی کی درستگی"
    },
    "Active Users": {
        "hi": "सक्रिय उपयोगकर्ता",
        "ja": "アクティブユーザー",
        "zh_Hans": "活跃用户",
        "ur": "فعال صارفین"
    },
    "Support Available": {
        "hi": "समर्थन उपलब्ध",
        "ja": "サポート利用可能",
        "zh_Hans": "提供支持",
        "ur": "سپورٹ دستیاب ہے"
    },
    "How It Works": {
        "hi": "यह कैसे काम करता है",
        "ja": "仕組み",
        "zh_Hans": "它是如何工作的",
        "ur": "یہ کیسے کام کرتا ہے"
    },
    "Create Profile": {
        "hi": "प्रोफ़ाइल बनाएं",
        "ja": "プロフィール作成",
        "zh_Hans": "创建个人资料",
        "ur": "پروفائل بنائیں"
    },
    "Health Assessment": {
        "hi": "स्वास्थ्य मूल्यांकन",
        "ja": "健康評価",
        "zh_Hans": "健康评估",
        "ur": "صحت کا جائزہ"
    },
    "Get Results": {
        "hi": "परिणाम प्राप्त करें",
        "ja": "結果を取得",
        "zh_Hans": "获取结果",
        "ur": "نتائج حاصل کریں"
    },
    "Ready to Assess Your Health?": {
        "hi": "क्या आप अपने स्वास्थ्य का आकलन करने के लिए तैयार हैं?",
        "ja": "健康状態を評価する準備はできましたか？",
        "zh_Hans": "准备好评估您的健康了吗？",
        "ur": "کیا آپ اپنی صحت کا اندازہ لگانے کے لیے تیار ہیں؟"
    },
    "Start Health Assessment": {
        "hi": "स्वास्थ्य मूल्यांकन शुरू करें",
        "ja": "健康評価を開始",
        "zh_Hans": "开始健康评估",
        "ur": "صحت کا جائزہ شروع کریں"
    },
    "Get Started Free": {
        "hi": "मुफ्त में शुरू करें",
        "ja": "無料で始める",
        "zh_Hans": "免费开始",
        "ur": "مفت شروع کریں"
    },
    "Quick Links": {
        "hi": "त्वरित लिंक",
        "ja": "クイックリンク",
        "zh_Hans": "快速链接",
        "ur": "فوری روابط"
    },
    "Support": {
        "hi": "समर्थन",
        "ja": "サポート",
        "zh_Hans": "समर्थन",
        "ur": "سپورٹ"
    },
    "Help Center": {
        "hi": "सहायता केंद्र",
        "ja": "ヘルプセンター",
        "zh_Hans": "帮助中心",
        "ur": "مدد کا مرکز"
    },
    "Privacy Policy": {
        "hi": "गोपनीयता नीति",
        "ja": "プライバシーポリシー",
        "zh_Hans": "隐私政策",
        "ur": "رازداری کی پالیسی"
    },
    "Terms of Service": {
        "hi": "सेवा की शर्तें",
        "ja": "利用規約",
        "zh_Hans": "服务条款",
        "ur": "سروس کی شرائط"
    },
    "Contact Us": {
        "hi": "संपर्क करें",
        "ja": "お問い合わせ",
        "zh_Hans": "联系我们",
        "ur": "ہم سے رابطہ کریں"
    },
    "All rights reserved.": {
        "hi": "सर्वाधिकार सुरक्षित।",
        "ja": "全著作権所有。",
        "zh_Hans": "版权所有。",
        "ur": "جملہ حقوق محفوظ ہیں۔"
    }
}

def populate_po_files():
    locales = ['hi', 'ja', 'zh_Hans', 'ur']
    base_dir = 'healthpredict/locale'
    
    for locale in locales:
        po_path = os.path.join(base_dir, locale, 'LC_MESSAGES', 'django.po')
        if not os.path.exists(po_path):
            print(f"File not found: {po_path}")
            continue
            
        print(f"Processing {locale}...")
        po = polib.pofile(po_path)
        
        count = 0
        for entry in po:
            if entry.msgid in translations:
                if locale in translations[entry.msgid]:
                    entry.msgstr = translations[entry.msgid][locale]
                    count += 1
            # Fallback for long strings or partial matches (simple heuristic)
            elif "machine learning" in entry.msgid.lower():
                 if locale == 'hi': entry.msgstr = "उन्नत मशीन लर्निंग मॉडल आपके स्वास्थ्य डेटा का विश्लेषण करते हैं।"
                 elif locale == 'ja': entry.msgstr = "高度な機械学習モデルがあなたの健康データを分析します。"
                 elif locale == 'zh_Hans': entry.msgstr = "先进的机器学习模型分析您的健康数据。"
                 elif locale == 'ur': entry.msgstr = "اعلی درجے کی مشین لرننگ ماڈل آپ کے صحت کے اعداد و شمار کا تجزیہ کرتے ہیں۔"
                 count += 1
        
        po.save()
        print(f"Updated {count} translations for {locale}.")

if __name__ == "__main__":
    populate_po_files()
