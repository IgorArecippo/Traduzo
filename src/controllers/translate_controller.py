from flask import Blueprint, render_template, request
from deep_translator import GoogleTranslator
from models.language_model import LanguageModel
from models.history_model import HistoryModel


translate_controller = Blueprint("translate_controller", __name__)


# Reqs. 4 e 5
@translate_controller.route("/", methods=["GET", "POST"])
def index():
    languages = LanguageModel.list_dicts()

    if request.method == "GET":
        return render_template(
            "index.html",
            languages=LanguageModel.list_dicts(),
            to_translate=request.form.get("text-to-ranslate")
            or "O que deseja traduzir",
            translate_from=request.form.get("translate-from") or "pt",
            translate_to=request.form.get("translate-to") or "en",
            translated="Tradução",
        )

    if request.method == "POST":
        languages = (LanguageModel.list_dicts(),)
        to_translate = request.form["text-to-translate"]
        translate_from = request.form["translate-from"]
        translate_to = request.form["translate-to"]
        translated = GoogleTranslator(
            source=translate_from, target=translate_to
        ).translate(to_translate)

    history_dict = {
        "text_to_translate": to_translate,
        "translate_from": translate_from,
        "translate_to": translate_to,
    }
    HistoryModel(history_dict).save()

    return render_template(
        "index.html",
        languages=languages,
        text_to_translate=to_translate,
        translate_from=translate_from,
        translate_to=translate_to,
        translated=translated,
    )


# Req. 6
@translate_controller.route("/reverse", methods=["POST"])
def reverse():
    languages = LanguageModel.list_dicts()
    translate_from = request.form.get("translate-to")
    translate_to = request.form.get("translate-from")
    translated = request.form.get("text-to-translate")
    translator_google = GoogleTranslator(
        source="auto", target=translate_from
    ).translate(translated)
    text_to_translate = translator_google or ""
    return render_template(
        "index.html",
        languages=languages,
        text_to_translate=text_to_translate,
        translate_from=translate_from,
        translate_to=translate_to,
        translated=translated,
    )
