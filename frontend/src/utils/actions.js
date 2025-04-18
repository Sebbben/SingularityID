"use server"
import { cookies } from 'next/headers'
import API from './api'
import { clientId, startLoginFlow } from "@/utils/auth"

export async function login() {
    "use server"
    startLoginFlow()
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
      

    const [status, res]  = await API.POST("http://api:3000/auth/token", {
        "grant_type": "authorization_code",
        "code": authCode,
        "redirect_uri": "/authorize",
        "client_id": clientId
    })

    // TODO: Make completly sure that res is a valid refresh token response
    if (res.refresh_token) {
        const [status, sessionTokenRes] = await API.POST("http://api:3000/session_token", {
            "refresh_token": res.refresh_token,
            "expires_in": res.expires_in,
            "access_token": res.access_token
        })
        
        const cookieStore = await cookies();
        cookieStore.set("session_token", sessionTokenRes.session_token, {httpOnly: true})
    }

}
