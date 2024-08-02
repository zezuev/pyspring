import unittest
from typing import TypedDict

from src.validation import get_schema, validate_schema, BadSchemaError


class School(TypedDict):
    name: str
    town: str


class Student(TypedDict):
    name: str
    age: int
    school: School


class ValidationTest(unittest.TestCase):

    def test_flat_schema(self):
        self.assertEqual(get_schema(School), {"name": str, "town": str})

    def test_nested_schema(self):
        self.assertEqual(
            get_schema(Student),
            {"name": str, "age": int, "school": {"name": str, "town": str}},
        )

    def test_bad_schema(self):
        bad_student = {
            "name": "John",
            "age": 20,
            "school": {
                "name": 123,
                "town": "NYC",
            },
        }
        student_schema = get_schema(Student)
        self.assertRaises(
            BadSchemaError,
            lambda: validate_schema(bad_student, student_schema),
        )


if __name__ == "__main__":
    unittest.main()