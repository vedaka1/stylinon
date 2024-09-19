def get_reset_password_template(reset_link: str) -> str:
    """
    Returns the reset password template
    """
    content = (
        """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Восстановление пароля</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0 auto;
                padding: 20px;
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #7b9acc, #c4e0e5);
                color: #333;
            }
            .container {
                background: rgba(255, 255, 255, 0.8);
                backdrop-filter: blur(10px);
                border-radius: 16px;
                padding: 20px 30px;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
                max-width: 400px;
                text-align: center;
            }
            h2 {
                margin-bottom: 20px;
                color: #333;
            }
            .message {
                margin-bottom: 20px;
                font-size: 16px;
                margin-top: 20px;
            }
            .button {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                cursor: pointer;
                text-decoration: none;
                font-size: 16px;
                transition: background-color 0.3s;
            }
            .button:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Восстановление пароля</h2>
            <div class="message">
                Мы получили запрос на восстановление пароля для вашей учетной записи. Пожалуйста, нажмите кнопку ниже, чтобы сбросить пароль.
            </div>
"""
        + """
            <a href="{reset_link}" class="button">Сбросить пароль</a>""".format(
            reset_link=reset_link,
        )
        + """
            <div class="message">
                Если вы не запрашивали восстановление пароля, просто игнорируйте это сообщение.
            </div>
        </div>
    </body>
    </html>
    """
    )
    return content
