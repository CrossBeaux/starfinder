import requests

import flask
from flask import url_for, render_template, request, redirect

from starfinder import forms, config, logging
from starfinder.db import models
from starfinder.helpers import helper

CONF = config.CONF
LOG = logging.get_logger(__name__)

helper = helper.Helper()
characters = flask.Blueprint('characters', __name__, template_folder='templates')
URL_PREFIX = '/characters'
BLUEPRINT = characters

@characters.route('/')
def view_all():
	characters = models.Character.query.all()
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
	return redirect(url_for('characters.race_selection', char_id=char.id))


@characters.route('/update_character', methods=['POST'])
def update():
	form = forms.CharacterUpdateForm(request.form)
	character = models.Character.get(form.id.data)
	helper.update_character(form, character)
	return redirect(url_for('characters.view_all', char_id=character.id))


@characters.route('/race_selection/<uuid:char_id>', methods=['GET', 'POST'])
def race_selection(char_id):
	form = forms.CharacterRaceForm(request.form)
	character = models.Character.get(char_id)
	context = {
		'form': form,
		'character': character
	}
	return render_template('characters/builder/race.html', **context)


@characters.route('/theme_selection/<uuid:char_id>', methods=['GET', 'POST'])
def theme_selection(char_id):
	form = forms.CharacterThemeForm(request.form)
	character = models.Character.get(char_id)
	context = {
		'form': form,
		'character': character
	}
	return render_template('characters/builder/theme.html', **context)


@characters.route('/delete_character/', methods=['POST'])
def delete():
	form = forms.CharacterDeleteForm(request.form)
	LOG.debug("Deleting Character by ID: %s", form.id.data)
	char = models.Character.get(form.id.data)
	models.Session.delete(char)	
	models.Session.commit()
	return redirect(url_for('characters.view_all'))
