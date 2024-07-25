import jwt
from datetime import datetime, timedelta
import config

class JwtUtil:

    def generate_jwt(self, payload):
        # 设置过期时间（可选）
        expiration_time = datetime.utcnow() + timedelta(hours=24 * 30)  # 过期时间为1小时后

        # 构建 JWT 的头部（Header）
        header = {
            'alg': 'HS256',  # 选择签名算法，HS256 是常用的对称加密算法
            'typ': 'JWT'
        }

        # 构建 JWT 的负载（Payload）
        payload.update({
            'exp': expiration_time,
            'iat': datetime.utcnow(),
        })

        # 使用 PyJWT 库生成 JWT
        jwt_token = jwt.encode(payload, config.SECRET_KEY, algorithm='HS256', headers=header)

        return jwt_token