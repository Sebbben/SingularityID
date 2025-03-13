"use client";
import { Card } from "@nextui-org/react";
import RegisterClientForm from "./clientForm";
import { useSearchParams } from "next/navigation";


export default function RegisterClientPage() {

    const searchParams = useSearchParams();
    const params = Object.fromEntries(searchParams.entries());

    return (
        <div className="flex items-center justify-center h-full">
            <Card className="p-8">
                <RegisterClientForm params={params}/>
            </Card>
        </div>
    );
}