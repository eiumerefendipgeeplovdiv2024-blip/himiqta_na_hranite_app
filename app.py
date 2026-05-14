import streamlit as st
import pytesseract
from PIL import Image
import pandas as pd

# ЗА WINDOWS: Трябва да посочиш пътя до инсталирания Tesseract
# Ако си на Linux или Mac, обикновено този ред не е нужен.
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

st.set_page_config(page_title="Локален Скенер за Етикети", page_icon="🚫")

st.title("🚫 Скенер за съставки (Локален)")
st.write("Качи снимка на етикета и приложението ще потърси вредни съставки чрез вградена база данни.")

# База данни с примерни вредни съставки и техните ефекти
DATABASE = {
    "аспартам": "Изкуствен подсладител; потенциално главоболие и метаболитни проблеми.",
    "палмово масло": "Високо съдържание на наситени мазнини; риск от сърдечно-съдови заболявания.",
    "глутамат": "Подобрител на вкуса; може да предизвика свръхчувствителност или главоболие.",
    "е133": "Синтетичен оцветител; риск от алергични реакции.",
    "е102": "Тартразин; хиперактивност при деца и алергии.",
    "натриев нитрит": "Консервант в месата; свързва се с риск от канцерогенни процеси при прекомерна консумация.",
    "фруктозен сироп": "Високо съдържание на захар; риск от затлъстяване и диабет тип 2.",
    "хидрогенирани мазнини": "Трансмазнини; повишават лошия холестерол и риска от инфаркт."
}

uploaded_file = st.file_uploader("Качи снимка на етикет...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Качена снимка', width=300)
    
    if st.button("Провери съставките"):
        with st.spinner("Разчитане на текста..."):
            # Извличане на текст от снимката (на български и английски)
            try:
                extracted_text = pytesseract.image_to_string(image, lang='bul+eng').lower()
                
                results = []
                found_any = False

                # Проверка на всяка съставка от нашата база данни в извлечения текст
                for ingredient, effect in DATABASE.items():
                    if ingredient in extracted_text:
                        results.append({
                            "Съставка": ingredient.capitalize(),
                            "Статус": "⚠️ Вредна",
                            "Бъдещи ефекти": effect
                        })
                        found_any = True

                if found_any:
                    st.subheader("📊 Резултати от анализа")
                    df = pd.DataFrame(results)
                    st.table(df)
                else:
                    st.success("Не бяха открити познати вредни съставки в този етикет.")
                    st.write("Текстът, който разчетох, е:")
                    st.text(extracted_text)

            except Exception as e:
                st.error(f"Грешка при разчитането: {e}")
                st.info("Увери се, че Tesseract OCR е инсталиран правилно на твоя компютър.")

st.divider()
st.caption("Забележка: Този скенер работи локално и разпознава само съставките, добавени в неговата база данни.")
