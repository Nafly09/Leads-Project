from datetime import datetime
from http import HTTPStatus
from sqlalchemy.orm.session import Session
from flask import jsonify, request
from app.models.leads_model import Leads
from app.configs.database import db
from sqlalchemy.exc import DataError, IntegrityError, InvalidRequestError
import re


def get_leads():
    leads: Leads = Leads.query.all()
    if len(leads) == 0:
        return {"error": "No data found."}, HTTPStatus.NOT_FOUND

    return jsonify(leads), HTTPStatus.OK


def create_leads():
    payload = request.get_json()
    values = ["email", "name", "phone"]
    data = {i: payload[i] for i in payload if i in values}

    if not re.fullmatch("(\(\d{2}\)\d{5}-\d{4})", data["phone"]):
        return {
            "error": "Phone number format invalid use (xx)xxxxx-xxxx"
        }, HTTPStatus.BAD_REQUEST

    for key in data.keys():
        try:
            if key != "email":
                data[key] = data[key].title()
        except AttributeError:
            return {
                "error": "Requested value type is not String"
            }, HTTPStatus.BAD_REQUEST

    leads = Leads(**data)

    for value in values:
        if value not in data.keys():
            return {"error": "Missing non nullable key"}, HTTPStatus.BAD_REQUEST

    for value in data.values():
        if type(value) != str:
            return {
                "error": "Requested value type is not String"
            }, HTTPStatus.BAD_REQUEST

    try:
        db.session.add(leads)
        db.session.commit()
    except IntegrityError:
        return {"error": "Duplicated value requested"}, HTTPStatus.CONFLICT
    except DataError:
        return {"error": "Requested value for CPF is too long"}, HTTPStatus.BAD_REQUEST

    return jsonify(leads), HTTPStatus.CREATED


def patch_leads():
    payload = request.get_json()

    session: Session = db.session
    base_query = session.query(Leads)

    try:
        leads_info = base_query.get(payload["email"])
    except KeyError:
        return {
            "error": "Invalid key requested, use 'email' key."
        }, HTTPStatus.BAD_REQUEST
    except InvalidRequestError:
        return {"error": "Request type must be string."}, HTTPStatus.BAD_REQUEST

    if not leads_info:
        return {"error": "leads not found"}, HTTPStatus.NOT_FOUND

    setattr(leads_info, "last_visit", datetime.now())
    setattr(leads_info, "visits", leads_info.visits + 1)

    session.add(leads_info)
    session.commit()

    return "", HTTPStatus.NO_CONTENT


def delete_leads():
    payload = request.get_json()

    session: Session = db.session
    base_query = session.query(Leads)
    try:
        leads_info = base_query.get(payload["email"])
    except KeyError:
        return {
            "error": "Invalid key requested, use 'email' key."
        }, HTTPStatus.BAD_REQUEST
    except InvalidRequestError:
        return {"error": "Request type must be string."}, HTTPStatus.BAD_REQUEST

    if not leads_info:
        return {"error": "leads not found"}, HTTPStatus.NOT_FOUND
    try:
        session.delete(leads_info)
        session.commit()
    except InvalidRequestError:
        return {"error": "Request type must be string."}

    return "", HTTPStatus.NO_CONTENT
