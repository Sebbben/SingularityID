
import { redirect } from 'next/navigation'
import { cookies } from 'next/headers'
import { makeParamsString } from './general'
import API from './api'

const clientId = "c0cdbdb5-d849-4709-882d-4ff53839f9f6" // TODO: get id from app DB (not IDP DB)

export function startLoginFlow() {
    redirect("/login?" + makeParamsString({
        "response_type": "code",
        "client_id": clientId,
        "redirect_uri": "/authorize",
        "state": "None"
    }))
}

export async function exchangeAuthCode(authCode) {
    const cookieStore = await cookies();

    API.POST("http://api:3000/auth/token", {
        "grant_type": "authorization_code",
        "code": authCode,
        "redirect_uri": "/authorize",
        "client_id": clientId
    },{},
    (data) => {
        let sessionToken = registerTokens(data)
        cookieStore.set("session", sessionToken, {
            httpOnly: true
        })
    },
    (staus, error) => {
        console.log(error)
    })
}

function registerTokens(tokens) {
    console.log(tokens)
    return "this_is_a_session_token"
}