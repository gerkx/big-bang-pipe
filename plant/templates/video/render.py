defs = {
    'program': {
        'type': 'alpha_numeric',
        'options': {},
    },
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
    'sequence': {
       'type': 'numeric',
        'options': {
            'min_length': 1,
            'max_length': 4
        }
    },
    'shot': {
       'type': 'numeric',
        'options': {
            'min_length': 1,
            'max_length': 4
        }
    },
}

# ver_def = {
#     'version': {
#         'type': 'numeric',
#         'options': {
#             'min_length': 1,
#             'max_length': 4
#         }
#     }
# }

render_template = {
    'name': 'render',
    'template': '${program}_S${season}E${episode}_SQ${sequence}_SH${shot}',
    'definitions': defs
}

# render_ver_template = {
#     'name': 'render_ver',
#     'template': '${program}_S${season}E${episode}_SQ${sequence}_SH${shot}_v${version}',
#     'definitions': {**defs, **ver_def}
# }
