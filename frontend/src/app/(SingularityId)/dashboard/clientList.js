"use client";

import API from "@/utils/api";
import React, { useEffect, useState } from "react";
import { Card } from "@nextui-org/react";
import { RedirectButton } from "@/components/Buttons/RedirectButton";
import { DataFetchButton } from "@/components/Buttons/DataFetchButton";
import { useRouter } from "next/navigation";

export function ClientList() {
    const [clients, setClients] = useState([]);
    const router = useRouter();

    const updateClients = () => {
        API.GET("/api/clients").then(([status, res]) => {
            setClients(res.clients);
        })
    };

    useEffect(updateClients, []);

    return (
        <div className="flex flex-col items-center justify-center h-full">
            <Card className="p-8 max-w-md w-full">
                <h1 className="text-xl font-semibold mb-4 text-center">Your Clients</h1>
                <ul className="space-y-4">
                    {clients.length > 0 ? (
                        clients.map((client) => (
                            <li 
                                key={client.id} 
                                className="border-b pb-2 cursor-pointer hover:bg-gray-700" 
                                onClick={() => router.push(`/clients/${client.id}`)}
                            >
                                <p className="font-medium">{client.name}</p>
                                <p className="text-sm text-gray-500">
                                    Access Token Lifetime: {client.access_token_lifetime}s
                                </p>
                                <p className="text-sm text-gray-500">
                                    Refresh Token Lifetime: {client.refresh_token_lifetime}s
                                </p>
                            </li>
                        ))
                    ) : (
                        <p className="text-center text-gray-500">No clients found.</p>
                    )}
                </ul>
                <div className="flex justify-between mt-6">
                    <DataFetchButton url="/api/clients" text = "Refresh" callback={(data => setClients(data.clients))}/>
                    <RedirectButton url="/register_client" text="Register client"/>
                </div>
            </Card>
        </div>
    );
}