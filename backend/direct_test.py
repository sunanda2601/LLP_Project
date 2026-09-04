import sys
import io

# Set stdout/stderr to UTF-8 to prevent cp1252 codec errors in Windows terminal
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, '.')

from app.tools.dictionary_tool import DictionaryTool
from app.tools.translation_tool import TranslationTool
from app.tools.synonym_tool import SynonymTool
from app.tools.antonym_tool import AntonymTool

print("--- Running Direct Backend Verification ---")

# 1. Dictionary Tool
dict_res = DictionaryTool.get_meaning("perseverance")
print("DictionaryTool('perseverance'):", dict_res)
assert dict_res.get("success") is True, "DictionaryTool failed"
assert dict_res.get("word") == "perseverance", "DictionaryTool returned wrong word"
assert dict_res.get("meaning") is not None, "DictionaryTool meaning is empty"

# 2. Translation Tool
trans_res1 = TranslationTool.translate("hello", target="telugu")
print("TranslationTool('hello', target='telugu'):", trans_res1)
assert trans_res1.get("success") is True, "TranslationTool failed for hello to telugu"
assert trans_res1.get("translated_text") in ["నమస్తే", "హలో"], f"TranslationTool returned unexpected translation: {trans_res1.get('translated_text')}"

trans_res2 = TranslationTool.translate("good morning", target="hindi")
print("TranslationTool('good morning', target='hindi'):", trans_res2)
assert trans_res2.get("success") is True, "TranslationTool failed for good morning to hindi"
assert "सुप्रभात" in trans_res2.get("translated_text") or "शुभ प्रभात" in trans_res2.get("translated_text") or "नमस्ते" in trans_res2.get("translated_text"), f"TranslationTool returned unexpected translation: {trans_res2.get('translated_text')}"

# 3. Synonym Tool
syn_res = SynonymTool.get_synonyms("happy")
print("SynonymTool('happy'):", syn_res)
assert syn_res.success is True, "SynonymTool failed"
assert len(syn_res.data.get("synonyms")) > 0, "SynonymTool returned empty synonyms"

# 4. Antonym Tool
ant_res = AntonymTool.get_antonyms("happy")
print("AntonymTool('happy'):", ant_res)
assert ant_res.success is True, "AntonymTool failed"
assert len(ant_res.data.get("antonyms")) > 0, "AntonymTool returned empty antonyms"

print("\n--- Direct Backend Verification Passed Successfully! ---")
