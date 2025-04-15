
import { redirect } from 'next/navigation'
import { makeParamsString } from './general'


export const clientId = process.env.CLIENT_ID;

export function startLoginFlow() {
    redirect("/login?" + makeParamsString({
        "response_type": "code",
        "client_id": clientId,
        "redirect_uri": "/authorize",
        "state": "None"
    }))
}
