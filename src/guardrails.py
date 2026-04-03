import re
import json


def validate_input(text: str) -> str:
    """
    Validates and sanitizes user input before sending to the LLM.

    Raises:
        ValueError: If the input is invalid, too short, or contains a prompt injection attempt.
    """
    if not isinstance(text, str):
        raise ValueError("Invalid input: expected a string.")
    if len(text.strip()) < 5:
        raise ValueError("Invalid input: text is too short (minimum 5 characters).")
    if "ignore previous" in text.lower():
        raise ValueError("Invalid input: potential prompt injection detected.")
    return text.strip()


def clean_json_output(raw: str) -> str:
    """
    Strips markdown code fences and extracts the first JSON object from raw LLM output.

    Handles cases like:
        ```json { ... } ```
        Here is the result: { ... }
    """
    # Remove markdown code fences (```json ... ``` or ``` ... ```)
    raw = re.sub(r"```(?:json)?\s*", "", raw)
    raw = raw.strip("`\n ")

    # Extract the first {...} block in case there is surrounding text
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        return match.group(0)

    return raw
