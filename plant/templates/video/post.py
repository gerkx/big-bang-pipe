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
    'ver': {
        'type': 'numeric',
        'options': {
            'min_length': 1,
            'max_length': 4
        }
    }
}

compo_template = {
    'name': 'compo',
    'template': '${program}_S${season}E${episode}_SQ${sequence}_SH${shot}_COMPO_V${ver}',
    'definitions': defs
}

grade_template = {
    'name': 'grade',
    'template': '${program}_S${season}E${episode}_SQ${sequence}_SH${shot}_GRADE_V${ver}',
    'definitions': defs
}