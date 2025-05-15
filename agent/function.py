import re
import html

def format_text_for_telegram(text: str) -> str:
    # Экранируем спецсимволы HTML (но НЕ заменяем \n)
    text = html.escape(text)

    # Заголовки: ### → <b>...</b>
    text = re.sub(r'###\s*(.+)', r'<b>\1</b>', text)
    text = re.sub(r'##\s*(.+)', r'<b>\1</b>', text)
    text = re.sub(r'#\s*(.+)', r'<b>\1</b>', text)

    # Маркированные списки: -, *, • → •
    text = re.sub(r'^\s*[-*•]\s+', '• ', text, flags=re.MULTILINE)

    # Очищаем лишние пробелы и добавляем двойной \n
    text = re.sub(r'\n{2,}', '\n\n', text.strip())

    return text
