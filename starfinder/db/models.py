import contextlib
import functools

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import sqlalchemy as sa
from sqlalchemy import orm, func
from sqlalchemy.ext import declarative
import sqlalchemy_utils

from starfinder import config, logging
from starfinder.db import utils as db_utils

CONF = config.CONF
LOG = logging.get_logger(__name__)
DB_NAME = "starfinder_{}".format(CONF.get("ENVIRONMENT"))
ENGINE_URL = CONF.get("DB_ENGINE_URL")
TABLE_KWARGS = {"mysql_engine": "InnoDB",
                "mysql_charset": "utf8",
                "mysql_collate": "utf8_general_ci"}

db_engine = config.db_engine

Session = db_engine.session

class ModelBase(object):
    __table_args__ = TABLE_KWARGS

    @declarative.declared_attr
    def __tablename__(cls):
        """ Returns a snake_case form of the table name. """
        return db_utils.pluralize(db_utils.to_snake_case(cls.__name__))

    def __eq__(self, other):
        if not other:
            return False
        return self.id == other.id

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key)

    def __setitem__(self, key, value):
        if hasattr(self, key):
            return setattr(self, key, value)
        raise AttributeError(key)

    def __contains__(self, key):
        return hasattr(self, key)

    def update(self, **fields):
        for attr, value in fields.items():
            if attr not in self:
                raise exception.ModelUnknownAttrbute(model=self, attr=attr)
            self[attr] = value
        return self

    @classmethod
    def get(cls, pk):
        return Session.query(cls).filter(cls.id == pk).first()

    @classmethod
    def _get_by_property(cls, prop):
        LOG.debug("Fetching '%s' by property '%s'", cls, prop)
        return Session.query(cls).filter(prop).first()

    @classmethod
    def _get_by(cls, field, value):
        LOG.debug("Fetching one '%s.%s' by value '%s'", cls, field, value)
        return Session.query(cls).filter(field == value).first()

    @classmethod
    def _get_all_by(cls, field, value):
        LOG.debug("Fetching all '%s.%s' with value '%s'", cls, field, value)
        return Session.query(cls).filter(field == value).all()

    def save(self):
        LOG.debug("Attempting to save '%s'", self)
        with transaction() as session:
            session.add(self)

    def delete(self):
        LOG.debug("Attempting to delete '%s'", self)
        with transaction() as session:
            session.delete(self)

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items()
                if not callable(value) and not key.startswith('_')}


def save(model):
    Session.add(model)
    Session.commit()


class GUID(sqlalchemy_utils.UUIDType):
    """
    Overload of the sqlalchemy_utils UUID class. There are issues
    with it and alembic, acknowledged by the maintainer:
    https://github.com/kvesteri/sqlalchemy-utils/issues/129

    """
    def __init__(self, length=16, binary=True, native=True):
        # pylint: disable=unused-argument
        # NOTE(mdietz): Ignoring length, see:
        # https://github.com/kvesteri/sqlalchemy-utils/issues/129
        super(GUID, self).__init__(binary, native)


class HasId(object):
    """id mixin, add to subclasses that have an id."""

    id = sa.Column(GUID,
                   primary_key=True,
                   default=db_utils.generate_guid)


class User(db_engine.Model, ModelBase, HasId):
    username = db_engine.Column(db_engine.String(80), unique=True, nullable=False)

    def __repr__(self):
        return self.username



-----------------
Character Classes
-----------------

class Character(Base, HasId):
    name = sa.Column(sa.String(), nullable=False)

    def __str__(self):
        return self.name

