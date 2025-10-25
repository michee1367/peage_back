from flask import Blueprint
from controllers.PicController import change_pic, get_pic, get_defalt_pic
from hashlib import pbkdf2_hmac

pic_route = Blueprint('pic_route', __name__)
pic_route.route('/table_names/<table_name>/records/<enregistrement_id>/change', methods=['POST'])(change_pic)
pic_route.route('/<table_name>/<filename>', methods=['GET'])(get_pic)
pic_route.route('/others/storages/default', methods=['GET'])(get_defalt_pic)
