import flask
import requests
from flask import url_for, render_template, request, redirect

from starfinder import forms, config, logging
from starfinder.db import models

CONF = config.CONF
LOG = logging.get_logger(__name__)

characters = flask.Blueprint('characters', __name__, template_folder='templates')
URL_PREFIX = '/characters'
BLUEPRINT = characters

@characters.route('/')
def view_all():
	characters = models.Character.query.all()
	LOG.debug(characters)
	context = {
		'characters': characters,
		'creation_form': forms.CharacterCreateForm(),
		'deletion_form': forms.CharacterDeleteForm(),
		'current_route': 'characters.view_all'
	}
	return render_template('characters/show.html', **context)

@characters.route('/new_character', methods=['POST'])
def create():
	form = forms.CharacterCreateForm(request.form)
	char = models.Character(name=form.name.data)
	models.Session.add(char)
	models.Session.commit()
	return redirect(url_for('characters.view_all'))

@characters.route('/delete_character/<uuid:char_id>', methods=['POST'])
def delete(char_id):
	char = models.Character.get(char_id)
	models.Session.delete(char)	
	models.Session.commit()
	return redirect(url_for('characters.view_all'))

