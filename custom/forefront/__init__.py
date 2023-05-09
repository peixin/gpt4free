from gpt4free import forefront
from enum import Enum
from . import account


class Persona(Enum):
    HelpfulAssistant = "607e41fe-95be-497e-8e97-010a59b2e2c0"
    SeniorSoftwareDeveloper = "7b4d5d60-ccd9-4e59-b566-4ab25e4af631"
    # TODO: find the correct value below
    # Copywriter = "4ba1f14e-b54b-41b5-b43d-66669b64ca23"
    # Einstein = "9eb04fc1-a65b-4ff5-a60d-4886f15034cf"
    # HarryPotter = "7c4139d6-ffc8-452a-995f-d0bf72341f20"
    # JargonTranslator = "305bbac6-17a4-4d9a-8931-7a1675e665f2"
    # Psychologist = "272ad220-f4f7-437f-aaf8-012530b2c0c2"
    # Socrates = "9388be7b-5373-4b3f-a422-e22e672f3117"
    # SoftwareGuru = "e0b13cd6-6ff2-4a4f-b88a-db7f5f656c1f"
    # Starlord = "157242d9-7165-4c68-9023-1a13bbc9b601"
    # SteveJobs = "206f0baa-82bc-45a2-b537-4df2023844b4"
    # SunTzu = "178b5c40-c74a-4edd-bd70-c749a53b58c1"
    # Thanos = "10ad5073-eb4a-498f-9c62-57c77001709f"
    # Voldemort = "31a4be35-5733-4791-8303-1c98665dd146"
    # Yugi = "bb5acc49-6c72-4bbc-a3c9-ee30f404ff55"


class Model(Enum):
    GTP_4 = "gpt-4"
    GTP_3 = "gpt-3.5-turbo"


def _chat(
    account_data: forefront.AccountData,
    prompt: str,
    model: Enum,
    persona: Enum,
):
    # get a response
    for response in forefront.StreamingCompletion.create(
        account_data=account_data,
        prompt=prompt,
        model=model.value,
        default_persona=persona.value,
    ):
        print(response.choices[0].text, end="")
    print("")


def chat(
    prompt: str,
    model=Model.GTP_3,
    persona=Persona.HelpfulAssistant,
):
    account_data = account.get_account()
    if account_data is None:
        print("no account, check cookies")
        return
    _chat(account_data=account_data, prompt=prompt, persona=persona, model=model)
