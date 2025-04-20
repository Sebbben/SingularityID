"use client"
import React, { useState, useEffect } from 'react';
import API from '@/utils/api'; // Import the API helper class
import { Card } from "@nextui-org/react";
    
export function ClientForm({ client_id }) {
    const [clientData, setClientData] = useState(null);
    const [accessTokenLifetime, setAccessTokenLifetime] = useState('');
    const [refreshTokenLifetime, setRefreshTokenLifetime] = useState('');
    const [isSaving, setIsSaving] = useState(false);

    useEffect(() => {
        const fetchClientData = async () => {
            const [status, clientDataRes] = await API.GET(
                "/api/clients",
                { client_id: client_id },
            );
            
            const client = clientDataRes["clients"][0] // Get first and only element from the clients returned
            setClientData(client);
            setAccessTokenLifetime(client.access_token_lifetime);
            setRefreshTokenLifetime(client.refresh_token_lifetime);
        };

        fetchClientData();
    }, [client_id]);

    const handleSave = async () => {
        setIsSaving(true);
        try {
            await API.POST(
                `/api/clients`,
                {
                    client_id: client_id,
                    access_token_lifetime: accessTokenLifetime,
                    refresh_token_lifetime: refreshTokenLifetime,
                },
            );
        } catch (error) {
            console.error('Unexpected error saving changes:', error);
        } finally {
            setIsSaving(false);
        }
    };

    function handleRemoveRedirectUri(uri) {
        setClientData((prev) => ({
            ...prev,
            redirect_uris: prev.redirect_uris.filter((item) => item !== uri),
        }));
    }

    function handleAddRedirectUri(e) {
        if (e.key === 'Enter' && e.target.value) {
            setClientData((prev) => ({
                ...prev,
                redirect_uris: [...prev.redirect_uris, e.target.value],
            }));
            e.target.value = '';
        }
    }

    function handleGrantTypeChange(e) {
        const selectedOptions = Array.from(e.target.selectedOptions).map((option) => option.value);
        setClientData((prev) => ({
            ...prev,
            grant_types: selectedOptions,
        }));
    }

    function handleRemoveScope(scope) {
        setClientData((prev) => ({
            ...prev,
            scopes: prev.scopes.filter((item) => item !== scope),
        }));
    }

    function handleAddScope(e) {
        if (e.key === 'Enter' && e.target.value) {
            setClientData((prev) => ({
                ...prev,
                scopes: [...prev.scopes, e.target.value],
            }));
            e.target.value = '';
        }
    }

    return (
        <div className="flex items-center justify-center h-full">
            <Card className="p-8 max-w-lg w-full bg-white dark:bg-gray-800 shadow-lg border border-gray-200 dark:border-gray-700">
                <div className="client-header mb-6">
                    <h2 className="text-xl font-semibold text-center mb-2 text-gray-900 dark:text-gray-100">{clientData?.name}</h2>
                    <p className="text-sm text-gray-600 dark:text-gray-400 text-center">ID: {client_id}</p>
                </div>
                <div className="client-body space-y-4">
                    <div className="form-group">
                        <label className="block text-sm font-medium text-gray-900 dark:text-gray-100">Access Token Lifetime</label>
                        <input
                            type="number"
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                            value={accessTokenLifetime}
                            onChange={(e) => setAccessTokenLifetime(e.target.value)}
                        />
                    </div>
                    <div className="form-group">
                        <label className="block text-sm font-medium text-gray-900 dark:text-gray-100">Refresh Token Lifetime</label>
                        <input
                            type="number"
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                            value={refreshTokenLifetime}
                            onChange={(e) => setRefreshTokenLifetime(e.target.value)}
                        />
                    </div>
                    <button
                        className="w-full py-2 px-4 bg-blue-600 text-white rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-75"
                        onClick={handleSave}
                        disabled={isSaving}
                    >
                        {isSaving ? "Saving..." : "Save Changes"}
                    </button>
                    <div className="form-group">
                        <label className="block text-sm font-medium text-gray-900 dark:text-gray-100">Redirect URIs</label>
                        <ul className="space-y-2">
                            {clientData?.redirect_uris?.map((uri, index) => (
                                <li key={index} className="flex items-center justify-between">
                                    <span className="text-sm text-gray-900 dark:text-gray-100">{uri}</span>
                                    <button
                                        className="text-red-600 hover:underline"
                                        onClick={() => handleRemoveRedirectUri(uri)}
                                    >
                                        Remove
                                    </button>
                                </li>
                            ))}
                        </ul>
                        <input
                            type="text"
                            className="mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                            placeholder="Add new redirect URI"
                            onKeyDown={(e) => handleAddRedirectUri(e)}
                        />
                    </div>
                    <div className="form-group">
                        <label className="block text-sm font-medium text-gray-900 dark:text-gray-100">Grant Types</label>
                        <select
                            multiple
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                            value={clientData?.grant_types || []}
                            onChange={(e) => handleGrantTypeChange(e)}
                        >
                            <option value="authorization_code">Authorization Code</option>
                            <option value="implicit">Implicit</option>
                            <option value="password">Password</option>
                            <option value="client_credentials">Client Credentials</option>
                        </select>
                    </div>
                    <div className="form-group">
                        <label className="block text-sm font-medium text-gray-900 dark:text-gray-100">Scopes</label>
                        <ul className="space-y-2">
                            {clientData?.scopes?.map((scope, index) => (
                                <li key={index} className="flex items-center justify-between">
                                    <span className="text-sm text-gray-900 dark:text-gray-100">{scope}</span>
                                    <button
                                        className="text-red-600 hover:underline"
                                        onClick={() => handleRemoveScope(scope)}
                                    >
                                        Remove
                                    </button>
                                </li>
                            ))}
                        </ul>
                        <input
                            type="text"
                            className="mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                            placeholder="Add new scope"
                            onKeyDown={(e) => handleAddScope(e)}
                        />
                    </div>
                </div>
            </Card>
        </div>
    );
}