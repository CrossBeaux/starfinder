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
	return redirect(url_for('characters.view_all', char_id=char.id))


@characters.route('/update_character', methods=['POST'])
def update():
	form = forms.CharacterUpdateForm(request.form)
	character = models.Character.get(form.id.data)
	helper.update_character(form, character)
	return redirect(url_for('characters.view_all', char_id=character.id))


@characters.route('/race_selection/<uuid:char_id>', methods=['GET'])
def race_selection(char_id):
	form = forms.CharacterUpdateForm(request.form)
	character = models.Character.get(char_id)
	context = {
		'form': form,
		'character': character,
		'next': 'characters.theme_selection',
		'previous': 'characters.view_all'
	}
	return render_template('characters/builder/race.html', **context)


@characters.route('/theme_selection/<uuid:char_id>', methods=['GET'])
def theme_selection(char_id):
	form = forms.CharacterUpdateForm(request.form)
	character = models.Character.get(char_id)
	context = {
		'form': form,
		'character': character,
		'next': 'characters.class_selection',
		'previous': 'characters.race_selection'
	}
	return render_template('characters/builder/theme.html', **context)


@characters.route('/class_selection/<uuid:char_id>', methods=['GET'])
def class_selection(char_id):
	form = forms.CharacterUpdateForm(request.form)
	character = models.Character.get(char_id)
	context = {
		'form': form,
		'character': character,
		'next':'characters.ability_allocation',
		'previous':'characters.theme_selection'
	}
	return render_template('characters/builder/class.html', **context)


@characters.route('/ability_allocation/<uuid:char_id>', methods=['GET'])
def ability_allocation(char_id):
	form = forms.CharacterUpdateForm(request.form)
	character = models.Character.get(char_id)
	context = {
		'form': form,
		'character': character,
		'next':'characters.class_options',
		'previous':'characters.class_selection'
	}
	return render_template('characters/builder/abilities.html', **context)


@characters.route('/class_options/<uuid:char_id>', methods=['GET'])
def class_option_selection(char_id):
	#form = forms.CharacterUpdateForm(request.form)
	character = models.Character.get(char_id)
	context = {
		'form': form,
		'character': character,
		'next': 'characters.spells_selection',
		'previous': 'characters.ability_allocation'
	}
	return render_template('characters/builder/class_options.html', **context)


@characters.route('/spells_selection/<uuid:char_id>', methods=['GET'])
def spells_selection(char_id):
	form = forms.CharacterSpellsForm(request.form)
	character = models.Character.get(char_id)
	context = {
		'form': form,
		'character': character,
		'next': 'characters.skills_allocation',
		'previous': 'characters.option_selection'
	}
	return render_template('characters/builder/class_options.html', **context)


@characters.route('/skills_allocation/<uuid:char_id>', methods=['GET'])
def skills_allocation(char_id):
	form = forms.CharacterSkillsForm(request.form)
	character = models.Character.get(char_id)
	context = {
		'form': form,
		'character': character,
		'next': 'characters.feat_selection',
		'previous': 'characters.spells_selection'
	}
	return render_template('characters/builder/skills.html', **context)


@characters.route('/feat_selection/<uuid:char_id>', methods=['GET'])
def feat_selection(char_id):
	form = forms.CharacterFeatsForm(request.form)
	character = models.Character.get(char_id)
	context = {
		'form': form,
		'character': character,
		'next': 'characters.alignment_selection',
		'previous': 'characters.skills_allocation'
	}
	return render_template('characters/builder/feats.html', **context)


@characters.route('/alignment_selection/<uuid:char_id>', methods=['GET'])
def alignment_selection(char_id):
	form = forms.CharacterUpdateForm(request.form)
	character = models.Character.get(char_id)
	context = {
		'form': form,
		'character': character,
		'next': 'characters.deity_selection',
		'previous': 'characters.feat_selection'
	}
	return render_template('characters/builder/alignment.html', **context)


@characters.route('/deity_selection/<uuid:char_id>', methods=['GET'])
def deity_selection(char_id):
	form = forms.CharacterUpdateForm(request.form)
	character = models.Character.get(char_id)
	context = {
		'form': form,
		'character': character,
		'next': 'characters.summary',
		'previous': 'characters.alignment_selection'
	}
	return render_template('characters/builder/deity.html', **context)
	

@characters.route('/summary/', methods=['GET'])
def summary():
    form = forms.CharacterUpdateForm(request.form)
    character = models.Character(name="Oracle",
                            	 description="Violently cute",
                            	 class_id="1",
								 alignment="Lawful Good",
								 #class_name="Mystic",
								 deity="filler",
								 home_world="filler",
								 race="human",
								 theme="Bounty Hunter",
								 level="2",
								 gender="Male",
								 strength="3",
								 dexterity="4",
								 constitution="1",
								 intelligence="12",
								 wisdom="12",
								 charisma="12",
								 character_skills="1",
								 character_feats="2",
								 character_equipment="3",
								 character_spells="4",
								 stamina="5",
								 hit_points="6",
								 str_mod="7",
								 dex_mod="8",
								 con_mod="2",
								 int_mod="4",
								 wis_mod="5",
								 char_mod="6",
								 misc_mod="7",
								 armor_bonus="8",
								 eac="6",
								 kac="6",
								 ac_vs_combat="4",
								 initiative="3",
								 base_save="5",
								 fortitude_save="6",
								 reflex_save="6",
								 will_save="3",
								 base_atk_bonus="3",
								 melee_atk="2",
								 ranged_atk="3",
								 thrown_atk="4")
    context = {
        'form': form,
        'character': character
    }
    return render_template('characters/builder/summary.html', **context)


@characters.route('/delete_character/', methods=['POST'])
def delete():
	form = forms.CharacterDeleteForm(request.form)
	LOG.debug("Deleting Character by ID: %s", form.id.data)
	char = models.Character.get(form.id.data)
	models.Session.delete(char)	
	models.Session.commit()
	return redirect(url_for('characters.view_all'))
