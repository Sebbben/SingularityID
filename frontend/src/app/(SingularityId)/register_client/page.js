import { Card } from "@nextui-org/react";
import RegisterClientForm from "./clientForm";
import { cookies } from "next/headers";
import { startLoginFlow } from "@/utils/auth";

export default async function RegisterClientPage() {

    const cookieStore = await cookies();

    if (!cookieStore.has("session_token")) startLoginFlow();

    return (
        <div className="flex items-center justify-center h-full">
            <Card className="p-8">
                <RegisterClientForm/>
            </Card>
        </div>
    );
}