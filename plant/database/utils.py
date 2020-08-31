from typing import Type

from .models import Shot, Project

def get_shot(proj_production_number:int, shot_number:int) -> Type[Shot]:
    try:
        project = Project.get(
            Project.production_number == proj_production_number
        )
        shot = next(shot for shot in project.shots if shot.name == shot_number)
        return shot
    except:
        return None

def get_prev_vers_number(proj_production_number:int, shot_number:int) -> int:
    shot = get_shot(proj_production_number, shot_number)
    return len(shot.renders) if shot else None

def check_for_int_vis(proj_production_number:int, shot_number:int) -> dict:
    shot = get_shot(proj_production_number, shot_number)
    if not shot:
        return None
    else:
        return {
            'renders': len(shot.renders) > 0,
            'grades': len(shot.grades) > 0,
            'compo': len(shot.compo) > 0
        }