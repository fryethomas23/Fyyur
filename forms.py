from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField
from wtforms.validators import DataRequired, AnyOf, URL, ValidationError
import re
import enum 

class Genres(enum.Enum):
    Alternative = 'Alternative'
    Blues = 'Blues'
    Classical = 'Classical'
    Country = 'Country'
    Electronic = 'Electronic'
    Folk = 'Folk'
    Funk = 'Funk'
    HipHop = 'Hip-Hop'
    HeavyMetal = 'Heavy Metal'
    Instrumental = 'Instrumental'
    Jazz = 'Jazz'
    MusicalTheatre = 'Musical Theatre'
    Pop = 'Pop'
    Punk = 'Punk'
    RandB = 'R and B'
    Reggae = 'Reggae'
    RocknRoll = 'Rock n Roll'
    Soul = 'Soul'
    Other = 'Other'

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

class States(enum.Enum):
    AL = 'AL'
    AK = 'AK'
    AZ = 'AZ'
    AR = 'AR'
    CA = 'CA'
    CO = 'CO'
    CT = 'CT'
    DE = 'DE'
    DC = 'DC'
    FL = 'FL'
    GA = 'GA'
    HI = 'HI'
    ID = 'ID'
    IL = 'IL'
    IN = 'IN'
    IA = 'IA'
    KS = 'KS'
    KY = 'KY'
    LA = 'LA'
    ME = 'ME'
    MT = 'MT'
    NE = 'NE'
    NV = 'NV'
    NH = 'NH'
    NJ = 'NJ'
    NM = 'NM'
    NY = 'NY'
    NC = 'NC'
    ND = 'ND'
    OH = 'OH'
    OK = 'OK'
    OR = 'OR'
    MD = 'MD'
    MA = 'MA'
    MI = 'MI'
    MN = 'MN'
    MS = 'MS'
    MO = 'MO'
    PA = 'PA'
    RI = 'RI'
    SC = 'SC'
    SD = 'SD'
    TN = 'TN'
    TX = 'TX'
    UT = 'UT'
    VT = 'VT'
    VA = 'VA'
    WA = 'WA'
    WV = 'WV'
    WI = 'WI'
    WY = 'WY'

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

def phone_validator(form, field):
    try:
        p = re.compile('^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$')
    except:
        raise ValidationError('Phone number must be in xxx-xxx-xxxx format')
    if p.match(field.data) == None:
        raise ValidationError('Phone number must be in xxx-xxx-xxxx format')
        


