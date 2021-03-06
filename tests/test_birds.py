from a1d05eba1.content_variations import X_Content


# BIRDS comes from an example XLSForm "Birds.xlsx"
BIRDS = {'choices': [{'label': 'Dry or low', 'list name': 'humidity', 'name': 'low'},
                     {'label': 'Normal or medium',
                      'list name': 'humidity',
                      'name': 'med'},
                     {'label': 'Wet or high', 'list name': 'humidity', 'name': 'high'},
                     {'label': 'Little or no wind', 'list name': 'wind', 'name': 'low'},
                     {'label': 'Breezy or light wind',
                      'list name': 'wind',
                      'name': 'med'},
                     {'label': 'Strong or very windy',
                      'list name': 'wind',
                      'name': 'high'},
                     {'label': 'Eagle',
                      'list name': 'birds',
                      'media::image': 'eagle.png',
                      'name': 'eagle'},
                     {'label': 'Kingfisher',
                      'list name': 'birds',
                      'media::image': 'kingfisher.png',
                      'name': 'kingfisher'},
                     {'label': 'Pigeon',
                      'list name': 'birds',
                      'media::image': 'pigeon.png',
                      'name': 'pigeon'},
                     {'label': 'Nuthatch',
                      'list name': 'birds',
                      'media::image': 'nuthatch.png',
                      'name': 'nuthatch'},
                     {'label': 'Robin',
                      'list name': 'birds',
                      'media::image': 'european-robin.png',
                      'name': 'robin'},
                     {'label': 'Tit',
                      'list name': 'birds',
                      'media::image': 'tit.png',
                      'name': 'tit'},
                     {'label': 'Sparrow',
                      'list name': 'birds',
                      'media::image': 'sparrow.png',
                      'name': 'sparrow'},
                     {'label': 'Starling',
                      'list name': 'birds',
                      'media::image': 'starling.png',
                      'name': 'starling'},
                     {'label': 'Hawfinch',
                      'list name': 'birds',
                      'media::image': 'hawfinch.png',
                      'name': 'hawfinch'},
                     {'label': 'Bluethroat',
                      'list name': 'birds',
                      'media::image': 'bluethroat.png',
                      'name': 'bluethroat'},
                     {'label': 'Wren',
                      'list name': 'birds',
                      'media::image': 'wren.png',
                      'name': 'wren'},
                     {'label': 'Knot',
                      'list name': 'birds',
                      'media::image': 'knot.png',
                      'name': 'knot'},
                     {'label': 'Jay',
                      'list name': 'birds',
                      'media::image': 'jay.png',
                      'name': 'jay'},
                     {'label': 'Woodpecker',
                      'list name': 'birds',
                      'media::image': 'woodpecker.png',
                      'name': 'woodpecker'},
                     {'label': 'Blackbird',
                      'list name': 'birds',
                      'media::image': 'blackbird.png',
                      'name': 'blackbird'},
                     {'label': 'Crow',
                      'list name': 'birds',
                      'media::image': 'carrioncrow.png',
                      'name': 'crow'},
                     {'label': 'Gull',
                      'list name': 'birds',
                      'media::image': 'gull.png',
                      'name': 'gull'},
                     {'label': 'Yellowgull',
                      'list name': 'birds',
                      'media::image': 'yellowgull.png',
                      'name': 'yellowgull'},
                     {'label': 'Shag',
                      'list name': 'birds',
                      'media::image': 'shag.png',
                      'name': 'shag'},
                     {'label': 'Pelican',
                      'list name': 'birds',
                      'media::image': 'pelican.png',
                      'name': 'pelican'},
                     {'label': 'Heron',
                      'list name': 'birds',
                      'media::image': 'heron.png',
                      'name': 'heron'},
                     {'label': 'Egret',
                      'list name': 'birds',
                      'media::image': 'egret.png',
                      'name': 'egret'},
                     {'label': 'Goose',
                      'list name': 'birds',
                      'media::image': 'goose.png',
                      'name': 'goose'},
                     {'label': 'Other Bird',
                      'list name': 'birds',
                      'name': 'otherbird'}],
         'settings': [{'formid': 'tha_birds'}],
         'survey': [{'name': 'start', 'type': 'start'},
                    {'name': 'end', 'type': 'end'},
                    {'name': 'today', 'type': 'today'},
                    {'name': 'imei', 'type': 'imei'},
                    {'appearance': 'field-list',
                     'label': 'Demographic information',
                     'name': 'demographic',
                     'type': 'begin group'},
                    {'label': 'Please enter your name:',
                     'name': 'name',
                     'type': 'text'},
                    {'label': 'Please enter your country:',
                     'name': 'nationality',
                     'type': 'text'},
                    {'type': 'end group'},
                    {'appearance': 'field-list',
                     'label': 'Weather information',
                     'name': 'weather',
                     'type': 'begin group'},
                    {'label': 'Temperature:', 'name': 'temp', 'type': 'text'},
                    {'label': 'Humidity:',
                     'name': 'humidity',
                     'type': 'select_one humidity'},
                    {'label': 'Wind conditions:',
                     'name': 'wind',
                     'type': 'select_one wind'},
                    {'type': 'end group'},
                    {'name': 'observation', 'type': 'begin repeat'},
                    {'label': 'If possible, please take a picture of your observation',
                     'name': 'picture',
                     'type': 'photo'},
                    {'hint': 'Some birds have included images or audio.',
                     'label': 'What bird did you see?',
                     'media::audio': 'question.wav',
                     'name': 'bird',
                     'type': 'select_one birds'},
                    {'label': 'Please record your location',
                     'name': 'location',
                     'type': 'gps'},
                    {'hint': 'This is optional, of course',
                     'label': 'Please enter any notes about your observation',
                     'name': 'notes',
                     'type': 'text'},
                    {'type': 'end repeat'}]}


def test_birds():
    cc = X_Content(BIRDS, validate=True)
    result = cc.export_to('2')
    assert result['choices']['humidity'][0]['$anchor'] == 'humidity.low'
    assert cc.media_files == ('question.wav', 'eagle.png', 'kingfisher.png',
        'pigeon.png', 'nuthatch.png', 'european-robin.png', 'tit.png',
        'sparrow.png', 'starling.png', 'hawfinch.png', 'bluethroat.png',
        'wren.png', 'knot.png', 'jay.png', 'woodpecker.png', 'blackbird.png',
        'carrioncrow.png', 'gull.png', 'yellowgull.png', 'shag.png',
        'pelican.png', 'heron.png', 'egret.png', 'goose.png')
