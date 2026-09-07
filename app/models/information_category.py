from enum import Enum


class InformationCategory(str, Enum):
    EXAM_STRESS = "exam_stress"
    ACADEMIC_CONCERN = "academic_concern"
    SLEEP_DIFFICULTY = "sleep_difficulty"
    FAMILY_INFORMATION = "family_information"
    SOCIAL_SUPPORT = "social_support"
    SAFETY_CONCERN = "safety_concern"
    AMBIGUOUS_STATEMENT = "ambiguous_statement"
    STUDY_ROUTINE = "study_routine"