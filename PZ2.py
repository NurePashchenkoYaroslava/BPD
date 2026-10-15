import sys
sys.stdout.reconfigure(encoding='utf-8')
from collections import Counter

ALPHABET = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"

LETTER_FREQUENCIES = {'а': 0.064, 'б': 0.013,'в': 0.046,'г': 0.013,'ґ': 0.0001, 'д': 0.027,'е': 0.042, 'є': 0.005,'ж': 0.007,
    'з': 0.020,'и': 0.055,'і': 0.044,'ї': 0.010,'й': 0.009,'к': 0.033,'л': 0.027,'м': 0.029,'н': 0.068,'о': 0.086,'п': 0.025,
    'р': 0.043,'с': 0.037,'т': 0.045,'у': 0.027,'ф': 0.003,'х': 0.011,'ц': 0.010,'ч': 0.011,'ш': 0.005,'щ': 0.004,'ь': 0.016,
    'ю': 0.008,'я': 0.019
}


def caesar_cipher(text, shift, decrypt=False):
    if decrypt:
        shift = -shift
    result = ""
    for char in text:
        is_upper = char.isupper()
        c_lower = char.lower()
        if c_lower in ALPHABET:
            idx = ALPHABET.index(c_lower)
            new_char = ALPHABET[(idx + shift) % len(ALPHABET)]
            result += new_char.upper() if is_upper else new_char
        else:
            result += char 
    return result

def score_text(text):
    letters = [char.lower() for char in text if char.lower() in ALPHABET]
    if not letters:
        return float("inf")
    counts = Counter(letters)
    total = len(letters)
    frequency_sum = sum(LETTER_FREQUENCIES.values())
    score = 0.0
    for letter in ALPHABET:
        actual = (counts.get(letter, 0) / total) * 100
        expected = (LETTER_FREQUENCIES[letter] / frequency_sum) * 100  
        score += abs(actual - expected)

    return score

def attack_caesar(ciphertext):
    print("Атака на шифр Цезаря\n")
    letters_only = [c.lower() for c in ciphertext if c.lower() in ALPHABET]
    if not letters_only:
        print("Немає літер для аналізу.")
        return
    most_common_cipher_char = Counter(letters_only).most_common(1)[0][0]
    most_common_ukr_chars = [ 'о', 'н', 'а', 'и', 'в','т', 'і', 'р', 'е', 'с'] 
    best_score = float("inf")
    best_text = ""
    best_shift = 0
    best_guess_char = ""

    for guess_char in most_common_ukr_chars:
        shift = (ALPHABET.index(most_common_cipher_char) - ALPHABET.index(guess_char)) % len(ALPHABET)
        decrypted_text = caesar_cipher(ciphertext, shift, decrypt=True)
        current_score = score_text(decrypted_text)
        if current_score < best_score:
            best_score = current_score
            best_text = decrypted_text
            best_shift = shift
            best_guess_char = guess_char
    print(f"Найчастіший символ шифру: '{most_common_cipher_char}'")
    print(f"Найкраща гіпотеза: це літера '{best_guess_char}'")
    print(f"Знайдений ключ: {best_shift}")
    print(f"Сума відхилень частот: {best_score:.2f}\n")
    print(f"Розшифрований текст:\n{best_text}")


test_cases = [
    (
        "Карл Ліней, творець першої наукової систематики тварин, ставився до метеликів по-особливому і вважав, що вони такі ж яскраві і прекрасні, як і герої міфів. Тому в назвах метеликів зустрічаються імена давньогрецьких богів і героїв.",
        5 
    ),
    (
        "Другий пункт — євроінтеграція, членство в ЄС. Це комплексний пакет, треба багато зробити, щоб там бути. Але це дуже важливо. Колись запитав Катаріну Матернову, посла Європейського Союзу в Україні, якою часткою свого економічного зростання Польща завдячує членству в ЄС? Вона сказала: 50% щонайменше. Це доступ до ринків, дотації, субсидії. Сам факт членства в ЄС означає, що певні реформи проведено.",
        12 
    ),
    (
        "Маленькі косатки залишаються зі своїми мамами на все життя. Навіть коли дорослі сини виростають у величезних дев'ятиметрових красенів, вони все одно плавають поруч із матусею, слухаються її та шукають її підтримки.",
        25
    )
]

for i, (original_text, secret_shift) in enumerate(test_cases, 1):
    print(f"\n{'='*50}")
    print(f"ТЕСТ {i} (Справжній ключ: {secret_shift})")
    print(f"{'='*50}")
    
    print(f"Оригінал:\n{original_text}\n")
    
    encrypted = caesar_cipher(original_text, secret_shift)
    print(f"Зашифровано:\n{encrypted}\n")
    
    attack_caesar(encrypted)
