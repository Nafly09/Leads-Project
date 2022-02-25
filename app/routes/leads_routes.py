from flask import Blueprint
from app.controllers import leads_controllers

bp = Blueprint("leads", __name__, url_prefix="/leads")

bp.get("")(leads_controllers.get_leads)
bp.post("")(leads_controllers.create_leads)
bp.patch("")(leads_controllers.patch_leads)
bp.delete("")(leads_controllers.delete_leads)
