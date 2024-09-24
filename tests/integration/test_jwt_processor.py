from dishka import AsyncContainer
from src.application.common.interfaces.jwt_processor import JWTProcessorInterface

webhook_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJjdXN0b21lckNvZGUiOiAiMzAwMTIzMTIzIiwgImFtb3VudCI6ICIwLjMzIiwgInBheW1lbnRUeXBlIjogImNhcmQiLCAib3BlcmF0aW9uSWQiOiAiYmVlYWM4YTQtNjA0Ny0zZjM4LTg5MjItYTY2NGU2YjVjNDNiIiwgInB1cnBvc2UiOiAiXHUwNDFlXHUwNDNmXHUwNDNiXHUwNDMwXHUwNDQyXHUwNDMwIFx1MDQzZlx1MDQzZSBcdTA0NDFcdTA0NDdcdTA0MzVcdTA0NDJcdTA0NDMgXHUyMTE2IDEgXHUwNDNlXHUwNDQyIDAxLjAxLjIwMjEuIFx1MDQxMVx1MDQzNVx1MDQzNyBcdTA0MWRcdTA0MTRcdTA0MjEiLCAid2ViaG9va1R5cGUiOiAiYWNxdWlyaW5nSW50ZXJuZXRQYXltZW50In0.FJfaan8N1OWxLRipfsMuxmYyE69mA7yhp3uP2ycImzmT3UpSXtgdedGKP8RoVDq-r4nOiiXLMCYO7bsH0L8660wZvnCMuqZzmE_K3vbczTBdFiWhp7ExFTNX-rALuYemmdjIk4iSc7nDU4DwWvTaQGh8_yJlm9MOqa9RSFXnHpfKElNRea0rNonk02KqGdPz_zRVF7MXPjr970tEATibR52hrZCFWYZxA6FiggFsrqOykGAPX6uZyR7OD_TP0oZM5v3KxNFcnSsIxb_G8UJpdGk2GvDWDx9Px7tjkROu_ja47-N8StlY54DxDmzpaqfl35mYnLv8awGmfaZXOWYZySADRG2MDAi-iii4TPKdUtPeZga-mo0T9Vv_Jqeg9O-glFufLjCvm4dEPl36ccdpBTcvpfLthQEwa60Eb_fiyrYhIVBmjucxJZOgiATuEiXbMXPe9Z7wXYlS6tilEzBPpjy8glUcH_WDMCkK5Lylu7SCERr1Uc0PFF8M93TCTnJB"


async def test_validate_acquiring_token(container: AsyncContainer) -> None:
    async with container() as container:
        jwt_processor = await container.get(JWTProcessorInterface)
        token_data = jwt_processor.validate_acquiring_token(token=webhook_token)
        expected = {
            "customerCode": "300123123",
            "amount": "0.33",
            "paymentType": "card",
            "operationId": "beeac8a4-6047-3f38-8922-a664e6b5c43b",
            "purpose": "Оплата по счету № 1 от 01.01.2021. Без НДС",
            "webhookType": "acquiringInternetPayment",
        }
        assert token_data == expected
