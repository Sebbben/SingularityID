"use client"
import React, { useState, useEffect } from 'react';
import { CustomForm } from '@/components/CustomForm'; // Adjust the path as needed
import API from '@/utils/api'; // Import the API helper class

const ClientPage = () => {
    const [clientData, setClientData] = useState(null);
    const [accessTokenLifetime, setAccessTokenLifetime] = useState('');
    const [refreshTokenLifetime, setRefreshTokenLifetime] = useState('');
    const [isSaving, setIsSaving] = useState(false);


    useEffect(() => {
        const fetchClientData = async () => {
            const clientData = await API.GET(
                "/api/clients",
                { client_id: client_id },
            );

            setClientData(clientData);
            setAccessTokenLifetime(clientData.access_token_lifetime);
            setRefreshTokenLifetime(clientData.refresh_token_lifetime);
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


    if (!clientData) {
        return <div>Loading...</div>;
    } else {
        const fields = [
            {
                label: 'Client ID',
                value: client_id,
                type: 'text',
                isRequired: false,
                isInvalid: false,
                errorMessage: '',
                placeholder: '',
                onValueChange: () => { },
                name: 'client_id',
            },
            {
                label: 'Name',
                value: clientData.name,
                type: 'text',
                isRequired: false,
                isInvalid: false,
                errorMessage: '',
                placeholder: '',
                onValueChange: () => { },
                name: 'name',
            },
            {
                label: 'Access Token Lifetime',
                value: accessTokenLifetime,
                type: 'number',
                isRequired: true,
                isInvalid: false,
                errorMessage: 'Please enter a valid number',
                placeholder: 'Enter access token lifetime',
                onValueChange: (value) => setAccessTokenLifetime(value),
                name: 'access_token_lifetime',
            },
            {
                label: 'Refresh Token Lifetime',
                value: refreshTokenLifetime,
                type: 'number',
                isRequired: true,
                isInvalid: false,
                errorMessage: 'Please enter a valid number',
                placeholder: 'Enter refresh token lifetime',
                onValueChange: (value) => setRefreshTokenLifetime(value),
                name: 'refresh_token_lifetime',
            },
        ];
        return (
            <div className="flex items-center justify-center h-full">
                <div className="w-full max-w-md">
                    <CustomForm
                        fields={fields}
                        onSubmit={handleSave}
                        submitButtonText="Save Changes"
                        resetButtonText="Reset"
                        isSubmitting={isSaving}
                    />
                </div>
            </div>
        );
    }
};

export default ClientPage;
