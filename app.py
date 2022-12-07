from flask import Flask, request
import uuid
from rlogger import Log
from orm_sqlalchemy import Database
from messages import Messages
from schemas import UserSchema
from utils import Utilities


app = Flask(__name__)


@app.route("/adduser", methods=["POST"])
def add_user():
    REQUEST_TRACEBACK_CODE = uuid.uuid4()

    recived_data = request.get_json()
    if recived_data is None or recived_data == {}:
        Log("add_user").add_info("Bad Request", REQUEST_TRACEBACK_CODE)
        return Messages(REQUEST_TRACEBACK_CODE).message_return_400()

    else:
        try:

            PAYLOAD = UserSchema().load(recived_data)

            db = Database(REQUEST_TRACEBACK_CODE)

            if PAYLOAD["password"] is None or PAYLOAD["password"] == "":
                password = Utilities().generate_random_password()

            else:
                password = PAYLOAD["password"]

            print("USER PASSWORD = ", password)

            db.add_user(
                name=PAYLOAD["name"],
                email=PAYLOAD["email"],
                role_id=PAYLOAD["role_id"],
                password=password,
            )

            Log("add_user").add_info("User added", REQUEST_TRACEBACK_CODE)
            msg = Messages(REQUEST_TRACEBACK_CODE).message_return_201()

        except Exception as e:
            Log("add_user").add_info("Bad Request", REQUEST_TRACEBACK_CODE)
            Log("add_user").add_error(e, REQUEST_TRACEBACK_CODE)
            msg = Messages(REQUEST_TRACEBACK_CODE).message_return_400(
                message=f"Bad Request - {e} - Traceback_code = {REQUEST_TRACEBACK_CODE}"
            )

        finally:

            return msg


@app.route("/user/<id>/role", methods=["GET"])
def get_user_role(id):
    REQUEST_TRACEBACK_CODE = uuid.uuid4()

    try:
        db = Database(REQUEST_TRACEBACK_CODE)

        role_id = db.get_user_role(user_id=id)

        if role_id["status_code"] == 200:

            Log("get_user_role").add_info("User role retrieved", REQUEST_TRACEBACK_CODE)
            msg = Messages(REQUEST_TRACEBACK_CODE).message_return_200(
                message=f"User role retrieved successfully - Role_ID:{role_id['data']}"
            )
        else:
            Log("get_user_role").add_info("Bad Request", REQUEST_TRACEBACK_CODE)
            msg = Messages(REQUEST_TRACEBACK_CODE).message_return_404(
                message=f"Not found =["
            )

    except Exception as e:
        Log("get_user_role").add_info("Bad Request", REQUEST_TRACEBACK_CODE)
        Log("get_user_role").add_error(e, REQUEST_TRACEBACK_CODE)
        msg = Messages(REQUEST_TRACEBACK_CODE).message_return_400(
            message=f"Bad Request - {e} - Traceback_code = {REQUEST_TRACEBACK_CODE}"
        )

    finally:

        return msg


if __name__ == "__main__":
    app.run(debug=True, port=5000)
