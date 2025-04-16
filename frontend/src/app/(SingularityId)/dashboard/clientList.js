"use client"

import API from '@/utils/api';
import React, { useEffect, useState } from 'react';

export function ClientList() {
    const [clients, setClients] = useState([]);

    useEffect(() => {
        API.GET("/api/clients", null, {}, (res) => {
                setClients(res)
            }
        );
    }, []);


    return <ul>
        {clients.length > 0 ? (
            clients.map((client) => (
                <li key={client.id}>
                    {client.name} - {client.owner}
                </li>
            ))
        ) : (
            <p>No clients found.</p>
        )}
    </ul>
}