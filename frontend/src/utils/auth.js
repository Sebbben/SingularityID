
import { redirect } from 'next/navigation'
import { makeParamsString } from './general'

const clientId = "c0cdbdb5-d849-4709-882d-4ff53839f9f6" // TODO: get id from app DB (not IDP DB)

export function startLoginFlow() {
    redirect("/login?" + makeParamsString({
        "response_type": "auth_code",
        "client_id": clientId,
        "redirect_uri": "/",
        "state": "None"
    }))
}