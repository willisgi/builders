from __future__ import annotations

from typing import Optional
import base64
import httpx
from datetime import datetime

from app.core.config import settings

MPESA_BASE = "https://sandbox.safaricom.co.ke"

async def get_access_token(client: Optional[httpx.AsyncClient] = None) -> str:
    own_client = client is None
    if own_client:
        client = httpx.AsyncClient()
    try:
        resp = await client.get(
            f"{MPESA_BASE}/oauth/v1/generate",
            params={"grant_type": "client_credentials"},
            auth=(settings.mpesa_consumer_key or "", settings.mpesa_consumer_secret or ""),
            timeout=20.0,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["access_token"]
    finally:
        if own_client:
            await client.aclose()

async def stk_push(
    phone_number: str,
    amount: int,
    account_reference: str,
    transaction_desc: str,
    callback_url: Optional[str] = None,
    client: Optional[httpx.AsyncClient] = None,
):
    token = await get_access_token(client)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    shortcode = settings.mpesa_short_code or "600XXX"
    passkey = settings.mpesa_passkey or ""
    password = base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode()

    own_client = client is None
    if own_client:
        client = httpx.AsyncClient()
    try:
        resp = await client.post(
            f"{MPESA_BASE}/mpesa/stkpush/v1/processrequest",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "BusinessShortCode": shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,
                "PartyA": phone_number,
                "PartyB": shortcode,
                "PhoneNumber": phone_number,
                "CallBackURL": callback_url or settings.mpesa_callback_url or "https://example.com/callback",
                "AccountReference": account_reference,
                "TransactionDesc": transaction_desc,
            },
            timeout=20.0,
        )
        resp.raise_for_status()
        return resp.json()
    finally:
        if own_client:
            await client.aclose()

async def stk_query(
    checkout_request_id: str,
    client: Optional[httpx.AsyncClient] = None,
):
    token = await get_access_token(client)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    shortcode = settings.mpesa_short_code or "600XXX"
    passkey = settings.mpesa_passkey or ""
    password = base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode()

    own_client = client is None
    if own_client:
        client = httpx.AsyncClient()
    try:
        resp = await client.post(
            f"{MPESA_BASE}/mpesa/stkpushquery/v1/query",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "BusinessShortCode": shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "CheckoutRequestID": checkout_request_id,
            },
            timeout=20.0,
        )
        resp.raise_for_status()
        return resp.json()
    finally:
        if own_client:
            await client.aclose()
