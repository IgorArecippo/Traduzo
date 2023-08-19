from flask import Blueprint, json
from models.history_model import HistoryModel

history_controller = Blueprint("history_controller", __name__)


@history_controller.route("/", methods=["GET"])
def index():
    history = HistoryModel.list_as_json()
    data = json.loads(history)

    return data
