from pprint import pprint

from app.services.case_service import build_case_context
from app.services.handover_service import generate_handover


def main():
    client_id = "C003"

    case = build_case_context(client_id)
    handover = generate_handover(case)

    pprint(handover.model_dump())


if __name__ == "__main__":
    main()