class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices= States.choices()
        # [
        #     ('AL', 'AL'),
        #     ('AK', 'AK'),
        #     ('AZ', 'AZ'),
        #     ('AR', 'AR'),
        #     ('CA', 'CA'),
        #     ('CO', 'CO'),
        #     ('CT', 'CT'),
        #     ('DE', 'DE'),
        #     ('DC', 'DC'),
        #     ('FL', 'FL'),
        #     ('GA', 'GA'),
        #     ('HI', 'HI'),
        #     ('ID', 'ID'),
        #     ('IL', 'IL'),
        #     ('IN', 'IN'),
        #     ('IA', 'IA'),
        #     ('KS', 'KS'),
        #     ('KY', 'KY'),
        #     ('LA', 'LA'),
        #     ('ME', 'ME'),
        #     ('MT', 'MT'),
        #     ('NE', 'NE'),
        #     ('NV', 'NV'),
        #     ('NH', 'NH'),
        #     ('NJ', 'NJ'),
        #     ('NM', 'NM'),
        #     ('NY', 'NY'),
        #     ('NC', 'NC'),
        #     ('ND', 'ND'),
        #     ('OH', 'OH'),
        #     ('OK', 'OK'),
        #     ('OR', 'OR'),
        #     ('MD', 'MD'),
        #     ('MA', 'MA'),
        #     ('MI', 'MI'),
        #     ('MN', 'MN'),
        #     ('MS', 'MS'),
        #     ('MO', 'MO'),
        #     ('PA', 'PA'),
        #     ('RI', 'RI'),
        #     ('SC', 'SC'),
        #     ('SD', 'SD'),
        #     ('TN', 'TN'),
        #     ('TX', 'TX'),
        #     ('UT', 'UT'),
        #     ('VT', 'VT'),
        #     ('VA', 'VA'),
        #     ('WA', 'WA'),
        #     ('WV', 'WV'),
        #     ('WI', 'WI'),
        #     ('WY', 'WY'),
        # ]
    )
    address = StringField(
        'address'
    )
    phone = StringField(
        'phone', validators=[phone_validator]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
            choices= Genres.choices()
        # [
        #     ('Alternative', 'Alternative'),
        #     ('Blues', 'Blues'),
        #     ('Classical', 'Classical'),
        #     ('Country', 'Country'),
        #     ('Electronic', 'Electronic'),
        #     ('Folk', 'Folk'),
        #     ('Funk', 'Funk'),
        #     ('Hip-Hop', 'Hip-Hop'),
        #     ('Heavy Metal', 'Heavy Metal'),
        #     ('Instrumental', 'Instrumental'),
        #     ('Jazz', 'Jazz'),
        #     ('Musical Theatre', 'Musical Theatre'),
        #     ('Pop', 'Pop'),
        #     ('Punk', 'Punk'),
        #     ('R&B', 'R&B'),
        #     ('Reggae', 'Reggae'),
        #     ('Rock n Roll', 'Rock n Roll'),
        #     ('Soul', 'Soul'),
        #     ('Other', 'Other'),
        # ]
    )
    website = StringField(
        # TODO implement enum restriction
        'website', validators=[URL()]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    seeking_talent = SelectField(
        # TODO implement enum restriction
        'seeking_talent', choices=[
            ('True','True'),
            ('False','False')
        ]
    )
    seeking_description = StringField(
        # TODO implement enum restriction
        'seeking description', 
    )

class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices= States.choices()
        # [
        #     ('AL', 'AL'),
        #     ('AK', 'AK'),
        #     ('AZ', 'AZ'),
        #     ('AR', 'AR'),
        #     ('CA', 'CA'),
        #     ('CO', 'CO'),
        #     ('CT', 'CT'),
        #     ('DE', 'DE'),
        #     ('DC', 'DC'),
        #     ('FL', 'FL'),
        #     ('GA', 'GA'),
        #     ('HI', 'HI'),
        #     ('ID', 'ID'),
        #     ('IL', 'IL'),
        #     ('IN', 'IN'),
        #     ('IA', 'IA'),
        #     ('KS', 'KS'),
        #     ('KY', 'KY'),
        #     ('LA', 'LA'),
        #     ('ME', 'ME'),
        #     ('MT', 'MT'),
        #     ('NE', 'NE'),
        #     ('NV', 'NV'),
        #     ('NH', 'NH'),
        #     ('NJ', 'NJ'),
        #     ('NM', 'NM'),
        #     ('NY', 'NY'),
        #     ('NC', 'NC'),
        #     ('ND', 'ND'),
        #     ('OH', 'OH'),
        #     ('OK', 'OK'),
        #     ('OR', 'OR'),
        #     ('MD', 'MD'),
        #     ('MA', 'MA'),
        #     ('MI', 'MI'),
        #     ('MN', 'MN'),
        #     ('MS', 'MS'),
        #     ('MO', 'MO'),
        #     ('PA', 'PA'),
        #     ('RI', 'RI'),
        #     ('SC', 'SC'),
        #     ('SD', 'SD'),
        #     ('TN', 'TN'),
        #     ('TX', 'TX'),
        #     ('UT', 'UT'),
        #     ('VT', 'VT'),
        #     ('VA', 'VA'),
        #     ('WA', 'WA'),
        #     ('WV', 'WV'),
        #     ('WI', 'WI'),
        #     ('WY', 'WY'),
        # ]
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone', validators=[phone_validator]
    )
    image_link = StringField(
        'image_link', validators=[URL()]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices= Genres.choices()
        # [
        #     ('Alternative', 'Alternative'),
        #     ('Blues', 'Blues'),
        #     ('Classical', 'Classical'),
        #     ('Country', 'Country'),
        #     ('Electronic', 'Electronic'),
        #     ('Folk', 'Folk'),
        #     ('Funk', 'Funk'),
        #     ('Hip-Hop', 'Hip-Hop'),
        #     ('Heavy Metal', 'Heavy Metal'),
        #     ('Instrumental', 'Instrumental'),
        #     ('Jazz', 'Jazz'),
        #     ('Musical Theatre', 'Musical Theatre'),
        #     ('Pop', 'Pop'),
        #     ('Punk', 'Punk'),
        #     ('R&B', 'R&B'),
        #     ('Reggae', 'Reggae'),
        #     ('Rock n Roll', 'Rock n Roll'),
        #     ('Soul', 'Soul'),
        #     ('Other', 'Other'),
        # ]
    )
    website = StringField(
        # TODO implement enum restriction
        'website', validators=[URL()]
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL()]
    )
    seeking_venue = SelectField(
        # TODO implement enum restriction
        'seeking_venue', choices=[
            ('True','True'),
            ('False','False')
        ]
    )
    seeking_description = StringField(
        # TODO implement enum restriction
        'seeking description', 
    )

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
