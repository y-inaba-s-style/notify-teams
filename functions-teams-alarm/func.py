import io
import json
import logging
import requests
from fdk import response

def handler(ctx, data: io.BytesIO = None):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    try:
        # TeamsのWebhook URL
        webhook_url = 'https://prod-23.japaneast.logic.azure.com:443/workflows/b51a61bd4e8b461bac7d817e5bcd2683/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=D4q_a8dLVrthPlACKMo1izgBn73R4UM_1iRKKLlPRIE'

        # 送信するメッセージ
        message = {
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": {
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "type": "AdaptiveCard",
                        "version": "1.2",
                        "body": [
                            {
                                "type": "TextBlock",
                                "text": "## Teamsへの通知テストです。\n\n* インスタンスのCPU使用率が80％を超えました。\n* 対応してください。",
                                "wrap": True,
                                "markdown": True
                            }
                        ]
                    }
                }
            ]
        }

        logger.info("Sending request to Teams webhook")
        # POSTリクエストを送信
        req_response = requests.post(
            url=webhook_url,
            data=json.dumps(message),
            headers={'Content-Type': 'application/json'}
        )

        # レスポンスを確認
        if req_response.ok:
            logger.info("Message sent successfully")
            return response.Response(
                ctx, response_data=json.dumps({"message": "メッセージが送信されました"}, ensure_ascii=False),
                headers={"Content-Type": "application/json"}
            )
        else:
            logger.error(f"Error sending message: {req_response.status_code}, {req_response.text}")
            return response.Response(
                ctx, response_data=json.dumps({"error": f"エラーが発生しました: {req_response.status_code}, {req_response.text}"}, ensure_ascii=False),
                headers={"Content-Type": "application/json"}
            )
    except Exception as e:
        logger.exception("An error occurred during function execution")
        return response.Response(
            ctx, response_data=json.dumps({"error": f"エラーが発生しました: {str(e)}"}, ensure_ascii=False),
            headers={"Content-Type": "application/json"}
        )

