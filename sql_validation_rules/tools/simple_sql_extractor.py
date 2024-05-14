from typing import List


def extract_sql_markdown(text: str) -> List[str]:
    back_tick_counter = 0
    start_capture = False
    extracted = ""
    previous = ""
    captured_list = []
    for c in text:
        if c == "`" and (previous == "`" or previous == "\n"):
            back_tick_counter += 1
            if back_tick_counter == 3:
                start_capture = not start_capture
                back_tick_counter = 0
                if start_capture == False:
                    captured_list.append(extracted.replace("sql\n", "").strip())
                    extracted = ""
        elif start_capture:
            extracted += c
        previous = c
    return captured_list


if __name__ == "__main__":
    from sql_validation_rules.test.provider.sql_markdown_extractor_provider import (
        create_stats_query_sql,
    )

    text = create_stats_query_sql()
    captured = extract_sql_markdown(text)
    assert len(captured) > 0
    for c in captured:
        print(c)
