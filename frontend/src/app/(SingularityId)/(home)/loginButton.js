"use client"
import { login } from "@/utils/actions"

export function LoginButton() {
    return <button onClick={() => {login()}}>Sign In</button>

}