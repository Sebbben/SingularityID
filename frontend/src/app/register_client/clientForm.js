import React, { useState } from "react";
import { CustomForm } from "@/components/CustomForm";
import API from '@/utils/api';

const RegisterClientForm = ({ params }) => {
    const [formData, setFormData] = useState({
        name: params.name || "",
        redirect_uris: params.redirect_uris || "",
        grant_types: params.grant_types || "",
        scopes: params.scopes || "",
    });

    const handleValueChange = (name, value) => {
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        API.POST("/api/auth/register_client", formData)
    };

    const handleReset = () => {
        setFormData({
            name: "",
            redirect_uris: "",
            grant_types: "",
        });
    };

    const fields = [
        {
            isRequired: true,
            label: "Client Name",
            labelPlacement: "outside",
            name: "name",
            placeholder: "Enter client name",
            type: "text",
            value: formData.name,
            onValueChange: (value) => handleValueChange("name", value),
        },
        {
            isRequired: true,
            label: "Redirect URIs",
            labelPlacement: "outside",
            name: "redirect_uris",
            placeholder: "Enter redirect URIs",
            type: "text",
            value: formData.redirect_uris,
            onValueChange: (value) => handleValueChange("redirect_uris", value),
        },
        {
            isRequired: true,
            label: "Grant Types",
            labelPlacement: "outside",
            name: "grant_types",
            placeholder: "Enter grant types",
            type: "text",
            value: formData.grant_types,
            onValueChange: (value) => handleValueChange("grant_types", value),
        },
        {
            isRequired: false,
            label: "Scopes",
            labelPlacement: "outside",
            name: "scopes",
            placeholder: "Enter scopes",
            type: "text",
            value: formData.scopes,
            onValueChange: (value) => handleValueChange("scopes", value),
        },
    ];

    return (
        <CustomForm
            fields={fields}
            onSubmit={handleSubmit}
            onReset={handleReset}
            submitButtonText="Register Client"
            resetButtonText="Reset"
            errors={{}}
        />
    );
};

export default RegisterClientForm;