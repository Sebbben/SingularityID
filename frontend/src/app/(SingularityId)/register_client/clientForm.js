"use client"
import React, { useState } from "react";
import { CustomForm } from "@/components/CustomForm";
import API from '@/utils/api';
import { useSearchParams } from "next/navigation";

const RegisterClientForm = () => {
    const params = useSearchParams();
    const formExtraParams = {}
  
    for (let key of ["response_type", "client_id", "redirect_uri", "state"]) {
      if (params.has(key)) formExtraParams[key] = params.get(key)
    }

    const fields = [
        {
            isRequired: true,
            label: "Client Name",
            labelPlacement: "outside",
            name: "name",
            placeholder: "Enter client name",
            type: "text",
        },
        {
            isRequired: true,
            label: "Redirect URIs",
            labelPlacement: "outside",
            name: "redirect_uris",
            placeholder: "Enter redirect URIs",
            type: "text",
        },
        {
            isRequired: true,
            label: "Grant Types",
            labelPlacement: "outside",
            name: "grant_types",
            placeholder: "Enter grant types",
            type: "text",
        },
        {
            isRequired: false,
            label: "Scopes",
            labelPlacement: "outside",
            name: "scopes",
            placeholder: "Enter scopes",
            type: "text",
        },
    ];

    return (
        <CustomForm
            fields={fields}
            url = "/api/auth/register_client"
            hiddenFormFields = {formExtraParams}
            />
    );
};

export default RegisterClientForm;