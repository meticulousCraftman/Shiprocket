import requests as r
import json


class ShipRocket:
    def __init__(self, email=None, password=None):
        if email and password:
            self.email = email
            self.password = password

            auth_token_url = "https://apiv2.shiprocket.in/v1/external/auth/login"
            payload = {"email": email, "password": password}
            headers = {"Content-Type": "application/json"}
            response = r.request(
                "POST",
                auth_token_url,
                headers=headers,
                data=json.dumps(payload),
                allow_redirects=False,
            )

            resp = response.json()
            self.company_id = resp["company_id"]
            self.auth_token = resp["token"]

    def check_courier_serviceability(
        self,
        pickup_postcode,
        delivery_postcode,
        weight,
        order_id=None,
        cod=0,
        length=None,
        breadth=None,
        height=None,
        declared_value=None,
        mode=None,
        is_return=None,
    ):
        url = "https://apiv2.shiprocket.in/v1/external/courier/serviceability/"
        payload = {
            "pickup_postcode": pickup_postcode,
            "delivery_postcode": delivery_postcode,
            "order_id": order_id,
        }
        if order_id:
            payload["order_id"] = int(order_id)

        payload["cod"] = int(cod)

        if weight:
            payload["weight"] = str(weight)

        if length and breadth and height:
            payload["length"] = int(length)
            payload["breadth"] = int(breadth)
            payload["height"] = int(height)

        if declared_value:
            payload["declared_value"] = int(declared_value)

        if mode:
            payload["mode"] = str(mode)

        if is_return:
            payload["is_return"] = int(is_return)

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.auth_token),
        }
        resp = r.request(
            "GET", url, headers=headers, data=json.dumps(payload), allow_redirects=False
        )
        return resp.json()
