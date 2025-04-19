"use client"
import React, { useState } from "react";
import { Input, Button, Checkbox, Form, Link } from "@nextui-org/react";
import API from "@/utils/api";

/**
 * CustomForm component to create reusable forms.
 * 
 * @param {Array} fields - Array of field objects to render in the form.
    * @param {Boolean} fields[].isRequired - Indicates if the field is required.
    * @param {String} fields[].errorMessage - Error message for the field.
    * @param {Boolean} fields[].isInvalid - Indicates if the field is invalid.
    * @param {String} fields[].label - Label for the field.
    * @param {String} fields[].labelPlacement - Placement of the label.
    * @param {String} fields[].name - Name of the field.
    * @param {String} fields[].placeholder - Placeholder text for the field.
    * @param {String} fields[].type - Type of the field (e.g., text, checkbox).
    * @param {String} fields[].value - Value of the field.
    * @param {Function} fields[].onValueChange - Function to handle value change of the field.
 * @param {Function} onSubmit - Function to handle form submission.
 * @param {Function} onReset - Function to handle form reset.
 * @param {String} submitButtonText - Text for the submit button.
 * @param {String} resetButtonText - Text for the reset button.
 * @param {String} linkText - Text for the optional link.
 * @param {String} linkHref - Href for the optional link.
 * @param {Function} linkOnClick - Function to handle click on the optional link.
 * @param {Object} errors - Object containing validation errors.
 * @param {String} errors.terms - Validation error message for terms and conditions.
 */
export const CustomForm = ({ children, fields, url, defaultSubmit = true, hiddenFormFields = {}}) => {

    const formDataInit = {}
    fields.forEach(field => {
        formDataInit[field.name] = field.value || "";
    });

    const [formData, setFormData] = useState(formDataInit)
    const [errors, setErrors] = useState({});

    const handleValueChange = (name, value) => {
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };

    const handleReset = () => {
        setFormData(formDataInit);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const data = Object.fromEntries(new FormData(e.currentTarget));

        try {
            await API.POST(url, { ...data, ...hiddenFormFields });
        } catch (error) {
            console.error("Error submitting form:", error);
            setErrors((prevErrors) => ({
                ...prevErrors,
                submit: "Failed to submit the form. Please try again.",
            }));
        }
    };

    return (
        <Form
            className="w-full justify-center items-center space-y-4"
            validationBehavior="native"
            validationErrors={errors}
            onSubmit={handleSubmit}
        >
            <div className="flex flex-col gap-4 max-w-md">
                {fields.filter(field => field.type === "text" || field.type === "password").map((field, index) => (
                    <Input
                        key={index}
                        isRequired={field.isRequired}
                        errorMessage={field.errorMessage}
                        isInvalid={field.isInvalid}
                        label={field.label}
                        labelPlacement="outside"
                        name={field.name}
                        placeholder={field.placeholder}
                        type={field.type}
                        value={formData[field.name]}
                        onChange={(e) => handleValueChange(field.name, e.target.value)}
                        fullWidth
                    />
                ))}
                {fields.filter(field => field.type === "checkbox").map((field, index) => (
                    <Checkbox
                        key={index}
                        isRequired={field.isRequired}
                        classNames={{ label: "text-small" }}
                        name={field.name}
                        validationBehavior="aria"
                        value={formData[field.name]}
                        onChange={(e) => handleValueChange(field.name, e.target.checked)}
                    >
                        {field.text}
                    </Checkbox>
                ))}
                {
                defaultSubmit ? 
                (<div className="flex gap-4">
                    <Button className="w-full" color="primary" type="submit">
                        Submit
                    </Button>
                    <Button type="reset" variant="bordered" onPress={handleReset}>
                        Reset
                    </Button>
                </div>)
                :
                ({...children})
                }
            </div>
        </Form>
    );
};

