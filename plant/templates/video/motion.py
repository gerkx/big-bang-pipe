defs = {
    'season': {
        'type': 'numeric',
        'options': {
            'min_length': 1,
            'max_length': 2
        }
    },
    'episode': {
        'type': 'numeric',
        'options': {
            'min_length': 1,
            'max_length': 2
        }
    },
    'shot': {
       'type': 'numeric',
        'options': {
            'min_length': 1,
            'max_length': 4
        }
    },
    'version': {
        'type': 'numeric',
        'options': {
            'min_length': 1,
            'max_length': 4
        }
    }
}

motion_template = {
    'name': 'motion',
    'template': 'S${season}_EP${episode}_MOTION_SH${shot}_V${version}',
    'definitions': defs
}