class CharacterDetail(Base, HasId):
    character_id = sa.Column(sa.ForeignKey("characters.id"),
                                     nullable=False)
    alignment_id = sa.Column(sa.ForeignKey("alignments.id"),
                                     nullable=False)
    class_id = sa.Column(sa.ForeignKey("classes.id"),
                                     nullable=False)
    deity_id = sa.Column(sa.ForeignKey("deities.id"),
                                     nullable=False)
    home_world_id = sa.Column(sa.ForeignKey("worlds.id"),
                                     nullable=False)
    race_id = sa.Column(sa.ForeignKey("races.id"),
                                     nullable=False)
    size_id = sa.Column(sa.ForeignKey("sizes.id"),
                                     nullable=False)
    theme_id = sa.Column(sa.ForeignKey("themes.id"),
                                     nullable=False)
    level = sa.Column(sa.Integer(), nullable=False)
    gender = sa.Column(sa.String(6), nullable=False)
    description = sa.Column(sa.String(160), nullable=False)

class CharacterEquipment(Base, HasId):
    character_id = sa.Column(sa.ForeignKey("characters.id"),
                                     nullable=False)
    attributes = sa.Column(sa.JSON("equipment.attributes"),
                                     nullable=False)

class CharacterFeat(Base, HasId):
    character_id = sa.Column(sa.ForeignKey("characters.id"),
                                     nullable=False)
    feat_id = sa.Column(sa.ForeignKey("feats.id"),
                                     nullable=False)

class CharacterSkill(Base, HasId):
    character_id = sa.Column(sa.ForeignKey("characters.id"),
                                     nullable=False)
    acrobatics = sa.Column(sa.Integer(), nullable=False, default=False)
    athletics = sa.Column(sa.Integer(), nullable=False, default=False)
    bluff = sa.Column(sa.Integer(), nullable=False, default=False)
    computers = sa.Column(sa.Integer(), nullable=False, default=False)
    culture = sa.Column(sa.Integer(), nullable=False, default=False)
    diplomacy = sa.Column(sa.Integer(), nullable=False, default=False)
    disguise = sa.Column(sa.Integer(), nullable=False, default=False)
    engineering = sa.Column(sa.Integer(), nullable=False, default=False)
    intimidate = sa.Column(sa.Integer(), nullable=False, default=False)
    life_science = sa.Column(sa.Integer(), nullable=False, default=False)
    medicine = sa.Column(sa.Integer(), nullable=False, default=False)
    mysticsm = sa.Column(sa.Integer(), nullable=False, default=False)
    perception = sa.Column(sa.Integer(), nullable=False, default=False)
    physical_science = sa.Column(sa.Integer(), nullable=False, default=False)
    piloting = sa.Column(sa.Integer(), nullable=False, default=False)
    profession = sa.Column(sa.Integer(), nullable=False, default=False)
    sense_motive = sa.Column(sa.Integer(), nullable=False, default=False)
    sleight_of_hand = sa.Column(sa.Integer(), nullable=False, default=False)
    stealth = sa.Column(sa.Integer(), nullable=False, default=False)
    survival = sa.Column(sa.Integer(), nullable=False, default=False)

# -----------------
# Equipment Classes
# -----------------

class Equipment(Base, HasId):
    attributes = sa.Column(sa.JSON("equipment.attributes"),
                                     nullable=False)

class Ammunition(Base, HasId):
    attributes = sa.Column(sa.JSON("ammunition.attributes"),
                                     nullable=False)

class Armor(Base, HasId):
    attributes = sa.Column(sa.JSON("armor.attributes"),
                                     nullable=False)

class ArmorUpgrade(Base, HasId):
    attributes = sa.Column(sa.JSON("armor_upgrades.attributes"),
                                     nullable=False)

class Augmentation(Base, HasId):
    attributes = sa.Column(sa.JSON("augmentations.attributes"),
                                     nullable=False)

class Computer(Base, HasId):
    attributes = sa.Column(sa.JSON("computers.attributes"),
                                     nullable=False)

class ComputerUpgrade(Base, HasId):
    attributes = sa.Column(sa.JSON("computer_upgrades.attributes"),
                                     nullable=False)

class Fusion(Base, HasId):
    attributes = sa.Column(sa.JSON("fusions.attributes"),
                                     nullable=False)

class Grenade(Base, HasId):
    attributes = sa.Column(sa.JSON("grenades.attributes"),
                                     nullable=False)

