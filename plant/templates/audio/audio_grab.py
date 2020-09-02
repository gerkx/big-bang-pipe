defs = {
    'char': {
        'type': 'alpha',
        'options': {}
    },
    'episode': {
        'type': 'numeric',
        'options': {
            'min_length': 1,
            'max_length': 4
        }
    },
    'take': {
        'type': 'alpha',
        'options': {}
    }
}

audio_grab_template = {
    'name': 'audio_grab',
    'template': '${char} CAP${episode} ${take}',
    'definitions': defs
}
