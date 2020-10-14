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
    },
    'title': {
        'type': 'alpha',
        'options': {}
    }
}

# audio_grab_template = {
#     'name': 'audio_grab',
#     'template': '${char} CAP${episode} ${take}',
#     'definitions': defs
# }

audio_grab_template = {
    'name': 'audio_grab',
    'template': 'MOMONSTERS_S02E${episode}_${title}_${char}_${take}',
    'definitions': defs
}
