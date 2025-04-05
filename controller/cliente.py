from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.models import db, Galleta, Pedido, DetallePedido
from datetime import datetime, timedelta
from models.forms import PedidoForm
from controller.auth import cliente_required

cliente_bp = Blueprint('cliente', __name__)

