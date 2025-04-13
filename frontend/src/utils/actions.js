"use server"
import { cookies } from 'next/headers'
import API from './api'

const clientId = "c0cdbdb5-d849-4709-882d-4ff53839f9f6" // TODO: get id from app DB (not IDP DB)

export async function test() {
    "use server"
    const cookieStore = cookies();
    cookieStore.set("Test", "test")
} 

export async function exchangeAuthCode(authCode) {
    "use server"


    // Example of expected response from token endpoint
    // {
    //     access_token: '4dc7e508-9d6f-48df-90f5-14ce9af0391f',
    //     expires_in: 3599,
    //     scope: '',
    //     token_type: 'bearer'
    // }
      

    const res  = await API.POST("http://api:3000/auth/token", {
        "grant_type": "authorization_code",
        "code": authCode,
        "redirect_uri": "/authorize",
        "client_id": clientId
    },{},)

    if (res.access_token) {
        const sessionToken = registerTokens(res);
        const cookieStore = cookies();
        cookieStore.set("session", sessionToken, {httpOnly: true})
    }

}

function registerTokens(tokens) {
    console.log(tokens)
    return "this_is_a_session_token"
}
