from .client import get_client


def get_updated_profile(
    message: str,
    current_profile: str,
    model: str,
) -> str | None:
    client = get_client()

    system = (
        "아래 메시지를 보고 이 사람의 프로필에 추가하거나 수정할 정보가 있으면 "
        "전체 프로필을 다시 작성해줘. 변경할 내용이 없으면 아무것도 출력하지 마."
    )
    user = f"[기존 프로필]\n{current_profile}\n\n[메시지]\n{message}"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'system', 'content': system},
            {'role': 'user', 'content': user},
        ],
    )

    if not response.choices:
        return None
    content = response.choices[0].message.content
    return content if content else None
