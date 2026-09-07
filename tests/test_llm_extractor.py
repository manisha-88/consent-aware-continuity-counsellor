from app.models import ExtractionResult


def test_extraction_result_schema():
    result = ExtractionResult.model_validate(
        {
            "information": [
                {
                    "category": "exam_stress",
                    "content": "Student reports examination-related stress.",
                },
                {
                    "category": "family_information",
                    "content": "Student reports family-related concerns.",
                },
            ]
        }
    )

    assert len(result.information) == 2
    assert result.information[0].category.value == "exam_stress"