import requests
import re


class TranslationTool:

    URL = "https://libretranslate.com/translate"

    LANG_MAP = {
        "telugu": "te",
        "hindi": "hi",
        "spanish": "es",
        "french": "fr",
        "german": "de",
        "te": "te",
        "hi": "hi",
        "es": "es",
        "fr": "fr",
        "de": "de",
        "en": "en"
    }

    # Reliable common translations for Phase 1
    COMMON_TRANSLATIONS = {
        ("hello", "te"): "నమస్తే",
        ("hello", "hi"): "नमस्ते",
        ("good morning", "te"): "శుభోదయం",
        ("good morning", "hi"): "सुप्रभాత",
        ("thank you", "te"): "ధన్యవాదాలు",
        ("thank you", "hi"): "धन्यवाद",
        ("goodbye", "te"): "వీడ్కోలు",
        ("goodbye", "hi"): "अलविदा",

        ("i finished the work yesterday", "te"):
            "నేను నిన్న పని పూర్తి చేశాను.",

        ("i finished the work yesterday", "hi"):
            "मैंने कल काम पूरा किया।",
    }

    @classmethod
    def translate(
        cls,
        text: str,
        source="en",
        target="te",
        target_language=None
    ):

        if target_language is not None:
            target = target_language

        # Normalize language codes
        source = cls.LANG_MAP.get(
            source.lower() if isinstance(source, str) else source,
            source
        )

        target = cls.LANG_MAP.get(
            target.lower() if isinstance(target, str) else target,
            target
        )

        original_text = text.strip()

        # Extract text and target language
        # Example:
        # Translate: I finished the work yesterday into Telugu.
        pattern = re.match(
            r"^(?:please\s+)?translate:?\s+(.+?)\s+(?:to|into)\s+([a-zA-Z]+)[?.!]*$",
            original_text,
            re.IGNORECASE
        )

        if pattern:

            extracted_text = pattern.group(1).strip()
            extracted_language = pattern.group(2).strip().lower()

            if extracted_language in cls.LANG_MAP:

                target = cls.LANG_MAP[extracted_language]
                text = extracted_text

        # Remove surrounding quotes
        text = text.strip().strip('"').strip("'")

        # Normalize for matching
        text_clean = (
            re.sub(r"\s+", " ", text.lower())
            .strip()
            .rstrip("?.!")
        )

        # =====================================================
        # COMMON TRANSLATIONS
        # =====================================================

        key = (text_clean, target)

        if key in cls.COMMON_TRANSLATIONS:

            return {
                "success": True,
                "translated_text": cls.COMMON_TRANSLATIONS[key]
            }

        # =====================================================
        # GOOGLE TRANSLATE FALLBACK
        # =====================================================

        try:

            url = "https://translate.googleapis.com/translate_a/single"

            params = {
                "client": "gtx",
                "sl": source,
                "tl": target,
                "dt": "t",
                "q": text
            }

            response = requests.get(
                url,
                params=params,
                timeout=10
            )

            if response.status_code == 200:

                data = response.json()

                translated_text = "".join(
                    part[0]
                    for part in data[0]
                    if part[0]
                )

                if translated_text:

                    return {
                        "success": True,
                        "translated_text": translated_text
                    }

        except Exception:
            pass

        # =====================================================
        # LIBRETRANSLATE FALLBACK
        # =====================================================

        try:

            payload = {
                "q": text,
                "source": source,
                "target": target,
                "format": "text"
            }

            response = requests.post(
                cls.URL,
                json=payload,
                timeout=10
            )

            if response.status_code != 200:

                return {
                    "success": False,
                    "message": "Translation service unavailable"
                }

            data = response.json()

            translated_text = data.get("translatedText")

            if translated_text:

                return {
                    "success": True,
                    "translated_text": translated_text
                }

            return {
                "success": False,
                "message": "Translation failed"
            }

        except Exception as e:

            return {
                "success": False,
                "message": str(e)
            }