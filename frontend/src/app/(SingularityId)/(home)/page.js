import { cookies } from "next/headers"
import { LoginButton } from "./loginButton";


export default async function Home() {

    const cookieStore = await cookies();
    const isLoggedIn = cookieStore.has("session_token");

    return (
        <div>
            <h1>Welcome to the Home Page</h1>
            {!isLoggedIn ? (
                <div>
                    <p>You are not logged in.</p>
                    <LoginButton/>
                </div>
            ) : (
                <div>
                    <p>You are logged in!</p>
                    <a href="/dashboard">Go to Dashboard</a>
                </div>
            )}
        </div>
    );
}