class MeleeWeapon(Base, HasId):
    attributes = sa.Column(sa.JSON("melee_weapons.attributes"),
                                     nullable=False)

class RangedWeapon(Base, HasId):
    attributes = sa.Column(sa.JSON("ranged_weapons.attributes"),
                                     nullable=False)


# ------------
# Info Classes
# ------------

class Alignment(Base, HasId):
    name = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.String(), nullable=False)

class Size(Base, HasId):
    name = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.String(), nullable=False)

class Deitie(Base, HasId):
    name = sa.Column(sa.String(), nullable=False)
    alignment_id = sa.Column(sa.ForeignKey("alignments.id"),
                                     nullable=False)
    description = sa.Column(sa.String(), nullable=False)

class World(Base, HasId):
    name = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.String(), nullable=False)

class PlacesOfWorship(Base, HasId):
    world_id = sa.Column(sa.ForeignKey("worlds.id"),
                                     nullable=False)
    deity_id = sa.Column(sa.ForeignKey("deities.id"),
                                     nullable=False)

class NativeRace(Base, HasId):
    world_id = sa.Column(sa.ForeignKey("worlds.id"),
                                     nullable=False)
    race_id = sa.Column(sa.ForeignKey("race.id"),
                                     nullable=False)


# ------------
# Race Classes
# ------------

class Race(Base, HasId):
    home_world_id = sa.Column(sa.ForeignKey("worlds.id"),
                                     nullable=False)
    size_id = sa.Column(sa.ForeignKey("sizes.id"),
                                     nullable=False)
    name = sa.Column(sa.String(), nullable=False)
    avg_height = sa.Column(sa.String(), nullable=False)
    avg_weight = sa.Column(sa.String(), nullable=False)
    age_of_maturity = sa.Column(sa.Integer(), nullable=False)
    max_age = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.String(), nullable=False)
    hit_points = sa.Column(sa.Integer(), nullable=False)
    type = sa.Column(sa.String(), nullable=False)
    physical_description = sa.Column(sa.String(), nullable=False)
    society_and_alignment = sa.Column(sa.String(), nullable=False)
    relations = sa.Column(sa.String(), nullable=False)
    adventurers = sa.Column(sa.String(), nullable=False)
    names = sa.Column(sa.String(), nullable=False)

class RacialTraits(Base, HasId):
    race_id = sa.Column(sa.ForeignKey("races.id"),
                                     nullable=False)
    name = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.String(), nullable=False)

class AssociatedFeats(Base, HasId):
    trait_id = sa.Column(sa.ForeignKey("traits.id"),
                                     nullable=False)
    feat_id = sa.Column(sa.ForeignKey("feats.id"),
                                     nullable=False)


# --------------------
# Feat & Spell Classes
# --------------------

class Feats(Base, HasId):
    modifier_id = sa.Column(sa.ForeignKey("races.id"),
                                     nullable=False)
    prereq_id = sa.Column(sa.ForeignKey("races.id"),
                                     nullable=False)
    name = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.String(), nullable=False)

class Spells(Base, HasId):
    name = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.String(), nullable=False)


# ----------------
# Modifier Classes
# ----------------

class Modifiers(Base, HasId):
    effected_stat = sa.Column(sa.String(), nullable=False)
    modification = sa.Column(sa.Integer(), nullable=False)

class TraitModifiers(Base, HasId):
    trait_id = sa.Column(sa.ForeignKey("traits.id"),
                                     nullable=False)
    modifier_id = sa.Column(sa.ForeignKey("modifiers.id"),
                                     nullable=False)

class FeatModifiers(Base, HasId):
    trait_id = sa.Column(sa.ForeignKey("traits.id"),
                                     nullable=False)
    modifier_id = sa.Column(sa.ForeignKey("modifiers.id"),
                                     nullable=False)

class ThemeModifiers(Base, HasId):
    trait_id = sa.Column(sa.ForeignKey("traits.id"),
                                     nullable=False)
    modifier_id = sa.Column(sa.ForeignKey("modifiers.id"),
                                     nullable=False)

db_engine.create_all()
