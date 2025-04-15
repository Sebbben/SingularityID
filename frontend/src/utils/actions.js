"use server"
import { cookies } from 'next/headers'
import API from './api'
import { clientId } from "@/utils/auth"

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

    // TODO: Make completly sure that res is a valid refresh token response
    if (res.refresh_token) {
        const sessionTokenRes = await API.POST("http://api:3000/session_token", {
            "refresh_token": res.refresh_token,
            "expires_in": res.expires_in
        })
        
        const cookieStore = await cookies();
        cookieStore.set("session", sessionTokenRes.session_token, {httpOnly: true})
    }

}

function registerTokens(tokens) {
    console.log(tokens)
    return "this_is_a_session_token"
}
